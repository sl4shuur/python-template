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
