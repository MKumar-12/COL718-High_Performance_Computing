// Blocked MM                           {better cache utilization}
//T.C. O(n^3)
//S.C. O(n^2)

#include<stdio.h>
#define N 75
#define BLOCK_SIZE 15

// Print small segment of MM result
// void printMatrix(int matrix[N][N]) {
//     for(int i = 0; i < 5; i++) {
//         for(int j = 0; j < 5; j++) 
//             printf("%d ", matrix[i][j]);

//         printf("\n");
//     }
// }


// Function to multiply matrices
void multiplyMatrices(int A[N][N], int B[N][N], int res[N][N]) {
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++) 
            res[i][j] = 0;              // Initialize value to 0
    }

    // Blocked Matrix multiplication
    for(int ii = 0; ii < N; ii += BLOCK_SIZE) {
        for(int jj = 0; jj < N; jj += BLOCK_SIZE) {
            for(int kk = 0; kk < N; kk += BLOCK_SIZE) {
                for(int i = ii; i < ii + BLOCK_SIZE && i < N; i++) {
                    for(int j = jj; j < jj + BLOCK_SIZE && j < N; j++) {
                        for(int k = kk; k < kk + BLOCK_SIZE && k < N; k++) 
                            res[i][j] += A[i][k] * B[k][j];
                    }
                }
            }
        }
    }
}


int main()
{
    int A[N][N], B[N][N];
    
    // matrix initialization
    for(int i = 0; i < N; i++) {
        for(int j = 0; j < N; j++) {
            if(i % 2 == 0) {
                A[i][j] = (j % 75) + 1;             // Even row: A values ranges from 1 to 75
                B[i][j] = (j % 75) + 76;            //           B values ranges from 76 to 150
            }
            else {
                A[i][j] = (j % 75) + 76;            // Odd row:  A values ranges from 76 to 150
                B[i][j] = (j % 75) + 1;             //           B values ranges from 1 to 75
            }
        }
    }

    
    // Perform blocked matrix multiplication
    int res[N][N];
    multiplyMatrices(A, B, res);
    // printMatrix(res);

    printf("Blocked MM completed!\n");
    return 0;
}