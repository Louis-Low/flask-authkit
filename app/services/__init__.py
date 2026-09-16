import sib_api_v3_sdk
from flask import current_app
from sib_api_v3_sdk.rest import ApiException


def send_password_reset_email(recipient_email, recipient_name, token_link):
    """Send a password-reset message through Brevo.

    The reset token is used only in the email body and is never logged. A missing
    API key is treated as a configuration failure so callers can show a generic
    recovery message without revealing account existence.
    """
    api_key = current_app.config.get("BREVO_API_KEY")
    if not api_key:
        current_app.logger.error("Brevo email is not configured; BREVO_API_KEY is missing.")
        return False

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = api_key
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    html_content = f"""
    <!doctype html>
    <html lang=\"en\">
      <body style=\"margin:0;background:#f7f9fb;color:#17212b;font-family:Arial,sans-serif;\">
        <table width=\"100%\" cellpadding=\"0\" cellspacing=\"0\" style=\"padding:40px 15px;background:#f7f9fb;\">
          <tr><td align=\"center\">
            <table width=\"600\" cellpadding=\"0\" cellspacing=\"0\" style=\"max-width:600px;background:#ffffff;border:1px solid #d9e0e7;border-radius:12px;\">
              <tr><td style=\"padding:32px;\">
                <p style=\"color:#2457d6;font-size:13px;font-weight:bold;letter-spacing:2px;text-transform:uppercase;\">{current_app.config['MAIL_FROM_NAME']}</p>
                <h1 style=\"font-size:28px;margin:0 0 18px;\">Reset your password</h1>
                <p style=\"color:#647180;font-size:16px;line-height:1.6;\">Hello {recipient_name}, use the button below to choose a new password. This link expires in one hour.</p>
                <p style=\"text-align:center;margin:32px 0;\"><a href=\"{token_link}\" style=\"background:#2457d6;color:#ffffff;text-decoration:none;padding:13px 22px;border-radius:7px;font-weight:bold;\">Choose a new password</a></p>
                <p style=\"color:#647180;font-size:13px;line-height:1.6;word-break:break-all;\">If the button does not work, copy this link:<br><a href=\"{token_link}\" style=\"color:#2457d6;\">{token_link}</a></p>
                <p style=\"color:#647180;font-size:13px;line-height:1.6;\">If you did not request this email, you can safely ignore it.</p>
              </td></tr>
            </table>
          </td></tr>
        </table>
      </body>
    </html>
    """

    message = sib_api_v3_sdk.SendSmtpEmail(
        sender={
            "name": current_app.config["MAIL_FROM_NAME"],
            "email": current_app.config["MAIL_FROM_EMAIL"],
        },
        to=[{"email": recipient_email, "name": recipient_name}],
        subject="Reset your Flask AuthKit password",
        html_content=html_content,
    )

    try:
        api_instance.send_transac_email(message)
        return True
    except ApiException:
        current_app.logger.exception("Brevo rejected a transactional email request.")
    except Exception:
        current_app.logger.exception("Unexpected error while sending transactional email.")
    return False
