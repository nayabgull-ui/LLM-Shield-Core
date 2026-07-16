# Phased Development Roadmap — LLM Shield

┌────────────────────────┐      ┌────────────────────────┐      ┌────────────────────────┐
│ Phase 1: Core Infra    │ ───> │ Phase 2: Secure Auth   │ ───> │ Phase 3: Defensive API │
│ Setup base directories │      │ Supabase Integration   │      │ LLM Interceptor Layer  │
└────────────────────────┘      └────────────────────────┘      └────────────────────────┘
│
┌────────────────────────┐      ┌────────────────────────┐                  ▼
│ Phase 6: Prod Launch   │ <─── │ Phase 5: CI/CD & Deploy│ <─── ┌────────────────────────┐
│ Verify DNS & CORS Sec  │      │ Vercel & Github Action │      │ Phase 4: React UI      │
└────────────────────────┘      └────────────────────────┘      │ Build Dashboards       │
└────────────────────────┘


| Phase | Milestone | Deliverables |
| :--- | :--- | :--- |
| **Phase 1** | Core Infrastructure Setup | Setup local dockerized development environments, base folder hierarchies, and dependencies. |
| **Phase 2** | Secure Auth & DB | Connect to Supabase, configure PostgreSQL tables, enable Row Level Security (RLS) policies. |
| **Phase 3** | Defensive API Layer | Implement FastAPI routes, Pydantic input validation schemas, and the core LLM sanitization proxy. |
| **Phase 4** | Frontend Development | Build the modular React components, integrate TailwindCSS, and connect to the API endpoints. |
| **Phase 5** | CI/CD Integration | Configure GitHub workflows, run Bandit security audits, and deploy previews on Vercel. |
| **Phase 6** | Hardening & Production | Enforce production-grade CORS, run penetration simulation test runs, and point to custom DNS domains. |