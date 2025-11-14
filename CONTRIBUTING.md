# Contributing to BOB Google Maps

First off, thank you for considering contributing to BOB Google Maps! 🔱

This document provides guidelines for contributing to the project. By participating in this project, you agree to abide by its terms and the [Code of Conduct](CODE_OF_CONDUCT.md).

## 🌟 Ways to Contribute

There are many ways to contribute to BOB Google Maps:

- **Report bugs** 🐛
- **Suggest new features** 💡
- **Improve documentation** 📚
- **Submit code changes** 💻
- **Review pull requests** 👀
- **Share the project** 📢

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Chrome/Chromium browser
- Basic understanding of web scraping and Playwright/Selenium

### Development Setup

1. **Fork the repository**
   ```bash
   # Click the "Fork" button on GitHub
   # Then clone your fork
   git clone https://github.com/YOUR_USERNAME/BOB-Google-Maps.git
   cd BOB-Google-Maps
   ```

2. **Create a development environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -e ".[dev]"
   playwright install chromium
   playwright install-deps
   ```

4. **Verify installation**
   ```bash
   python -c "from bob import HybridExtractor; print('✅ Setup successful!')"
   pytest tests/ -v
   ```

## 📋 Development Workflow

### 1. Create a Branch

Always create a new branch for your work:

```bash
# For features
git checkout -b feature/your-feature-name

# For bug fixes
git checkout -b fix/issue-description

# For documentation
git checkout -b docs/what-you-are-documenting
```

### 2. Make Your Changes

- Write clear, concise code
- Follow the existing code style
- Add/update tests as needed
- Update documentation if needed

### 3. Test Your Changes

Run the full test suite before submitting:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=bob --cov-report=term-missing

# Run specific test types
./scripts/run_tests.sh unit
./scripts/run_tests.sh integration
```

### 4. Commit Your Changes

Write meaningful commit messages following conventional commits:

```bash
git add .
git commit -m "type(scope): description"
```

**Commit Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**
```bash
git commit -m "feat(extractors): add email extraction from websites"
git commit -m "fix(cache): handle corrupted cache entries gracefully"
git commit -m "docs(readme): update installation instructions"
```

### 5. Push to Your Fork

```bash
git push origin your-branch-name
```

### 6. Create a Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill out the PR template
5. Submit the pull request

## 📝 Pull Request Guidelines

### PR Title

Use conventional commit format:
```
type(scope): Brief description of changes
```

### PR Description

Include:
- **What**: What changes did you make?
- **Why**: Why did you make these changes?
- **How**: How did you implement the changes?
- **Testing**: How did you test the changes?
- **Screenshots**: If applicable

### PR Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] All tests pass (`pytest tests/`)
- [ ] New tests added for new features
- [ ] Documentation updated (if needed)
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] No breaking changes (or clearly documented)
- [ ] Commits are clean and well-organized
- [ ] PR description is clear and complete

## 🎨 Code Style Guidelines

### Python Style

Follow PEP 8 with these specifics:

```python
# Line length: 100 characters (not 80)
MAX_LINE_LENGTH = 100

# Use double quotes for strings
message = "Hello, World!"

# Type hints everywhere
def extract_business(query: str) -> Dict[str, Any]:
    pass

# Docstrings for all public functions
def extract_business(query: str) -> Dict[str, Any]:
    """
    Extract business data from Google Maps.

    Args:
        query: Search query for the business

    Returns:
        Dictionary containing business data and metadata

    Raises:
        ExtractionError: When extraction fails
    """
    pass
```

### Code Formatting

Use these tools (automatically run in CI):

```bash
# Format code with Black
black bob/ tests/ --line-length 100

# Sort imports with isort
isort bob/ tests/ --profile black

# Lint with flake8
flake8 bob/ tests/ --max-line-length=100

# Type check with mypy
mypy bob/ --ignore-missing-imports
```

### Naming Conventions

```python
# Classes: PascalCase
class BusinessExtractor:
    pass

# Functions/methods: snake_case
def extract_business_data():
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Private members: _leading_underscore
def _internal_helper():
    pass
```

## 🧪 Testing Guidelines

### Test Structure

```python
# tests/unit/test_feature.py
def test_feature_success():
    """Test successful feature execution."""
    # Arrange
    input_data = "test input"

    # Act
    result = function(input_data)

    # Assert
    assert result.success is True
    assert result.data == expected_data
```

