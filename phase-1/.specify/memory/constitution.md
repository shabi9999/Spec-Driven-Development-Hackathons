# AI-Native Todo Application Constitution

## Core Principles

### I. Spec-Driven Development
No implementation proceeds without an approved specification. Every feature, phase, and change must have a written spec that defines scope, requirements, and acceptance criteria. Specs are the source of truth for acceptance testing and architecture decisions.

### II. Deterministic Core Logic
Todo business logic (CRUD operations) must be deterministic and fully testable. State must never be hidden or implicitly managed. All operations are explicitly invoked and their effects are traceable. No side effects beyond the operation's declared scope.

### III. Simplicity First, Scalability Later
Implement the minimal viable solution for the current phase. YAGNI principle applies: do not add features, abstractions, or infrastructure for hypothetical future phases. Each phase solves its own problem without premature generalization.

### IV. Clear Separation of Concerns
Distinct layers must not be mixed: logic (business rules), storage (persistence), API (contracts), UI (presentation), AI (interface), and infrastructure (deployment). Changes in one layer must not force changes in others.

### V. AI as Assistant, Not Authority
AI acts as an interface layer and must never be a source of hidden state or implicit logic. All AI actions must call explicit, auditable functions. No hallucinated state. All decisions and mutations must be logged and explainable.

### VI. No Phase Breaks Previous Guarantees
Each successive phase builds on prior phases without removing or degrading their guarantees. Phase I in-memory guarantees remain valid in Phase II (just with persistence). Phase II API contracts remain valid in Phase III (AI adds a layer on top).

### VII. Documentation Parity
Every command, API endpoint, AI interaction, and deployment procedure must be documented. Documentation is updated when code changes; stale docs are technical debt.

## Phase Standards

### Phase I — In-Memory Python Console App
- Language: Python (3.10+)
- Storage: In-memory only (no files, no external storage)
- Interface: Console-based CLI
- Dependencies: Standard library only
- Testing: Unit tests for all business logic
- Success: Fully functional CRUD via console with zero external dependencies

### Phase II — Full-Stack Web Application
- Frontend: Next.js with TypeScript
- Backend: FastAPI with OpenAPI documentation
- ORM: SQLModel for type-safe database access
- Database: Neon (PostgreSQL)
- Architecture: Stateless backend, RESTful API only
- Frontend constraint: No direct database access; all communication via API
- Testing: Integration tests for API contracts, end-to-end tests for workflows

### Phase III — AI-Powered Todo Chatbot
- AI Framework: OpenAI ChatKit + Claude Agent SDK
- Tool Integration: Official MCP SDK for tool bindings
- Core constraint: AI calls explicit functions; no hallucinated mutations
- Logging: All AI decisions and mutations logged with audit trail
- Testing: Verify AI correctly invokes functions and respects error boundaries

### Phase IV — Local Kubernetes Deployment
- Containerization: Docker (one Dockerfile per service)
- Local cluster: Minikube
- Package manager: Helm for templating
- Operations: kubectl CLI for management
- Architecture: Clear service boundaries (frontend, backend, AI, database)
- Success: Reproducible local deployment without cloud dependencies

### Phase V — Advanced Cloud Deployment
- Messaging: Kafka for inter-service communication
- Orchestration: Dapr for service-to-service patterns
- Cloud: DigitalOcean Kubernetes Service (DOKS)
- Architecture: Event-driven where applicable, horizontally scalable
- Observability: Logs, metrics, traces ready for production monitoring
- Secrets: Environment-based, no hardcoded values

## Development Standards

### Testing Discipline
- Unit tests for isolated business logic (no mocks for pure functions)
- Integration tests for API contracts and database operations
- End-to-end tests for user workflows (Phase II onward)
- TDD encouraged: write tests before implementation
- All tests must be deterministic and runnable in isolation
- Test coverage targets: 80%+ for business logic, 60%+ overall

### Code Quality
- Code must be readable by junior-to-mid level developers
- Prefer explicit over implicit; no magic or hidden behavior
- Comments explain "why," not "what" (code reads like prose)
- Avoid premature abstractions; refactor only when duplication > 3 instances
- Type hints required in Python (Phase I+) and TypeScript (Phase II+)
- No hardcoded secrets, API keys, or environment-specific values

### API Design (Phase II+)
- RESTful endpoints with clear HTTP semantics
- OpenAPI/Swagger documentation auto-generated and kept current
- Consistent error responses with descriptive messages
- Request/response validation at API boundary
- Versioning strategy: URL-based (`/api/v1/`) for backward compatibility
- Idempotency: POST to create (201), PUT to update (200)

### Security
- Secrets managed via environment variables (`.env` files, never checked in)
- Input validation at all boundaries (API, CLI, AI tool invocations)
- No SQL injection, XSS, or other OWASP Top 10 vulnerabilities
- Authentication (if required): Stateless tokens, JWT or session-based
- Audit trail for all mutations, especially AI-initiated actions
- Rate limiting on public APIs

## Governance

### Amendment Process
1. Propose amendment with rationale and impact analysis
2. Update the constitution with version bump and ratification date
3. Propagate changes to affected templates (spec, plan, tasks)
4. Document changed principles and migration plan
5. All team members acknowledge and commit to amendment

### Version Bumping
- MAJOR: Backward incompatible removals or redefinitions of principles
- MINOR: New principles or material expansion of guidance
- PATCH: Clarifications, wording fixes, non-semantic refinements

### Compliance
- Every spec must reference relevant constitution principles
- Every plan must justify architectural decisions against constitution
- Every task must align with phase standards and testing discipline
- Pull requests must verify compliance with principles
- Code reviews explicitly check for separation of concerns and hidden logic

### Guidance Files
- Runtime development guidance: `docs/DEVELOPMENT.md` (if needed per phase)
- Phase-specific READMEs at project root
- Architecture Decision Records in `history/adr/` for significant decisions
- Prompt History Records in `history/prompts/` for all development sessions

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
