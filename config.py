import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///authkit.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    PASSWORD_RESET_MAX_AGE = 3600
    EMAIL_VERIFICATION_MAX_AGE = 86400

    BREVO_API_KEY = os.getenv("BREVO_API_KEY")
    MAIL_FROM_EMAIL = os.getenv("MAIL_FROM_EMAIL", "noreply@example.com")
    MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Flask AuthKit")
    BREVO_PASSWORD_RESET_TEMPLATE_ID = _int_env("BREVO_PASSWORD_RESET_TEMPLATE_ID")
    BREVO_EMAIL_VERIFICATION_TEMPLATE_ID = _int_env("BREVO_EMAIL_VERIFICATION_TEMPLATE_ID")
    BREVO_WELCOME_TEMPLATE_ID = _int_env("BREVO_WELCOME_TEMPLATE_ID")


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True


def _int_env(name):
    value = os.getenv(name)
    return int(value) if value and value.isdigit() else None
