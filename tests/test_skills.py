#!/usr/bin/env python3
"""
jord0.skills.bat — Skill Validation Test Suite

Runs against all skills in the repository to ensure quality standards.
Execute: python -m pytest tests/ -v
Or:      python tests/test_skills.py
"""

import re
import ast
import subprocess
import sys
from pathlib import Path

# Find repo root (parent of tests/)
REPO_ROOT = Path(__file__).parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

# All expected skills
EXPECTED_SKILLS = [
    "PORTAL", "STRICT", "FORGE", "CONCLAVE", "NOTIFY",
    "RECON", "RECALL", "ECHO", "MIRROR", "SPARK",
]

# Personal references that must never appear
BANNED_PATTERNS = [
    r"(?i)\brayne\b",
    r"(?i)\bjordo\b",
    r"(?i)\bnina\b",
    r"(?i)cosmic.lounge",
    r"(?i)cosmic_lounge",
    r"/\.rayne/",
    r"~/\.rayne",
    r"(?i)\bbesties\b",
    r"(?i)\balpha prime\b",
    r"(?i)\bneural drift\b",
    r"(?i)\bobaachan\b",
    r"(?i)\bzephyrus\b",
    r"(?i)\broom18\b",
    r"(?i)\broom42\b",
]

# Required YAML frontmatter fields
REQUIRED_FRONTMATTER = ["name", "description", "user-invocable", "allowed-tools"]

