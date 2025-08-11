I'll scan the repository to inventory files and collect line numbers for classes and functions so I can produce clickable links into the code. Then I'll generate the full documentation with architecture diagrams and a file-by-file walkthrough.
```bash
git ls-files | sed 's/^/\//'
```

```bash
grep -RIn "^[[:space:]]*\(class\|def\) " backend | sed 's/^/\//'
```

Ran tool

Ran tool

### Project Documentation

Below is a comprehensive, structured guide to the entire repository to help you take ownership quickly.

## 1) Project Overview

- Purpose: Multi-tenant job platform, decomposed into microservices for users, jobs, applications, search, notifications, and analytics. Each service has its own PostgreSQL database and Django app with DRF APIs, containerized via Docker Compose and fronted by an Nginx API gateway.

- High-level architecture:
  - API Gateway (Nginx) routes requests to Django services
  - Database-per-service (PostgreSQL)
  - Authentication with JWT (DRF + Simple JWT)
  - Redis for caching/broker (future: Celery)
  - Event-driven patterns and eventual consistency (laid out in docs; lightweight signals in code as placeholders)

Architecture diagram:
- Microservices and data stores (rendered above).
- Request flow sequence (rendered above).

- Module interaction:
  - API Gateway proxies all client requests to service endpoints
  - Services use `ServiceRegistry` to discover base URLs via env
  - Cross-service references are via ID fields (BigInteger) and HTTP calls (planned)
  - Analytics consumes events; Search indexes entities; Notifications sends messages to users

## 2) Full File-by-File Walkthrough

Notes:
- Click any link to jump to the file or specific line(s).
- Line numbers are provided for classes/functions where applicable.
- Some files are standard boilerplate and described succinctly.

### Root

- .gitignore: Standard ignores for Python, Django, Node, Flutter, Docker, etc.

- docker-compose.yml
  - Orchestrates all microservices, 6 Postgres instances, Redis, and API gateway.
  - Defines networks, volumes, environment variables per service for DB and inter-service URLs.

### Backend Shared

