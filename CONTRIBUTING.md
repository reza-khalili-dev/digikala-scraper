
```markdown
# Contributing to Digikala Scraper

First off, thank you for considering contributing to Digikala Scraper! It's people like you that make this tool better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Style Guidelines](#style-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Requests](#pull-requests)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

### Our Standards

- **Use welcoming and inclusive language**
- **Be respectful of differing viewpoints and experiences**
- **Gracefully accept constructive criticism**
- **Focus on what is best for the community**
- **Show empathy towards other community members**

## Getting Started

### Prerequisites

- Python 3.7+
- Git
- Basic knowledge of:
  - Python programming
  - Tkinter GUI
  - REST APIs
  - Web scraping concepts

### Setting Up Development Environment

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/reza-khalili-dev/digikala-scraper.git
cd digikala-scraper

Create a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Create a new branch:
git checkout -b feature/your-feature-name



How Can I Contribute?
🐛 Reporting Bugs
Good bug reports include:

A quick summary and/or background

Steps to reproduce

What you expected would happen

What actually happens

Notes (possibly including why you think this might be happening)

💡 Suggesting Enhancements
Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

Use a clear and descriptive title

Provide a step-by-step description of the suggested enhancement

Provide specific examples to demonstrate the steps

Describe the current behavior and explain which behavior you expected to see instead

📚 Improving Documentation
Documentation improvements are always welcome! This includes:

README.md improvements

Code comments

Docstrings

Wiki pages

Style Guidelines
Python Style Guide
Follow PEP 8 guidelines

Use 4 spaces for indentation (no tabs)

Maximum line length: 100 characters

Use descriptive variable names (Persian transliteration is acceptable for Persian-specific content)

Add docstrings to all classes and functions



Example:

def format_price(self, price: int) -> str:
    """
    Format price to Persian currency format.
    
    Args:
        price (int): Price in Rials
        
    Returns:
        str: Formatted price string (e.g., "1,234,567 تومان")
    """
    return f"{price:,} تومان"


GUI Guidelines
All Persian text must be RTL compatible

Maintain consistent padding (5-10px)

Use Tahoma font for Persian text

Use Consolas font for logs and English text

Commit Messages
Use the present tense ("Add feature" not "Added feature")

Use the imperative mood ("Move cursor to..." not "Moves cursor to...")

Limit the first line to 72 characters or less

Reference issues and pull requests liberally after the first line



Format:

[Type] Short summary (72 chars or less)

More detailed explanatory text, if necessary. Wrap it to about 72
characters. The blank line separating the summary from the body is
critical.

Type can be:
- FEATURE: New feature
- FIX: Bug fix
- DOCS: Documentation only
- STYLE: Style changes
- REFACTOR: Code refactoring
- PERF: Performance improvement
- TEST: Test changes

Pull Requests

1- Fill in the required template

2- Do not include issue numbers in the PR title

3- Include screenshots for GUI changes

4- Update documentation for any changed functionality

5- Follow the Python style guide

6- Ensure all tests pass (if applicable)

PR Review Process

1- Maintainers will review your PR

2- They may request changes

3- Once approved, a maintainer will merge it


📝 Additional Notes
Persian Text Support
When adding Persian text to the GUI:

# Always set justify='right' and anchor='e'
label = tk.Label(
    text="متن فارسی",
    justify='right',
    anchor='e'
)

# For ScrolledText, use tags
text.tag_configure('persian', justify='right')
text.insert(tk.END, "متن فارسی\n", 'persian')


API Changes
If modifying API requests:

Test with different page sizes

Handle rate limiting gracefully

Add appropriate error handling

Update the Config class if adding new parameters

🎉 Recognition
Contributors will be recognized in the README.md file. Significant contributions may also be acknowledged in release notes.


Thank you for contributing! 🚀