# Required sections in every SKILL.md
REQUIRED_SECTIONS = ["Usage", "Prerequisites"]

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def get_skill_dirs() -> list[Path]:
    """Return all skill directories."""
    return sorted(
        [d for d in SKILLS_DIR.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    )


def read_skill(skill_dir: Path) -> str:
    """Read SKILL.md content."""
    return (skill_dir / "SKILL.md").read_text(encoding="utf-8")


def parse_frontmatter(content: str) -> dict[str, str]:
    """Extract YAML frontmatter from markdown."""
    if not content.startswith("---"):
        return {}
    end = content.index("---", 3)
    frontmatter_text = content[3:end].strip()
    result = {}
    current_key = None
    current_value = []

    for line in frontmatter_text.split("\n"):
        # Check for key: value
        match = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if match:
            # Save previous key
            if current_key:
                result[current_key] = "\n".join(current_value).strip()
            current_key = match.group(1)
            current_value = [match.group(2)] if match.group(2) and not match.group(2) == "|" else []
        elif current_key and line.startswith("  "):
            current_value.append(line.strip())

    # Save last key
    if current_key:
        result[current_key] = "\n".join(current_value).strip()

    return result


def get_sections(content: str) -> list[str]:
    """Extract ## section headers from markdown."""
    return re.findall(r"^##\s+(.+)$", content, re.MULTILINE)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []

    def ok(self, name: str):
        self.passed += 1
        print(f"  PASS  {name}")

    def fail(self, name: str, reason: str):
        self.failed += 1
        self.errors.append(f"{name}: {reason}")
        print(f"  FAIL  {name} — {reason}")


def test_all_skills_exist(results: TestResults):
    """Every expected skill directory exists with a SKILL.md."""
    for skill_name in EXPECTED_SKILLS:
        skill_dir = SKILLS_DIR / skill_name
        skill_file = skill_dir / "SKILL.md"
        if not skill_dir.exists():
            results.fail(f"exists/{skill_name}", f"Directory missing: skills/{skill_name}/")
        elif not skill_file.exists():
            results.fail(f"exists/{skill_name}", f"SKILL.md missing in skills/{skill_name}/")
        else:
            results.ok(f"exists/{skill_name}")


def test_frontmatter(results: TestResults):
    """Every SKILL.md has valid YAML frontmatter with required fields."""
    for skill_dir in get_skill_dirs():
        name = skill_dir.name
        content = read_skill(skill_dir)

        if not content.startswith("---"):
            results.fail(f"frontmatter/{name}", "No YAML frontmatter found")
            continue

        fm = parse_frontmatter(content)
        missing = [f for f in REQUIRED_FRONTMATTER if f not in fm]

        if missing:
            results.fail(f"frontmatter/{name}", f"Missing fields: {', '.join(missing)}")
        elif fm.get("user-invocable", "").strip() != "true":
            results.fail(f"frontmatter/{name}", "user-invocable must be 'true'")
        elif not fm.get("name", "").strip():
            results.fail(f"frontmatter/{name}", "name field is empty")
        else:
            results.ok(f"frontmatter/{name}")


def test_no_personal_references(results: TestResults):
    """Zero personal references in any file."""
    for skill_dir in get_skill_dirs():
        name = skill_dir.name
        # Check all files in the skill directory
        for file_path in skill_dir.rglob("*"):
            if not file_path.is_file():
                continue
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            violations = []
            for pattern in BANNED_PATTERNS:
                matches = re.findall(pattern, content)
                if matches:
                    violations.extend(matches)

            rel_path = file_path.relative_to(SKILLS_DIR)
            if violations:
                results.fail(
                    f"personal-refs/{rel_path}",
                    f"Found: {', '.join(set(violations)[:3])}"
                )
            else:
                results.ok(f"personal-refs/{rel_path}")


def test_required_sections(results: TestResults):
    """Every SKILL.md has required sections."""
    for skill_dir in get_skill_dirs():
        name = skill_dir.name
        content = read_skill(skill_dir)
        sections = get_sections(content)

        missing = [s for s in REQUIRED_SECTIONS if not any(s.lower() in sec.lower() for sec in sections)]

        if missing:
            results.fail(f"sections/{name}", f"Missing sections: {', '.join(missing)}")
        else:
            results.ok(f"sections/{name}")


def test_skill_names_uppercase(results: TestResults):
    """All skill directory names are ALL CAPS."""
    for skill_dir in get_skill_dirs():
        name = skill_dir.name
        if name != name.upper():
            results.fail(f"uppercase/{name}", f"Should be {name.upper()}")
        else:
            results.ok(f"uppercase/{name}")


def test_frontmatter_name_matches_dir(results: TestResults):
    """Frontmatter 'name' matches directory name."""
    for skill_dir in get_skill_dirs():
        dir_name = skill_dir.name
        fm = parse_frontmatter(read_skill(skill_dir))
        fm_name = fm.get("name", "").strip()

        if fm_name.upper() != dir_name.upper():
            results.fail(f"name-match/{dir_name}", f"Frontmatter name '{fm_name}' != dir '{dir_name}'")
        else:
            results.ok(f"name-match/{dir_name}")


def test_scripts_syntax(results: TestResults):
    """All Python scripts pass syntax check. All shell scripts pass bash -n."""
    for skill_dir in get_skill_dirs():
        scripts_dir = skill_dir / "scripts"
        if not scripts_dir.exists():
            continue

        for script in scripts_dir.iterdir():
            rel_path = script.relative_to(SKILLS_DIR)

            if script.suffix == ".py":
                try:
                    source = script.read_text(encoding="utf-8")
                    ast.parse(source, filename=str(script))
                    results.ok(f"syntax/{rel_path}")
                except SyntaxError as e:
                    results.fail(f"syntax/{rel_path}", f"Python syntax error: {e}")

            elif script.suffix == ".sh":
                try:
                    result = subprocess.run(
                        ["bash", "-n", str(script)],
                        capture_output=True,
                        text=True,
                        timeout=10,
                    )
                    if result.returncode == 0:
                        results.ok(f"syntax/{rel_path}")
                    else:
                        results.fail(f"syntax/{rel_path}", f"Bash syntax error: {result.stderr.strip()}")
                except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                    results.fail(f"syntax/{rel_path}", str(e))


def test_no_absolute_paths(results: TestResults):
    """No hardcoded absolute paths to personal directories."""
    # Paths that are OK (documentation examples)
    allowed_patterns = [r"~/.claude/skills/", r"~/.claude/portals/"]

    for skill_dir in get_skill_dirs():
        name = skill_dir.name
        for file_path in skill_dir.rglob("*"):
            if not file_path.is_file():
                continue
            try:
                content = file_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            # Check for /home/user or /Users/specific-person type paths
            bad_paths = re.findall(r"/home/\w+/\.", content)
            bad_paths += re.findall(r"/Users/\w+/\.", content)

            rel_path = file_path.relative_to(SKILLS_DIR)
            if bad_paths:
                results.fail(f"abs-paths/{rel_path}", f"Hardcoded paths: {bad_paths[:2]}")
            else:
                results.ok(f"abs-paths/{rel_path}")


def test_readme_skill_count(results: TestResults):
    """README mentions the correct number of skills."""
    readme = REPO_ROOT / "README.md"
    if not readme.exists():
        results.fail("readme/exists", "README.md not found")
        return

    content = readme.read_text(encoding="utf-8")
    actual_count = len(get_skill_dirs())

    # Check that the stated count matches reality
    if f"{actual_count} production" in content.lower() or f"{actual_count} skills" in content.lower():
        results.ok(f"readme/skill-count ({actual_count})")
    else:
        results.fail("readme/skill-count", f"README doesn't mention {actual_count} skills")


def test_plugin_json(results: TestResults):
    """Plugin manifest exists and has required fields."""
    plugin_file = REPO_ROOT / ".claude-plugin" / "plugin.json"
    if not plugin_file.exists():
        results.fail("plugin/exists", ".claude-plugin/plugin.json not found")
        return

    import json
    try:
        data = json.loads(plugin_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        results.fail("plugin/valid-json", f"Invalid JSON: {e}")
        return

    results.ok("plugin/valid-json")

    required_fields = ["name", "description", "version", "author", "license"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        results.fail("plugin/required-fields", f"Missing: {', '.join(missing)}")
    else:
        results.ok("plugin/required-fields")

    # Check no personal references in plugin.json
    content = plugin_file.read_text(encoding="utf-8")
    violations = []
    for pattern in BANNED_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            violations.extend(matches)
    if violations:
        results.fail("plugin/no-personal-refs", f"Found: {', '.join(set(violations)[:3])}")
    else:
        results.ok("plugin/no-personal-refs")


def test_marketplace_json(results: TestResults):
    """Marketplace catalog exists and has required fields."""
    marketplace_file = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    if not marketplace_file.exists():
        results.fail("marketplace/exists", ".claude-plugin/marketplace.json not found")
        return

    import json
    try:
        data = json.loads(marketplace_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        results.fail("marketplace/valid-json", f"Invalid JSON: {e}")
        return

    results.ok("marketplace/valid-json")

    required_fields = ["name", "owner", "plugins"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        results.fail("marketplace/required-fields", f"Missing: {', '.join(missing)}")
    else:
        results.ok("marketplace/required-fields")

    # Check plugins array is non-empty
    plugins = data.get("plugins", [])
    if not plugins:
        results.fail("marketplace/has-plugins", "plugins array is empty")
    else:
        results.ok(f"marketplace/has-plugins ({len(plugins)})")

    # Check no personal references
    content = marketplace_file.read_text(encoding="utf-8")
    violations = []
    for pattern in BANNED_PATTERNS:
        matches = re.findall(pattern, content)
        if matches:
            violations.extend(matches)
    if violations:
        results.fail("marketplace/no-personal-refs", f"Found: {', '.join(set(violations)[:3])}")
    else:
        results.ok("marketplace/no-personal-refs")


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def main():
    print()
    print("=" * 60)
    print("  jord0.skills.bat — Skill Validation Suite")
    print("=" * 60)
    print()

    results = TestResults()

    print("[1/11] Skill directories exist")
    test_all_skills_exist(results)
    print()

    print("[2/11] YAML frontmatter valid")
    test_frontmatter(results)
    print()

    print("[3/11] No personal references")
    test_no_personal_references(results)
    print()

    print("[4/11] Required sections present")
    test_required_sections(results)
    print()

    print("[5/11] Names are ALL CAPS")
    test_skill_names_uppercase(results)
    print()

    print("[6/11] Frontmatter name matches directory")
    test_frontmatter_name_matches_dir(results)
    print()

    print("[7/11] Script syntax valid")
    test_scripts_syntax(results)
    print()

    print("[8/11] No hardcoded absolute paths")
    test_no_absolute_paths(results)
    print()

    print("[9/11] README consistency")
    test_readme_skill_count(results)
    print()

    print("[10/11] Plugin manifest")
    test_plugin_json(results)
    print()

    print("[11/11] Marketplace catalog")
    test_marketplace_json(results)
    print()

    print("=" * 60)
    total = results.passed + results.failed
    if results.failed == 0:
        print(f"  ALL {total} CHECKS PASSED")
    else:
        print(f"  {results.passed}/{total} passed, {results.failed} FAILED")
        print()
        for error in results.errors:
            print(f"  X  {error}")
    print("=" * 60)
    print()

    sys.exit(1 if results.failed else 0)


if __name__ == "__main__":
    main()
