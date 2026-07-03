/* Exercise 2-2. Write a loop equivalent to the for loop above without using && or ||*/

/* The break statement was intentionally not used, since it has not yet been introduced in the book. Instead, I tried to emulate its behavior. */

#include <stdio.h>

#define MAXLINE 1000

int get_line(char line[], int maxline);

int main(void)
{
    char line[MAXLINE];

    while ((get_line(line, MAXLINE)) > 0)
        printf("%s", line);

    return 0;
}

int get_line(char line[], int maxline)
{
    int c, i, break_;

    break_ = 1;
    for (i = 0; break_ == 1; ) {
        c = getchar();
        if (c == EOF)
            break_ = 0;
        else if (c == '\n') {
            if (i < maxline - 1) {
                line[i] = c;
                ++i;
            }
            break_ = 0;
        } else {
            if (i < maxline - 1) {
                line[i] = c;
                ++i;
            }
        }
    }
    line[i] = '\0';
    return i;
}

