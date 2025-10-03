#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(void)
{
    char input[64];
    char decoded[16];
    int in_index;
    int out_index;

    printf("Please enter key: ");
    if (scanf("%63s", input) != 1) {
        printf("Nope.\n");
        return 1;
    }

    if (input[0] != '0' || input[1] != '0') {
        printf("Nope.\n");
        return 1;
    }

    decoded[0] = 'd';
    out_index = 1;

    in_index = 2;

    while (in_index + 2 < (int)strlen(input) && out_index < 8) {
        char triplet[4];
        int code;

        triplet[0] = input[in_index];
        triplet[1] = input[in_index + 1];
        triplet[2] = input[in_index + 2];
        triplet[3] = '\0';

        code = atoi(triplet);

        decoded[out_index] = (char)code;

        in_index += 3;
        out_index++;
    }

    decoded[out_index] = '\0';

    if (strcmp(decoded, "delabere") == 0) {
        printf("Good Job.\n");
    } else {
        printf("Nope.\n");
    }

    return 0;
}
