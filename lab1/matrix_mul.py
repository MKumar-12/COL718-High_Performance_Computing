# Naive MM - T.C. O(n^3)        S.C. O(n^2)


import random
import time

# Multiply 2 matrices fn.
def matrix_multiply(A, B):
    # rows and columns for matrices A and B
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    # Initializing the result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]

    # Matrix multiplication
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i][j] += A[i][k] * B[k][j]

    return result


# Create a large random matrix
def generate_matrix(size):
    return [[random.randint(0, 100) for _ in range(size)] for _ in range(size)]


# Format time fn.
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"


# Usage
if __name__ == '__main__':
    print(f"[LOG] Starting execution.")
    print()

    # Generating two random matrices
    A = generate_matrix(1024)
    B = generate_matrix(1024)

    start_time = time.time()
    result = matrix_multiply(A, B)
    end_time = time.time()

    # Printing partial result
    print("Resulting matrix (first few rows and columns): ")
    for row in result[:5]:
        print(row[:5])

    execution_time = end_time - start_time
    formatted_time = format_time(execution_time)
    print()
    print(f"[LOG] Execution completed in {formatted_time}.")


# WSL:
# python3 matrix_mul.py