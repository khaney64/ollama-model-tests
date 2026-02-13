# API Task: Weather Station API

## Prompt

You are a senior Python developer. Build a **Weather Station API** using FastAPI with in-memory storage and a matching test suite.

### Deliverables

Produce exactly **two files**:

1. `weather_api.py` — the FastAPI application
2. `test_weather_api.py` — pytest tests using `httpx.AsyncClient`

### Data Model

A weather reading has these fields:

| Field | Type | Description |
|-------|------|-------------|
| id | int | Auto-assigned, starts at 1 |
| station_id | str | Weather station identifier, e.g. `"WS-001"` |
| timestamp | str | ISO 8601 datetime, e.g. `"2025-01-15T08:30:00"` |
| temperature_c | float | Temperature in Celsius |
| humidity_pct | float | Relative humidity percentage (0-100) |
| description | str | Brief weather description, e.g. `"Clear sky"` |

### Endpoints

Implement these four endpoints:

#### `POST /readings`
- Accepts a JSON body with all fields **except** `id` (auto-assigned)
- Returns the created reading with its `id`
- Status code: `201`

#### `GET /readings`
- Returns a list of all readings
- Supports optional query parameters:
  - `station_id` — filter by station ID (exact match)
  - `min_temp` — filter readings where `temperature_c >= min_temp`
  - `max_temp` — filter readings where `temperature_c <= max_temp`
- Filters combine with AND logic when multiple are provided
- Returns `200` with a JSON array (empty array if no matches)

#### `GET /readings/stats`
- Returns per-station aggregate statistics
- Response is a JSON object keyed by `station_id`, each containing:
  - `count` — number of readings
  - `min_temp` — lowest temperature
  - `max_temp` — highest temperature
  - `avg_temp` — average temperature (rounded to 2 decimal places)
- Returns `200` with an empty object `{}` if no readings exist

#### `DELETE /readings/{id}`
- Deletes the reading with the given `id`
- Returns `204` with no body on success
- Returns `404` with `{"detail": "Reading not found"}` if the ID does not exist

### Storage

- Use a plain Python list to store readings as dictionaries
- Use a module-level integer counter for auto-incrementing IDs
- No database, no persistence — data lives only in memory

### Test Suite (`test_weather_api.py`)

Write tests using `pytest` and `httpx.AsyncClient` with FastAPI's `ASGITransport`. Cover:

1. **Create a reading** — POST returns `201` and the reading includes an `id`
2. **List all readings** — GET returns the created readings
3. **Filter by station** — GET with `station_id` param returns only matching readings
4. **Filter by temperature range** — GET with `min_temp`/`max_temp` returns correct subset
5. **Get stats** — GET `/readings/stats` returns correct min/max/avg/count per station
6. **Delete a reading** — DELETE returns `204`, subsequent GET excludes it
7. **Delete non-existent** — DELETE returns `404`

Each test should be independent. Reset the storage between tests using a fixture.

### Constraints

- Dependencies: `fastapi`, `uvicorn`, `pytest`, `httpx` only
- No database drivers, no SQLAlchemy, no external services
- The API must run with: `uvicorn weather_api:app --reload`
- Tests must run with: `pytest test_weather_api.py -v`
- Use type hints on all function signatures
- Use Pydantic models for request/response validation

## Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Correctness | 30% | All four endpoints work as specified |
| Test Coverage | 25% | All seven test scenarios pass and are meaningful |
| Code Quality | 20% | Clean structure, type hints, Pydantic models |
| API Design | 15% | Proper status codes, error responses, query params |
| Constraints | 10% | Follows all constraints (no DB, correct deps, etc.) |

**Score each criterion 1-10 and calculate weighted total.**
