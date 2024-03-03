"""
CMPS 2200  Assignment 2.
See assignment-02.pdf for details.
"""
import time

class BinaryNumber:
    """ done """
    def __init__(self, n):
        self.decimal_val = n               
        self.binary_vec = list('{0:b}'.format(n)) 
        
    def __repr__(self):
        return('decimal=%d binary=%s' % (self.decimal_val, ''.join(self.binary_vec)))
    

## Implement multiplication functions here. Note that you will have to
## ensure that x, y are appropriately sized binary vectors for a
## divide and conquer approach.
def binary2int(binary_vec): 
    if len(binary_vec) == 0:
        return BinaryNumber(0)
    return BinaryNumber(int(''.join(binary_vec), 2))

def split_number(vec):
    return (binary2int(vec[:len(vec)//2]),
            binary2int(vec[len(vec)//2:]))

def bit_shift(number, n):
    # append n 0s to this number's binary string
    return binary2int(number.binary_vec + ['0'] * n)
    
def pad(x,y):
    # pad with leading 0 if x/y have different number of bits
    # e.g., [1,0] vs [1]
    if len(x) < len(y):
        x = ['0'] * (len(y)-len(x)) + x
    elif len(y) < len(x):
        y = ['0'] * (len(x)-len(y)) + y
    # pad with leading 0 if not even number of bits
    if len(x) % 2 != 0:
        x = ['0'] + x
        y = ['0'] + y
    return x,y

def subquadratic_multiply(x, y):

    xvec, yvec = pad(x.binary_vec, y.binary_vec)
    
    #x = binary2int(xvec) #unnecessary
    #y = binary2int(yvec)
    
    # Base Case -> The lengths of the vectors <= 1 
    if len(xvec) <= 1 or len(yvec) <= 1:
        return BinaryNumber(x.decimal_val * y.decimal_val)
    
    #Helper variables for length
    n = len(xvec)
    m = n // 2
    
    #Split
    x_left, x_right = split_number(x.binary_vec)
    y_left, y_right = split_number(y.binary_vec)
    
    #I was having errors before adding this line confirming none of the halves = 0
    if x_left.decimal_val == 0 or x_right.decimal_val == 0 or y_left.decimal_val == 0 or y_right.decimal_val == 0:
        return BinaryNumber(x.decimal_val * y.decimal_val)
    
    #Recursive calls 
    P1 = subquadratic_multiply(x_left, y_left)
    P2 = subquadratic_multiply(x_right, y_right)
    P3 = subquadratic_multiply(BinaryNumber(x_left.decimal_val + x_right.decimal_val), 
                             BinaryNumber(y_left.decimal_val + y_right.decimal_val))
    
    #Derived directly from the karatsuba equation
    result = BinaryNumber(bit_shift(P1, 2*m).decimal_val + bit_shift(BinaryNumber(P3.decimal_val - P1.decimal_val - P2.decimal_val), m).decimal_val + P2.decimal_val)

    return result
    




def time_multiply(x, y, f):
    start = time.time()
    f(x,y)
    return (time.time() - start)*1000

    
#We can use this to check the runtime of the algorithm
#It iterates through different bit vector sizes and runs the algo on each one
for i in range(1, 10): 
    n = 2 ** i
    x = BinaryNumber(int('1' * n, 2))
    y = BinaryNumber(int('1' * n, 2))

    time_subquadratic = time_multiply(x, y, subquadratic_multiply)

    print(f"Size: {n} bits, Algorithm Runtime: {time_subquadratic:.4f} ms")

'''
Size: 2 bits, Algorithm Runtime: 0.0401 ms
Size: 4 bits, Algorithm Runtime: 0.1130 ms
Size: 8 bits, Algorithm Runtime: 0.3510 ms
Size: 16 bits, Algorithm Runtime: 1.0371 ms
Size: 32 bits, Algorithm Runtime: 2.9781 ms
Size: 64 bits, Algorithm Runtime: 7.8890 ms
Size: 128 bits, Algorithm Runtime: 22.2561 ms
Size: 256 bits, Algorithm Runtime: 65.6819 ms
Size: 512 bits, Algorithm Runtime: 203.1801 ms 

Our algorithm is clearly running in subquadratic time, as we have 65ms for 256 bits, and 203ms for 512 bits. 
This difference would be exponentially greater if the algorithm were running in O(n^2) time
Though we can't quite measure the algorithm at O(n^1.58), this comes down to implementation/hardware. 
In our limited environment we cannot expect such precise results


Karatsuba should run at O(n ^ log_2(3)) time, that is ~ O(n^1.58)

'''