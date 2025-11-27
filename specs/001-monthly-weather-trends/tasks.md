---

description: "Task list for Monthly Weather Trends feature"
---

# Tasks: Monthly Weather Trends

**Input**: Design documents from `/specs/1-monthly-weather-trends/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are explicitly requested. Tasks include unit and integration tests per user story to support ≥90% coverage.

**Organization**: Tasks are grouped by user story and phase to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic backend/frontend structure using uv, FastAPI, and Next.js.

- [x] T001 Create backend project structure per plan in `backend/` (src/, tests/, domain/, api/, infrastructure/)
- [x] T002 Initialize uv-managed Python 3.12 environment and backend dependencies (FastAPI, uvicorn, pandas, pydantic, pytest, pytest-cov) in `backend/`
- [x] T003 Initialize frontend Next.js (TypeScript, app router) project in `frontend/` with eslint/prettier configs
- [x] T004 [P] Add shared Git/CI configuration for running backend and frontend tests with coverage thresholds

---

## Phase 2: Foundational (Blocking Backend Prerequisites)

**Purpose**: Core backend infrastructure that MUST be complete before any user story implementation.

- [x] T005 Create `backend/src/infrastructure/csv_loader.py` to read `src/main/resources/WeatherData.csv` using pandas
- [x] T006 Create domain models in `backend/src/domain/models/` for `WeatherObservation`, `MonthlySummary`, `DailyAggregate`, and `MonthlyTrend`
- [x] T007 Create aggregation and trend services in `backend/src/domain/services/` for yearly summaries and monthly trends
- [x] T008 Implement FastAPI app entrypoint in `backend/src/main.py` and basic router wiring under `backend/src/api/v1/`
- [x] T009 Add initial backend unit test configuration in `backend/tests/unit/` and `backend/tests/integration/` (pytest.ini or equivalent)

**Checkpoint**: Backend foundation ready - user story implementation and tests can now begin.

---

## Phase 3: User Story 1 - View yearly averages (Priority: P1) 🎯 MVP

**Goal**: Provide APIs and UI support to display yearly average temperature and humidity per month as two side-by-side charts.

**Independent Test**: User can open the app and see populated yearly average charts for the latest full year without additional configuration.

### Backend Tests for User Story 1 (US1)

- [x] T010 [P] [US1] Add unit tests for yearly aggregation logic in `backend/tests/unit/test_yearly_aggregation.py`
- [x] T011 [P] [US1] Add integration tests for `/api/v1/yearly-summary` in `backend/tests/integration/test_yearly_summary_endpoint.py`
- [x] T012 [US1] Implement yearly aggregation service using pandas in `backend/src/domain/services/yearly_aggregation_service.py`
- [x] T013 [US1] Implement `/api/v1/yearly-summary` FastAPI endpoint in `backend/src/api/v1/yearly_summary.py` using contracts from `specs/1-monthly-weather-trends/contracts/api-contracts.md`
- [x] T014 [US1] Wire yearly summary router into FastAPI app in `backend/src/main.py`
- [x] T015 [P] [US1] Add unit tests for yearly averages chart component in `frontend/tests/unit/YearlyAveragesChart.test.tsx`
- [x] T016 [US1] Add basic E2E test for loading yearly overview in `frontend/tests/e2e/yearly_overview.spec.ts`
- [x] T017 [US1] Implement typed API client for yearly summary in `frontend/lib/apiClient.ts`
- [x] T018 [US1] Implement `YearlyAveragesChart` component in `frontend/components/YearlyAveragesChart.tsx` showing two side-by-side charts for average temperature and humidity
- [x] T019 [US1] Implement main page layout in `frontend/app/page.tsx` to display yearly averages chart using data from `/api/v1/yearly-summary`

**Checkpoint**: User Story 1 complete – yearly averages charts work end-to-end and are independently testable.

---

## Phase 4: User Story 2 - Explore trends for a selected month (Priority: P2)

**Goal**: Allow user to select a month and view daily temperature and humidity trends plus the most common weather condition.

**Independent Test**: User can select any month with data and see daily trends and the most common condition for that month.

### Backend Tests for User Story 2 (US2)

- [ ] T020 [P] [US2] Add unit tests for monthly trend aggregation in `backend/tests/unit/test_monthly_trend_aggregation.py`
- [ ] T021 [P] [US2] Add integration tests for `/api/v1/monthly-trend` in `backend/tests/integration/test_monthly_trend_endpoint.py`

### Backend Implementation for User Story 2 (US2)

- [ ] T022 [US2] Implement monthly trend service to produce `MonthlyTrend` with daily aggregates and most common condition in `backend/src/domain/services/monthly_trend_service.py`
- [ ] T023 [US2] Implement `/api/v1/monthly-trend` FastAPI endpoint in `backend/src/api/v1/monthly_trend.py`
- [ ] T024 [US2] Ensure deterministic tie-breaking for most common condition in `backend/src/domain/services/monthly_trend_service.py`

### Frontend Tests for User Story 2 (US2)

- [ ] T025 [P] [US2] Add unit tests for month selector component in `frontend/tests/unit/MonthSelector.test.tsx`
- [ ] T026 [P] [US2] Add unit tests for monthly trend view component in `frontend/tests/unit/MonthlyTrendView.test.tsx`
- [ ] T027 [US2] Add E2E test for selecting a month and viewing trend in `frontend/tests/e2e/monthly_trend.spec.ts`

### Frontend Implementation for User Story 2 (US2)

- [ ] T028 [US2] Implement `MonthSelector` component in `frontend/components/MonthSelector.tsx` to allow choosing a month from available data
- [ ] T029 [US2] Implement monthly trend API client function in `frontend/lib/apiClient.ts` to call `/api/v1/monthly-trend`
- [ ] T030 [US2] Implement `MonthlyTrendView` component in `frontend/components/MonthlyTrendView.tsx` to display daily temperature/humidity charts and most common condition
- [ ] T031 [US2] Integrate `MonthSelector` and `MonthlyTrendView` into `frontend/app/page.tsx` so selecting a month updates the trend view

**Checkpoint**: User Story 2 complete – month selection and detailed trends work end-to-end and are independently testable.

---

## Phase 5: User Story 3 - Understand data assumptions and limitations (Priority: P3)

**Goal**: Clearly communicate data coverage, assumptions, and computation rules so users can interpret results correctly.

**Independent Test**: User can explain where data comes from, which year is shown, and how averages and trends are computed, based on information in the UI.

### Backend Tasks for User Story 3 (US3)

- [ ] T032 [US3] Ensure backend exposes metadata about selected year and data coverage via `/api/v1/yearly-summary` (e.g., year and observation counts)

### Frontend Tests for User Story 3 (US3)

- [ ] T033 [P] [US3] Add unit tests for data assumptions/metadata UI component in `frontend/tests/unit/DataAssumptions.test.tsx`

### Frontend Implementation for User Story 3 (US3)

- [ ] T034 [US3] Implement `DataAssumptions` component in `frontend/components/DataAssumptions.tsx` describing data source, selected year, and aggregation rules
- [ ] T035 [US3] Integrate `DataAssumptions` component into `frontend/app/page.tsx` near the charts and trend views

**Checkpoint**: User Story 3 complete – users can understand data assumptions and limitations from the UI.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and non-functional requirements.

- [ ] T036 [P] Add logging and error handling for CSV load and aggregation in `backend/src/infrastructure/csv_loader.py` and domain services
- [ ] T037 [P] Add frontend error states for missing/invalid data in `frontend/app/page.tsx` and relevant components
- [ ] T038 [P] Configure coverage reporting to enforce ≥90% coverage in backend and frontend test commands (CI and local)
- [ ] T039 [P] Update `specs/1-monthly-weather-trends/quickstart.md` with steps to run backend/frontend, tests, and view coverage reports
- [ ] T040 Perform final code cleanup and refactoring across `backend/` and `frontend/` to maintain SOLID boundaries and Next.js best practices

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - blocks all user stories.
- **User Stories (Phase 3–5)**: All depend on Foundational completion; implement in order US1 → US2 → US3.
- **Polish (Final Phase)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2); no dependencies on other stories.
- **User Story 2 (P2)**: Depends on User Story 1’s yearly summary being available for context in the UI.
- **User Story 3 (P3)**: Depends on User Stories 1 and 2 so it can reference actual behavior and data.

### Within Each User Story

- Tests MUST be written and fail before implementation tasks are fully completed.
- Domain services before API endpoints.
- API endpoints before frontend integration.
- Frontend components before E2E tests are finalized.

### Parallel Opportunities

- Setup tasks marked [P] can run in parallel.
- Backend and frontend test tasks marked [P] can run in parallel where they touch different files.
- Within a story, some component tests and implementation tasks can be parallelized if they do not modify the same files.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational backend.
3. Complete Phase 3: User Story 1 (yearly averages).
4. **Stop and VALIDATE**: Run backend and frontend tests; confirm charts render correctly.
5. Deploy/demo if ready.

### Incremental Delivery

1. Add User Story 2 (monthly trends) → Test independently → Deploy/Demo.
2. Add User Story 3 (data assumptions) → Test independently → Deploy/Demo.
3. Apply Polish & Cross-Cutting tasks.

### Per-Feature Sequencing

Implement one user story at a time (US1 → US2 → US3), with tests integrated into each phase to support ≥90% coverage and alignment with the constitution.
