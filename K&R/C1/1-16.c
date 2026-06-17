/*
 Exercise 1-16. Revise the main routine of the longest-line program so it will correctly print
the length of arbitrary long input lines, and as much as possible of the text.
*/
#include <stdio.h>
#define MAXLINE 1000

int get_line(char line[], int maxline);
void copy(char to[], char from[]);

int main() {
    int len;
    int max;
    char line[MAXLINE];
    char longest[MAXLINE];

    max = 0;

    while ((len = get_line(line, MAXLINE)) > 0)
        if (len > max) {
            max = len;
            copy(longest, line);
        }
    printf("Longest line: %s\nInput raw length: %d - Longest line limited by defined buffer size: %d\n", longest, max, MAXLINE);
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
        i++;
        if (j < lim - 1) {
            s[j] = c;
            j++;
        }
    }
    s[j] = '\0';
    return i;
}

void copy(char to[], char from[]) {
    int i;

    i = 0;

    while ((to[i] = from[i]) != '\0')
        i++;
}
