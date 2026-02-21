import pytest
import sys

# Add the directory containing calculate.py to the Python path
sys.path.insert(0, './')

# Run pytest on the test file
pytest.main([sys.argv[1]])
