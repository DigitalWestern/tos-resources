Review my recent code changes as a second pair of eyes.

1. Run `git diff HEAD~1` to get the most recent committed changes. If that fails, run `git diff` for uncommitted changes instead.

2. Read the full content of every file that was modified (not just the diff hunks) so you understand the surrounding context.

3. Review for the following, and ONLY flag things that actually appear in the changes. Do not give generic advice.

**Logical inconsistencies** — Does anything in the new code contradict itself? For example:
- A condition that can never be true/false
- A variable set but never used, or used before being set
- An event listener added but never removed when it should be
- Math or string operations that produce unexpected results

**Pattern violations** — Does the new code break patterns already established in the file?
- Naming conventions (if existing code uses camelCase, flag snake_case and vice versa)
- Indentation or formatting that doesn't match the surrounding code
- A new function/section structured differently from its siblings
- CSS specificity or selector patterns that diverge from the existing stylesheet

**Dead code** — Flag:
- Functions or variables that are defined but never called/referenced
- CSS rules that don't match any element in the HTML
- Commented-out code blocks that were left in (not explanatory comments — actual dead code)
- Imports or script tags for things that aren't used

**Unintentional changes** — Things that look like accidents:
- Debug statements (console.log, alert, print) left in
- Hardcoded test values that should be dynamic
- TODO/FIXME/HACK comments that suggest unfinished work
- Changes to unrelated parts of the file that look like accidental edits

4. Output your review as a flat list of findings. For each one:
- **File and line number**
- **What you found** (quote the specific code)
- **Why it matters** (one sentence)

If everything looks clean, say so — don't manufacture issues. Be direct, not diplomatic.

5. After reporting, fix each issue you flagged. Remove dead code, fix pattern violations to match the surrounding conventions, remove debug statements, and resolve logical inconsistencies.

Keep the user in the loop throughout — narrate what you're reviewing, what you found, what you're fixing, and why. Don't work silently.
