# Contributing to Diane

First off, thank you for considering contributing to **Diane**! 
Diane is an open-source geopolitical simulation project, and we welcome contributions from everyone, whether you're a developer, a designer, a writer, or just someone passionate about geopolitics and simulations.

This guide will help you get started. **No contribution is too small!**

---

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [How Can I Contribute?](#how-can-i-contribute)
   - [Reporting Bugs](#reporting-bugs)
   - [Suggesting Features](#suggesting-features)
   - [Improving Documentation](#improving-documentation)
   - [Contributing Code](#contributing-code)
3. [Development Setup](#development-setup)
4. [Submitting Changes](#submitting-changes)
5. [Style Guidelines](#style-guidelines)
6. [Recognition](#recognition)

---

## Code of Conduct
By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the expectations for all contributors.

---

## How Can I Contribute?

### Reporting Bugs
If you find a bug, please open an issue on GitHub with the following details:
- A **clear and descriptive title**.
- A **step-by-step description** of how to reproduce the bug.
- The **expected behavior** and the **actual behavior**.
- Any relevant **screenshots, logs, or error messages**.
- Your **operating system** and **Python version** (if applicable).

**Example:**
```
Title: Simulation crashes when loading custom scenario

Description:
1. I created a custom scenario using `!capture_draft`.
2. I tried to load it with `!start_custom`.
3. The bot crashed with the error: "KeyError: 'region_id'".

Expected: The simulation should load without errors.
Actual: The bot crashes.
```

---

### Suggesting Features
We love new ideas! To suggest a feature:
1. Open an issue on GitHub with the label `enhancement`.
2. Provide a **detailed description** of the feature.
3. Explain **why** this feature would be useful for Diane.
4. (Optional) Include mockups, examples, or pseudocode.

**Example:**
```
Title: Add diplomatic alliance simulation

Description:
It would be great if Diane could simulate the formation and dissolution of alliances between factions. This would add depth to the geopolitical interactions.

Why:
Alliances are a key part of real-world geopolitics, and simulating them would make Diane more realistic and engaging.
```

---

### Improving Documentation
Good documentation is crucial! You can help by:
- Fixing typos or unclear explanations.
- Adding examples or tutorials.
- Improving the `README.md` or wiki.

---

### Contributing Code
To contribute code, follow these steps:

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/diane.git
   cd diane
   ```
3. **Create a new branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes** and test them thoroughly.
5. **Commit your changes** with a descriptive message:
   ```bash
   git commit -m "Add diplomatic alliance simulation"
   ```
6. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request (PR)** on the main repository. Include:
   - A clear title and description.
   - A reference to any related issues (e.g., "Fixes #123").
   - Screenshots or logs if applicable.

---

## Development Setup
To set up Diane for development:

1. **Install Python 3.11+** and pip.
2. **Clone the repository**:
   ```bash
   git clone https://github.com/your-organization/diane.git
   cd diane
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables** (e.g., `BOT_TOKEN` for Discord). Use the `.env.example` file as a template.
5. **Run the bot** for testing:
   ```bash
   python discord_bot.py
   ```

---

## Submitting Changes
- Ensure your code follows the [Style Guidelines](#style-guidelines).
- Write **clear commit messages** and **detailed PR descriptions**.
- Keep your PRs **small and focused**. If you're making multiple changes, split them into separate PRs.
- Be ready to **address feedback** and iterate on your changes.

---

## Style Guidelines
### Python Code
- Follow [PEP 8](https://pep8.org/) guidelines.
- Use **type hints** for functions and variables.
- Write **docstrings** for classes, methods, and functions.
- Use **snake_case** for variable and function names, and **PascalCase** for class names.

### Example:
```python
def calculate_power_index(faction: Faction, world: World) -> float:
    """Calculate the composite power index for a faction.

    Args:
        faction: The faction to calculate the index for.
        world: The world containing the faction.

    Returns:
        The composite power index.
    """
    return faction.power.total * (1 + faction.knowledge / 100)
```

### Documentation
- Use **clear and concise language**.
- Provide **examples** where helpful.
- Keep the `README.md` up-to-date.

---

## Recognition
All contributors to Diane will be recognized! We’ll:
- List you in the `CONTRIBUTORS.md` file.
- Thank you in release notes.

---

## Questions?
If you have questions or need help, feel free to:
- Open an issue on GitHub.
- Contact the maintainers at [naa.veoos@gmail.com].

**Thank you for contributing to Diane!** Your help makes this project better for everyone.
