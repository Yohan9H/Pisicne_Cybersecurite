#include <stdio.h>
#include <string.h>

int main(void)
{
    char input[128];

    printf("Please enter key: ");
    if (scanf("%127s", input) != 1) {
        printf("No input!\n");
        return 1;
    }

    const char expected[] = "__stack_check";

    if (strcmp(input, expected) == 0) {
        printf("Good job.\n");
    } else {
        printf("Nope.\n");
    }

    return 0;
}
