/*Exercise 2-4. Write an alternative version of squeeze(s1,s2) that deletes each character in
s1 that matches any character in the string s2.*/

/* At this point in the book, O(n x m) is acceptable */

#include <stdio.h>
#define ARR_SIZE 5

void squeeze(char s[], char s2[]);
int in_string(char c, char s2[]);

int main() {
    char s1[ARR_SIZE], s2[ARR_SIZE];
    int i;
    int j = 0;

    for (i = 0; i < 8; i++) {
        if (i < ARR_SIZE - 1)
            s1[i] = i + '0';        /* only write s1 for the first 4 */
        if (i % 2 != 0)
            s2[j++] = i + '0';      /* write s2 only on odd i */
    }
    s1[ARR_SIZE - 1] = '\0';    /* s1 always ends up with exactly 4 chars, so this is fixed */
    s2[j] = '\0';    /* j tracks how many chars s2 actually got */

    printf("Delete matching characters between two strings\ns1: [%s]\ts2: [%s]\n", s1, s2);

    squeeze(s1, s2);

    printf("new s1: [%s]\n", s1);

    return 0;
}

void squeeze(char s[], char s2[])
{
    int i, j;
    for (i = j = 0; s[i] != '\0'; i++) {
        if (in_string(s[i], s2) == 0) {
            s[j++] = s[i];
        }
    }
    s[j] = '\0';
}

int in_string(char c, char s[])
{
    /* return 1 if c appears anywhere in s2, else return 0 */
    int i;
    for (i = 0; s[i] != '\0'; i++) {
        if (s[i] == c) {
            return 1;
        }
    }
    return 0;
}
