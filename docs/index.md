<div class="hero-ascii">

       ██╗ ██████╗ ██████╗ ██████╗  ██████╗
       ██║██╔═══██╗██╔══██╗██╔══██╗██╔═████╗
       ██║██║   ██║██████╔╝██║  ██║██║██╔██║
  ██   ██║██║   ██║██╔══██╗██║  ██║████╔╝██║
  ╚█████╔╝╚██████╔╝██║  ██║██████╔╝╚██████╔╝
   ╚════╝  ╚═════╝ ╚═╝  ╚═╝╚═════╝  ╚═════╝

            C:\> jord0.skills
    10 production skills for Claude Code

</div>

---

# Copy a Folder. Get a Superpower.

**jord0.skills** is a collection of 10 production-grade skills for [Claude Code](https://docs.anthropic.com/en/docs/claude-code/overview). No build step. No dependencies. No configuration. Just copy a skill folder into `~/.claude/skills/` and it works.

<div class="prompt">C:\> <span class="cmd">cp -r PORTAL ~/.claude/skills/PORTAL</span></div>

That's it. You just gave Claude persistent memory across sessions.

---

## The Arsenal

<div class="skill-grid" markdown>

<a class="skill-card" href="skills/portal/">
<h3>> PORTAL</h3>
<p>Save and restore session context across sessions, projects, and machines. Never lose your place again.</p>
<span class="tag tag-context">context</span>
</a>

<a class="skill-card" href="skills/strict/">
<h3>> STRICT</h3>
<p>11 non-negotiable coding rules. Load at session start. No placeholders, no half-measures, no excuses.</p>
<span class="tag tag-quality">quality</span>
</a>

<a class="skill-card" href="skills/forge/">
<h3>> FORGE</h3>
<p>Deep project onboarding. Point it at a codebase, get a complete CLAUDE.md with architecture, patterns, conventions.</p>
<span class="tag tag-system">system</span>
</a>

<a class="skill-card" href="skills/conclave/">
<h3>> CONCLAVE</h3>
<p>9-voice structured debate. Minimalist vs chaos agent vs philosopher. Let them fight before you decide.</p>
<span class="tag tag-cognitive">cognitive</span>
</a>

<a class="skill-card" href="skills/echo/">
<h3>> ECHO</h3>
<p>Decision records that persist. When future-you asks "why did we do it this way?" — ECHO has the answer.</p>
<span class="tag tag-context">context</span>
</a>

<a class="skill-card" href="skills/mirror/">
<h3>> MIRROR</h3>
<p>Force counterarguments against your own recommendations. 8 challenge frameworks. Find the blind spots.</p>
<span class="tag tag-cognitive">cognitive</span>
</a>

<a class="skill-card" href="skills/spark/">
<h3>> SPARK</h3>
<p>Divergent thinking engine. When standard approaches feel stale, SPARK explores the weird, wild long tail.</p>
<span class="tag tag-cognitive">cognitive</span>
</a>

<a class="skill-card" href="skills/recon/">
<h3>> RECON</h3>
<p>Deep technical research that auto-saves to a knowledge base. Never research the same thing twice.</p>
<span class="tag tag-research">research</span>
</a>

<a class="skill-card" href="skills/recall/">
<h3>> RECALL</h3>
<p>Search your knowledge base before searching the web. The retrieval half of RECON.</p>
<span class="tag tag-research">research</span>
</a>

<a class="skill-card" href="skills/notify/">
<h3>> NOTIFY</h3>
<p>Cross-platform desktop notifications. Simple alerts, interactive buttons, progress bars. Claude taps you on the shoulder.</p>
<span class="tag tag-system">system</span>
</a>

</div>

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/jord0-cmd/jord0.skills.git

# Copy a skill (or all of them)
cp -r jord0.skills/skills/PORTAL ~/.claude/skills/PORTAL

# Use it
# In Claude Code, just type:
/PORTAL create my-project
```

See the [Installation Guide](getting-started/install.md) for all install methods including the plugin marketplace.

---

## Why Skills?

Claude Code is powerful out of the box. But it forgets everything between sessions. It doesn't know your coding standards. It can't carry context across machines.

Skills fix that. They're markdown files that teach Claude new behaviors — persistent memory, structured debate, research pipelines, coding discipline. Each one is a single folder you can drop in and immediately use.

**No API keys.** **No external services.** **No configuration files.**

Just markdown and, occasionally, a bash script.

---

<p style="text-align: center; color: #555; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; margin-top: 3rem;">
C:\> Built by <a href="https://github.com/jord0-cmd">jord0.cmd</a> | MIT License
</p>
