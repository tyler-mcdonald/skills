---
name: deploy-aisearch
description: Update aisearch backend/frontend image tags from latest git tags and open an MR. Use when user wants to deploy aisearch, bump image versions, or update deployment tags.
---

Update aisearch container image tags in this repo's Terraform files from the latest git tags in the source repos, then commit, push, and open an MR.

**Args**: `backend`, `frontend`, or omit for both.

## Steps

### 1. Branch setup (in this repo)

```bash
git fetch origin
git checkout main
git pull origin main
```

If branch `aisearch-deployment-patch` exists locally, check it out and merge main:
```bash
git checkout aisearch-deployment-patch
git merge main
```
If not, create it:
```bash
git checkout -b aisearch-deployment-patch
```

### 2. Read latest tags

For each target (backend and/or frontend based on args):

**Backend** (`~/code/aisearch-backend`, default branch `master`):
```bash
cd ~/code/aisearch-backend
git fetch origin
git checkout master
git pull origin master
git describe --tags --abbrev=0
```

**Frontend** (`~/code/aisearch-frontend`, default branch `master`):
```bash
cd ~/code/aisearch-frontend
git fetch origin
git checkout master
git pull origin master
git describe --tags --abbrev=0
```

Use the tag exactly as returned — no stripping or modification.

### 3. Compare & update

Read the TF files in this repo:
- `instance/backend.tf` — the `aisearch_backend_image` local on line 2
- `instance/frontend.tf` — the `aisearch_frontend_image` local on line 2

Extract the current version from each image string (everything after the last `:`).

For each target:
- If tag matches current version → notify user "backend (or frontend) already at <version>", skip
- If different → use the Edit tool to replace the old image string with the new tag

### 4. Early exit

If nothing changed (all tags match), inform the user and stop. No commit, no branch push, no MR.

### 5. Commit

Stage only changed files:
```bash
git add instance/backend.tf instance/frontend.tf
```

Commit message format: `chore: backend <version>, frontend <version>`
- Omit whichever service wasn't updated
- If only one changed: `chore: backend <version>` or `chore: frontend <version>`

### 6. Push & MR

```bash
git push -u origin aisearch-deployment-patch
```

Check if an MR already exists for the branch. If not, create one:
- Title: `aisearch deployment`
- Target: `main`
- Assigned to user
- No description

If MR already exists, note its URL — the push already updated it.