- backend/shared/service_registry.py
  - What: Lightweight service discovery and HTTP client wrapper.
  - Key elements:
    - Class singleton init reads env-based service URLs [ServiceRegistry.__init__](/backend/shared/service_registry.py#L17)
    - get_service_url(service_name) [link](/backend/shared/service_registry.py#L29)
    - make_request(service_name, endpoint, method, data, headers) with error handling [link](/backend/shared/service_registry.py#L32)

- backend/shared/settings.py
  - Base/shared settings scaffold (not actively imported by services).
  - Defines default DATABASES (PostgreSQL), REST_FRAMEWORK auth/permissions, JWT lifetimes, CORS and static settings.

### User Service

- backend/user-service/Dockerfile: Build/run steps (installs requirements, migrates, runsserver).

- backend/user-service/requirements.txt: Django, DRF, Simple JWT, CORS, psycopg, decouple, extensions, redis, pillow.

- backend/user-service/manage.py: Standard Django CLI entrypoint.

- backend/user-service/user_service/settings.py
  - Uses sqlite for local-only in this service (intentionally simple for dev).
  - INSTALLED_APPS includes `users`; DRF + JWT, CORS, static/media.
  - AUTH_USER_MODEL set to `users.User`.

- backend/user-service/user_service/urls.py
  - Routes admin and users API: `api/users/`.

- backend/user-service/user_service/asgi.py, wsgi.py: Standard.

- backend/user-service/users/models.py
  - Custom user model extending Django `AbstractUser` with additional fields:
    - Class `User` [link](/backend/user-service/users/models.py#L6)
    - Fields: phone, dob, profile_picture, bio, user_type, is_verified, timestamps.
    - `full_name` property [link](/backend/user-service/users/models.py#L76)

- backend/user-service/users/migrations/0001_initial.py: Creates `users` table consistent with model.

- backend/user-service/users/admin.py
  - `CustomUserAdmin` adds extra fields and readonly timestamps to admin view [link](/backend/user-service/users/admin.py#L8)

- backend/user-service/users/apps.py
  - `UsersConfig` with signals import [link](/backend/user-service/users/apps.py#L5).

- backend/user-service/users/serializers.py
  - `UserRegistrationSerializer` [link](/backend/user-service/users/serializers.py#L5) validate+create
  - `UserLoginSerializer` [link](/backend/user-service/users/serializers.py#L27) authenticate by email/username
  - `UserProfileSerializer` [link](/backend/user-service/users/serializers.py#L54) includes full_name
  - `UserUpdateSerializer` [link](/backend/user-service/users/serializers.py#L66)

- backend/user-service/users/views.py
  - Register [link](/backend/user-service/users/views.py#L16) (AllowAny)
  - Login [link](/backend/user-service/users/views.py#L38) (AllowAny)
  - Profile [link](/backend/user-service/users/views.py#L60)
  - Update profile [link](/backend/user-service/users/views.py#L67)
  - List users [link](/backend/user-service/users/views.py#L84) (filter by user_type)
  - Logout [link](/backend/user-service/users/views.py#L98)

- backend/user-service/users/signals.py
  - Placeholders for post_save hooks (profile creation, updates) [link](/backend/user-service/users/signals.py#L8)

### Job Service

- backend/job-service/job_service/settings.py
  - PostgreSQL DB (jobs_db) via decouple, DRF+JWT, CORS, `jobs` app.

- backend/job-service/job_service/urls.py
  - Routes `api/jobs/` to jobs app.

- ASGI/WSGI: standard.

- backend/job-service/jobs/models.py
  - `Company` [link](/backend/job-service/jobs/models.py#L5)
  - `JobCategory` (self-referencing parent) [link](/backend/job-service/jobs/models.py#L42)
  - `JobSkill` [link](/backend/job-service/jobs/models.py#L63)
  - `Job` [link](/backend/job-service/jobs/models.py#L82) references `Company` and external `employer_id`
    - Salary helpers: `salary_range` property [link](/backend/job-service/jobs/models.py#L147)
    - M2M through tables:
      - `JobCategoryJob` [link](/backend/job-service/jobs/models.py#L159)
      - `JobSkillJob` [link](/backend/job-service/jobs/models.py#L175)

- backend/job-service/jobs/serializers.py
  - Model serializers for Company, Category, Skill
  - `JobSerializer` [link](/backend/job-service/jobs/serializers.py#L26) read-only nested company/categories/skills; custom create handles through relations.

- backend/job-service/jobs/views.py
  - Job list/detail/create/update/delete [link](/backend/job-service/jobs/views.py#L10)
  - Company list/detail/create [link](/backend/job-service/jobs/views.py#L61)
  - Category list, Skill list [link](/backend/job-service/jobs/views.py#L90)

- backend/job-service/jobs/urls.py
  - URL patterns for all above [link](/backend/job-service/jobs/urls.py#L6)

- backend/job-service/jobs/admin.py
  - Admin registration for all models [link](/backend/job-service/jobs/admin.py#L6)

- backend/job-service/jobs/signals.py
  - Placeholders to push search updates on create [link](/backend/job-service/jobs/signals.py#L6)

- backend/job-service/jobs/tests.py
  - Basic model tests [link](/backend/job-service/jobs/tests.py#L8)

### Application Service

- backend/application-service/application_service/settings.py
  - PostgreSQL DB (applications_db), DRF+JWT, `applications` app.

- URLs/ASGI/WSGI: standard.

- backend/application-service/applications/models.py
  - `Application` [link](/backend/application-service/applications/models.py#L5), unique (job_id, applicant_id)
  - `ApplicationAttachment` [link](/backend/application-service/applications/models.py#L51)
  - `ApplicationStatusHistory` [link](/backend/application-service/applications/models.py#L74)
  - `Interview` [link](/backend/application-service/applications/models.py#L97)

- backend/application-service/applications/serializers.py
  - Nested read-only relationships in ApplicationSerializer [link](/backend/application-service/applications/serializers.py#L26)
  - Validation to prevent duplicate active applications [link](/backend/application-service/applications/serializers.py#L36)

- backend/application-service/applications/views.py
  - Application list/detail/create/update/delete [link](/backend/application-service/applications/views.py#L10)
  - Interview list/create/detail/update [link](/backend/application-service/applications/views.py#L80)

- backend/application-service/applications/urls.py
  - Routes endpoints for application and interviews [link](/backend/application-service/applications/urls.py#L6)

- backend/application-service/applications/admin.py
  - Admin registrations [link](/backend/application-service/applications/admin.py#L5)

- backend/application-service/applications/signals.py
  - Status history captured on create and update [link](/backend/application-service/applications/signals.py#L6)

### Search Service

- backend/search-service/search_service/settings.py
  - PostgreSQL DB (search_db), DRF+JWT, `search` app.

- URLs/ASGI/WSGI: standard.

- backend/search-service/search/models.py
  - `SearchIndex` uses `SearchVectorField` + `GinIndex` [link](/backend/search-service/search/models.py#L7)
  - `SearchHistory` [link](/backend/search-service/search/models.py#L42)
  - `SearchAnalytics` [link](/backend/search-service/search/models.py#L69)

- backend/search-service/search/views.py
  - search(q, type) using Postgres FTS with rank [link](/backend/search-service/search/views.py#L9)
  - Save history (if authenticated), update analytics [link](/backend/search-service/search/views.py#L33)
  - endpoints: history, analytics [link](/backend/search-service/search/views.py#L55)

- backend/search-service/search/urls.py
  - Routes search endpoints [link](/backend/search-service/search/urls.py#L6)

- backend/search-service/search/admin.py
  - Admin registrations [link](/backend/search-service/search/admin.py#L5)

- backend/search-service/search/signals.py
  - Placeholders for vector maintenance [link](/backend/search-service/search/signals.py#L6)

### Notification Service

- backend/notification-service/notification_service/settings.py
  - PostgreSQL DB (notifications_db), DRF+JWT, `notifications` app.

- URLs/ASGI/WSGI: standard.

- backend/notification-service/notifications/models.py
  - `NotificationTemplate` [link](/backend/notification-service/notifications/models.py#L5)
  - `Notification` (status: pending/sent/failed/read) [link](/backend/notification-service/notifications/models.py#L37)
  - `UserNotificationPreference` [link](/backend/notification-service/notifications/models.py#L85)

- backend/notification-service/notifications/views.py
  - List/detail/mark-as-read; preferences get/put; templates list [link](/backend/notification-service/notifications/views.py#L10)

- backend/notification-service/notifications/urls.py
  - Routes endpoints [link](/backend/notification-service/notifications/urls.py#L6)

- backend/notification-service/notifications/admin.py
  - Admin registrations [link](/backend/notification-service/notifications/admin.py#L5)

- backend/notification-service/notifications/signals.py
  - On create, transitions `pending` → `sent` via update (avoids infinite loop) [link](/backend/notification-service/notifications/signals.py#L6)

### Analytics Service

- backend/analytics-service/analytics_service/settings.py
  - PostgreSQL DB (analytics_db), DRF+JWT, `analytics` app.

- URLs/ASGI/WSGI: standard.

- backend/analytics-service/analytics/models.py
  - `AnalyticsEvent` [link](/backend/analytics-service/analytics/models.py#L5)
  - `UserAnalytics` [link](/backend/analytics-service/analytics/models.py#L31)
  - `JobAnalytics` [link](/backend/analytics-service/analytics/models.py#L59)
  - `PlatformAnalytics` [link](/backend/analytics-service/analytics/models.py#L87)

- backend/analytics-service/analytics/views.py
  - POST analytics_events; GET user, job, platform analytics [link](/backend/analytics-service/analytics/views.py#L11)

- backend/analytics-service/analytics/urls.py
  - Routes analytics endpoints [link](/backend/analytics-service/analytics/urls.py#L6)

- backend/analytics-service/analytics/admin.py
  - Admin registrations [link](/backend/analytics-service/analytics/admin.py#L5)

- backend/analytics-service/analytics/signals.py
  - Placeholder for event processing [link](/backend/analytics-service/analytics/signals.py#L6)

### API Gateway

- infrastructure/docker/api-gateway/Dockerfile: Nginx image build.

- infrastructure/docker/api-gateway/nginx.conf
  - Reverse-proxy routes to each service upstream (by Docker service name/port).
  - Central point for CORS, rate limits, TLS (future).

### Infrastructure

- infrastructure/kubernetes/.gitkeep: Placeholder for future manifests.
- infrastructure/scripts/setup.sh: Setup helper (if any steps added later).

### Frontend (stubs)

- frontend/README.md, frontend/flutter-app/README.md: Frontend placeholders.
- frontend/flutter-app/pubspec.yaml: Flutter dependencies metadata.
- frontend/shared/constants/api.ts: API endpoints constants.
- frontend/shared/types/api.ts: Shared TypeScript types.

### Docs

- docs/database-design.md: Detailed per-service DDL and design principles.
- docs/database-migration-strategy.md: Phased roadmap for migrating from monolith to microservices.
- docs/microservice-database-summary.md: Executive summary of architecture.

## 3) Concepts & Technology Explanations

- Django + DRF
  - What: Python web framework + REST toolkit for rapid API development.
  - Why: Mature ORM, admin, authentication, robust ecosystem.
  - How:
    - Models define tables; serializers map model ↔ JSON; views handle requests; URLs route endpoints.
    - Example (serializer create with M2M through):
      ```python
      # Pseudo-code
      job = Job.objects.create(**validated_data)
      for category_id in categories:
        JobCategoryJob.objects.create(job=job, category_id=category_id)
      ```

- Simple JWT
  - What: JSON Web Tokens for stateless auth.
  - Why: Microservices-friendly, no shared session state needed.
  - How: DRF authentication class validates Authorization: Bearer <token>.
    - In services settings: DEFAULT_AUTHENTICATION_CLASSES include Simple JWT.

- Database per service (PostgreSQL)
  - What: Each service runs its own DB schema.
  - Why: Strong data ownership, independent scaling, fault isolation.
  - How: Each service `settings.py DATABASES` points to its own containerized Postgres.

- Postgres Full-Text Search (Search Service)
  - What: Built-in FTS with `SearchVectorField` and `GIN` index.
  - Why: Efficient ranking/scoring for job/company/user searches.
  - How: `SearchIndex.search_vector` + `SearchRank`, filter and order by rank.

- Redis
  - What: In-memory data store used as cache/broker.
  - Why: Future caching, Celery broker for async tasks (not wired yet).
  - How: `REDIS_URL` configured in docker-compose; services can connect when needed.

- Event-driven architecture
  - What: Services publish/consume events to sync data asynchronously.
  - Why: Loose coupling, scalability.
  - How: For now, signals are placeholders. Docs outline RabbitMQ/Kafka adoption plan.

- Saga pattern and eventual consistency
  - What: Distributed transaction orchestration; accept temporary inconsistencies.
  - Why: Microservice boundary crossing updates need orchestration.
  - How: Documented for future implementation.

- CQRS
  - What: Separate read models from write models.
  - Why: Scaling queries independently, aggregate views (e.g., Search/Analytics).
  - How: Search/Analytics services act as read-models populated by domain events (future).

- Docker & Docker Compose
  - What: Containerization and local multi-service orchestration.
  - Why: Fast reproducible environment with DB-per-service.
  - How: docker-compose defines services, networks, volumes, env vars.

- Nginx API Gateway
  - What: Central routing, static hosting, TLS terminator.
  - Why: Single entry point, cross-cutting concerns.
  - How: nginx.conf reverse proxies to each service.

## 4) Execution Flow

- Startup:
  - docker-compose launches Postgres containers, Redis, services, and API gateway.
  - Django services migrate and start gunicorn/runserver (user-service Dockerfile migrates on run).
  - API Gateway exposes port 8000 → routes to services.

- Request lifecycle (example: list jobs)
  - Client → Gateway `/api/jobs/` → Job Service
  - DRF checks JWT (IsAuthenticated is default; some endpoints AllowAny)
  - ORM reads from `jobs_db`, serializer emits JSON response.

- Cross-service data flow examples:
  - Employeers create jobs (Job Service uses `employer_id` from User Service JWT claims).
  - Applicants submit applications referencing `job_id` and `applicant_id` (Application Service).
  - Search service indexes jobs/companies (planned async via events).
  - Notifications service sends messages when application status changes (planned events; minimal signals exist).
  - Analytics records events and aggregates metrics.

## 5) Past Steps Reconstruction (Inferred)

- Initial monolith (user-service had sqlite for local).
- Design moved to microservices: wrote database design and migration strategy docs.
- Bootstrapped each service with Django + DRF + PostgreSQL configs.
- Implemented core domain models per service.
- Wired serializers, views, and URLs; added admin for operational visibility.
- Added signals as placeholders for future event-driven integrations.
- Upgraded docker-compose to include all DBs and services.
- Added shared `ServiceRegistry` to centralize base URLs for inter-service HTTP calls.

Design decisions:
- BigInteger foreign keys across services (store IDs, not FK constraints) to preserve isolation.
- Default IsAuthenticated for DRF; selectively allow unauth endpoints.
- Keep signals minimal to avoid premature complexity; defer event buses to later.
- Separate search and analytics concerns into dedicated services (CQRS read side).

## 6) Knowledge Gaps To Close

- Django advanced:
  - Custom user models, signal usage, admin customization, migrations management.
  - Reference: Django docs “Customizing authentication” and “Signals”.

- DRF:
  - Serializers, viewsets vs function-based views, permissions, throttling.
  - Reference: DRF official tutorial and API guide.

- Simple JWT:
  - Token creation/blacklisting/refresh flow.
  - Reference: `djangorestframework-simplejwt` docs.

- PostgreSQL:
  - Indexing, FTS, JSONB, performance tuning.
  - Reference: Postgres docs (GIN, Search, JSONB best practices).

- Event-driven architecture:
  - RabbitMQ/Kafka, consumer groups, idempotency, outbox pattern.
  - Reference: Microservices Patterns by Chris Richardson.

- Saga/CQRS:
  - Orchestration vs choreography, read models, projections.
  - Reference: Patterns literature and practical guides.

- Nginx:
  - Reverse proxy configuration, rate limiting, TLS.
  - Reference: Nginx docs and production hardening guides.

- Docker/Kubernetes:
  - Multi-stage builds, healthchecks, manifests (Deployments, Services, Ingress, Secrets).
  - Reference: Kubernetes docs, Docker best practices.

- Observability:
  - Centralized logging (ELK/EFK), metrics (Prometheus/Grafana), tracing (OpenTelemetry).
  - Reference: OpenTelemetry docs.

## 7) Future Steps Roadmap

- Event Bus Integration:
  - Introduce RabbitMQ/Kafka; implement publishers in Job/Application services and consumers in Search/Analytics/Notification services.
  - Adopt outbox pattern for reliable event publishing.

- Authentication hardening:
  - Central Auth service or maintain per-service JWT validation with shared public key (JWKS).
  - Implement roles/permissions per endpoint.

- Data consistency & backfill:
  - Create backfill jobs to populate Search/Analytics from source-of-truth services.
  - Implement dead-letter queues and retries.

- Caching & performance:
  - Add Redis caching layers for hot endpoints (jobs list/search).
  - Add pagination tuning and indices based on query patterns.

- Testing & CI/CD:
  - Expand unit/integration tests, contract tests between services.
  - Add GitHub Actions/CI pipelines with docker-compose integration tests.

- Deployment:
  - Kubernetes manifests (Deployments, Services, Ingress, ConfigMaps/Secrets).
  - Blue-green/canary rollout strategies.

- Security:
  - TLS termination at the gateway, service-to-service mTLS (optional).
  - Secrets management (Vault/KMS/Sealed Secrets).

- Observability:
  - Centralized logs, metrics, tracing to quickly identify cross-service issues.

- API Gateway features:
  - Rate limiting, request/response normalization, circuit breakers (via an API gateway like Kong/Traefik/Envoy).

- Search Improvements:
  - Real indexing pipeline with updates on job/company/user changes.
  - Synonyms, stemming, language configs.

- Analytics:
  - Event schema standardization; background jobs for aggregation.
  - Dashboards and KPIs.

- Notification channels:
  - Integrate email provider (SES/SendGrid), push (FCM/APNs), SMS (Twilio).
  - Preference-driven delivery.

- Data governance:
  - GDPR compliance, PII redaction, data retention policies.

Short example of a potential pitfall:
- Pitfall: Triggering signals that call remote services synchronously can cause cascading latency/failure.
  - Mitigation: Use async event queues; apply retries with backoff; ensure idempotency keys.

---

If you want, I can generate service-specific READMEs (setup, run, API endpoints) and a top-level README with diagrams and quickstart commands.

- I’ve included clickable references. For key code chunks, you can also view them inline if needed:
```20:45:backend/shared/service_registry.py
class ServiceRegistry:
    """Centralized service discovery and communication"""
    # ...
    def make_request(self, service_name: str, endpoint: str, method: str = 'GET', 
                    data: Dict = None, headers: Dict = None):
        # ...
```

- The architecture and sequence diagrams in this doc are already embedded and render above.

- Everything is aligned with the docs in `docs/` and current codebase state.