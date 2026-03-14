# Code Review Guidelines — jord0.skills

## Always check
- Skills follow UPPERCASE naming convention (PORTAL, OPTIC, LOCUS, etc.)
- SKILL.md has complete and valid YAML frontmatter (name, description, at minimum)
- No hardcoded file paths, credentials, API keys, or machine-specific references
- Error handling is present in all scripts — no silent failures
- MkDocs documentation updated for any new or modified skills
- Skill descriptions are concise, single-line, action-oriented
- Reference files in `references/` are correctly linked from SKILL.md

## Security
- No credentials, tokens, or secrets in any file
- No shell injection vectors in skill instructions that pass user input to Bash
- No instructions that bypass Claude Code permission modes without explicit user consent

## Style
- Skill instructions use imperative voice ("Generate the image", not "You should generate")
- Markdown formatting is clean — no trailing whitespace, consistent heading levels
- Code blocks specify language for syntax highlighting

## Skip
- Formatting-only changes in documentation
- Changes to .gitignore or editor config files
- MkDocs theme or navigation-only changes
