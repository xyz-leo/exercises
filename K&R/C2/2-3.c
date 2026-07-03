/*Exercise 2-3. Write a function htoi(s), which converts a string of hexadecimal digits
(including an optional 0x or 0X) into its equivalent integer value. The allowable digits are 0
through 9, a through f, and A through F.*/

#include <stdio.h>

int htoi(char s[]);

int main() {
    printf("%d\n", htoi("0x1A3"));   /* should print 419 */
    printf("%d\n", htoi("ff"));      /* should print 255 */
    printf("%d\n", htoi("0xFF"));    /* should print 255 */
    return 0;
}

int htoi(char s[]) {
    int i;
    int n = 0;

    if (s[0] == '0' && (s[1] == 'x' || s[1] == 'X')) {
        i = 2;
    }
    else {
        i = 0;
    }

    for (; (s[i] >= '0' && s[i] <= '9') || (s[i] >= 'a' && s[i] <= 'f') || (s[i] >= 'A' && s[i] <= 'F'); i++) {
        if (s[i] >= '0' && s[i] <= '9') {
            n = n * 16 + (s[i] - '0');
        }

        else if (s[i] >= 'a' && s[i] <= 'f') {
            n = n * 16 + (s[i] - 'a' + 10);
        }

        else if (s[i] >= 'A' && s[i] <= 'F') {
            n = n * 16 + (s[i] - 'A' + 10);
        }
    }
    return n;
}
