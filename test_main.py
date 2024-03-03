from main import *

## Feel free to add your own tests here.
def test_multiply():
    assert subquadratic_multiply(BinaryNumber(2), BinaryNumber(2)).decimal_val == 2*2
    assert subquadratic_multiply(BinaryNumber(13), BinaryNumber(13)).decimal_val == 13*13
    assert subquadratic_multiply(BinaryNumber(9), BinaryNumber(9)).decimal_val == 9*9
    assert subquadratic_multiply(BinaryNumber(14), BinaryNumber(16)).decimal_val == 14*16
