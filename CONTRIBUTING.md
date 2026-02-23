# Contributing to jord0.skills

Thanks for wanting to contribute. Here's how.

## Submitting a New Skill

### Requirements

Every skill must:

1. **Be self-contained** — works by copying one folder to `~/.claude/skills/`
2. **Have a `SKILL.md`** with valid YAML frontmatter:
   ```yaml
   ---
   name: SKILLNAME
   description: |
     When to invoke this skill. Clear trigger conditions.
   user-invocable: true
   allowed-tools: Read, Write, Bash  # only what's needed
   ---
   ```
3. **Document prerequisites** — if it needs anything installed, say so explicitly
4. **Include usage examples** — show real invocations with expected output
5. **Have an AUTO-EXECUTE protocol** — tell Claude exactly what to do when invoked
6. **Be zero-personal-reference** — no personal names, paths, or project-specific data
7. **Use ALL CAPS naming** — skill folder and name must be uppercase

### Skill Structure

```
SKILLNAME/
  SKILL.md              # Required — the skill definition
  scripts/              # Optional — supporting scripts
    script.py
    script.sh
```

### Quality Bar

- Zero absolute paths to personal infrastructure
- Clear "When to use" trigger conditions
- Working examples
- Self-contained — no hidden dependencies on other skills (document pairings)
- Dependencies clearly documented with install instructions

## Improving Existing Skills

1. Fork the repo
2. Make your changes
3. Test by copying the skill to `~/.claude/skills/` and using it
4. Submit a PR with:
   - What changed
   - Why it's better
   - How you tested it

## Reporting Issues

Open an issue with:
- Which skill
- What you expected
- What happened
- Your platform (Linux, macOS, WSL)
- Claude Code version

## Style Guide

- **Skill names**: ALL CAPS, short (1 word preferred)
- **Descriptions**: Start with verb, explain when to use
- **Tone**: Direct, practical, no fluff
- **Examples**: Real invocations, not hypothetical
- **Tagline**: Every skill ends with an italicized one-liner

## Code of Conduct

Be decent. Help each other. Ship quality.
