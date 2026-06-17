#include <stdio.h>

int main() {
    float celsius, fahr;
    float lower, upper, step;

    lower = 0;
    upper = 300;
    step = 20;

    celsius = lower;
    printf("Celsius\tFahr\n");
    while (celsius <= upper) {
        fahr = (celsius * 1.8) + 32;
        printf("%3.0f\t%3.0f\n", celsius, fahr);
        celsius += step;
    }

    return 0;
}
