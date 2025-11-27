# [PROJECT_NAME] Constitution
<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

<!--
Sync Impact Report
- Version change: unknown → 1.0.0 (initial adoption for weather-app-speckit)
- Modified principles:
  - N/A (initial definition of all principles)
- Added sections:
  - Architecture & Next.js Constraints
  - Development Workflow & Quality Gates
- Removed sections:
  - None (template-only placeholders replaced)
- Templates requiring updates (assessment):
  - ✅ .specify/templates/plan-template.md (Constitution Check may reference SOLID, Next.js constraints, and test coverage gate)
  - ✅ .specify/templates/spec-template.md (User stories and requirements must support testability and SOLID design)
  - ✅ .specify/templates/tasks-template.md (Tasks must include testing, architecture, and observability work to satisfy principles)
  - ✅ .specify/templates/checklist-template.md (Checklists should include SOLID, Next.js practices, and coverage checks where relevant)
  - ⚠ .specify/templates/commands/* (no command templates present in this repo; none updated)
- Deferred items:
  - TODO(RATIFICATION_DATE): Original ratification date was not known at time of v1.0.0
-->

## Core Principles

### I. SOLID Weather Domain Design

The weather analysis application MUST model its domain using SOLID principles:

- Each component, hook, and service has a **single responsibility** (e.g., data loading,
  chart rendering, statistics computation).
- Domain logic (e.g., aggregations, anomaly detection, summary statistics) lives in
  framework-agnostic modules that can be tested without Next.js or React.
- Dependencies between modules follow clear contracts (TypeScript interfaces or
  abstract types) so implementations can be swapped without breaking consumers.
- Data sources (local CSV/JSON files, mocked APIs) are injected via interfaces rather
  than hard-coded imports.
- UI components depend on domain interfaces, not concrete data loaders.

**Rationale**: Keeps exploratory analysis logic reusable and testable while enabling UI
experiments without corrupting core calculations.

### II. Next.js Simplicity & Conventions

The application MUST use Next.js in a simple, convention-aligned way:

- Use the `app/` directory and file-system routing; avoid custom routing layers.
- Prefer **Server Components** by default; mark components as `"use client"` only when
  interactive state is required.
- Co-locate feature code under a single top-level route (single-page UX) using nested
  layout and child segments instead of separate apps.
- Use `next/image` for all weather-related imagery and `next/link` for intra-app
  navigation (if any navigation links are present).
- Centralize configuration and environment variables via `.env.local` and Next.js
  runtime configuration; never hard-code secrets or file paths.

**Rationale**: Aligns with Next.js best practices, reduces boilerplate, and keeps the
single-page app easy to reason about.

### III. Test-First with ≥90% Coverage (NON-NEGOTIABLE)

Testing discipline is mandatory for all work on this project:

- Adhere to a **Red–Green–Refactor** cycle: write failing tests, implement minimal
  code to pass, then refactor.
- Maintain **≥90% line and branch coverage** across domain logic, data loaders, and
  critical UI components.
- All new or changed behavior MUST be covered by unit and/or integration tests before
  merge.
- Exploratory analysis helpers (statistics, aggregations, transformations) MUST be
  pure functions with deterministic tests.

**Rationale**: High coverage is required to safely evolve the analysis logic and UI
while adding new datasets and visualizations.

### IV. Reliable Exploratory Analysis & Data Safety

Weather data handling MUST be deterministic, transparent, and safe:

- Treat local data files as **source of truth** and document their schemas.
- All parsing, validation, and transformation logic MUST handle missing, malformed, or
  out-of-range values explicitly.
- Computed metrics (e.g., daily averages, rolling means, anomalies) MUST be
  encapsulated in reusable, tested functions.
- The UI MUST clearly differentiate raw values from derived metrics (labels, legends,
  units).

**Rationale**: Users must be able to trust the analysis produced from local weather
datasets and understand how charts are derived.

### V. Observability, Performance & Maintainability

The application MUST remain observable and responsive as analysis features grow:

- Use structured logging (where applicable) and clear error surfaces in the UI for
  data loading and parsing failures.
- Prefer streaming or incremental data processing for large local files to avoid
  blocking the UI thread.
- Avoid premature optimization; profile before making performance-sensitive changes,
  but regressions in perceived performance MUST be investigated.
- Keep components small and focused; favor composition over inheritance.

**Rationale**: Ensures that the single-page experience remains fast and debuggable
even with larger weather datasets.

## Architecture & Next.js Constraints

The weather analysis app MUST satisfy the following architecture and Next.js
constraints:

- Use **TypeScript** with `strict` mode enabled for all Next.js code.
- Organize code with clear directories, e.g. `app/`, `components/`, `lib/`, and
  `data/` for local weather files.
- Encapsulate data access behind interfaces in `lib/` (e.g., `WeatherRepository`)
  implemented by concrete adapters that read local files.
- Use Next.js **data fetching** primitives (e.g., `fetch` or server functions) for any
  asynchronous data work, avoiding unnecessary client-side waterfalls.
- Prefer **static generation** or incremental static regeneration for views that do not
  depend on per-request secrets; fall back to dynamic rendering only when needed.
- Use `next/head` or the Next.js metadata API to define descriptive titles and
  meta tags for the main analysis page.
- Enforce a single entry route (e.g., `/`) that hosts the main exploratory dashboard;
  other routes, if any, support this primary experience.
- Configure ESLint with the official Next.js plugin and keep the codebase lint-clean
  before merging.
- Use Prettier (or equivalent) for consistent formatting across all Next.js and
  domain files.
- Keep third-party visualization libraries isolated behind thin adapter components so
  they can be swapped without changing domain logic.

These constraints MUST be reflected in implementation plans, tasks, and checklists
generated from this repository's Speckit templates.

## Development Workflow & Quality Gates

The development workflow MUST respect the following quality gates:

- Every feature starts with a **specification** (`spec.md`) capturing user journeys,
  acceptance criteria, and testability.
- An **implementation plan** (`plan.md`) MUST explicitly document:
  - Where SOLID boundaries live (domain vs. UI vs. data adapters).
  - How Next.js routes, layouts, and data fetching will be structured.
  - How the ≥90% coverage target will be achieved (test strategy).
- The **tasks** document (`tasks.md`) MUST include:
  - Explicit tasks for unit, integration, and (if needed) visual regression tests.
  - Tasks for linting, type-checking, and coverage enforcement.
  - Tasks for validating local data assumptions and schemas.
- No pull request may be merged unless:
  - All tests pass and coverage remains ≥90%.
  - ESLint and TypeScript checks pass.
  - Changes are consistent with the Core Principles and Architecture constraints.
  - Any intentional deviations are documented in plan.md (Complexity Tracking).

**Rationale**: Keeps the development process aligned with this constitution and makes
quality expectations explicit and enforceable.

## Governance

This constitution governs all engineering work in this repository:

- It supersedes ad-hoc conventions or historical practices where in conflict.
- Amendments MUST be recorded by updating this document, including version and
  `Last Amended` date.
- Any change that weakens a Core Principle or lowers quality gates requires a
  **MINOR** or **MAJOR** version bump, with clear rationale in the commit message.
- All PR reviews MUST explicitly consider:
  - SOLID adherence and separation of concerns.
  - Next.js architectural constraints and best practices.
  - Test coverage and quality of assertions.
  - Data safety and transparency of analysis.
- The Speckit templates (`plan-template.md`, `spec-template.md`, `tasks-template.md`,
  `checklist-template.md`) SHOULD be updated when this constitution changes in a way
  that affects gates or required sections.

**Version**: 1.0.0 | **Ratified**: TODO(RATIFICATION_DATE) | **Last Amended**: 2025-11-27

