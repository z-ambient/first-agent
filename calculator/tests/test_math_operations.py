
def test_multiplication():
    assert 2 * 3 == 6
    assert 5 * -2 == -10
    assert 0 * 100 == 0

def test_division():
    assert 10 / 2 == 5
    assert 7 / 2 == 3.5
    assert -10 / 5 == -2
    try:
        10 / 0
        assert False, "Division by zero should raise an error"
    except ZeroDivisionError:
        assert True

def test_addition():
    assert 2 + 3 == 5
    assert -1 + 1 == 0
    assert 10 + (-5) == 5

def test_subtraction():
    assert 5 - 2 == 3
    assert 2 - 5 == -3
    assert 0 - 10 == -10
    assert -5 - (-3) == -2

# A simple way to run these tests if not using a test runner like pytest
if __name__ == "__main__":
    print("Running tests...")
    try:
        test_multiplication()
        print("Multiplication tests passed!")
    except AssertionError as e:
        print(f"Multiplication tests failed: {e}")
    
    try:
        test_division()
        print("Division tests passed!")
    except AssertionError as e:
        print(f"Division tests failed: {e}")
    
    try:
        test_addition()
        print("Addition tests passed!")
    except AssertionError as e:
        print(f"Addition tests failed: {e}")
    
    try:
        test_subtraction()
        print("Subtraction tests passed!")
    except AssertionError as e:
        print(f"Subtraction tests failed: {e}")
    print("All tests completed.")
