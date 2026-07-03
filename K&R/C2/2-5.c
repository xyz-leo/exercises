/*Exercise 2-5. Write the function any(s1,s2), which returns the first location in a string s1
where any character from the string s2 occurs, or -1 if s1 contains no characters from s2.
(The standard library function strpbrk does the same job but returns a pointer to the
location.)*/

#include <stdio.h>
#define ARR_SIZE 5

int any(char s1[], char s2[]);

int main() {
    char s1[ARR_SIZE], s2[ARR_SIZE];
    int i, loc;
    int j = 0;

    for (i = 0; i < 8; i++) {
        if (i < ARR_SIZE - 1)
            s1[i] = i + '0';
        if (i % 2 != 0)
            s2[j++] = i + '0';
    }
    s1[ARR_SIZE - 1] = '\0';
    s2[j] = '\0';

    printf("Location of first matching character in two strings\ns1: [%s]\ts2: [%s]\n", s1, s2);
    loc = any(s1, s2);
    printf("%d\n", loc);

    return 0;
}

int any(char s1[], char s2[])
{
    int i, j;
    for (i = 0; s1[i] != '\0'; i++) {
        for (j = 0; s2[j] != '\0'; j++) {
            if (s1[i] == s2[j])
                return i;
        }
    }
    return -1;
}
