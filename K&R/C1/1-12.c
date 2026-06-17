#include <stdio.h>
#define IN 1
#define OUT 0

// Exercise 1-12. Write a program that prints its input one word per line.

int main() {
    int c, state;
    state = OUT;

    while ((c = getchar()) != EOF) {
        if (c != ' ' && c != '\n' && c != '\t') {
            putchar(c);
            state = IN;
        }
        if (c == ' ' || c == '\n' || c == '\t') {
            if (state == IN) {
                printf("\n");
            state = OUT;
            }
        }
    }
    return 0;
}
