/*
Exercise 1-17. Write a program to print all input lines that are longer than 80 characters.
*/
#include <stdio.h>
#define MINIMUM 80      // min input length
#define ARRAY_SIZE 1000 // array size

int get_line(char line[], int lim);


int main() {
    int len;
    char line[ARRAY_SIZE];

    while ((len = get_line(line, ARRAY_SIZE)) > 0) {
        if (len >= MINIMUM)
            printf("%s\n", line);
    }
    
    return 0;
}


int get_line(char s[], int lim) {
    int i, c;

    for (i = 0; (c = getchar()) != EOF && c != '\n'; i++) {
        if (i < lim - 1)
            s[i] = c;
    }
    if (c == '\n') {
        if (i < lim - 1) {
            s[i] = c;
        }
        i++;
    }
    if (i < lim - 1)
        s[i] = '\0';
    else
        s[lim - 1] = '\0';
    return i;
}
