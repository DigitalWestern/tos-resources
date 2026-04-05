Pre-ship check. Run a security review and code review back-to-back, then give me a Go/No-Go.

Keep me in the loop throughout — tell me what you're doing at each stage.

## Step 1: Security Review

Run `git diff HEAD~1` to get the most recent committed changes. If that fails, run `git diff` for uncommitted changes instead.

Scan every changed file (skip binaries) for:
- API keys, tokens, secrets (AWS, Stripe, GitHub, Bearer, private keys, generic key/token assignments)
- Hardcoded passwords (`password=`, `DB_PASSWORD=`, connection strings with credentials)
- Sensitive personal data (SSNs, credit card numbers, emails in unexpected places — skip HTML)
- Broken local asset references in HTML (`href`/`src` pointing to files that don't exist in the repo)

Fix anything you find. Replace secrets with placeholders, fix broken references.

## Step 2: Code Review

Read the full content of every modified file for context, then review the diff for:
- Logical inconsistencies (dead conditions, unused variables, contradictions)
- Pattern violations (naming, formatting, structure that breaks file conventions)
- Dead code (unused functions, unmatched CSS, commented-out code blocks)
- Unintentional changes (debug statements, hardcoded test values, TODOs, accidental edits)

Fix anything you find. Remove dead code, fix pattern breaks, clean up debug statements.

## Step 3: Consolidated Summary

After both reviews, output a single summary with exactly three sections:

**Security** — One-line status per category (secrets, passwords, PII, broken refs). If clean, say clean. If something was flagged and fixed, say what and where.

**Code Quality** — One-line status per category (logic, patterns, dead code, unintentional). Same format.

**Go / No-Go** — Be decisive:
- **Go** if everything is clean or all issues were minor and already fixed. I should feel confident pushing.
- **No-Go** if anything remains that needs my attention — something you couldn't auto-fix, a judgment call, or a risk I need to sign off on. Tell me exactly what to address first.

Be fast. Don't pad the summary. One sentence per line item, not a paragraph.
