# Functional and Non-Functional Requirements — LLM Shield

## 1. Functional Requirements (FR)
* **FR-1: Decoupled Multi-Tenant Architecture:** The application must strictly separate the Frontend UI (React) from the Backend API (FastAPI).
* **FR-2: Search Query Execution:** Users must be able to perform search queries via an API endpoint (`/api/v1/leads/search`) to retrieve parsed job lead structures.
* **FR-3: Secure User Authentication:** Integration with Supabase Auth to handle user registration, login, password recovery, and secure JWT-based session management.
* **FR-4: Automated Email Notifications:** Integration with the Resend API (Free Tier) to dispatch system alerts and notifications when security thresholds are met or job leads match user criteria.
* **FR-5: Defensive LLM Proxying (LLM Shield):** Implementation of an intercepting validation layer that sanitizes user queries to LLMs, blocking prompt injections and data exfiltration vectors.

## 2. Non-Functional Requirements (NFR)
### Security & Compliance
* **NFR-1.1 (Least Privilege):** Docker containers must not execute as the `root` root user.
* **NFR-1.2 (Static Code Analysis):** Automatic static application security testing (SAST) must be performed on every code commit to catch vulnerabilities (OWASP Top 10).
* **NFR-1.3 (Secret Management):** No plaintext secrets, API keys, or database URIs are permitted in the codebase. All secrets must load dynamically via environment configurations.

### Performance & Scalability
* **NFR-2.1 (API Latency):** Core endpoints must maintain a latency of $< 200\text{ms}$ for 95% of standard requests.
* NFR-2.2 (Stateless scaling):** The backend API must be entirely stateless, storing session data in Supabase/Redis to enable seamless scale-to-zero compute.

### Deployment Specifications
* **NFR-3.1:** Local development must be completely orchestratable using `docker-compose` with mock environment profiles.
* **NFR-3.2:** Production environment must be deployable on Vercel's Fluid Compute platform running OCI-compatible container images.