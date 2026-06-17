/*
Exercise 1-19. Write a function reverse(s) that reverses the character string s. Use it to
write a program that reverses its input a line at a time.
*/

/* Since Chapter 1 does not introduce dynamically allocated buffers,
 * input longer than the array size is truncated.
 */
#include <stdio.h>
#define ARRAY_SIZE 1000

int get_line(char s[], int lim);
void reverse(char s[]);

int main() {
    char line[ARRAY_SIZE];
    int len;

    while ((len = get_line(line, ARRAY_SIZE)) > 0) {
        reverse(line);
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

void reverse(char s[]) {
    int i, j, tmp;
    i = j = 0;

    while (s[j] != '\0')
        j++;
    j--;

    while (j >= 0 && (s[j] == ' ' || s[j] == '\t' || s[j] == '\n')) {
        j--;
    }
    s[j + 1] = '\0'; 

    for (i = 0; i < j ; i++, j--) {
        tmp = s[i];
        s[i] = s[j];
        s[j] = tmp;
    }
}
