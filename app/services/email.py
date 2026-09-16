import sib_api_v3_sdk
from flask import current_app
from sib_api_v3_sdk.rest import ApiException


def _send_template_email(recipient_email, recipient_name, subject, template_id, params):
    api_key = current_app.config.get("BREVO_API_KEY")
    if not api_key:
        current_app.logger.error("Brevo email is not configured; BREVO_API_KEY is missing.")
        return False
    if not template_id:
        current_app.logger.error("No Brevo template ID is configured for %s.", subject)
        return False

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    message = sib_api_v3_sdk.SendSmtpEmail(
        sender={"name": current_app.config["MAIL_FROM_NAME"], "email": current_app.config["MAIL_FROM_EMAIL"]},
        to=[{"email": recipient_email, "name": recipient_name}],
        subject=subject,
        template_id=template_id,
        params=params,
    )
    try:
        api_instance.send_transac_email(message)
        return True
    except ApiException:
        current_app.logger.exception("Brevo rejected a transactional email request.")
    except Exception:
        current_app.logger.exception("Unexpected error while sending transactional email.")
    return False


def send_password_reset_email(recipient_email, recipient_name, token_link):
    return _send_template_email(
        recipient_email,
        recipient_name,
        "Reset your Flask AuthKit password",
        current_app.config.get("BREVO_PASSWORD_RESET_TEMPLATE_ID"),
        {"username": recipient_name, "reset_link": token_link, "app_name": current_app.config["MAIL_FROM_NAME"]},
    )


def send_verification_email(recipient_email, recipient_name, verification_link):
    return _send_template_email(
        recipient_email,
        recipient_name,
        "Verify your Flask AuthKit email",
        current_app.config.get("BREVO_EMAIL_VERIFICATION_TEMPLATE_ID"),
        {"username": recipient_name, "verification_link": verification_link, "app_name": current_app.config["MAIL_FROM_NAME"]},
    )


def send_welcome_email(recipient_email, recipient_name):
    return _send_template_email(
        recipient_email,
        recipient_name,
        "Welcome to Flask AuthKit",
        current_app.config.get("BREVO_WELCOME_TEMPLATE_ID"),
        {"username": recipient_name, "app_name": current_app.config["MAIL_FROM_NAME"]},
    )
