# System & Security Architecture — LLM Shield

## 1. Component Interaction Diagram
┌─────────────────────────┐
                          │    React Frontend       │
                          │   (Deployed on Vercel)  │
                          └─────────────────────────┘
                                       │
                                       │ HTTPS (CORS Bound)
                                       ▼
                          ┌─────────────────────────┐
                          │     FastAPI Backend     │
                          │ (Vercel Container Image)│
                          └─────────────────────────┘
                             │       │         │
   PostgreSQL / REST Queries │       │         │ SMTP / REST
                             │       │         │
                             ▼       │         ▼
     ┌─────────────────────────┐     │    ┌─────────────────────────┐
     │     Supabase Service    │     │    │       Resend API        │
     │  (Database & Auth engine)     │    │   (Email Notification)  │
     └─────────────────────────┘     │    └─────────────────────────┘
                                     ▼
                        ┌─────────────────────────┐
                        │    LLM / OpenAI API     │
                        │  (Sanitized Proxy Pass) │
                        └─────────────────────────┘

                        ## 2. Security Architecture Deep Dive
* **Authentication Flow:** Users authenticate directly via Supabase Auth client SDKs. The client receives a JWT, which is passed in the `Authorization: Bearer <JWT>` header on all subsequent requests to the FastAPI backend.
* **Authorization (Row Level Security):** The Supabase database implements Row Level Security (RLS). FastAPI acts as a secure agent using service-role tokens or forward-user JWTs, ensuring database rows are only accessible to their respective owners.
* **Data Transit Protection:** All external communications are strictly forced over HTTPS TLS v1.3.