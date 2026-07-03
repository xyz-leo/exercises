/*
Exercise 2-1. Write a program to determine the ranges of char, short, int, and long
variables, both signed and unsigned, by printing appropriate values from standard headers
and by direct computation. Harder if you compute them: determine the ranges of the various
floating-point types.
*/

#include <stdio.h>
#include <limits.h>

int ranges(void);

int main(void) {
    int i;

    // Using limits.h
    printf("Signed values range, using limits.h\nINT_MAX: %d\tINT_MIN: %d\nCHAR_MAX %d\tCHAR_MIN %d\nSHRT_MAX %d\tSHRT_MIN %d\nLONG_MAX %ld\tLONG_MIN %ld\n\n", INT_MAX, INT_MIN, CHAR_MAX, CHAR_MIN, SHRT_MAX, SHRT_MIN, LONG_MAX, LONG_MIN);
    printf("Unsigned values range, using limits.h (min always 0)\nUINT_MAX: %u\nUCHAR_MAX %d\nUSHRT_MAX %d\nULONG_MAX %lu\n\n", UINT_MAX, UCHAR_MAX, USHRT_MAX, ULONG_MAX);

    // Direct computation
    ranges();

    return 0;
}

int ranges(void) {
    printf("Signed ranges by computation\n");
    // char
    char c = 1, lc = 0;
    while (c > 0) { lc = c; c *= 2; }
    printf("CHAR_MAX: %d\n", lc * 2 - 1);

    // short
    short s = 1, ls = 0;
    while (s > 0) { ls = s; s *= 2; }
    printf("SHRT_MAX: %d\n", ls * 2 - 1);

    // int
    int n = 1, ln = 0;
    while (n > 0) { ln = n; n *= 2; }
    printf("INT_MAX: %d\n", ln * 2 - 1);

    // long
    long l = 1, ll = 0;
    while (l > 0) { ll = l; l *= 2; }
    printf("LONG_MAX: %ld\n", ll * 2 - 1);

    printf("\nUnsigned ranges by computation\n");

    // unsigned char
    unsigned char uc = 1, ulc = 0;
    while (uc != 0) { ulc = uc; uc *= 2; }
    printf("UCHAR_MAX: %d\n", ulc * 2 - 1);

    // unsigned short
    unsigned short us = 1, uls = 0;
    while (us != 0) { uls = us; us *= 2; }
    printf("USHRT_MAX: %d\n", uls * 2 - 1);

    // unsigned int
    unsigned int un = 1, uln = 0;
    while (un != 0) { uln = un; un *= 2; }
    printf("UINT_MAX: %u\n", uln * 2 - 1);

    // unsigned long
    unsigned long ul = 1, ull = 0;
    while (ul != 0) { ull = ul; ul *= 2; }
    printf("ULONG_MAX: %lu\n", ull * 2 - 1);
}
