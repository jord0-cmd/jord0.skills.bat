# PORTAL

<span class="tag tag-context">context</span>

**Save and restore session context across sessions, projects, and machines.**

Never lose your place. Never re-explain context. Just portal in and pick up where you left off.

---

## The Problem PORTAL Solves

Claude Code has no memory between sessions. Every time you start fresh, you lose:

- What you were working on
- Decisions you made and why
- Which files you modified
- What's left to do

PORTAL captures all of this in a single snapshot and lets you restore it anywhere.

---

## Usage

### Create a portal

```
/portal create my-feature
```

Claude captures 5 standardized fields plus optional context:

| Field | What's Captured |
|-------|----------------|
| **Git state** | Active branch, last commit hash |
| **Current task** | What you're working on right now |
| **Decisions** | Key architectural/design choices from this session |
| **Next steps** | What's blocked, what's next |
| **Files modified** | Which files you touched |

You get back a unique portal ID:

```
PORTAL-7X3F
```

### Open a portal

=== "By ID"

    ```
    /portal open PORTAL-7X3F
    ```

=== "By name"

    ```
    /portal open my-feature
    ```

Claude reads the snapshot, internalizes the context, and continues as if the session never ended.

### List portals

```
/portal list
```

Shows all saved portals with names, dates, and summaries.

### Update a portal

```
/portal update PORTAL-7X3F
```

Refreshes an existing portal with the current session state.

### Close a portal

```
/portal close PORTAL-7X3F
```

Deletes a portal you no longer need.

---

## Advanced Tricks

### Cross-machine portals

Portals are JSON files stored in a `portals/` directory. Put that directory in a git-tracked location and push it:

```bash
cd ~/my-project
git add portals/
git commit -m "portal: save session context"
git push
```

On another machine:

```bash
git pull
# Now /portal list shows the portals from your other machine
```

!!! tip "The git connection is the bridge"
    Any machine that can `git pull` the same repo can open any portal created on any other machine. The portal travels with your code.

### Project-switching portals

Working on multiple projects? Create a portal before switching:

```
/portal create frontend-auth
```

Switch to another project, do some work. When you come back:

```
/portal open frontend-auth
```

Full context restored. No mental overhead.

### End-of-day ritual

Make it a habit. Before closing any session:

```
/portal create eod-feb-22
```

Next morning:

```
/portal open eod-feb-22
```

Yesterday's context, today's session. Seamless continuity.

### Pair with ECHO

Big decision during a session? Capture the reasoning with ECHO before portalling out:

```
/echo create auth-approach
/portal create my-feature
```

When you portal back in, the decision record is there too. Context + reasoning = full picture.

---

## How It Works

1. When you create a portal, Claude gathers the 5 context fields
2. Serializes them to a JSON file in `portals/`
3. Generates a unique ID: `PORTAL-XXXX` (4 random alphanumeric characters)
4. When you open a portal, Claude reads the JSON and integrates the context
5. Responds with a summary of what was restored

The portal file looks like this:

```json
{
  "id": "PORTAL-7X3F",
  "name": "my-feature",
  "created": "2026-02-22T14:30:00Z",
  "git": {
    "branch": "feature/auth",
    "commit": "abc1234"
  },
  "task": "Implementing JWT refresh token rotation",
  "decisions": [
    "Using httpOnly cookies over localStorage for token storage",
    "Refresh tokens rotate on every use (one-time use)"
  ],
  "next_steps": [
    "Add token revocation endpoint",
    "Write integration tests for rotation flow"
  ],
  "files_modified": [
    "src/auth/tokens.ts",
    "src/middleware/auth.ts"
  ]
}
```

---

## Prerequisites

- Claude Code with Bash, Read, Write tools
- Git (for cross-machine sync)
- `portals/` directory is auto-created on first use

---

*Context is everything. PORTAL makes sure you never lose it.*
