# LLM Shield: Secure Email API Integration & Threat Analysis

### 1. Selected Technology
* **API Name:** Resend API (Free Developer Tier)
* **Purpose:** To automatically notify users when high-quality job leads are extracted by our platform.

### 2. Vulnerability Assessment & Mitigations

* **Vulnerability 1: API Key Leakage (Credential Exposure)**
  * *Threat:* Accidental hardcoding of the Resend API key inside our Git repository.
  * *Mitigation:* The API key is loaded dynamically from system environment variables via our Pydantic `config.py` setup. Real credentials are restricted to GitHub Secrets or Vercel Environment Configuration panels.

* **Vulnerability 2: SMTP / Email Header Injection**
  * *Threat:* An attacker manipulating input fields (like the "to" or "subject" fields) to send spam messages through our platform.
  * *Mitigation:* We run strict data serialization and sanitization on all incoming request objects using Pydantic schemas before processing.

* **Vulnerability 3: Rate Limiting Abuse**
  * *Threat:* Attackers continuously triggering the email notification endpoint to drain our daily API limits.
  * *Mitigation:* We utilize Redis-based rate-limiting in front of any route that triggers an external API action.