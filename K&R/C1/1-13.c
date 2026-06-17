/*
Exercise 1-13. Write a program to print a histogram of the lengths of words in its input. It is
easy to draw the histogram with the bars horizontal; a vertical orientation is more challenging.
*/
#include <stdio.h>
#define IN 1            // inside word
#define OUT 0           // outside word
#define MAX_WORD_LEN 10 // max length of the input

int main () {
    // c: current character. i and j: loop counters. nc: current word length
    int c, i, j, nc, state; 

    nc = i = j = 0;

    int histogram[MAX_WORD_LEN];
    
    // initialize array elements to 0
    for (i = 0; i < MAX_WORD_LEN; i++)
        histogram[i] = 0;

    state = OUT;

    while ((c = getchar()) != EOF) {
        if (c != '\n' && c != '\t' && c != ' ') {
            state = IN;
            nc++;
        }
        if (c == '\n' || c == '\t' || c == ' ') {
            if (state == IN) {
                if (nc > MAX_WORD_LEN) {
                    printf("max word length = %d\n", MAX_WORD_LEN);
                }
                else
                    histogram[nc - 1]++; // word length 1 maps to index 0
            }
            state = OUT;
            nc = 0; // reset nc when outside word
        }
    }
    
    // handle a word that ends directly at EOF
    if (state == IN) {
        if (nc > MAX_WORD_LEN) {
            printf("max word length = %d\n", MAX_WORD_LEN);
        }
        else {
            printf("\n");
            histogram[nc - 1]++;
        }
    }

    // loops for printing the histogram
    for (i = 0; i < MAX_WORD_LEN; i++) {
        printf("%3d | ", i + 1);
        // print '*' repeatedly because C has no string repetition operator
        for (j = 0; j < histogram[i]; j++)
            printf("*");
        printf("\n");
    }
    return 0;
}
