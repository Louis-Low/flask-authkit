# Email delivery with Brevo

AuthKit now supports three Brevo transactional templates:

- Password reset: `BREVO_PASSWORD_RESET_TEMPLATE_ID`
- Email verification: `BREVO_EMAIL_VERIFICATION_TEMPLATE_ID`
- Welcome message: `BREVO_WELCOME_TEMPLATE_ID`

Create each template in Brevo, select the verified sender, and use these template variables:

- All templates: `{{ params.username }}`, `{{ params.app_name }}`
- Verification: `{{ params.verification_link }}`
- Password reset: `{{ params.reset_link }}`

Configure the numeric template IDs in `.env` along with `BREVO_API_KEY`, `MAIL_FROM_EMAIL`, and `MAIL_FROM_NAME`. The application never logs API keys, passwords, or token links.

## Registration flow

1. The user submits the registration form.
2. AuthKit stores a bcrypt password hash and sets `email_verified` to false.
3. Brevo sends the verification template and a welcome template.
4. The user clicks the signed link, which expires after `EMAIL_VERIFICATION_MAX_AGE` seconds (24 hours by default).
5. The account can sign in only after verification.

The resend page intentionally returns the same message for known and unknown email addresses to reduce account enumeration risk.
