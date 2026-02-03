# Security Policy for Diane

Thank you for helping keep **Diane** safe and secure!

This document outlines the security practices for the Diane project and provides guidelines for reporting security vulnerabilities.

---

## Supported Versions
Only the **latest stable release** of Diane is currently supported with security updates. If you are using an older version, we strongly recommend upgrading to the latest release.

| Version | Supported          |
|---------|--------------------|
| Latest   | ✅ Yes              |
| < 1.0.0  | ❌ No (Upgrade!)    |

---

## Reporting a Vulnerability
If you discover a security vulnerability in Diane, **please do not open a public issue**. Instead, follow these steps:

1. **Send an email** to us at **[naa.veoos@gmail.com]**.
2. Provide the following details:
   - A **description** of the vulnerability.
   - **Steps to reproduce** the issue.
   - The **version of Diane** you are using.
   - Any additional context (e.g., logs, screenshots).

3. We will acknowledge your report within **48 hours** and provide a timeline for a fix.

4. Once the vulnerability is fixed, we will:
   - Release a **security update**.
   - Credit you in the release notes (unless you prefer to remain anonymous).

---

## Security Practices
### Code Review
- All pull requests are reviewed by at least one maintainer before merging.
- We prioritize security fixes and release patches as soon as possible.

### Dependencies
- We regularly update dependencies to their latest secure versions.
- We use tools like `pip-audit` and `safety` to check for known vulnerabilities in Python dependencies.

### Data Protection
- Diane does **not** collect or store personal user data beyond what is necessary for the simulation.
- If you use the Discord bot, ensure your **bot token is kept private** and never committed to public repositories.

### Secure Development
- Avoid hardcoding sensitive information (e.g., API keys, tokens).
- Use environment variables (`.env` files) for secrets and **never commit them** to GitHub.

---

## Responsible Disclosure
We follow the principles of **responsible disclosure**:
1. **Private Reporting**: Vulnerabilities are reported privately to the maintainers.
2. **Timely Fixes**: We work to fix vulnerabilities as quickly as possible.
3. **Public Disclosure**: Once a fix is released, we publicly disclose the vulnerability (with credit to the reporter, if desired).

---

## Security Updates
Security updates are released as **patch versions** (e.g., `1.0.1`). To stay secure:
- Always use the **latest version** of Diane.
- Subscribe to [GitHub releases](https://github.com/your-organization/diane/releases) for update notifications.

---

## FAQ
### How do I securely configure my Diane bot?
1. Use environment variables for sensitive data (e.g., `BOT_TOKEN`).
2. Restrict your bot’s permissions on Discord to only what it needs.
3. Regularly update your bot and dependencies.

### What should I do if I accidentally expose my bot token?
1. **Revoke the token** immediately in the [Discord Developer Portal](https://discord.com/developers/applications).
2. Generate a new token and update your `.env` file.

---

## Contact
For security-related questions or concerns, contact us at **[security@diane-project.org]**.

**Thank you for helping us keep Diane secure!** 🛡️
