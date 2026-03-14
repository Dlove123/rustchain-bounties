# GitHub Actions CI/CD Workflow

Automated CI/CD pipeline for RustChain projects.

## Features

- Multi-version testing (Node.js 18/20, Python 3.9/3.10/3.11)
- Automated testing on push and PR
- Code coverage upload to Codecov
- Auto deployment on main branch

## Files

- .github/workflows/ci.yml - CI/CD workflow configuration
- README.md - Documentation

## Usage

Workflow runs automatically on:
- Push to `main` or `develop` branches
- Pull requests to `main` branch

---

Fixes #1591
