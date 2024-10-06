// Rearranged Nested Loops MM           {modifies the mem. access pattern}
//T.C. O(n^3)
//S.C. O(n^2)

#include<stdio.h>
#define N 75


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

    for(int i = 0; i < N; i++) {
        for(int k = 0; k < N; k++) {        // iterate over elements in selected R & C
            for(int j = 0; j < N; j++)                  // reordered loop
                res[i][j] += A[i][k] * B[k][j];         // accumulate partial sums
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

    
    // Perform matrix multiplication
    int res[N][N];
    multiplyMatrices(A, B, res);
    // printMatrix(res);

    printf("Rearranged nested loops MM completed!\n");
    return 0;
}