# Coding Style and Working Agreement

Project-agnostic defaults for how code is written and changed.
Project-specific facts (layout, commands, domain) belong in the README, not here.

## Principles

- Prefer the smallest implementation that fully solves the requested problem.
- Prefer explicit, readable control flow over hidden state or framework magic.
- Do not introduce abstractions, layers, registries, or factories without a concrete reason.
- Keep files and functions focused on one clear responsibility.
- Give every concern a single owner. Do not duplicate it elsewhere: if the logger creates its own directory, startup code must not create it too.
- Preserve existing public contracts unless the task explicitly changes them.
- When simplicity and extensibility conflict, choose the simpler design that preserves a clear replacement boundary.

## Structure

- Start as a compact modular monolith and split by responsibility.
- Where they exist, keep these separate: transport (API/CLI), use cases, interfaces (ports), domain models, and external adapters.
- Core code depends on interfaces and typed domain models. Provider and SDK objects stay inside adapters.
- `bootstrap.py` is the composition root: it builds dependencies, selects implementations, and runs startup side effects (e.g. applying the logging config). Other modules do not wire themselves.
- Initialize process-wide resources once at startup (bootstrap or app lifespan), never at import time.

## Python

- Python 3.13+, `uv` for environments and dependencies, `ruff` for lint and format (line length 100).
- Modern typing: built-in generics, `X | Y`, `Literal` for closed sets of values, PEP 695 syntax for generics.
- Pydantic models at boundaries (I/O, settings). Frozen dataclasses for plain internal containers.
- Required dependencies are required in constructors and type annotations.
- Do not add `| None` or defensive branches for impossible states.
- Prefer module-level functions over classes that hold no state. Prefix module-internal helpers with `_`.
- Keep identifiers, comments, logs, and prompts in English.
- Comments explain why, not what. Keep docstrings short and only where they add information.

## Configuration

- Configure behavior through environment variables, loaded with `pydantic-settings`.
- Group related options into nested models (`logging`, `llm`, ...) with a fixed env prefix and `__` as the nested delimiter, e.g. `APP_LOGGING__LEVEL`.
- Loading settings is side-effect free: no directory creation, no logging setup. Expose a single cached accessor such as `get_config()`.
- Resolve relative paths against the project root, not the working directory.
- `.env.example` lists every variable with its default and is updated in the same change as the settings. `.env` and credentials are never committed or baked into images.

## Logging and Observability

- Configure logging once at startup. Modules only obtain loggers and never configure them.
- Log stage outcomes, failures, and useful identifiers. Do not log every micro-step.
- Trace external calls (LLM, HTTP, storage) with provider, model, status, latency, and usage.

## Infrastructure

- Keep local infrastructure in Docker Compose.
- Avoid shell scripts when Docker Compose can express the workflow clearly.

## Verification

- Run the smallest relevant lint, type, build, and smoke checks (`ruff check`, `ruff format`, targeted `pytest`).
- Do not add tests mechanically for low-risk prototype changes. Add them when requested or when behavior cannot be verified safely otherwise.
- Keep manual HTTP examples in a committed `rest.http` file when the project exposes an API.
- Preserve unrelated working-tree changes. Report pre-existing failures instead of fixing them silently.

## Collaboration

- Ask for clarification only when a choice materially changes the API, persisted data, security,
  cost, or destructive behavior. Otherwise pick a sensible default and state it.
- Commit messages use conventional prefixes (`feat:`, `fix:`, `refactor:`). Commit only when asked.
- Reply in the language the user writes in. Code, comments, and logs stay in English.
