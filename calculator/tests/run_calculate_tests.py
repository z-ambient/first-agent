import sys
sys.path.insert(0, './')
from calculate import divide

def run_tests():
    print("Running tests for calculate.py...")

    # Test case 1: divide positive numbers
    try:
        result = divide(10, 2)
        assert result == 5
        print("Test 'divide positive numbers' PASSED")
    except AssertionError:
        print(f"Test 'divide positive numbers' FAILED: Expected 5, got {result}")
    except Exception as e:
        print(f"Test 'divide positive numbers' FAILED with error: {e}")

    # Test case 2: divide by zero
    try:
        divide(10, 0)
        print("Test 'divide by zero' FAILED: Expected ValueError, but no exception was raised.")
    except ValueError as e:
        assert str(e) == "Cannot divide by zero"
        print("Test 'divide by zero' PASSED")
    except Exception as e:
        print(f"Test 'divide by zero' FAILED with unexpected error: {e}")

    # Test case 3: divide negative numbers
    try:
        result = divide(-10, 2)
        assert result == -5
        print("Test 'divide negative numbers' PASSED")
    except AssertionError:
        print(f"Test 'divide negative numbers' FAILED: Expected -5, got {result}")
    except Exception as e:
        print(f"Test 'divide negative numbers' FAILED with error: {e}")

    # Test case 4: divide float numbers
    try:
        result = divide(10.0, 3.0)
        assert abs(result - 3.333333) < 0.00001 # Using a small tolerance for float comparison
        print("Test 'divide float numbers' PASSED")
    except AssertionError:
        print(f"Test 'divide float numbers' FAILED: Expected approximately 3.33333, got {result}")
    except Exception as e:
        print(f"Test 'divide float numbers' FAILED with error: {e}")

    # Test case 5: divide by negative number
    try:
        result = divide(10, -2)
        assert result == -5
        print("Test 'divide by negative number' PASSED")
    except AssertionError:
        print(f"Test 'divide by negative number' FAILED: Expected -5, got {result}")
    except Exception as e:
        print(f"Test 'divide by negative number' FAILED with error: {e}")

if __name__ == "__main__":
    run_tests()
