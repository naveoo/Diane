# Testing Guide

This document explains how to run the test suite for the Diane simulation engine.

---

## Quick Start

### Install Test Dependencies

```bash
pip install pytest pytest-cov
```

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=. --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

---

## Test Structure

The test suite is organized into the following modules:

```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures and test utilities
├── test_domains.py          # Domain model tests (Faction, Region, World)
├── test_systems.py          # System tests (Power, Economy, Legitimacy, etc.)
├── test_deltas.py           # Delta system tests (Builder, Applier, Validator)
├── test_persistence.py      # Database and serialization tests
├── test_metrics.py          # Analytics and metrics tests
└── test_integration.py      # End-to-end integration tests
```

---

## Running Specific Tests

### Run a Single Test File

```bash
pytest tests/test_domains.py
```

### Run a Specific Test Class

```bash
pytest tests/test_domains.py::TestFaction
```

### Run a Specific Test Function

```bash
pytest tests/test_domains.py::TestFaction::test_faction_creation
```

### Run Tests by Marker

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

---

## Test Coverage

### Coverage by Module

The test suite provides comprehensive coverage for:

- **Domain Models** (100%): Faction, Region, World, Power, Resources
- **Systems** (90%+): All 10 systems (Power, Economy, Legitimacy, Research, Trade, Alliance, Conflict, War, Investment, Region)
- **Deltas** (95%+): Builder, Applier, Validator
- **Persistence** (90%+): Database operations, serialization
- **Metrics** (95%+): All geopolitical indicators and rankings
- **Integration** (80%+): End-to-end simulation flows

### Generate Coverage Report

```bash
pytest --cov=. --cov-report=term-missing
```

This shows which lines are not covered by tests.

---

## Test Fixtures

Common test fixtures are defined in `conftest.py`:

### Available Fixtures

- `default_config`: Returns default Defaults() configuration
- `simple_faction`: A single test faction
- `simple_region`: A single test region
- `simple_world`: World with one faction and one region
- `balanced_world`: World with two equal factions
- `unbalanced_world`: World with one dominant faction
- `temp_db`: Temporary database for persistence tests

### Using Fixtures

```python
def test_example(simple_world, default_config):
    # Use fixtures in your test
    assert len(simple_world.factions) == 1
```

---

## Writing New Tests

### Test Naming Convention

- Test files: `test_*.py`
- Test classes: `Test*`
- Test functions: `test_*`

### Example Test

```python
import pytest
from domains.faction import Faction

class TestMyFeature:
    """Tests for my new feature."""
    
    def test_basic_functionality(self, simple_faction):
        """Test that basic functionality works."""
        # Arrange
        initial_value = simple_faction.power.total
        
        # Act
        # ... perform action ...
        
        # Assert
        assert result == expected_value
    
    @pytest.mark.slow
    def test_expensive_operation(self):
        """Test that takes significant time."""
        # ... slow test ...
```

### Test Markers

Use markers to categorize tests:

```python
@pytest.mark.unit
def test_unit_test():
    pass

@pytest.mark.integration
def test_integration_test():
    pass

@pytest.mark.slow
def test_slow_test():
    pass
```

---

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

---

## Troubleshooting

### Tests Fail with Import Errors

Ensure you're running tests from the project root:

```bash
cd /path/to/Diane
pytest
```

### Database Lock Errors

Integration tests use temporary databases. If you see lock errors, ensure previous test runs have completed.

### Slow Test Execution

Skip slow tests during development:

```bash
pytest -m "not slow"
```

---

## Test Philosophy

### Unit Tests

- Test individual components in isolation
- Use mocks/fixtures to avoid dependencies
- Fast execution (< 1 second per test)
- High coverage of edge cases

### Integration Tests

- Test system interactions
- Use real components (no mocks)
- Verify end-to-end workflows
- May be slower (marked with `@pytest.mark.slow`)

### Test Data

- Use fixtures for reusable test data
- Keep test data minimal and focused
- Avoid hardcoded values when possible

---

## Best Practices

1. **One assertion per test** (when possible)
2. **Descriptive test names** that explain what is being tested
3. **Arrange-Act-Assert** pattern for clarity
4. **Test edge cases** (empty inputs, boundary values, etc.)
5. **Keep tests independent** (no shared state between tests)
6. **Use fixtures** to reduce code duplication

---

**For questions or issues with tests, please open a GitHub issue.**
