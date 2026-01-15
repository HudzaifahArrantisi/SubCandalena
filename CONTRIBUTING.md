# Contributing to SubCandalena

First off, thank you for considering contributing to SubCandalena! It's people like you that make SubCandalena such a great tool.

## 🌟 How Can I Contribute?

### 🐛 Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When you create a bug report, include as many details as possible:

**Bug Report Template:**
```
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. With configuration '...'
3. See error

**Expected behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
 - OS: [e.g. Windows 10, Ubuntu 20.04]
 - Python Version: [e.g. 3.9.5]
 - SubCandalena Version: [e.g. 3.0]

**Additional context**
Any other relevant information.
```

### ✨ Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

**Feature Request Template:**
```
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
A clear description of what you want to happen.

**Describe alternatives you've considered**
Any alternative solutions or features you've considered.

**Additional context**
Any other context or screenshots.
```

### 🔧 Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/SubCandalena.git
   cd SubCandalena
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/amazing-feature
   # or
   git checkout -b fix/bug-fix
   ```

3. **Make Your Changes**
   - Write clean, readable code
   - Follow PEP 8 style guide
   - Add comments for complex logic
   - Update documentation if needed

4. **Test Your Changes**
   ```bash
   # Run the tool to ensure it works
   python main.py example.com --quick
   
   # Test with different configurations
   python main.py example.com --threads 100
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```
   
   **Commit Message Format:**
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for updates to existing features
   - `Docs:` for documentation changes
   - `Refactor:` for code refactoring

6. **Push to Your Fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your branch
   - Fill in the PR template

**Pull Request Template:**
```
**Description**
Brief description of the changes.

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**Testing**
- [ ] I have tested my changes
- [ ] I have updated the documentation
- [ ] My code follows the project's style guidelines

**Related Issues**
Closes #(issue number)
```

## 📝 Code Style Guidelines

### Python Code Style

Follow PEP 8 with these specifics:

```python
# Good
def scan_domain(domain: str, threads: int = 50) -> list:
    """
    Scan domain for subdomains.
    
    Args:
        domain: Target domain to scan
        threads: Number of concurrent threads
        
    Returns:
        List of discovered subdomains
    """
    results = []
    # Implementation
    return results

# Bad
def scan(d,t=50):
    r=[]
    # Implementation
    return r
```

**Key Points:**
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use type hints for function arguments and returns
- Write docstrings for all functions and classes
- Use meaningful variable names
- Add comments for complex logic

### File Organization

```
subhunterx/
├── __init__.py          # Package initialization
├── core/                # Core functionality
│   ├── __init__.py
│   ├── engine.py        # Main engine
│   ├── passive.py       # Passive recon
│   └── brute.py         # Brute force
├── modules/             # Feature modules
│   ├── __init__.py
│   └── analyzer.py      # Analysis module
└── utils/               # Utility functions
    ├── __init__.py
    └── helpers.py       # Helper functions
```

### Documentation

- Update README.md if adding new features
- Add docstrings to new functions
- Include code examples in docstrings
- Update CHANGELOG.md

Example docstring:
```python
def find_subdomains(domain: str, sources: list = None) -> dict:
    """
    Find subdomains using passive reconnaissance.
    
    This function queries multiple passive sources including:
    - Certificate Transparency logs
    - DNS databases
    - Search engines
    
    Args:
        domain (str): The target domain (e.g., 'example.com')
        sources (list, optional): List of sources to use. 
                                  Defaults to all sources.
    
    Returns:
        dict: Dictionary containing:
            - 'subdomains': List of discovered subdomains
            - 'count': Total number found
            - 'sources': Dictionary of results per source
    
    Raises:
        ValueError: If domain format is invalid
        ConnectionError: If all sources fail
    
    Example:
        >>> results = find_subdomains('example.com')
        >>> print(f"Found {results['count']} subdomains")
        Found 127 subdomains
    """
    pass
```

## 🧪 Testing

### Manual Testing

Before submitting, test your changes:

```bash
# Basic functionality
python main.py example.com --quick

# With different options
python main.py example.com --threads 100
python main.py example.com --dashboard

# Edge cases
python main.py invalid-domain.com
python main.py subdomain.example.com
```

### Adding Tests

If adding new functionality, consider adding tests:

```python
# tests/test_engine.py
import unittest
from subhunterx.core.engine import SubHunterXEngine

class TestEngine(unittest.TestCase):
    def test_domain_validation(self):
        """Test domain validation"""
        engine = SubHunterXEngine('example.com', {})
        self.assertTrue(engine.validate_domain('example.com'))
        self.assertFalse(engine.validate_domain('invalid'))
    
    def test_subdomain_discovery(self):
        """Test subdomain discovery"""
        engine = SubHunterXEngine('example.com', {})
        results = engine.find_subdomains()
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
```

## 🎯 Development Setup

### Setting Up Development Environment

```bash
# Clone your fork
git clone https://github.com/yourusername/SubCandalena.git
cd SubCandalena

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (if available)
pip install -r requirements-dev.txt

# Run in development mode
python main.py example.com --quick
```

### Useful Development Tools

```bash
# Code formatting
pip install black
black subhunterx/

# Linting
pip install pylint
pylint subhunterx/

# Type checking
pip install mypy
mypy subhunterx/
```

## 📚 Resources

- [Python PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Git Commit Message Guidelines](https://chris.beams.io/posts/git-commit/)
- [Writing Good Documentation](https://www.writethedocs.org/guide/)

## 🤝 Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inspiring community for all.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- Trolling, insulting/derogatory comments, and personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Other conduct which could reasonably be considered inappropriate

## 📞 Questions?

Feel free to:
- Open an issue for questions
- Join our community discussions
- Reach out to maintainers

## 🎉 Recognition

Contributors will be recognized in:
- README.md Contributors section
- CHANGELOG.md for their contributions
- GitHub Contributors page

Thank you for contributing to SubCandalena! 🚀
