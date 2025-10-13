# GitHub Actions - Docker Build

Automatically builds and publishes the Docker image to GitHub Container Registry.

## Setup

1. **Push this workflow to GitHub:**
   ```bash
   git add .github/
   git commit -m "ci: add Docker build workflow"
   git push origin main
   ```

2. **Enable GitHub Actions:**
   - Go to repo **Settings** → **Actions** → **General**
   - Allow "Read and write permissions"

## How It Works

The workflow (`docker-publish.yml`) automatically:

1. **Checks out code with submodules** - Handles the `src/app` submodule automatically
2. **Builds Docker image** - Uses `src/Dockerfile`
3. **Publishes to GitHub Container Registry** - Tagged appropriately

### Triggers

- **Push to main/master** → Builds and publishes with `latest` tag
- **Pull requests** → Builds only (doesn't publish)
- **Git tags `v*.*.*`** → Publishes with version tags
- **Manual** → Run from Actions tab

### Image Tags

```bash
ghcr.io/unpast/unpast-backend:latest          # main branch
ghcr.io/unpast/unpast-backend:pr-42           # pull request #42
ghcr.io/unpast/unpast-backend:v1.0.0          # git tag v1.0.0
ghcr.io/unpast/unpast-backend:main-abc1234    # commit SHA
```

## Using the Published Image

```bash
# Pull the latest image
docker pull ghcr.io/unpast/unpast-backend:latest

# Use in docker-compose.yml
services:
  app:
    image: ghcr.io/unpast/unpast-backend:latest
```

## Releasing a New Version

When you update the submodule or backend code:

```bash
# Tag the release
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# GitHub Actions will build and publish:
# - ghcr.io/unpast/unpast-backend:v1.0.0
# - ghcr.io/unpast/unpast-backend:1.0
# - ghcr.io/unpast/unpast-backend:latest
```

## Updating the Submodule

When there's a new version of the unpast package:

```bash
# Update submodule to new commit
cd src/app
git fetch origin
git checkout <new-commit-or-tag>
cd ../..

# Commit the update
git add src/app
git commit -m "chore: update unpast submodule to v0.1.12"
git push origin main

# Create a new release tag
git tag -a v1.0.1 -m "Update unpast to v0.1.12"
git push origin v1.0.1
```

## Troubleshooting

### Submodule not initialized

If the build fails with "submodule not initialized":

```bash
# Ensure .gitmodules is committed
git add .gitmodules
git commit -m "fix: add submodule config"
git push
```

### Build fails with dependency errors

The Dockerfile has been updated to fix numpy/scipy build issues:
- Pinned base image: `continuumio/miniconda3:23.5.2-0`
- Upgraded pip/setuptools before installing packages
- Removed conflicting numpy version

### Image not found when pulling

Make the package public:
- Go to GitHub → **Packages** → **unpast-backend**
- **Package settings** → Change visibility to Public

## Monitoring Builds

- **Actions tab**: See all workflow runs
- **Commit badges**: ✅ or ❌ next to commits
- **PR checks**: Build status shown in pull requests

---

That's it! Push to main and watch your image build automatically. 🚀
