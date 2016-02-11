#include <stdio.h>
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

    int next_char;

    while ((next_char = fgetc(infile)) != EOF) {
        fputc(next_char ^ (key[counter % key_len]), outfile);
    }

    fclose(infile);
    fclose(outfile);
}
