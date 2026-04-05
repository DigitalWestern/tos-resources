Run a security review on my recent changes.

1. Run `git diff HEAD~1` to get the most recent committed changes. If that fails, run `git diff` for uncommitted changes instead.

2. Scan every changed file for the following categories. Skip binary files (PDFs, images, xlsx, zip).

**API keys & tokens** — Look for:
- AWS access keys (AKIA followed by 16 alphanumeric chars)
- Stripe keys (sk_live_*, sk_test_*)
- GitHub tokens (ghp_*, gho_*, github_pat_*)
- Bearer tokens
- Private key blocks (-----BEGIN * PRIVATE KEY-----)
- Any pattern like `api_key = "..."`, `api_secret = "..."`, `token = "..."`

**Hardcoded passwords & secrets** — Look for:
- `password`, `passwd`, `pwd`, or `secret` followed by an assignment with a real value
- `DB_PASSWORD=` with a value
- Database connection strings with embedded credentials (e.g., `://user:pass@host`)

**Sensitive personal data** — Look for:
- Social Security Numbers (XXX-XX-XXXX pattern)
- Credit card numbers (Visa, Mastercard, Amex, Discover patterns)
- Email addresses in unexpected places (skip HTML files where mailto is normal)

**Broken asset references** — For any HTML files in the diff:
- Extract all `href="..."` and `src="..."` values
- Filter to local paths only (ignore http, https, #anchors, mailto, data:, javascript:)
- Check that each referenced file actually exists in the repo
- Flag any that are missing

3. Output a summary with this structure:
- Group findings by category
- For each finding, show the **file path**, **line number**, the **matched text** (truncated if long), and **why it was flagged**
- If nothing is found in a category, say "No issues found" for that category
- End with a clear PASS or FAIL verdict

Be specific about line numbers. Do not give generic advice — only flag things that actually appear in the diff.

4. After reporting, fix each issue you flagged. For secrets and passwords, replace the value with a placeholder (e.g., `YOUR_API_KEY_HERE` or an environment variable reference). For broken asset references, correct the path or remove the dead reference.

Keep the user in the loop throughout — narrate what you're scanning, what you found, what you're fixing, and why. Don't work silently.
