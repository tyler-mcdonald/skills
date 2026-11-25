---
name: conventional-commits
description: >
  Conventional Commits cheatsheet (types, examples, reminders). Use for PR titles (see open-pr),
  and for commit messages only in repos whose own instructions (e.g. project CLAUDE.md) require
  Conventional Commits.
---

Reference: https://gist.github.com/Zekfad/f51cb06ac76e2457f11c80ed705c95a3

## Quick examples
* `feat: new feature`
* `fix(scope): bug in scope`
* `feat!: breaking change` / `feat(scope)!: rework API`
* `build(deps): update dependencies`
* `build(docker): rebuild images only on dep changes`

## Commit types
* **`build`: Changes that affect the build system or external dependencies, including Docker, compose and Makefiles (example scopes: docker, deps, npm)**
* `ci`: Changes to CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
* `chore`: Last resort for changes no other type fits
* `docs`: Documentation only changes
* **`feat`: A new feature**
* **`fix`: A bug fix**
* `perf`: A code change that improves performance
* `refactor`:  A code change that neither fixes a bug nor adds a feature
* `revert`: Revert something
* `style`: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
* `test`: Adding missing tests or correcting existing tests

## Reminders
* Scope names the part of the codebase or tool changed (`web`, `backend`, `docker`), not the audience
* Put newline before extended commit body
* More details at **[conventionalcommits.org](https://www.conventionalcommits.org/)**