### Test Coverage

- Aim for **80%+ coverage** on new code
- Write tests for:
  - Happy path (success cases)
  - Error cases
  - Edge cases
  - Boundary conditions

### Running Tests

```bash
# All tests
pytest tests/

# Specific test file
pytest tests/unit/test_extractors.py

# Specific test function
pytest tests/unit/test_extractors.py::test_playwright_extraction

# With coverage
pytest tests/ --cov=bob --cov-report=html

# Fast tests only
pytest tests/ -m "not slow"
```

## 📚 Documentation Guidelines

### Code Documentation

```python
def extract_business(
    query: str,
    include_reviews: bool = False,
    max_reviews: int = 10
) -> Dict[str, Any]:
    """
    Extract comprehensive business data from Google Maps.

    This function searches for a business on Google Maps and extracts
    detailed information including contact details, ratings, and optionally
    customer reviews.

    Args:
        query: Search query for the business (e.g., "Starbucks Seattle")
        include_reviews: Whether to extract customer reviews
        max_reviews: Maximum number of reviews to extract (if include_reviews=True)

    Returns:
        Dictionary containing:
        - success (bool): Whether extraction succeeded
        - business (Business): Business data object (if successful)
        - error (str): Error message (if failed)
        - extraction_time_seconds (float): Time taken for extraction

    Raises:
        ExtractionError: When extraction fails completely
        ExtractionTimeout: When extraction times out
        NoResultsFound: When no business matches the query

    Example:
        >>> extractor = HybridExtractor()
        >>> result = extractor.extract_business("Starbucks Reserve Seattle")
        >>> if result['success']:
        ...     print(f"Found: {result['business'].name}")
        Found: Starbucks Reserve Roastery

    Note:
        This function uses intelligent caching to avoid re-extracting
        the same business within 24 hours.
    """
    pass
```

### README Updates

When adding features, update:
- Feature list
- Usage examples
- Configuration options
- Troubleshooting section

## 🐛 Bug Reports

### Before Reporting

1. **Search existing issues** - Your bug might already be reported
2. **Update to latest version** - Bug might already be fixed
3. **Reproduce the bug** - Ensure it's reproducible

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Initialize extractor with '...'
2. Call method '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- BOB Version: [e.g., 4.2.0]
- Python Version: [e.g., 3.10.0]
- OS: [e.g., Ubuntu 22.04]
- Browser: [e.g., Chromium 119.0]

**Additional context**
- Error logs/traceback
- Screenshots (if applicable)
- Any other relevant information
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Additional context**
- Use cases
- Examples from other projects
- Mockups/diagrams
```

## 🔍 Code Review Process

### For Contributors

- Respond to review feedback promptly
- Be open to suggestions
- Ask questions if feedback is unclear
- Update PR based on feedback

### For Reviewers

- Be respectful and constructive
- Focus on code, not the person
- Explain the "why" behind suggestions
- Approve when ready, request changes when needed

## 🎯 Priority Areas

We especially welcome contributions in these areas:

1. **Performance Optimization**
   - Faster extraction algorithms
   - Memory usage reduction
   - Caching improvements

2. **New Features**
   - Additional extraction engines
   - More data fields
   - Export format support

3. **Testing**
   - More test coverage
   - Edge case testing
   - Performance benchmarks

4. **Documentation**
   - Usage examples
   - Architecture documentation
   - Video tutorials

5. **Bug Fixes**
   - See [Issues](https://github.com/div197/BOB-Google-Maps/issues) labeled `bug`

## 🏆 Recognition

Contributors are recognized in:
- README.md Contributors section
- Release notes
- Git commit history
- Special thanks in documentation

## 💬 Communication

- **GitHub Issues** - For bugs and feature requests
- **Pull Requests** - For code contributions
- **Discussions** - For questions and general discussion

## 📜 License

By contributing to BOB Google Maps, you agree that your contributions will be licensed under the MIT License.

## 🙏 Acknowledgments

This project follows the principles of **Nishkaam Karma Yoga** (selfless action). We believe in:
- Quality over quantity
- Clear code over clever code
- Documentation over assumptions
- Collaboration over competition

Thank you for contributing to making BOB Google Maps better! 🔱

---

**Questions?** Open an issue or start a discussion!

**🔱 JAI SHREE KRISHNA!**

---

**Last Updated:** November 14, 2025
**Version:** 4.2.0
