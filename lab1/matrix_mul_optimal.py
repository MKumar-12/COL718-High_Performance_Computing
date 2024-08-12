# Strassen's MM - T.C. O(n^2.81)        S.C. O(n^2)
# {Requires input matrix to be of order 2^m}


import numpy as np
import time

# Strassen's matrix multiplication
def strassen_multiply(A, B):
    # Base case when size of matrices is 1x1
    if len(A) == 1:
        return A * B

    # Splitting the matrices into quadrants
    mid = len(A) // 2
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]

    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]

    # Calculating the seven products using Strassen's formula
    M1 = strassen_multiply(A11 + A22, B11 + B22)
    M2 = strassen_multiply(A21 + A22, B11)
    M3 = strassen_multiply(A11, B12 - B22)
    M4 = strassen_multiply(A22, B21 - B11)
    M5 = strassen_multiply(A11 + A12, B22)
    M6 = strassen_multiply(A21 - A11, B11 + B12)
    M7 = strassen_multiply(A12 - A22, B21 + B22)

    # Calculating the values of the four quadrants of the final matrix
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Combining the four quadrants into a single matrix
    C = np.vstack((np.hstack((C11, C12)), np.hstack((C21, C22))))

    return C


# Create a large random matrix using numpy
def generate_matrix_np(size):
    return np.random.randint(0, 100, size=(size, size))


# Format time function
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"

    
# Usage
if __name__ == '__main__':
    print(f"[LOG] Starting execution.")
    print()

    # Generating two random matrices (must be a power of 2 for Strassen's algorithm)
    A = generate_matrix_np(1024)
    B = generate_matrix_np(1024)

    start_time = time.time()
    result = strassen_multiply(A, B)
    end_time = time.time()

    # Print partial result
    print("Resulting matrix (first few rows and columns): ")
    for row in result[:5, :5]:
        print(row)

    execution_time = end_time - start_time
    formatted_time = format_time(execution_time)
    print()
    print(f"[LOG] Execution completed in {formatted_time}.")


# WSL:
# python3 matrix_mul_optimal.py