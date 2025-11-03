# GitHub Copilot Configuration

This directory contains configuration files for GitHub Copilot to provide context-aware assistance when working with this repository.

## Structure

```
.github/
├── copilot-instructions.md          # Main instructions applied to all files (**)
├── instructions/                     # Specialized instruction files
│   ├── python.instructions.md       # Python development guidelines (*.py)
│   ├── terraform.instructions.md    # Terraform conventions (*.tf)
│   ├── terraform-azure.instructions.md  # Azure-specific Terraform (*.tf, *.tfvars, etc.)
│   └── github-actions-ci-cd-best-practices.instructions.md  # GitHub Actions (workflows/*.yml)
├── chatmodes/                        # Custom chat modes
├── prompts/                          # Reusable prompts
└── workflows/                        # GitHub Actions workflows
```

## Instruction Files

### Main Instructions: `copilot-instructions.md`

- **Applies to:** All files (`**`)
- **Purpose:** Provides comprehensive project overview, development workflow, and architecture guidelines
- **Key topics:**
  - Project architecture and design principles
  - Development workflow (prepare, implement, test, commit)
  - Code generation rules (Python 3.13, Reflex, FastAPI, SQLAlchemy 2.0)
  - Testing strategy (≥80% coverage)
  - Security and configuration hygiene
  - Pre-PR checklist

### Specialized Instructions

#### `instructions/python.instructions.md`

- **Applies to:** All Python files (`**/*.py`)
- **Purpose:** Python-specific development guidelines
- **Key topics:**
  - Project setup and installation
  - Running the application (development, debug, production modes)
  - Testing and coverage requirements
  - Linting and formatting with ruff
  - Database migrations with Alembic
  - Code style guidelines (especially logging patterns)
  - Common patterns for Reflex components and state management

#### `instructions/terraform.instructions.md`

- **Applies to:** Terraform files (`**/*.tf`)
- **Purpose:** General Terraform conventions and best practices
- **Key topics:**
  - Security best practices (secrets, encryption, IAM)
  - Modularity and reusability
  - Code style and formatting
  - Documentation standards
  - Testing infrastructure configurations

#### `instructions/terraform-azure.instructions.md`

- **Applies to:** Azure Terraform files (`**/*.terraform, **/*.tf, **/*.tfvars, etc.`)
- **Purpose:** Azure-specific Terraform guidance
- **Key topics:**
  - Azure Verified Modules (AVM) usage
  - Resource naming and tagging
  - Networking considerations
  - Security and compliance
  - Cost management
  - State management with Azure Storage

#### `instructions/github-actions-ci-cd-best-practices.instructions.md`

- **Applies to:** GitHub Actions workflow files (`.github/workflows/*.yml`)
- **Purpose:** Comprehensive CI/CD pipeline best practices
- **Key topics:**
  - Workflow structure and design
  - Security (secrets, OIDC, least privilege)
  - Optimization (caching, parallelization, matrix strategies)
  - Testing strategies (unit, integration, E2E, performance)
  - Deployment strategies (staging, production, rollbacks)
  - Troubleshooting common issues

## How It Works

GitHub Copilot automatically loads these instruction files when you:

1. Work on files in this repository
2. Open pull requests
3. Chat with Copilot in supported IDEs (VS Code, GitHub.com, etc.)
4. Assign issues to @copilot

The instructions are applied based on the `applyTo` field in the YAML frontmatter:

```yaml
---
applyTo: '**/*.py'
description: 'Python development guidelines'
---
```

## Using These Instructions

### For Developers

When working with this repository:

1. **File-specific guidance:** Copilot will automatically apply relevant instructions based on the file you're editing
2. **Ask for help:** Mention @copilot in PR comments or chat to get context-aware assistance
3. **Follow patterns:** The instructions include code examples and patterns to follow

### For Copilot

When assigned to an issue or mentioned in a PR:

1. Read and follow all applicable instruction files
2. Apply the guidelines from `copilot-instructions.md` for general workflow
3. Use specialized instructions for specific file types
4. Follow the pre-commit checklist before submitting changes
5. Ensure all quality gates pass (tests, linting, coverage)

## Quick Reference

### Common Commands

```bash
# Setup
make install              # Install dependencies with uv

# Development
make reflex              # Start development server
make reflex-debug        # Start with debug logging
make reflex-prod         # Start in production mode

# Quality Checks
make test                # Run tests
make lint                # Check code style
make format              # Format code
make check               # Run all checks

# Database
make alembic             # Check migration status
make db-migrate          # Apply migrations
make db-migrate-history  # View migration history
make db-migrate-down     # Rollback one migration

# Cleanup
make clean               # Remove cache and build artifacts
```

### Key Requirements

- **Python:** 3.13+
- **Package Manager:** uv
- **Logging:** No f-strings in logger calls (use `log.info("msg: %s", var)`)
- **Type Annotations:** Required for all functions
- **Test Coverage:** ≥ 80%
- **Commit Style:** Conventional commits (`feat:`, `fix:`, `refactor:`, etc.)

## Updating Instructions

To update or add new instruction files:

1. Create/edit files in `.github/instructions/` with `.instructions.md` extension
2. Add YAML frontmatter with `applyTo` and `description` fields:
   ```yaml
   ---
   applyTo: 'pattern/**/*.ext'
   description: 'Brief description'
   ---
   ```
3. Document the new instructions in this README
4. Test by asking Copilot to work on relevant files

## Best Practices

1. **Keep instructions focused:** Each file should cover a specific domain or file type
2. **Use clear examples:** Include code examples with ✅ correct and ❌ incorrect patterns
3. **Update regularly:** Keep instructions aligned with current project practices
4. **Be specific:** Provide concrete guidelines rather than vague suggestions
5. **Include context:** Explain why certain patterns are preferred

## References

- [GitHub Copilot Best Practices](https://docs.github.com/en/copilot/tutorials/coding-agent/get-the-best-results)
- [Custom Instructions Documentation](https://github.blog/changelog/2025-07-23-github-copilot-coding-agent-now-supports-instructions-md-custom-instructions/)
- [Building Custom Copilot Agents](https://montemagno.com/building-better-apps-with-github-copilot-custom-agents/)

---

**Last Updated:** November 2025  
**Maintained by:** Project maintainers
