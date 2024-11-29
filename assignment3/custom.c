#include<stdio.h>
#include<stdint.h>

int main() {
    uint32_t a = 10, b = 0, value = 0;
    uint32_t n = 8, r = 5, comb = 0;

    asm volatile("fact %0, %1, %2\n"
                :"=r"(value)                // output operand
                :"r"(a),"r"(b)              // input operand
                :
    );            // inline assembly ins. for factorial
    
    asm volatile("comb %0, %1, %2\n"
                :"=r"(comb)                 // output operand
                :"r"(n),"r"(r)              // input operand
                :
    );           // inline assembly ins. for combination

    printf("\nValue for expansion of %d!   :    %u", a, value);
    printf("\nValue for expansion of %dn%d :    %u", n, r, comb);
    return 0;
}