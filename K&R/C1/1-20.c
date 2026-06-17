/*
Exercise 1-20. Write a program detab that replaces tabs in the input with the proper number
of blanks to space to the next tab stop. Assume a fixed set of tab stops, say every n columns.
Should n be a variable or a symbolic parameter?
*/

// n should be a symbolic parameter, since tabstop is a fixed value
#include <stdio.h>
#define TABSTOP 8

int col;

void detab(void);

int main() {
    extern int col;
    int c;

    col = 0;
        
    while ((c = getchar()) != EOF) {
        if (c == '\t') {
            detab();
        }
        else if (c == '\n') {
            col = 0;
            putchar(c);
        }
        else {
            col++;
            putchar(c);
        }
            
    }
    return 0;
}

void detab(void) {
    int spaces, i;
    spaces = TABSTOP - (col % TABSTOP);

    for (i = 0; i < spaces; i++)
        putchar(' ');
    col += spaces;
}
