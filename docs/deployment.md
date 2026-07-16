```markdown
# Environment-Specific Deployments — LLM Shield

The application leverages three distinct pipeline branches for staging environments:

1. **`dev` (Development):** Runs locally or on feature branches using `docker-compose`. Uses hot-reloading configurations.
2. **`staging` (Staging):** Automated staging deployments triggered on PRs merged to the `staging` branch. Connects to the staging database.
3. **`production` (Production):** Triggered on commits to `main`. Points to live production resources on Vercel and production databases.

## Local Docker Execution
Developers run local systems through Docker Compose:
```bash
docker-compose --env-file .env.dev up --build