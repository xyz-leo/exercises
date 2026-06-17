/*
Exercise 1-14. Write a program to print a histogram of the frequencies of different characters
in its input 
*/
#include <stdio.h>
#define ASCII_SIZE 128

int main() {
    int c, i, j;
    int histogram[ASCII_SIZE];
    
    for (i = 0; i < ASCII_SIZE; i++)
        histogram[i] = 0;

    while ((c = getchar()) != EOF) {
        if (c < 0 || c >= ASCII_SIZE) {
            printf("c > ascii_size");
            continue;
        }
        histogram[c]++;
    }

    for (i = 0; i < ASCII_SIZE; i++) {
        if (histogram[i] != 0) {
            if (i == '\n')
                printf("%5s | ", "\\n");
            else if (i == '\t')
                printf("%5s | ", "\\t");
            else if (i == ' ')
                printf("%5s | ", "SPACE");
            else
                printf("%5c | ", i);
            for (j = 0; j < histogram[i]; j++)
                printf("*");
            printf("\n");
        }
    }

    return 0;
}
