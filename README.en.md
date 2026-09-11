> [English](./README.en.md) | [中文](./README.md)
> **Blueprint**: see [BluePrint.md](./BluePrint.md)
> **Usage guide**: see [USAGE.md](./USAGE.md) · **Fill workflow**: see [FillWorkflow.md](./FillWorkflow.md)
> **Project status & acceptance record**: see [docs/project-status.md](./docs/project-status.md)
> **Status**: **ARCHIVED (no longer evolving)** — sealed 2026-09-11 as a methodology reference exemplar (mode A).
> Done before sealing: audit H1–H14, three self-found rounds X1–X25, dry run REQ-0000; `make gate` green.
> Skeleton 100% complete — but **fill 0%, pilot 0%, no real requirement walked the 10 stages**: **UNVERIFIED**.
> Sealing rationale, reusable assets (`scripts/` gate scripts) and revival conditions: `docs/project-status.md`.
>
# AI Delivery Harness Engineering

> **Note on language**: this is the English translation of the Chinese [`README.md`](./README.md).
> **All other documentation in this repository — `BluePrint.md`, `USAGE.md`, `FillWorkflow.md`,
> `docs/`, `harness/` — is in Chinese.** This file is self-contained enough to judge whether the
> project is relevant to you; the deep documentation is not translated.
>
> An AI code delivery Harness: using external constraints and a feedback system to make
> AI-generated code genuinely shippable.

