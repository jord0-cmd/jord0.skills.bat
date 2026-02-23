# Cross-Machine Workflow

**Skills used:** PORTAL + Git

Start on your laptop. Continue on your desktop. Same context, different hardware.

---

## The Problem

You've got multiple machines. Laptop for the couch, desktop for serious work, maybe a remote server. Your code syncs via git, but your *context* doesn't. You switch machines and Claude has no idea what you were doing 10 minutes ago on the other one.

---

## The Setup (One Time)

Portals are JSON files. Put them somewhere git can reach.

### Option A: In your project repo

```bash
# Add portals directory to your project
mkdir -p portals
echo "portals/" >> .gitignore  # Optional — keep portals private
```

!!! tip "To share or not to share"
    If you `.gitignore` portals, they stay local. If you don't, they travel with the repo. Your call — portals don't contain secrets, just context summaries.

### Option B: Dedicated sync repo

```bash
# Create a private repo just for portals
mkdir -p ~/portal-sync/portals
cd ~/portal-sync
git init
git remote add origin git@github.com:you/portal-sync.git
```

Clone this repo on every machine. All portals live here.

---

## The Workflow

### Machine A (Laptop)

You're working. Time to switch machines.

```
/portal create current-work
```

Push it:

```bash
cd ~/your-project  # or ~/portal-sync
git add portals/
git commit -m "portal: save context"
git push
```

### Machine B (Desktop)

Pull and restore:

```bash
git pull
```

```
/portal open current-work
```

Claude picks up exactly where you left off. Different machine, same context, zero re-explaining.

---

## The Fast Version

If you use the same project repo for portals, it's even simpler:

```bash
# Machine A
/portal create current-work
git add -A && git commit -m "wip + portal" && git push

# Machine B
git pull
/portal open current-work
```

Two commands on each side. That's it.

---

## Real Scenarios

### Laptop → Desktop

Hacking on the couch, hit a wall that needs your big monitor and GPU:

```
/portal create move-to-desktop
# push
# walk to desk, pull
/portal open move-to-desktop
```

### Desktop → Remote Server

Need to test on production-like hardware:

```
/portal create deploy-testing
# push
# SSH into server, pull
/portal open deploy-testing
```

### Work → Home

```
/portal create end-of-work
# push to private repo
# at home, pull
/portal open end-of-work
```

---

## Tips

!!! tip "Consistent portal names"
    Use a naming convention: `laptop-eod`, `desktop-wip`, `server-debug`. Makes it easy to know which portal came from where.

!!! tip "Combine with branch names"
    Name portals after branches: `/portal create feature-auth`. When you pull and checkout the branch, the matching portal is right there.

!!! warning "Git is the bridge"
    This only works if both machines can access the same git remote. No git connection = no cross-machine portals. SSH keys on all machines, push access configured.
