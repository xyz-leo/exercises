/*
Exercise 1-18. Write a program to remove trailing blanks and tabs from each line of input,
and to delete entirely blank lines. 
*/
#include <stdio.h>
#define ARRAY_SIZE 1000

int get_line(char s[], int lim);
void strip_line(char s[]);

int main() {
    char line[ARRAY_SIZE];
    int len;
    len = 0;

    while ((len = get_line(line, ARRAY_SIZE)) > 0) {
        strip_line(line);
        if (line[0] != '\0')
            printf("%s\n", line);
    }

    return 0;
}

int get_line(char s[], int lim) {
    int c, i, j;

    j = 0;

    for (i = 0; (c = getchar()) != EOF && c != '\n'; i++) {
        if (j < lim - 1) {
            s[j] = c;
            j++;
        }
    }

    if (c == '\n') {
        if (j < lim - 1) {
            s[j] = c;
            j++;
        }
        i++;
    }

    if (j < lim)
        s[j] = '\0';
    else
        s[lim - 1] = '\0';

    return i;
}

void strip_line(char s[]) {
    int i;
    i = 0;

    if (s[i] == '\0')
        return;
    while (s[i] != '\0') {
        i++;
    }
    i--; // decrementing i because last element was \0

    while (i >= 0 && (s[i] == ' ' || s[i] == '\t' || s[i] == '\n')) {
        i--;
    }
    s[i + 1] = '\0'; 
}
