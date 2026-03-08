# Code Review Pipeline

**Skills used:** REFRAX + STRICT + ECHO

AI wrote the code. Now you need to understand it, validate it, and record why you approved it. Three skills, one pipeline.

---

## The Problem

AI-generated code ships fast. Too fast. You're approving pull requests full of logic you've never traced, risks you've never assessed, and decisions you can't explain to your team lead.

Code review shouldn't be "it runs, ship it." But reading 500 lines of generated code is slow, error-prone, and boring. You need a system.

---

## The Pipeline

### Step 1: STRICT — Set the Rules

Load your coding standards before anything else:

```
/strict
```

STRICT establishes 11 non-negotiable rules: no placeholders, no silent failures, complete error handling, security-first. Everything REFRAX flags will be measured against these standards.

### Step 2: REFRAX — See the Code

Point REFRAX at the AI-generated code:

```
analyse the auth service in src/auth/
```

REFRAX reads the code, maps every step, decision, and side effect, then serves an interactive diagram at `localhost:8789`.

**What to look for:**

- **The spine** — Does the logic flow make sense? Are there unnecessary steps? Missing steps?
- **Decision nodes** — Are all branches handled? What happens on the unhappy path?
- **Side effects** — Database writes, API calls, file operations. Are they where you expect?
- **Risk cards** — Security holes, performance issues, logic errors. Each one has a severity rating and a fix prompt.

### Step 3: Fix What REFRAX Found

For each risk card:

1. Read the plain-language explanation
2. Check the severity — high risks get fixed now, medium risks get tickets
3. Click **Copy Fix Prompt** — paste it back to Claude
4. Claude fixes the code and updates data.json
5. The diagram morphs to show the fix — verify it visually

This loop — see risk, copy prompt, fix, verify — is where the real value lives. You're not just reading code; you're having a visual conversation about it.

### Step 4: Toggle Novice Mode

Before showing the review to stakeholders, toggle to **NOV** mode. The same spine, the same logic, but in plain English:

- "Checks the password" instead of "bcrypt.compare()"
- "Saves to database" instead of "INSERT INTO users"
- "Is the email valid?" instead of "regex match against RFC 5322"

Non-technical team members can now follow the logic without a translator.

### Step 5: Review the Diff

If you're reviewing a pull request, REFRAX shows diff hunks linked to spine nodes. You see:

- Which logic steps were added or modified
- What risks the changes introduced
- Before/after comparisons with explanations

This is code review with a map, not a wall of green and red.

### Step 6: ECHO — Record the Decision

Once you've reviewed, fixed, and approved:

```
/echo create "Approved auth service after REFRAX review"
```

ECHO captures:

- What was reviewed
- What risks were found and how they were resolved
- Why the code was approved
- The decision context for future reference

When someone asks "why did we approve this?" six months from now, ECHO has the answer.

---

## The Complete Flow

```
/strict                          # Set the rules
"analyse src/auth/"              # REFRAX maps the code
  → Review spine, check risks
  → Copy fix prompts, apply fixes
  → Verify fixes visually
  → Toggle NOV mode for stakeholders
/echo create "Approved auth"     # Record the decision
```

Three skills. One pipeline. Every review is visual, validated, and documented.

---

## Tips

!!! tip "STRICT before REFRAX"
    Loading STRICT first means Claude's analysis is shaped by your coding standards. Risks flagged by REFRAX will align with the rules you care about.

!!! tip "Use the fix prompt loop"
    The copy-fix-verify loop is the killer feature. Don't just read the risks — fix them in place and watch the diagram update. That's the review.

!!! tip "NOV mode for PRs"
    When writing PR descriptions, toggle NOV mode and screenshot the spine. A visual flow diagram communicates more than "refactored auth logic" ever will.

!!! tip "ECHO everything"
    Record approvals AND rejections. "We rejected this approach because REFRAX showed a circular dependency in the error handling" is gold for future decision-making.

---

*See it. Fix it. Record it.*
