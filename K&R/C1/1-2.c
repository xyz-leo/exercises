#include <stdio.h>
// exercise just to trigger a warning

int main() {
    printf("hello, world\c");
}

// warning:
//main.c: In function ‘main’:
//main.c:5:28: warning: unknown escape sequence: ‘\c’
//    5 |     printf("hello, world\c");
//      |
