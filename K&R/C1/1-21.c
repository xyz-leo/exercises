/*
Exercise 1-21. Write a program entab that replaces strings of blanks by the minimum
number of tabs and blanks to achieve the same spacing. Use the same tab stops as for detab.
When either a tab or a single blank would suffice to reach a tab stop, which should be given
preference?
*/
#include <stdio.h>
#define TABSTOP 8

int col = 0;

void entab(int blanks);

int main(void) {
    int c;
    int blanks = 0;

    while ((c = getchar()) != EOF) {
        if (c == ' ') {
            blanks++;
        } else {
            entab(blanks);
            blanks = 0;
            putchar(c);

            if (c == '\n')
                col = 0;
            else
                col++;
        }
    }
    entab(blanks);
    return 0;
}

void entab(int blanks) {
    int spaces_to_tab;

    while (blanks > 0) {
        spaces_to_tab = TABSTOP - (col % TABSTOP);

        if (spaces_to_tab <= blanks && spaces_to_tab > 1) {
            putchar('\t');
            blanks -= spaces_to_tab;
            col += spaces_to_tab;
        } else {
            putchar(' ');
            blanks--;
            col++;
        }
    }
}