[![CI](https://github.com/heweidong-ecco/ai-delivery-harness-engineering/actions/workflows/harness-ci.yml/badge.svg)](https://github.com/heweidong-ecco/ai-delivery-harness-engineering/actions/workflows/harness-ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
![Status](https://img.shields.io/badge/status-archived-lightgrey)

---

## Contents

- [1. What this is](#1-what-this-is)
- [2. Why you need it](#2-why-you-need-it)
- [3. Core philosophy](#3-core-philosophy)
- [4. What problems it solves](#4-what-problems-it-solves)
- [5. Overall architecture](#5-overall-architecture)
- [6. Directory structure](#6-directory-structure)
- [7. Core components in detail](#7-core-components-in-detail)
- [8. The ten-stage development pipeline](#8-the-ten-stage-development-pipeline)
- [9. Quick start](#9-quick-start)
- [10. Complete usage guide](#10-complete-usage-guide)
- [11. Fill guide](#11-fill-guide)
- [12. CI and gates](#12-ci-and-gates)
- [13. Metrics](#13-metrics)
- [14. Key lessons](#14-key-lessons)
- [15. FAQ](#15-faq)
- [16. Contributing](#16-contributing)
- [17. Versions and roadmap](#17-versions-and-roadmap)
- [18. License](#18-license)

---

## 1. What this is

**AI Delivery Harness Engineering** is an AI code delivery skeleton that is **not tied to any specific project**.

It has exactly one goal:

> **To make the code an AI writes not merely "syntactically correct", but genuinely shippable — after requirements analysis,
> review, unit tests, CI and deployment validation.**

It does not swap in a stronger model, and it does not lean on any particular framework. Instead it builds an
**external system of constraints and feedback**:

- **Rules**: write down the implicit rules that live inside senior developers' heads;
- **Skills**: turn each stage's best practices into an SOP;
- **Knowledge base**: feed business context to the Agent on demand;
- **Change management**: leave a trail across the whole flow;
- **Agent roles**: separate orchestration, execution and review;
- **Ten-stage pipeline**: a complete closed loop from requirement to delivery;
- **Quality gates**: verifiable programmatically;
- **Rollback paths**: route a problem precisely to the stage that has to fix it;
- **Human checkpoints**: the final say on key decisions always stays with a human.

### What it is **not** (said up front, to prevent misuse)

This is where the repo is most easily misread — read this part first:

| It is not | It actually is |
| --------- | -------------- |
| ❌ **Code scaffolding / a project starter**. It **generates no application code** — `src/` holds nothing but an empty `__init__.py`; no tech-stack selection, no module templates, no CRUD or API generators | A **constraint and process layer** sitting **on top of existing code**: rules + ten stages + gates + an end-to-end trail |
| ❌ **A starting tool for new projects**. The inputs of the 14 fill Agents are **exclusively existing artifacts** (incident reports / code reviews / architecture docs / DDL / legacy code), and **a new project has no raw material to fill** | Designed for **brownfield projects** — `BluePrint.md` §0 spells it out: hundreds of thousands of lines, many modules, an RPC framework, a workflow engine, a config center, a full middleware stack |
| ❌ **Swapping in a stronger model** | It only adds an external constraint and feedback system; model capability is out of scope for this repo |
| ❌ **Replacing human decisions** | Decision authority at the five human checkpoints always stays with a human |

It **is a container, not content**. With no real sources, it is an empty shell.

### Current status: **ARCHIVED (no longer evolving)**

- The skeleton is 100% complete; after three rounds of fixes plus one mechanical dry run, `make gate` is all green and
  `pre-commit` is 16/16 idempotent;
- But **fill 0%, pilot 0%, and the ten stages have never been walked by a real requirement** — the methodology's
  effectiveness is **UNVERIFIED**;
- **Archived ≠ abandoned**: the 5 gate scripts under `scripts/` can be lifted into any Python project, independently of
  the rest of this skeleton.

**You can verify it for yourself right now — you don't have to take any claim in this document on faith**:

```bash
bash scripts/dev-setup.sh     # one-shot environment setup (create venv, install deps, install hooks)
make gate                     # expected: EXIT=0, 137 tests passing
```

> This repo's core claim is that "**any constraint a machine cannot verify is not a constraint at all**" —
> so the description of the repo itself ought to be machine-verifiable too. Just run it.

### Known limitations (no window dressing)

| # | Limitation | Impact |
| - | ---------- | ------ |
| 1 | The CI `commit-message` job carries `if: github.event_name == 'pull_request'` | Under this repo's "push straight to main, no PRs" workflow it **never runs**; commit message discipline rests entirely on the local `check-commit-msg` hook |
| 2 | The `Markdownlint` / `Yamllint` steps run via `pre-commit run` | They pull the hook environment (including node) at CI runtime — an **added CI network dependency** |
| 3 | The `rev` in `.pre-commit-config.yaml` and the `>=` in `pyproject.toml` stay in sync through **human discipline** | They are aligned today (ruff 0.16.7 / mypy 2.3.1), but **nothing checks that consistency mechanically**; leave it long enough and it drifts |
| 4 | **Of the five human checkpoints, only HC-5 is machine-verified** | HC-1 ~ HC-4 are pure prose conventions; `human-checkpoints.md` says "blocking" but **no mechanism enforces it** |
| 5 | **`pip-audit` audits the whole environment, including packages the runner ships with** | Its verdict **depends on the host**: CI's Python 3.11 ships `setuptools 79.0.1` (PYSEC-2026-3447), while the local venv has no setuptools → you get "green locally, red in CI". **When a new CVE lands this gate can turn red on its own**, with nothing to do with this repo's code |

### Assets still reusable after archiving

The following scripts under `scripts/` **do not depend on the rest of this skeleton** and can be moved into any Python
project as they are:

| Script | Purpose |
| ------ | ------- |
| `check_pytest_report.py` | Blocks the three illusions of "all tests green": nothing ran at all / skips passed off as passes / the report is missing |
| `check_python_rules.py` | 8 programmatically enforced hard rules (money as float, HTTP timeout, bare except, print, eval, secrets, timezone…) |
| `check_secrets.py` | Secret scanning (supports line-level waivers via `pragma: allowlist secret`) |
| `check_harness_docs.py` | Document structure and code fence validation |
| `stage_gate.py` | Stage state machine: releases only when the previous stage passed **and its artifacts still exist right now**; resumes from where it stopped |

There is also material that can be adopted on its own **as process documentation**: the ten-stage pipeline, the five human
checkpoints, and the **three anti-fabrication gates**
(sources mandatory / executable mandatory / tests mandatory).

### Which document to read

| Document | For whom | When |
| -------- | -------- | ---- |
| **`README.md`** (this file) | Everyone | First look: what it is, what it is not, how far it got |
| [`docs/project-status.md`](./docs/project-status.md) | Anyone deciding "can I trust this?" | **Before deciding whether to use it** — contains measured evidence and "what you still can't trust" |
| [`BluePrint.md`](./BluePrint.md) | Designers, architecture groups | When you want to know **why it is designed this way** (L0–L7 layering, gate rollback matrix, metrics) |
| [`USAGE.md`](./USAGE.md) | Users, copiers | When you are actually **about to use it**: three usage modes, what to change after copying |
| [`FillWorkflow.md`](./FillWorkflow.md) | Fillers, Agent operators | When you are actually **about to fill in content**: source pool, the 14 Agents' prompts, the review checklist |
| [`docs/quickstart.md`](./docs/quickstart.md) | Newcomers | When you want the fastest possible start |
| [`harness/pipeline/stages.md`](./harness/pipeline/stages.md) | Executors | The **authoritative definition** of the ten stages |
| [`harness/iteration/patch-log.md`](./harness/iteration/patch-log.md) | Anyone wondering "is this credible?" | The **revision trail**: 29 defects (external audit H1–H14 + self-found X1–X25), with evidence item by item |
| [`docs/freeze.md`](./docs/freeze.md) | Maintainers | Freeze / unfreeze / archive records and changes to the working method |

> **Where this repo's credibility comes from**: it went through an **external audit**
> ([`.claude/AUDIT-外审记录与修正建议.md`](./.claude/AUDIT-外审记录与修正建议.md); the ticket headers are marked `[已修]`),
> and every one of the **14** audited defects (H1–H14) plus the **25** self-found ones (X1–X25) that followed
> **was fixed and evidenced individually**,
> with **reverse verification** as well (break a gate → the tests must go red).
> All of it is recorded in `patch-log.md` — which is far more credible than a claim like "we were very careful".

---

## 2. Why you need it

### The status quo

You may already be writing code with AI, and it does feel faster. But in a real enterprise-grade project:

- hundreds of thousands of lines of code;
- an RPC framework;
- a workflow engine;
- a config center;
- a distributed cache;
- a full middleware stack.

You have very likely run into this:

- the AI-generated code is syntactically flawless and stylistically consistent;
- but the business logic contains subtle errors;
- it compiles fine, yet falls apart at runtime.

### Typical mistakes

- A price field typed as `Double` instead of `Long`, with the unit wrong;
- changing the main path but missing the parallel change on the internationalization path;
- calling an external service with no timeout and no fallback;
- muddled transaction boundaries;
- hard-coded configuration;
- caches with no TTL.

### Why

These mistakes are **not because the model isn't smart enough**. They happen because:

> **The model doesn't know the rules of your project that were never written down.**

Those rules used to be carried by:

- word of mouth;
- code review;
- incident postmortems;
- old hands mentoring newcomers.

Now the Agent needs to know them too.

### The result (**a reference case, not a measurement from this repo**)

> ⚠ The numbers below come from **another team whose practice this repo borrows from**, working on a brownfield project.
> They are **not results measured in this repo**. **This repo's own real-world usage data is zero** (fill 0%, pilot 0%).
> They are listed to show that "this approach has worked elsewhere", **not** to claim "this repo has been proven effective".

An Alibaba team spent one week standing up a Harness system on a brownfield project:

- Project-level AI code ratio: **24.86% → 90.54%**
- Individual-level AI code ratio: **14.24% → 87.85%**
- Rework rounds: **3–5 → usually 1**

They did not switch to a stronger model. They simply built an external system of constraints and feedback.

---

## 3. Core philosophy

### Principle 1: engineer the errors away

Every time the Agent makes a mistake, the response is not to add a line saying "please be careful not to do this again",
but rather:

> **Turn the constraint into a file, a rule, an automated check — make it part of the system.**

### Principle 2: programmatically verifiable

> **Any constraint a machine cannot verify is not a constraint at all when an Agent is executing.**

For example:

- ❌ "Check whether CI passed" → the Agent may treat a `Success` status as passing and ignore a test count of 0;
- ✅ "Status=SUCCESS and TotalTest>0 and Passed=Total" → the ambiguity is eliminated entirely.

### Principle 3: separate execution from judgement

> **The Agent that does the work and the Agent that judges it must be different.**

The review Agent doesn't need to be smarter; it just needs a **checklist from a different angle** with which to examine
the artifacts.

### Principle 4: just enough context

> **Give the Agent exactly enough context at any moment — no more, no less.**

Loaded in three layers:

1. **Session-resident**: the Agent definition + rule files;
2. **Stage-triggered**: load the matching Skill only when entering that stage;
3. **On-demand lookup**: the Wiki is not loaded proactively; the Agent consults it on its own.

### Principle 5: process consistency beats process efficiency

> **Cases of a small change causing a huge incident are too numerous to count.**

A tiny requirement touching only two files and six lines of code still walks the full ten stages. When a requirement is
simple enough, every stage naturally takes less time — but process consistency guarantees that no key step is skipped
just because "this change is small".

### Principle 6: specs are living documents

> **Every line of the spec corresponds to a historical failure case.**

Every time real-world use surfaces a new problem, it is patched into the Harness immediately. When a rule strikes you as
redundant or long-winded, there is usually a pit someone really fell into behind it.

---

## 4. What problems it solves

### Four typical failure modes

| Failure mode                       | Symptom                                                     | Root cause                |
| ---------------------------------- | ----------------------------------------------------------- | ------------------------- |
| **Trying to do it all in one go**  | Quality collapses fast once context usage passes 40%        | No stage decomposition    |
| **Declaring victory too early**    | "Coding done" after finishing part of the work              | No acceptance gate        |
| **No end-to-end verification**     | A broken critical path is discovered only after deployment  | No CI verification        |
| **The cold-start problem**         | Re-understanding the project from scratch every session     | No accumulated knowledge  |

### The common root

> **The Agent lacks external, structured constraints and a feedback mechanism.**

Anthropic put it plainly in an engineering blog post:

> **Agents cannot accurately evaluate the quality of their own output. You cannot expect an Agent to review itself.**

---

## 5. Overall architecture

### Layered architecture

```text
L0 Goals and metrics layer
  ├── AI code ratio
  ├── Rework rounds
  ├── Human confirmation rounds
  └── Quality gate pass rate

L1 Governance and rules layer
  ├── Engineering structure rules
  ├── Development process standard
  ├── Project coding standard
  ├── Python coding standard
  ├── Python layering standard
  ├── Security standard
  ├── Error handling standard
  ├── Logging standard
  ├── Observability standard
  ├── Performance standard
  ├── Database standard
  ├── API design standard
  ├── Concurrency standard
  ├── Caching standard
  ├── Idempotency standard
  ├── Timezone standard
  ├── Dependency standard
  ├── Testing standard
  └── Internationalization standard

L2 Orchestration and roles layer
  ├── Application Owner Agent
  ├── Coding Agent
  ├── Review Agent
  └── Human decision maker

L3 Knowledge and skills layer
  ├── 9 core Skills
  ├── Extension Skills
  ├── Wiki knowledge base
  └── Layered context loading

L4 Execution pipeline layer
  ├── Requirements analysis → Requirements review → Plan review
  ├── Implementation → Code review
  ├── Unit test authoring → Unit test review
  └── CI verification → Deployment verification → User confirmation

L5 Quality gates and rollback layer
  ├── Programmatic verification
  ├── Review loop limits
  ├── Precise rollback paths
  └── Human escalation mechanism

L6 Change and knowledge accumulation layer
  ├── Independent directory per requirement
  ├── End-to-end trail
  ├── Incrementing review versions
  └── A living project development handbook

L7 Continuous iteration layer
  ├── Dry-run verification
  ├── Real-world problem patches
  └── Continuous spec iteration
```

### Data flow

```text
Real sources (incidents / reviews / architecture / DDL / codebase)
        ↓
   Fill Agents
        ↓
  Rules / Skills / Wiki
        ↓
   Ten-stage pipeline
        ↓
    Quality gates
        ↓
   Feedback and Patch
        ↓
   Back to rules / skills / Wiki
```

---

## 6. Directory structure

```text
ai-delivery-harness-engineering/
│
├── README.md                              # this file
├── LICENSE                                # MIT license
├── CONTRIBUTING.md                        # contributing guide
├── CHANGELOG.md                           # changelog
├── SECURITY.md                            # security policy
├── Dockerfile                             # containerization
├── docker-compose.yml                     # local orchestration
├── pyproject.toml                         # Python project configuration
├── Makefile                               # common commands
├── requirements.txt                       # compatibility with legacy tooling
├── requirements-dev.txt                   # compatibility with legacy tooling
│
├── .pre-commit-config.yaml                # Pre-commit hooks
├── .gitignore                             # Git ignores
├── .gitattributes                         # Git attributes
├── .editorconfig                          # editor configuration
├── .env.example                           # example environment variables
├── .env.ci                                # CI environment variables
├── .env.test                              # test environment variables
├── .gitmessage                            # commit template
├── .yamllint.yml                          # YAML linting
├── .markdownlint.yml                      # Markdown linting
├── .coveragerc                            # coverage configuration
├── .bandit                                # security scan configuration
├── .importlinter                          # layered dependency checking
├── .dockerignore                          # container ignores
│
├── .github/
│   ├── workflows/
│   │   ├── harness-ci.yml                 # main CI workflow
│   │   ├── auto-label.yml                 # automatic labeling
│   │   ├── stale.yml                      # stale issues
│   │   ├── release.yml                    # release
│   │   ├── dependency-update.yml          # dependency updates
│   │   └── security-scan.yml              # security scan
│   ├── PULL_REQUEST_TEMPLATE.md           # PR template
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md                  # bug template
│   │   ├── feature_request.md             # feature request template
│   │   └── config.yml                     # issue configuration
│   ├── labeler.yml                        # label rules
│   ├── CODEOWNERS                         # code owners
│   └── dependabot.yml                     # dependency updates
│
├── .vscode/
│   ├── settings.json                      # VSCode configuration
│   └── extensions.json                    # recommended extensions
│
├── config/                                # observability config (examples, **none of them wired up** — see each file's header)
│   ├── prometheus.yml                     # Prometheus example
│   ├── alert-rules.yml                    # alert rules example (metric names not produced yet)
│   ├── logging.yml                        # logging config example (no consumer yet)
│   └── grafana/
│       └── dashboard.json                 # Grafana dashboard example (no datasource/query)
│
├── docs/
│   ├── quickstart.md                      # quick start
│   ├── fill-guide.md                      # fill guide
│   ├── faq.md                             # FAQ
│   ├── architecture.md                    # skeleton architecture
│   ├── freeze.md                          # freeze / unfreeze records
│   ├── project-status.md                  # project status and acceptance record (what to trust, what not to)
│   ├── naming-conventions.md              # naming conventions
│   ├── versioning.md                      # versioning policy
│   ├── anti-patterns.md                   # anti-patterns
│   ├── best-practices.md                  # best practices
│   ├── glossary.md                        # glossary
│   ├── roadmap.md                         # roadmap
│   ├── integrations.md                    # integration notes
│   ├── compliance.md                      # compliance notes
│   ├── data-governance.md                 # data governance
│   ├── threat-model.md                    # threat model
│   ├── capacity-planning.md               # capacity planning
│   ├── adr/
│   │   ├── README.md                      # ADR index
│   │   └── template.md                    # ADR template
│   └── tutorials/
│       ├── first-rule.md                  # your first rule
│       ├── first-agent.md                 # your first Agent
│       └── first-requirement.md           # your first requirement
│
├── harness/
│   │
│   ├── rules/                             # rule system
│   │   ├── project-structure.md           # engineering structure
│   │   ├── dev-process.md                 # development process
│   │   ├── coding-standard.md             # coding standard
│   │   ├── python-coding-standard.md      # Python coding standard
│   │   ├── python-layers.md               # Python layering
│   │   ├── security-standard.md           # security standard
│   │   ├── error-handling.md              # error handling
│   │   ├── logging-standard.md            # logging standard
│   │   ├── observability-standard.md      # observability
│   │   ├── performance-standard.md        # performance standard
│   │   ├── database-standard.md           # database standard
│   │   ├── api-design-standard.md         # API design standard
│   │   ├── concurrency-standard.md        # concurrency standard
│   │   ├── cache-standard.md              # caching standard
│   │   ├── idempotency-standard.md        # idempotency standard
│   │   ├── timezone-standard.md           # timezone standard
│   │   ├── dependency-standard.md         # dependency standard
│   │   ├── testing-standard.md            # testing standard
│   │   ├── i18n-standard.md               # internationalization standard
│   │   └── _template.md                   # rule template
│   │
│   ├── skills/                            # skill system
│   │   ├── _template/
│   │   │   └── SKILL.md
│   │   ├── coding/
│   │   │   └── SKILL.md                   # coding skill
│   │   ├── expert-reviewer/
│   │   │   ├── SKILL.md                   # review skill
│   │   │   └── checklists/
│   │   │       └── python.md              # Python review checklist
│   │   ├── unit-test/
│   │   │   ├── SKILL.md                   # unit test skill
│   │   │   ├── test-data-guide.md         # test data guide
│   │   │   └── mocking-guide.md           # mocking guide
│   │   ├── request-analysis/
│   │   │   └── SKILL.md                   # requirements analysis
│   │   ├── task-breakdown/
│   │   │   └── SKILL.md                   # task decomposition
│   │   ├── ci-validation/
│   │   │   └── SKILL.md                   # CI verification
│   │   ├── deploy-validation/
│   │   │   ├── SKILL.md                   # deployment verification
│   │   │   └── rollback-sop.md            # rollback SOP
│   │   ├── doc-management/
│   │   │   └── SKILL.md                   # document management
│   │   ├── knowledge-qa/
│   │   │   └── SKILL.md                   # knowledge Q&A
│   │   ├── performance/
│   │   │   └── profiling.md               # performance profiling
│   │   ├── security/
│   │   │   └── audit.md                   # security audit
│   │   ├── refactor/
│   │   │   └── SKILL.md                   # refactoring
│   │   ├── migration/
│   │   │   └── SKILL.md                   # migration
│   │   ├── api-versioning/
│   │   │   └── SKILL.md                   # API versioning
│   │   └── db-migration/
│   │       └── SKILL.md                   # database migration
│   │
│   ├── wiki/                              # knowledge base
│   │   ├── README.md                      # Wiki index
│   │   ├── glossary.md                    # glossary
│   │   ├── data-model.md                  # data model
│   │   ├── business-flows.md              # business flows
│   │   ├── monitoring.md                  # monitoring metrics
│   │   ├── rollback-playbook.md           # rollback playbook
│   │   ├── onboarding.md                  # newcomer onboarding
│   │   └── faq.md                         # business FAQ
│   │
│   ├── templates/                         # general templates
│   │   ├── incident.md                    # incident
│   │   ├── postmortem.md                  # postmortem
│   │   ├── design-doc.md                  # design document
│   │   ├── rfc.md                         # RFC
│   │   └── runbook.md                     # runbook
│   │
│   ├── changes/                           # change management
│   │   ├── README.md                      # change index + template notes + artifact checklist
│   │   └── _template/                     # deliverables only (so `cp *.md` gives you the full set of seven)
│   │       ├── requirement-analysis.md    # requirements analysis
│   │       ├── task-breakdown.md          # task decomposition
│   │       ├── coding-report.md           # coding report
│   │       ├── review-record-v1.md        # review record
│   │       ├── unit-test-report.md        # unit test report
│   │       ├── ci-result.md               # CI result
│   │       └── deploy-validation.md       # deployment validation
│   │
│   ├── pipeline/                          # pipeline
│   │   ├── stages.md                      # the ten stages
│   │   ├── human-checkpoints.md           # the five human checkpoints
│   │   ├── escalation.md                  # escalation
│   │   ├── hotfix-process.md              # hotfix
│   │   ├── release-process.md             # release
│   │   └── rollback-process.md            # rollback
│   │
│   ├── metrics/                           # metrics
│   │   ├── metrics.md                     # metrics
│   │   ├── dashboard.md                   # dashboard
│   │   ├── collection.md                  # collection
│   │   ├── badges.md                      # badges
│   │   └── sla.md                         # SLA
│   │
│   ├── iteration/                         # iteration
│   │   ├── README.md                      # patch notes
│   │   ├── patch-log.md                   # patch log
│   │   └── retrospective.md               # retrospective
│   │
│   ├── sources/                           # source pool
│   │   ├── README.md                      # source notes
│   │   ├── incidents/                     # incidents
│   │   ├── reviews/                       # reviews
│   │   ├── architecture/                  # architecture
│   │   ├── ddl/                           # DDL
│   │   ├── api/                           # APIs
│   │   ├── flows/                         # flows
│   │   └── code/                          # code
│   │
│   ├── agents/                            # Agent roles (definitions + fill agents, same directory)
│   │   ├── README.md                      # Agent index
│   │   ├── orchestrator.md                # orchestration
│   │   ├── fill-harness.md                # fill master guide
│   │   ├── orchestrator-report.md         # orchestration report
│   │   ├── application-owner.md           # primary orchestration role
│   │   ├── application-owner-python.md    # Python extension
│   │   ├── architecture-agent.md          # architecture parsing
│   │   ├── incident-agent.md              # incident reverse-engineering
│   │   ├── review-agent.md                # review distillation
│   │   ├── code-archaeology-agent.md      # code archaeology
│   │   ├── data-modeling-agent.md         # data modeling
│   │   ├── gate-agent.md                  # gate parsing
│   │   ├── security-agent.md              # security
│   │   ├── performance-agent.md           # performance
│   │   ├── refactor-agent.md              # refactoring
│   │   ├── dependency-agent.md            # dependencies
│   │   └── doc-agent.md                   # documentation
│   │
│   ├── glossary/                          # domain glossary index
│   │   └── README.md
│   │
│   ├── pilot/                             # dry runs and pilots
│   │   ├── runbook.md                     # dry-run runbook
│   │   └── findings.md                    # dry-run findings
│   │
│   ├── state/                             # requirement state
│   │   ├── README.md
│   │   └── stages.json                    # ten-stage gate configuration (stage → artifacts)
│   │
│   ├── audit/                             # audit
│   │   └── README.md
│   │
│   ├── checkpoints/                       # checkpoints (HC-1~HC-5 records)
│   │   ├── README.md
│   │   └── _template.md                   # HC record template (required by the stage-10 artifact)
│   │
│   └── schemas/                           # schemas
│       ├── rule-schema.json
│       ├── skill-schema.json
│       └── data/                          # data files (created when filling; if missing the gate reports "not implemented" explicitly)
│
├── scripts/                               # check scripts
│   ├── check_pytest_report.py             # test report check
│   ├── check_python_rules.py              # Python rule check
│   ├── check_harness_docs.py              # Harness file check
│   ├── check_layers.py                    # layering check
│   ├── check_commit_msg.py                # commit message check
│   ├── check_secrets.py                   # secret scanning
│   ├── check_complexity.py                # complexity check
│   ├── check_dependencies.py              # dependency check
│   ├── check_i18n.py                      # i18n check
│   ├── collect_metrics.py                 # metrics collection
│   ├── audit_log.py                       # audit log
│   ├── state_tracker.py                   # state tracking (deprecated, forwards to stage_gate)
│   ├── stage_gate.py                      # stage state machine (precondition check + resume)
│   ├── validate_schemas.py                # schema validation
│   ├── check-gates.sh                     # stage artifact gate (incremental --stage)
│   ├── install-hooks.sh                   # install hooks
│   └── dev-setup.sh                       # development environment
│
├── src/                                   # business code (to be filled)
│   └── __init__.py
│
└── tests/                                 # tests
    ├── README.md                          # test notes
    ├── conftest.py                        # shared fixtures
    ├── test_smoke.py                      # smoke test
    └── test_scripts.py                    # script tests
```

---

## 7. Core components in detail

### 1. The rule system (`harness/rules/`)

**Purpose**: to tell the Agent what "standard" means — stable constraints that do not change from requirement to
requirement.

**Characteristics**:

- not in the code, yet every senior developer knows them;
- formerly passed on by word of mouth, now written into files;
- behind every rule is a pit somebody actually fell into.

**The six-part rule**:

| Field            | Description                       |
| ---------------- | --------------------------------- |
| Rule             | A one-line description            |
| Reason           | The incident / review / doc it came from |
| Counter-example  | The wrong code                    |
| Example          | The right code                    |
| Check            | An executable script or lint rule |
| Test             | A test that can fail and can pass |

### 2. The skill system (`harness/skills/`)

**Purpose**: to turn each stage's best practices into a structured SOP.

**Core Skills**:

| Skill             | Purpose                                        |
| ----------------- | ---------------------------------------------- |
| Coding            | Implement layer by layer following the layering spec |
| Expert Reviewer   | Independently review the plan and the execution |
| UnitTest          | Change-driven tests                            |
| Request Analysis  | Requirements analysis                          |
| Task Breakdown    | Task decomposition                             |
| CI Validation     | CI verification                                |
| Deploy Validation | Deployment verification                        |
| Doc Management    | Document management                            |
| Knowledge QA      | Knowledge Q&A                                  |

**The key design of the review Skill**:

Every review comment must contain:

- a description of the problem
- a suggested change
- a priority level (P0/P1/P2)

### 3. The knowledge base (`harness/wiki/`)

**Purpose**: the raw material with which the Agent understands business context.

**Characteristics**:

- it is **not loaded in full proactively**;
- the Agent consults it on its own as the task requires;
- the whole point is "fetch on demand".

**Contents**:

- domain glossary
- data model
- core business flows
- monitoring metrics
- rollback playbook
- newcomer onboarding
- business FAQ

### 4. Change management (`harness/changes/`)

**Purpose**: an independent directory per requirement, with a trail across the whole flow.

**Directory structure**:

```text
harness/changes/REQ-XXXX/
├── requirement-analysis.md
├── task-breakdown.md
├── coding-report.md
├── review-record-v1.md
├── review-record-v2.md     # version increments
├── unit-test-report.md
├── ci-result.md
└── deploy-validation.md
```

**Characteristics**:

- review files increment by version;
- old versions are never deleted;
- the whole flow is traceable.

### 5. Agent roles (`harness/agents/`)

> Role definitions (`application-owner*.md`) and the fill Agents (`*-agent.md`, `orchestrator.md`,
> `fill-harness.md` — 14 in total) live **in the same directory**; for the index see `harness/agents/README.md`.

**Application Owner**: the orchestration hub of the entire system, roughly 400 lines, containing 5 modules:

| Module                               | Contents                                                                 |
| ------------------------------------ | ------------------------------------------------------------------------ |
| Role and project background          | 20–30 lines, just enough project vision                                  |
| Configuration hub index              | The paths, responsibilities and trigger scenarios of Rules, Skills, Wiki and MCP |
| Seven core responsibilities          | Requirement understanding, task decomposition, task dispatch, task acceptance, quality control, document management, knowledge Q&A |
| Workflow scheduling instructions     | The complete scheduling logic for the ten stages                         |
| Communication principles and hard constraints | Two lists: must do / must not do                                |

### 6. Pipeline (`harness/pipeline/`)

**The ten stages**:

1. Requirements analysis
2. Requirements review
3. Plan review
4. Implementation
5. Code review
6. Unit test authoring
7. Unit test review
8. CI verification
9. Deployment verification
10. User confirmation

**Three elements per stage**:

- trigger condition
- Skill loading
- quality gate

**Rollback paths**:

| Failure                        | Roll back to        |
| ------------------------------ | ------------------- |
| CI fails but the test count is 0 | Unit test authoring |
| Compile error                  | Implementation      |
| Requirement mismatch           | Requirements analysis |
| Review limit exceeded          | Escalate to a human |

**Review loop limits**:

- Requirements review: at most 3 rounds
- Code review: at most 2 rounds
- Unit test review: at most 2 rounds

### 7. Quality gates (`scripts/` + CI)

**Programmatically verifiable conditions**:

| Gate        | Command                  | Pass condition                  |
| ----------- | ------------------------ | ------------------------------- |
| Lint        | `ruff check .`           | exit 0                          |
| Format      | `ruff format --check .`  | exit 0                          |
| Type        | `mypy src`               | exit 0                          |
| Test        | `pytest --json-report`   | exit 0                          |
| Test Report | `check_pytest_report.py` | `TotalTest>0` and `Passed=Total` |
| Rules       | `check_python_rules.py`  | no output                       |
| Layers      | `check_layers.py`        | no output                       |
| Secrets     | `check_secrets.py`       | no output                       |
| Complexity  | `check_complexity.py`    | no output                       |
| i18n        | `check_i18n.py`          | no output                       |
| Docs        | `check_harness_docs.py`  | nothing missing                 |
| Schema      | `validate_schemas.py`    | no errors                       |
| Bandit      | `bandit -r src -q`       | exit 0                          |

### 8. Fill Agents (`harness/agents/`)

**Purpose**: extract rules from real sources and fill the Harness.

| Agent            | Input               | Output                |
| ---------------- | ------------------- | --------------------- |
| Orchestrator     | Everything          | Scheduling            |
| Architecture     | architecture/, src/ | Layering rules        |
| Incident         | incidents/          | Hard constraint rules |
| Review           | reviews/            | Coding standard       |
| Code Archaeology | src/                | Templates and counter-examples |
| Data Modeling    | ddl/, api/, flows/  | Wiki                  |
| Gate             | CI, Makefile        | Gate checklist        |
| Security         | Security audit      | Security rules        |
| Performance      | Performance incidents | Performance rules   |
| Refactor         | src/                | Refactoring rules     |
| Dependency       | pyproject.toml      | Dependency rules      |
| Doc              | src/, changes/      | Documentation         |

**The three anti-fabrication gates**:

1. **Sources mandatory**: every rule must have a source; an empty source is rejected;
2. **Executable mandatory**: every rule must have a check command; if it doesn't run, it is rejected;
3. **Tests mandatory**: every P0 rule must have a test, and the test must be able to fail as well as pass.

---

## 8. The ten-stage development pipeline

| Stage              | Trigger              | Skill             | Artifacts       | Gate                                      | Rollback      | Human confirmation       |
| ------------------ | -------------------- | ----------------- | --------------- | ----------------------------------------- | ------------- | ------------------------ |
| 1. Requirements analysis | New requirement | request-analysis | Requirements analysis doc | Boundaries clear           | -             | Pending-decision confirmation |
| 2. Requirements review | Analysis complete | expert-reviewer | Review record  | Comments complete                          | Requirements analysis | Pending-decision confirmation |
| 3. Plan review     | Breakdown complete   | expert-reviewer   | Plan review     | Actionable                                | Task decomposition | Confirmation after plan review |
| 4. Implementation  | Plan confirmed       | coding            | Code, report    | Compiles                                  | Implementation | -                       |
| 5. Code review     | Coding complete      | expert-reviewer   | Review record   | Issues graded                             | Implementation | Confirmation after code review |
| 6. Unit test authoring | Coding passed    | unit-test         | Tests, report   | Cases > 0                                 | Unit test authoring | -                  |
| 7. Unit test review | Tests complete      | expert-reviewer   | Review record   | Assertions complete                       | Unit test authoring | -                  |
| 8. CI verification | Tests passed         | ci-validation     | CI result       | Status=SUCCESS, TotalTest>0, Passed=Total | Unit test authoring | -                  |
| 9. Deployment verification | CI passed    | deploy-validation | Deployment report | Parameters correct                     | Parameter confirmation | Deployment environment parameters confirmed |
| 10. User confirmation | Deployment passed | doc-management    | Delivery confirmation | User approves                      | Requirements analysis | Final delivery confirmation |

### The five human checkpoints

| ID   | Name                              | Timing                | Decision content               |
| ---- | --------------------------------- | --------------------- | ------------------------------ |
| HC-1 | Pending-decision confirmation     | After requirements review | Boundaries, acceptance, priority |
| HC-2 | Confirmation after plan review    | After plan review     | Tasks, dependencies, risks     |
| HC-3 | Confirmation after code review    | After code review     | Code quality, business logic   |
| HC-4 | Deployment environment parameters confirmed | Before deployment | Environment, configuration, parameters |
| HC-5 | Final delivery confirmation       | User confirmation stage | Whether the requirement is met |

---

## 9. Quick start

### Prerequisites

- Python 3.11+
- Git
- Make
- (Optional) Docker

### Installation

```bash
# 1. Clone
git clone <repo-url>
cd ai-delivery-harness-engineering

# 2. One-shot initialization (recommended)
bash scripts/dev-setup.sh

# Or manually
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e ".[dev]"

# 3. Install hooks
pre-commit install
pre-commit install --hook-type commit-msg
git config commit.template .gitmessage
```

### Running the gates

```bash
make gate
```

Equivalent to:

```bash
ruff check .
ruff format --check .
mypy src
pytest --json-report --json-report-file=pytest-report.json
python scripts/check_pytest_report.py pytest-report.json
python scripts/check_python_rules.py src
python scripts/check_layers.py src
python scripts/check_complexity.py src
python scripts/check_i18n.py src
python scripts/check_secrets.py .
python scripts/check_harness_docs.py
python scripts/validate_schemas.py
```

### Running with Docker

```bash
docker compose up harness
```

---

## 10. Complete usage guide

### Scenario 1: use it as a standalone exemplar

You want to use this Harness as a methodology exemplar for your team.

**Steps**:

1. Fork or clone this repository;
2. read `docs/architecture.md` to understand the overall architecture;
3. read `harness/pipeline/stages.md` to understand the ten-stage pipeline;
4. read `harness/agents/application-owner.md` to understand the orchestration logic;
5. follow `docs/fill-guide.md` to fill in your project's content with the Agents;
6. have the team execute along the ten-stage pipeline.

### Scenario 2: introduce it into an existing Python project

**Steps**:

```bash
# 1. In the existing project
cd your-existing-project

# 2. Copy the harness directory over
cp -r /path/to/ai-delivery-harness-engineering/harness ./harness
cp -r /path/to/ai-delivery-harness-engineering/scripts ./scripts
cp /path/to/ai-delivery-harness-engineering/.pre-commit-config.yaml .
cp /path/to/ai-delivery-harness-engineering/Makefile .

# 3. Merge the dev dependencies from pyproject.toml

# 4. Install
pip install -e ".[dev]"
pre-commit install

# 5. Run the gates
make gate
```

**Note**: if you already have CI, merge `.github/workflows/harness-ci.yml` into your existing CI.

### Scenario 3: fill the Harness

**Steps**:

```bash
# 1. Create the source pool
mkdir -p harness/sources/{incidents,reviews,architecture,ddl,api,flows,code}

# 2. Drop in real material (all of it desensitized)
# - Incident reports → incidents/
# - Review comments → reviews/
# - Architecture docs → architecture/
# - DDL → ddl/
# - API docs → api/
# - Flow diagrams → flows/
# - Codebase → point directly at src/

# 3. Run the Agents in order (each on its own branch + PR)
# Agent 1: architecture parsing
# Agent 2: incident reverse-engineering
# Agent 3: review distillation
# Agent 4: code archaeology
# Agent 5: data modeling
# Agent 6: gate parsing

# 4. Human review of each Agent's output
# 5. Merge and fill back in
# 6. Update the check scripts and tests
# 7. Commit
```

### Scenario 4: execute one requirement

**Steps**:

```bash
# 1. Create a branch
git checkout -b feature/req-0001

# 2. Create the requirement directory
mkdir -p harness/changes/REQ-0001
cp harness/changes/_template/*.md harness/changes/REQ-0001/

# 3. Write the requirements analysis
vim harness/changes/REQ-0001/requirement-analysis.md

# 4. Requirements review
# Load Expert Reviewer, review, at most 3 rounds
# HC-1 human confirmation

# 5. Task decomposition
vim harness/changes/REQ-0001/task-breakdown.md

# 6. Plan review
# Load Expert Reviewer, review, at most 3 rounds
# HC-2 human confirmation

# 7. Implementation
# Load the Coding Skill, implement following the layering spec

# 8. Code review
# Load Expert Reviewer, review, at most 2 rounds
# HC-3 human confirmation

# 9. Unit test authoring
# Load the UnitTest Skill, change-driven tests

# 10. Unit test review
# Load Expert Reviewer, review, at most 2 rounds

# 11. CI verification
make gate

# 12. Deployment verification
# HC-4 environment parameter confirmation
# Verify the critical path after deployment

# 13. User confirmation
# HC-5 final delivery confirmation

# 14. Commit
git add harness/changes/REQ-0001
git commit -m "docs: add req-0001"
git push -u origin feature/req-0001
gh pr create --title "REQ-0001" --body "Executed through the Harness ten-stage process"
```

### Scenario 5: dry-run verification

**Goal**: before using it on a real requirement, do one dry run to surface defects in the system itself.

```bash
# 1. Create a dry-run requirement
mkdir -p harness/changes/REQ-0000
cp harness/changes/_template/*.md harness/changes/REQ-0000/

# 2. Walk all ten stages
# 3. Record the defects found at each stage

# 4. Common dry-run defects
# - The CI gate only checks the status code, ignoring a test count of 0
# - Under a simple requirement the review report does not produce a file
# - Duplicate lines appear in the summary file
# - Deployment parameters are guessed wrong by the Agent

# 5. Record them in harness/pilot/findings.md
# 6. Patch every defect back into the Harness
```

### Scenario 6: hotfix

```bash
git checkout -b hotfix/fix-payment-timeout
# Minimal change
# A new test is mandatory
# A new incident rule is mandatory
# Two-person review
# CI passes
# Deployment verification
# Record it under harness/changes/HOTFIX-XXXX/
```

### Scenario 7: release

```bash
# Pre-release checks
- [ ] All requirements pass CI
- [ ] All human checkpoints are complete
- [ ] Regression tests pass
- [ ] Monitoring is ready
- [ ] A rollback plan is ready

# Tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Deploy staging → verify → deploy prod → monitor
```

### Scenario 8: rollback

```bash
# Triggers
# - The critical path is broken
# - Monitoring is abnormal
# - The data is abnormal

# Steps
# 1. The decision maker confirms
# 2. Run the rollback command
# 3. Verify the main path
# 4. Verify the internationalization path
# 5. Verify data consistency
# 6. Watch the monitoring
# 7. Record it in patch-log.md
# 8. Retrospective
```

---

## 11. Fill guide

### The fill formula

```text
Real sources + structured Prompt + six-part output + human review + executable checks = thick rules
```

### The six core fill Agents

#### Agent 1: architecture parsing

**Input**:

- `harness/sources/architecture/`
- `src/`

**Steps**:

1. scan every package and module under `src/`;
2. count who imports each module;
3. infer the layering;
4. find imports that violate the layering direction;
5. generate the layering rules.

**Output**: `harness/sources/architecture/extracted-rules.md`

#### Agent 2: incident reverse-engineering

**Input**: `harness/sources/incidents/`

**For each incident, answer**:

1. could one rule have stopped it?
2. can it be verified programmatically?
3. which file does it belong to?
4. what is the counter-example?
5. what is the correct example?
6. what test goes with it?

**Output**: six-part rules → `harness/sources/incidents/extracted-rules.md`

#### Agent 3: review distillation

**Input**: `harness/sources/reviews/`

**Output**:

- repeated 3 times or more: a six-part rule;
- seen only once: the observation pool.

#### Agent 4: code archaeology

**Input**: `src/`

**Output**:

- 3 best practices per layer;
- 3 counter-examples per layer;
- templates and rules.

#### Agent 5: data modeling

**Input**: `ddl/`, `api/`, `flows/`

**Output**:

- `wiki/data-model.md`
- `wiki/business-flows.md`

#### Agent 6: gate parsing

**Input**: CI configuration, `Makefile`

**Output**: a checklist of programmatically enforced gates.

### The three anti-fabrication gates

1. **Sources mandatory**: empty source → rejected;
2. **Executable mandatory**: the check command doesn't run → rejected;
3. **Tests mandatory**: a P0 rule with no test → rejected.

### Human review checklist

- [ ] every rule has a source;
- [ ] the source is traceable;
- [ ] the counter-example actually trips the check;
- [ ] the correct example passes the check;
- [ ] the check script can catch it;
- [ ] the test can fail and can pass;
- [ ] the priority is reasonable;
- [ ] the Owner is explicit.

---

## 12. CI and gates

### The main CI workflow

`.github/workflows/harness-ci.yml` (the `python-harness` job, in actual order):

1. Install (`pip install -e ".[dev]"`);
2. Ruff lint;
3. Ruff format;
4. Mypy;
5. **Markdownlint** (via `pre-commit run`; it had been configured but never ran — see patch-log X18);
6. **Yamllint** (same as above);
7. Pytest;
8. Test report check;
9. Python rules check;
10. Layering check;
11. Complexity check;
12. i18n check;
13. Secret scan;
14. Harness file check;
15. **Stage gate check** (runs `check-gates.sh` for each `harness/changes/REQ-*`; the stage gate used to be in no
    pipeline at all — see H5);
16. Schema validation;
17. Bandit;
18. pip-audit (`--skip-editable`).

> ⚠ Two known limitations (details in `docs/project-status.md` §9):
> **①** The second job, `commit-message`, carries `if: github.event_name == 'pull_request'`, so under this repo's
> "push straight to main, no PRs" workflow it **never runs**;
> **②** Steps 5 and 6 run via `pre-commit run`, which pulls the hook environment (including node) at CI runtime —
> an **added CI network dependency**.

### Commit message check

The second job in `.github/workflows/harness-ci.yml`:

```bash
for sha in $(git rev-list "$base..$head"); do
  git log -1 --format=%s "$sha" > /tmp/msg.txt
  python scripts/check_commit_msg.py /tmp/msg.txt
done
```

### Commit message format

```text
<type>: <subject>
```

**type**:

- `feat`: new feature
- `fix`: fix
- `docs`: documentation
- `ci`: CI
- `chore`: chores
- `rule`: rules
- `agent`: Agent
- `test`: tests

**Example**:

```text
rule: add PAY-001 from INC-2024-0421

The payment callback must set a timeout; on timeout, mark it pending.

Source: harness/sources/incidents/INC-2024-0421.md
```

---

## 13. Metrics

### Core metrics

| Metric                              | Target |
| ----------------------------------- | ------ |
| Project-level AI code ratio         | 90%    |
| Individual-level AI code ratio      | 85%    |
| Rework rounds                       | <=1    |
| Human confirmation rounds           | 1      |
| Quality gate pass rate              | 100%   |
| Test coverage                       | >=80%  |

### Quality metrics

| Metric                          | Target |
| ------------------------------- | ------ |
| Money-as-float violations       | 0      |
| External calls without a timeout | 0     |
| Bare except                     | 0      |
| Leftover print statements       | 0      |
| Hard-coded configuration        | 0      |
| Interfaces with no tests        | 0      |

### Process metrics

| Metric                            | Target           |
| --------------------------------- | ---------------- |
| Requirements review rounds        | <=3              |
| Code review rounds                | <=2              |
| Unit test review rounds           | <=2              |
| Review escalations to a human     | The fewer the better |

### Knowledge accumulation metrics

| Metric                        | Target            |
| ----------------------------- | ----------------- |
| Number of rules               | Growing steadily  |
| Rule source coverage          | 100%              |
| Programmatically enforced rate | 100%             |
| Rule test coverage            | 100%              |

### Measurement frequency

- Weekly: AI code ratio, rework rounds, gate pass rate;
- monthly: number of rules, source coverage, knowledge accumulation;
- quarterly: a full retrospective.

---

## 14. Key lessons

### Lesson 1: dry-run the whole flow before using it on a real requirement

The team found 4 defects during a dry run:

1. the CI gate only checked the status code and ignored the anomaly of a test case count of 0;
2. under a simple requirement the review report did not produce a file;
3. duplicate lines appeared in the summary file because of the Agent's tendency to append;
4. deployment parameters were guessed wrong by the Agent.

Had these only surfaced in a real requirement, every one of them would have caused serious rework.

### Lesson 2: quality files must be programmatically verifiable

The core lesson from OpenAI's million-line code project:

> **If a constraint cannot be enforced mechanically, the Agent will drift away from it.**

A natural-language instruction like "check whether CI passed" is not enough. The Agent may treat a status of `Success` as
passing while ignoring a test case count of 0.

Rewrite it as three programmatically verifiable conditions:

- `Status = SUCCESS`
- `TotalTest > 0`
- `Passed = Total`

The problem disappears entirely.

> **Any constraint a machine cannot verify is not a constraint at all when an Agent is executing.**

### Lesson 3: process consistency beats process efficiency

A small requirement touching only two files and six lines of code still walks the full ten stages, and passes in a single
review round.

A good process should not impose a significant burden on simple tasks. When a requirement is simple enough, every stage
naturally takes less time — but process consistency guarantees that no key step is skipped just because "this change is
small".

> **In enterprise-grade systems, cases of a small change causing a huge incident are too numerous to count.**

### Lesson 4: specs are living documents and need continuous iteration

Every new problem found in real use is patched into the Harness immediately.

> **Every line of the spec corresponds to a historical failure case.**

When a rule strikes you as redundant or long-winded, there is usually a pit someone really fell into behind it.

### Lesson 5: execution and judgement must be separated

The review Agent does not need to be smarter; it just needs a checking perspective different from the coding Agent's with
which to examine the artifacts.

In practice, the review Agent has:

- caught channel-branching logic the coding Agent had missed — a potential production outage;
- detected an Agent trying to skip the review stage and forced it to roll back.

---

## 15. FAQ

### Q1: Why is the skeleton so "thin"?

**A**: The skeleton is scaffolding; thickness comes from real project work. A thick rule looks like this:

```text
A price field must use Long, in units of cents.
Reason: in 2024-03 the order module used Double to compute discounts,
      0.1 + 0.2 = 0.30000000000000004,
      a reconciliation discrepancy of 370,000, incident ID INC-2024-0312.
Counter-example: OrderService.calcDiscount()
Example: PriceUtil.add()
Check: scripts/check_python_rules.py line 42
Test: tests/pricing/test_discount.py::test_float_precision
```

Without history, a rule is empty.

### Q2: Where do rules come from?

**A**: Incident reports, code reviews, architecture documents, DDL, API documents, the codebase, CI configuration,
production monitoring.

### Q3: Will the Agent make things up?

**A**: Yes. That is why there are three gates: sources mandatory, executable mandatory, tests mandatory.

### Q4: What if there are no incidents?

**A**: Reverse-engineer them from reviews and architecture. A code review comment repeated 3 times or more is ready to be
written up as a rule.

### Q5: What if there are too many rules?

**A**: Grade them P0/P1/P2. P0 is a hard constraint (blocks release), P1 must be fixed this round, P2 is future
optimization.

### Q6: Must CI pass?

**A**: Yes. Nothing merges while CI is failing.

### Q7: Can the Agent change main directly?

**A**: No. It must go through a PR.

> **This repo's own exception is on record**: during the external-audit fixes on 2026-09-11 the owner explicitly required
> **committing straight to main, no PRs** (no `gh` CLI on this machine). That deviation is recorded in `docs/freeze.md`
> under "working method change log", together with this note:
> **if this repo is ever published as a methodology exemplar, PRs must be restored first** —
> an exemplar that violates its own rules is the worst possible counter-example. Since this repo was archived there have
> been no further commits, and the deviation ended with it.

### Q8: How do I get started?

**A**:

1. run `bash scripts/dev-setup.sh`;
2. read `docs/quickstart.md`;
3. read `docs/fill-guide.md`;
4. run the 6 fill Agents in order;
5. dry-run REQ-0000;
6. execute your first real requirement.

### Q9: How do the skeleton and the project fit together?

**A**: See `docs/fill-guide.md`. The core idea is to put real sources into `harness/sources/`, use the Agents to extract
rules, and fill them back in after human review.

### Q10: Can it be used for non-Python projects?

**A**: Yes, but the Python-specific rules, scripts and CI would need to be replaced. The skeleton structure itself is
language-agnostic.

---

## 16. Contributing

See `CONTRIBUTING.md`.

### Branch conventions

| Branch         | Purpose          |
| -------------- | ---------------- |
| main           | Stable branch    |
| feature/<name> | Feature work     |
| agent/<name>   | Agent filling    |
| fix/<name>     | Fixes            |
| docs/<name>    | Documentation    |
| rule/<id>      | Rules            |
| hotfix/<name>  | Hotfixes         |

### Commit conventions

```text
<type>: <subject>

<body>

<footer>
```

### Contributing rules

Every rule must contain the six parts:

1. Rule
2. Reason
3. Counter-example
4. Example
5. Check
6. Test

An empty source is rejected.

### Prohibited

- Committing secrets, real data or production configuration is prohibited;
- rules without sources are prohibited;
- skipping CI is prohibited;
- the Agent changing main directly is prohibited.

---

## 17. Versions and roadmap

### Current version

**v0.1.0-skeleton**: the completed-skeleton release, **archived (no longer evolving) on 2026-09-11**

- Covers rules, skills, the knowledge base, changes, Agents, the pipeline, gates, metrics and iteration;
  for file counts (with the counting method) see [`docs/project-status.md`](./docs/project-status.md) §4;
- **Gates work**: `make gate` all green, `pre-commit` 16/16 idempotent, one mechanical dry run completed;
- **But never used for real**: fill 0%, pilot 0%.

### Roadmap

#### Phase 0: skeleton (done ✅)

- [x] Directory structure, rules, skills, Agent definitions, CI skeleton, documentation, engineering configuration
- [x] The gate system works (after three rounds of fixes: external audit H1–H14 + self-found X1–X25)

#### Phase 1: fill (not started ⬜ — **blocked on the lack of real sources**)

- [ ] Architecture parsing / incident reverse-engineering / review distillation / code archaeology / data modeling /
  gate parsing

> ⚠ The inputs of these Agents are **all existing artifacts**. With no brownfield project there is nothing to fill —
> forcing it would only produce **fabricated content**, which is exactly what this repo's three anti-fabrication gates
> exist to reject.
> **This is the direct reason for archiving.**

#### Phase 2: pilot (partially done ⏳)

- [x] Mechanical dry run REQ-0000 (2026-09-11, using template placeholders; evidence in `harness/pilot/findings.md`)
- [x] Fix the dry-run defects (4 of them)
- [ ] Pilot with a real requirement
- [ ] Metrics collection

> What was completed is only the **mechanical dry run**: proof that "the pipeline runs and blocks as it should".
> The **real-requirement pilot** has still not started, so "does this process actually work" remains unknown.

#### Phases 3–5: rollout / optimization / extension (not started ⬜)

All of them presuppose "phase 1 fill + phase 2 real pilot"; the starting conditions are **not met** today.

### Versioning policy

- **MAJOR**: incompatible changes
- **MINOR**: new features
- **PATCH**: fixes

---

## 18. License

MIT, see [LICENSE](./LICENSE).

---

## Appendix: Quick navigation

| I want to...                        | Go to                                     |
| ----------------------------------- | ----------------------------------------- |
| **Decide whether I can use it**     | `docs/project-status.md` (status and acceptance) |
| **See the design overview / blueprint** | `BluePrint.md`                        |
| **Learn how to use this kit**       | `USAGE.md`                                |
| **Learn how to fill in content**    | `FillWorkflow.md`                         |
| **See the revision trail**          | `harness/iteration/patch-log.md`          |
| See the external audit tickets (fixed) | `.claude/AUDIT-外审记录与修正建议.md`  |
| See the freeze / archive records    | `docs/freeze.md`                          |
| Get started quickly                 | `docs/quickstart.md`                      |
| Fill the Harness                    | `docs/fill-guide.md`                      |
| Understand the architecture         | `docs/architecture.md`                    |
| See the ten stages                  | `harness/pipeline/stages.md`              |
| See the Agent definitions           | `harness/agents/application-owner.md`     |
| Write your first rule               | `harness/rules/_template.md`              |
| Write your first Skill              | `harness/skills/_template/SKILL.md`       |
| Run the fill Agents                 | `harness/agents/README.md`                |
| See the anti-patterns               | `docs/anti-patterns.md`                   |
| See the best practices              | `docs/best-practices.md`                  |
| See the glossary                    | `docs/glossary.md`                        |
| File an issue                       | `.github/ISSUE_TEMPLATE/`                 |
| Open a PR                           | `.github/PULL_REQUEST_TEMPLATE.md`        |

---

> **The value of a Harness is not that it makes the Agent smarter, but that it makes the Agent's mistakes controllable,
> discoverable and fixable.**
>
> **This is in the same lineage as traditional software quality assurance: we do not expect programmers to write
> zero-defect code; we rely on code review, unit testing and CI/CD to make sure defects are intercepted layer by layer.
> What the Harness does is essentially identical — except the thing being intercepted has changed from a programmer to
> an Agent.**
