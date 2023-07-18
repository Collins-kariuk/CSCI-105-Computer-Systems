#include <stdio.h>
#include <stdlib.h>

typedef unsigned char byte;

int main(int argc, char ** argv){

    //Collaborators: Collins Kariuki, Michael Cho, Max Linden

    int is_ok = EXIT_FAILURE;

    char* file_name = "./image.blob";

    FILE* file = fopen(file_name, "r");
    if(!file) {
        perror("File opening failed");
        return is_ok;
    }
    
    int width;
    int height;

    int file_scan = fscanf(file,"CS105 %d %d", &width, &height);

    if (file_scan == EOF)
    {
        printf("Could not read PPM file header.\n");
        return EXIT_FAILURE;
    }

    int num_pixels = width * height;
    // A byte is 256, for all rgb values 0 - 255
    byte* red = malloc(num_pixels * sizeof(byte));
    byte* green = malloc(num_pixels * sizeof(byte));
    byte* blue = malloc(num_pixels * sizeof(byte));

    size_t read_file_red = fread(red, sizeof(byte), num_pixels, file);
    size_t read_file_green = fread(green, sizeof(byte), num_pixels, file);
    size_t read_file_blue = fread(blue, sizeof(byte), num_pixels, file);

    fclose(file);


    char* image_name = "./image.ppm";

    FILE* image = fopen(image_name, "wb");

    int image_print = fprintf(image, "P6 %d %d %d\n", width, height, 255);
    if (image_print < 0)
    {
        printf("Could not write to file.\n");
        return EXIT_FAILURE;
    }

    for(int i = 0; i < num_pixels; i++){
        fputc(*(red + i), image);
        fputc(*(green + i), image);
        fputc(*(blue + i), image);
    }
    
    fclose(image);

    free(red);
    free(green);
    free(blue);

    printf("Made the ppm image from blob\n");
}