#include <stdio.h>

int main() {
    int c, past_c;

    past_c = 0;

    for (; (c = getchar()) != EOF; ) {
        if (c == ' ') {
            if (past_c == ' ') {
                continue;
            }
        }
        putchar(c);
        past_c = c;
    }

    return 0;
}

/* if (!(c == ' ' && past_c == ' ')) {
    putchar(c);
}
*/
