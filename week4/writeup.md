# Week 4 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Alfred Yu \
SUNet ID: ayu1001 \
Citations: Used Windsurf as base IDE, used Claude Code. 

This assignment took me about 1.5 hours to do. 


## YOUR RESPONSES
### Automation #1
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
According to the best practices guide, the CLAUDE.md file should include “Testing instructions",  "Core files and utility functions" and "Developer Environment Setup.” I mirrored that by documenting the repo map, Makefile targets, lint/test workflow, SQLite seeding behavior, and frontend touchpoints so Claude sees the same context a teammate/human would. The file is also readable for a human, as mentioned in "We recommend keeping them concise and human-readable." 

b. Design of each automation, including goals, inputs/outputs, steps
The goal is to give Claude enough orientation that it can run the right commands and reference the right files without me restating instructions each session.

Inputs/outputs: Claude reads `CLAUDE.md` automatically; the “output” is higher-quality, repo-aware assistance.

Build/maintenance steps:
1. Create `CLAUDE.md` at repo root scoped to Week 4.
2. Populate sections for Quick Start commands, repo layout, database rules, frontend expectations, style/tooling guidance, and QA habits. Populate accordingly to the Claude Best Practices document. 
3. Update the file whenever workflows or tooling change so new guidance is immediately available to Claude.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
No command is needed - Claude loads the file automatically. When editing, review with `git status`/`git diff` and commit alongside related changes. If a revision causes confusion, revert it through normal git history (e.g., `git restore` before committing or a follow-up fix commit). The file is static, so there are no runtime side effects.

d. Before vs. after (i.e. manual workflow vs. automated workflow)
Before, every session started with me reminding Claude how to run `make test`, what `data/app.db` does, or which directory holds routers. After the automation, Claude already knows those answers and surfaces the correct commands and files immediately, reducing back-and-forth and preventing risky shell suggestions. Claude is given valuable context on the codebase. 

e. How you used the automation to enhance the starter application
Claude was able to automatically have context on the codebase, and is able to run certain actions on its own. This helps speed up the development flow - Claude Code doesn't have to ask redundant questions with frequent pauses anymore, since it's able to work by itself. 


### Automation #2
a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
I took cues from the best-practices article’s section on custom slash commands—their test-runner example in particular. It suggested capturing repeatable workflows (like `pytest …`) inside `.claude/commands/*.md` with clear intent, optional inputs, and structured outputs. I mirrored that approach in my `tests.md` command, extending it to mention this repo’s Makefile targets and desired reporting style.

b. Design of each automation, including goals, inputs/outputs, steps
Goal: give Claude a deterministic “run Week 4 tests” routine so I can trigger the full pytest suite or a filtered run without retyping shell commands to avoid manual work. 
Input: optional pytest selector provided via `$ARGUMENTS`.
Output: a concise summary of the command(s) executed, pass/fail status, failure details when present, and suggested follow-ups (lint, coverage, rerun flags, etc.).

The steps were mainly encoded into the .md file, but to be more explicit, these are the steps: 
1. Move into the Week 4 folder (`cd week4`).
2. Run `make test` when no arguments are supplied, otherwise run `pytest -q backend/tests $ARGUMENTS`.
3. On failure, collect the failing test names, relevant traceback snippets, and concrete remediation ideas.
4. On success, acknowledge the clean run and call out optional next checks (lint/coverage).
5. Guardrail: explicitly instruct Claude not to edit or add tests unless told elsewhere.

c. How to run it (exact commands), expected outputs, and rollback/safety notes
Invoke it inside Claude Code with `/tests` or `/project:tests -k "search_term"`. Claude executes the scripted steps, then reports back with success/failure context. The command is read-only; it touches no source files and will do not editing. 

d. Before vs. after (i.e. manual workflow vs. automated workflow)
Before, I manually ran `cd week4 && make test`, copied failure snippets, and wrote my own follow-up checklist. After adding the slash command, I simply run the command and Claude runs the suite, summarizes failures, and reminds me of next steps without extra prompting. It turned a repetitive shell routine into a single action.

e. How you used the automation to enhance the starter application
After modifications to the backend of the app to `backend/app/routers/notes.py` (a delete functionality and a statistics dashboard), I triggered `/tests' to help save the time associated with actually running the test. This allows for quick backend testing. Ideally, I would also have a /addtests slash command that also adds tests accordingly to a summarization of a changes that Claude Code made, that way, the tests can be more tailored to the application. 

### *(Optional) Automation #3*
*If you choose to build additional automations, feel free to detail them here!*

a. Design inspiration (e.g. cite the best-practices and/or sub-agents docs)
> TODO

b. Design of each automation, including goals, inputs/outputs, steps
> TODO

c. How to run it (exact commands), expected outputs, and rollback/safety notes
> TODO

d. Before vs. after (i.e. manual workflow vs. automated workflow)
> TODO

e. How you used the automation to enhance the starter application
> TODO
