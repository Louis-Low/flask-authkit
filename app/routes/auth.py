from datetime import datetime, timezone

from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app import db
from app.forms import (
    ForgotPasswordForm,
    LoginForm,
    RegistrationForm,
    ResendVerificationForm,
    ResetPasswordForm,
)
from app.models import User
from app.services.email import send_password_reset_email, send_verification_email, send_welcome_email


auth_bp = Blueprint("auth", __name__)


def _serializer(salt):
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt=salt)


def _reset_token(email):
    return _serializer("password-reset").dumps(email)


def _email_from_token(token):
    return _serializer("password-reset").loads(token, max_age=current_app.config["PASSWORD_RESET_MAX_AGE"])


def _verification_token(email):
    return _serializer("email-verification").dumps(email)


def _email_from_verification_token(token):
    return _serializer("email-verification").loads(token, max_age=current_app.config["EMAIL_VERIFICATION_MAX_AGE"])


def _verification_link(user):
    return url_for("auth.verify_email", token=_verification_token(user.email), _external=True)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))
    form = LoginForm()
    if form.validate_on_submit():
        identity = form.identity.data.strip()
        user = User.query.filter((User.email == identity.lower()) | (User.username == identity)).first()
        if user and user.check_password(form.password.data):
            if not user.email_verified:
                flash("Please verify your email before signing in.", "info")
                return redirect(url_for("auth.resend_verification"))
            if not user.is_active:
                flash("This account is not available.", "error")
            else:
                user.last_login = datetime.now(timezone.utc)
                db.session.commit()
                login_user(user, remember=form.remember.data)
                flash("Welcome back.", "success")
                return redirect(url_for("main.profile"))
        else:
            flash("Invalid sign-in details.", "error")
    return render_template("auth/login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.profile"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.strip(), email=form.email.data.strip().lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_verification_email(user.email, user.username, _verification_link(user))
        send_welcome_email(user.email, user.username)
        flash("Account created. Check your email to verify your account.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)


@auth_bp.route("/verify-email/<token>")
def verify_email(token):
    try:
        email = _email_from_verification_token(token)
    except (BadSignature, SignatureExpired):
        flash("That verification link is invalid or expired.", "error")
        return redirect(url_for("auth.resend_verification"))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("That verification link is invalid or expired.", "error")
        return redirect(url_for("auth.resend_verification"))
    if not user.email_verified:
        user.email_verified = True
        db.session.commit()
        flash("Your email is verified. You can now sign in.", "success")
    else:
        flash("Your email is already verified.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/resend-verification", methods=["GET", "POST"])
def resend_verification():
    form = ResendVerificationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user and not user.email_verified:
            send_verification_email(user.email, user.username, _verification_link(user))
        flash("If an unverified account matches that email, a verification email has been sent.", "info")
        return redirect(url_for("auth.resend_verification"))
    return render_template("auth/resend_verification.html", form=form)


@auth_bp.get("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "success")
    return redirect(url_for("auth.login"))


@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.strip().lower()).first()
        if user:
            send_password_reset_email(user.email, user.username, url_for("auth.reset_password", token=_reset_token(user.email), _external=True))
        flash("If an account matches that email, reset instructions have been sent.", "info")
        return redirect(url_for("auth.forgot_password"))
    return render_template("auth/forgot_password.html", form=form)


@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    try:
        email = _email_from_token(token)
    except (BadSignature, SignatureExpired):
        flash("That password-reset link is invalid or expired.", "error")
        return redirect(url_for("auth.forgot_password"))
    user = User.query.filter_by(email=email).first()
    if not user:
        flash("That password-reset link is invalid or expired.", "error")
        return redirect(url_for("auth.forgot_password"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Your password has been reset. Please sign in.", "success")
        return redirect(url_for("auth.login"))
    return render_template("auth/reset_password.html", form=form)
