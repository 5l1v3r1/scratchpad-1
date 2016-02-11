#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>

int main(int argc, char *argv[]) {
    if (argc != 4) {
        printf("xor key INPUTFILE OUTPUTFILE\n");
        return 1;
    }

    char *key = argv[1];
    size_t key_len = strlen(key);
    char *filename = argv[2];
    char *outfilename = argv[3];

    FILE *infile = fopen(filename, "rb");
    FILE *outfile = fopen(outfilename, "wb");

    int64_t counter = 0;

    char *next_chars = malloc(key_len);
    char *next_chars_write = malloc(key_len);

    size_t num_chars;
    while (num_chars = fread(next_chars, 1, key_len, infile)) {
        for (size_t i = 0; i < num_chars; i++) {
            next_chars_write[i] = next_chars[i] ^ key[i];
        }

        fwrite(next_chars_write, 1, num_chars, outfile);
    }

    fclose(infile);
    fclose(outfile);
}
