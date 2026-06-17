/*
Exercise 1-22. Write a program to ``fold'' long input lines into two or more shorter lines after
the last non-blank character that occurs before the n-th column of input. Make sure your
program does something intelligent with very long lines, and if there are no blanks or tabs
before the specified column.
*/

#include <stdio.h>
#define MAXLINE 1000    // Array max size
#define FOLDCOL 10      // Fold column (\n)

int get_line(char line[], int maxline);
void fold(char line[]);
void insert_char(char line[], int pos, int len, char c);
int string_length(char s[]);

int main(void) {
    char line[MAXLINE];
    int i;
    int len;

    while ((len = get_line(line, MAXLINE)) > 0) {
        fold(line);
        printf("\n%s\n", line);

    }
    return 0;
}

int get_line(char line[], int maxline) {
    int c;
    int i;

    for (i = 0; i < maxline - 1
         && (c = getchar()) != EOF
         && c != '\n';
         i++) {

        line[i] = c;
    }

    if (c == '\n') {
        line[i] = c;
        i++;
    }

    line[i] = '\0';

    return i;
}

void fold(char line[]) {
    int i;
    int col = 0;
    int last_blank = -1;

    for (i = 0; line[i] != '\0'; i++) {
        if (line[i] == '\n') {
            col = 0;
            last_blank = -1;
            continue;
        }

        if (line[i] == ' ') {
            last_blank = i;
        }

        if (col >= FOLDCOL) {
            if (last_blank != -1) {
                line[last_blank] = '\n';
                col = i - last_blank - 1;
                last_blank = -1;
            }
            else {
                insert_char(line, i, string_length(line), '\n');
                col = 0;
                last_blank = -1;
                i--;
            }
        }

        col++;
    }
}

void insert_char(char line[], int pos, int len, char c) {
    int j;

    for (j = len; j >= pos; j--)
        line[j + 1] = line[j];

    line[pos] = c;
}

int string_length(char s[]) {
    int i = 0;

    while (s[i] != '\0')
        i++;

    return i;
}
