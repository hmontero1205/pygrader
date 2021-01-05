#include <stdio.h>
#include <stdlib.h>

void swap(int *p, int *q) {
    int temp = *p;
    *p = *q;
    *q = temp;
}

int main(int argc, char **argv) {
    int x = atoi(argv[1]);
    int y = atoi(argv[2]);

    printf("Before: %d %d\n", x, y);
    swap(&x, &y);
    printf("After: %d %d\n", x, y);
}
