# Gitea Actions for Mus Project

This document explains the Gitea Actions workflows set up for the Mus card game simulator project.

## Overview

The project includes several automated workflows that run on different triggers to ensure code quality, run tests, build the application, and manage releases.

## Workflows

### 1. Test Suite (`test.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Purpose:**
- Runs unit tests across multiple Python versions (3.8, 3.9, 3.10, 3.11)
- Performs code linting with flake8
- Generates test coverage reports
- Uploads coverage to Codecov (for Python 3.11 only)

**Key Features:**
- Matrix strategy for testing multiple Python versions
- Caching of pip dependencies for faster builds
- Coverage reporting with HTML and XML outputs
- Integration with Codecov for coverage tracking

### 2. Code Quality (`lint.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Purpose:**
- Comprehensive code quality checks
- Code formatting validation
- Import sorting verification
- Type checking
- Security vulnerability scanning

**Tools Used:**
- `flake8`: Python linting
- `black`: Code formatting
- `isort`: Import sorting
- `mypy`: Type checking
- `bandit`: Security analysis
- `safety`: Known vulnerability checking

### 3. Build Application (`build.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Purpose:**
- Builds executable versions of the application
- Tests across multiple operating systems (Ubuntu, Windows, macOS)
- Creates distributable artifacts

**Key Features:**
- Multi-platform builds (Linux, Windows, macOS)
- Multiple Python version support
- PyInstaller for creating standalone executables
- Artifact upload for distribution

### 4. Release Management (`release.yml`)

**Triggers:**
- Push of version tags (e.g., `v1.0.0`)

**Purpose:**
- Automates the release process
- Builds and validates Python packages
- Creates GitHub releases with artifacts

**Key Features:**
- Automatic package building
- Package validation with twine
- GitHub release creation
- Asset upload to releases

### 5. Notebook Validation (`notebook.yml`)

**Triggers:**
- Push to `main` or `develop` branches (when notebooks change)
- Pull requests affecting notebook files

**Purpose:**
- Validates Jupyter notebooks can be executed
- Ensures notebook code runs without errors
- Tests data analysis workflows

**Key Features:**
- Notebook execution testing
- Error detection in notebook cells
- Integration with the project's data analysis workflows

### 6. Continuous Integration (`ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Purpose:**
- Comprehensive CI pipeline
- Combines multiple quality checks
- Ensures the application works end-to-end

**Key Features:**
- All-in-one quality check
- GUI import testing (with graceful failure in headless environments)
- Data loading validation
- Coverage threshold enforcement (80%)
- Artifact upload for coverage reports

## Usage

### Running Workflows Locally

While Gitea Actions run automatically, you can run similar checks locally:

```bash
# Install dependencies
pip install -r requirements.txt
pip install pytest pytest-cov flake8 black isort mypy bandit safety

# Run tests
pytest tests/ -v --cov=src --cov-report=html

# Check code formatting
black --check .
isort --check-only .

# Lint code
flake8 .

# Type checking
mypy src/

# Security checks
bandit -r src/
safety check

# Build executable
pyinstaller --onefile --name=mus-simulator src/main.py
```

### Workflow Status

You can check the status of workflows in your Gitea repository:
1. Go to your repository
2. Click on "Actions" tab
3. View the status of recent workflow runs
4. Click on individual runs to see detailed logs

### Customizing Workflows

To modify the workflows:

1. Edit the `.gitea/workflows/*.yml` files
2. Adjust triggers, steps, or configurations as needed
3. Commit and push changes
4. Workflows will automatically use the updated configuration

### Common Modifications

**Adding New Python Versions:**
```yaml
strategy:
  matrix:
    python-version: [3.8, 3.9, 3.10, 3.11, 3.12]  # Add 3.12
```

**Changing Coverage Threshold:**
```yaml
- name: Run tests
  run: |
    python -m pytest tests/ -v --cov=src --cov-report=xml --cov-report=html --cov-fail-under=90  # Change from 80 to 90
```

**Adding New Linting Tools:**
```yaml
- name: Install dependencies
  run: |
    pip install pylint  # Add new tool
    
- name: Lint with pylint
  run: |
    pylint src/
```

## Troubleshooting

### Common Issues

1. **Tests failing due to GUI dependencies:**
   - The CI workflow includes special handling for GUI imports
   - GUI tests are expected to fail in headless environments

2. **Coverage threshold not met:**
   - Increase test coverage or lower the threshold
   - Check the coverage report for uncovered areas

3. **Build failures on specific platforms:**
   - Check platform-specific dependencies
   - Ensure all required libraries are in requirements.txt

4. **Notebook execution timeouts:**
   - Increase timeout in the notebook workflow
   - Optimize notebook code for faster execution

### Getting Help

- Check the workflow logs in Gitea Actions tab
- Review the specific step that failed
- Ensure all dependencies are properly specified
- Test changes locally before pushing

## Best Practices

1. **Keep workflows fast:** Use caching and parallel execution where possible
2. **Test locally first:** Run checks locally before pushing
3. **Monitor coverage:** Maintain good test coverage
4. **Security first:** Regular security scans help catch vulnerabilities
5. **Document changes:** Update this documentation when modifying workflows
