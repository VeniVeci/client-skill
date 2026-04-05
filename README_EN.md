# Client.skill

> *"This direction is good, but I still feel it can be a bit more premium. Don't finalize it yet."*

**Distill your client into an AI Skill before they change the brief again.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

Provide source materials from your real collaboration with a client:
chat logs, emails, meeting notes, briefs, review comments, plus your own interpretation.

Generate an **AI Skill that behaves like that client**:
talks in their tone, remembers their business priorities, knows who really approves things, and asks for "one small change" at the worst possible time.

⚠️ **For internal alignment, training, rehearsal, and retrospectives only. Not for impersonation, fraud, or bypassing real approval.**

[Installation](#installation) · [Usage](#usage) · [Examples](#examples) · [中文](README.md)

---

## Installation

### Claude Code

```bash
mkdir -p .claude/skills
git clone https://github.com/VeniVeci/client-skill .claude/skills/create-client
```

### OpenClaw

```bash
git clone https://github.com/VeniVeci/client-skill ~/.openclaw/workspace/skills/create-client
```

### Optional dependencies

```bash
pip3 install -r requirements.txt
```

---

## Usage

In Claude Code, run:

```text
/create-client
```

Then provide:

1. A codename for the client
2. The project context
3. Their communication / decision style

After creation, use `/{slug}` to invoke the generated client Skill.

### Commands

| Command | Description |
|---------|-------------|
| `/list-clients` | List all generated client Skills |
| `/{slug}` | Full Skill |
| `/{slug}-project` | Project memory only |
| `/{slug}-persona` | Persona only |
| `/client-rollback {slug} {version}` | Roll back to a previous version |
| `/delete-client {slug}` | Delete |
| `/close-project {slug}` | Gentler alias for delete |

---

## Examples

> Input: `Brand director for a skincare company, aesthetic-driven, budget-sensitive, often says "make it feel more premium", working on a 618 campaign page`

**Scenario 1: Design Review**

```text
You            ❯ Can this landing page pass?

Client.skill   ❯ Directionally it's better than the last one.
                But it still doesn't feel premium enough.
                The hero section is too crowded and too promotional.
                Don't hand this to dev yet. Give me one calmer version first.
```

**Scenario 2: Requirement Change**

```text
You            ❯ But this was already approved yesterday

Client.skill   ❯ Yesterday was based on yesterday's information.
                The boss reviewed it this morning and wants the free gift highlighted.
                Don't get stuck on whether it changed. Let's solve it first.
```

**Scenario 3: Schedule Pressure**

```text
You            ❯ Adding this animation will cost two extra days

Client.skill   ❯ Two days doesn't work. The milestone can't move.
                Find a lighter implementation.
                I want the effect, but not something expensive to build.
```

---

## How It Works

Each generated client Skill has two parts:

| Part | Purpose |
|------|---------|
| **Part A — Project Memory** | Business goals, red lines, revision history, approval chain, style preferences, delivery risks |
| **Part B — Approval Persona** | Communication style, decision logic, feedback patterns, collaboration behavior |

Runtime logic:

```text
new proposal/question
  -> Approval Persona decides the stance
  -> Project Memory injects context
  -> output sounds like the real client
```

---

## Supported Sources

| Source | Formats | What it helps recover |
|--------|---------|-----------------------|
| Chat logs | txt / json / md | Tone, urgency, review habits |
| Emails | eml / txt | Formal feedback and approval trail |
| Briefs / PRDs / docs | md / txt / pdf | Goals, constraints, success criteria |
| Meeting notes / transcripts | md / txt | Hidden decisions and stakeholder dynamics |
| Review comments | txt / json / exported notes | Aesthetic preferences and recurring complaints |
| Direct paste | plain text | Tacit knowledge from working together |

---

## Repository Structure

```text
create-client/
├── SKILL.md
├── prompts/
├── tools/
├── clients/
│   └── example_brand_director/
├── docs/PRD.md
├── requirements.txt
└── LICENSE
```

---

## Sample Client

This repo ships with a ready-to-read sample:

- `clients/example_brand_director/`
- A fictional brand director
- Strong aesthetic preference, budget pressure, hidden stakeholder influence

It works both as a demo and as a template for your own generated client Skills.
