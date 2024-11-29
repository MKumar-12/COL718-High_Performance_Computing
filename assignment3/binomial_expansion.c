// Function to compute the binomial expansion (a + x) ^ n

#include <stdio.h>
#include <math.h>
#include<stdint.h>

#define ll long long 

ll fact(int n) {
    ll res = 1;
    for(int i = 2; i <= n; i++)
        res *= i;

    return res;
}

ll nCr(int n, int r) {
    if(r > n - r) 
        r = n - r;          // Use symmetry property nCr = nC(n-r)

    return fact(n) / (fact(r) * fact(n - r));
}

// ll compute_expansion(int a, int x, int n) {
//     ll res = 0;
//     for(int i = 0; i <= n; i++) 
//         res += nCr(n, i) * pow(a, i) * pow(x, n - i); 

//     return res;
// }


int main() {
    int a = 10, n = 8, r = 5;
    
    // printf("Value for expansion (%d + %d)^%d :    %lld", a, x, n, compute_expansion(a, x, n));
    uint32_t value = fact(a);
    uint32_t comb = nCr(n, r);

    printf("\nValue for expansion of %d!   :    %u", a, value);
    printf("\nValue for expansion of %dn%d :    %u", n, r, comb);
    return 0;
}