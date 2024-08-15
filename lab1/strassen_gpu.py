# Strassen's MM - T.C. O(n^2.81)        S.C. O(n^2)
# {using GPU}
# {Requires input matrix to be of order 2^m}


import cupy as cp
import time

# Strassen's matrix multiplication on GPU using CuPy
def strassen_multiply_gpu(A, B, threshold=64):
    n = A.shape[0]
    if n <= threshold:
        return cp.dot(A, B)  # Use CuPy's optimized GPU matrix multiplication

    # Splitting the matrices into quadrants
    mid = n // 2
    A11 = A[:mid, :mid]
    A12 = A[:mid, mid:]
    A21 = A[mid:, :mid]
    A22 = A[mid:, mid:]

    B11 = B[:mid, :mid]
    B12 = B[:mid, mid:]
    B21 = B[mid:, :mid]
    B22 = B[mid:, mid:]

    # Calculating the seven products using Strassen's formula
    M1 = strassen_multiply_gpu(A11 + A22, B11 + B22, threshold)
    M2 = strassen_multiply_gpu(A21 + A22, B11, threshold)
    M3 = strassen_multiply_gpu(A11, B12 - B22, threshold)
    M4 = strassen_multiply_gpu(A22, B21 - B11, threshold)
    M5 = strassen_multiply_gpu(A11 + A12, B22, threshold)
    M6 = strassen_multiply_gpu(A21 - A11, B11 + B12, threshold)
    M7 = strassen_multiply_gpu(A12 - A22, B21 + B22, threshold)

    # Calculating the values of the four quadrants of the final matrix
    C11 = M1 + M4 - M5 + M7
    C12 = M3 + M5
    C21 = M2 + M4
    C22 = M1 - M2 + M3 + M6

    # Combining the four quadrants into a single matrix
    C = cp.vstack((cp.hstack((C11, C12)), cp.hstack((C21, C22))))

    return C


# Create a large random matrix on GPU using CuPy
def generate_matrix_gpu(size):
    return cp.random.randint(0, 100, size=(size, size))


# Format time function
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours}h {minutes}m {seconds}s"


# Usage
if __name__ == '__main__':
    print(f"[LOG] Starting execution on GPU.")
    print()

    # Generating two 1024x1024 random matrices on GPU
    A = generate_matrix_gpu(1024)
    B = generate_matrix_gpu(1024)

    start_time = time.time()
    result = strassen_multiply_gpu(A, B)
    end_time = time.time()

    # Move result back to CPU and print partial result
    result_cpu = cp.asnumpy(result)
    print("Resulting matrix (first few rows and columns): ")
    for row in result_cpu[:5, :5]:
        print(row)

    execution_time = end_time - start_time
    formatted_time = format_time(execution_time)
    print()
    print(f"[LOG] Execution completed in {formatted_time}.")


# WSL
# python3 strassen_gpu.py