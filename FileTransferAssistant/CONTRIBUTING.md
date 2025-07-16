# Contributing to File Transfer Assistant

First off, thank you for considering contributing to File Transfer Assistant! It's people like you that make this project better.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Environment Setup](#development-environment-setup)
- [Coding Standards](#coding-standards)
- [Commit Message Guidelines](#commit-message-guidelines)
- [License](#license)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/yourusername/FileTransferAssistant/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/yourusername/FileTransferAssistant/issues/new). Be sure to include:
  - A clear and descriptive title
  - A description of the expected behavior
  - Steps to reproduce the issue
  - Any relevant error messages
  - Screenshots if applicable
  - Your operating system and Python version

### Suggesting Enhancements

- Use GitHub Issues to submit feature requests
- Clearly describe the feature and why it would be useful
- Include any relevant screenshots or mockups

### Pull Requests

1. Fork the repository and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Development Environment Setup

1. Fork and clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If you have separate dev requirements
   ```
4. Run the application:
   ```bash
   python -m src
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints for all function parameters and return values
- Write docstrings for all public modules, functions, and classes
- Keep functions small and focused on a single task
- Write meaningful commit messages

### Pre-commit Hooks

We use pre-commit hooks to maintain code quality. Install them with:

```bash
pre-commit install
```

The hooks will run automatically on each commit.

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code (white-space, formatting, etc)
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools and libraries

Example:
```
feat: add dark mode support
fix: resolve issue with file transfer cancellation
```

## License

By contributing, you agree that your contributions will be licensed under its MIT License.
