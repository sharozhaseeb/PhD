#include <stdio.h>
#define LIMIT 10

/* leading < comment + 1 */
int add(int a, int b) {
    int r = a + b; // trailing + 2
    if (r < LIMIT && a >= 1) {
        r = r - 3;
    }
    printf("a < b + 4\n");
    return r;
}

int outside(int a) {
    return a + 1 < 5 || a == 2;
}

REDUCE_ALL(foo, DTYPE0) {
    x->y = -a + b++;
    for (i = 0; i <= n; i++) x += 5;
    return z;
}
