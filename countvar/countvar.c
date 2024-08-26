/*
 * This program counts how many combinations are present in a given file.
 *
 */

#include <stdio.h>
#include <unistd.h>
#include <malloc.h>
#include <stdlib.h>
#include <memory.h>
#include "melodies.h"
#include "util.h"
#include <bits/getopt_core.h>


byte *melodies;

bool verbose = FALSE;

void set_bit(byte* position, int bit_index)
{
  byte bitmask = 1 << bit_index;
  *position |= bitmask;
}


void flag_melody(int index)
{
  int bit_index = index & BYTE_INDEX_MASK;
  int address = index >> BYTE_INDEX_BITS;
  //printf("address: %d, bit: %d\n", address, bit_index);
  set_bit(melodies+address, bit_index);
  
}

byte check_bit(byte *position, int bit_index)
{
  return  (*position >> bit_index) & 1;
}

byte check_melody(int index)
{
  int bit_index = index & BYTE_INDEX_MASK;
  int address = index >> BYTE_INDEX_BITS;
  return check_bit(melodies+address,bit_index);
}


long get_file_size(FILE* f)
{
  fseek(f, 0L, SEEK_END);
  return ftell(f);
}

void check_file(const char* filename)
{
  FILE* f;
  int count = 0;
  int data = 0;
  long steps = 0;
  long file_size = 0;
  long read_bytes = 0;

  f = fopen(filename,"rb");
  if(f == NULL) {
    printf("Could not open file: %s\n", filename);
    return;
  }
  file_size = get_file_size(f);
  
  
  fseek(f, 0L, SEEK_SET);
  if(verbose)
    printf("file size: %ld\r", file_size);

  //TODO: how does this work with big endian?
  count = fread(&data, MELODY_BYTES, 1, f);
  while(count > 0) {
    steps++;
    flag_melody(data);
    data = 0;
    count = fread(&data, MELODY_BYTES, 1, f);
    if((steps % 100000) == 0) {
      read_bytes = steps* MELODY_BYTES;
      if(verbose)
        printf("steps: %ld (%ld bytes)\r", steps, read_bytes);
    }
  }

  if(verbose) 
    printf("steps: %ld\n", steps);

  fclose(f);

}

int count_melodies()
{
  int count = 0;
  for(int i=0; i<ALL_MELODIES; i++) {
    count += check_melody(i);
  }
  return count;
}



int process_file(const char* filename_in, const char* filename_out)
{
    int memsize = MEM_SIZE;
  if(verbose)
    printf("allocating: %d bytes\n", memsize);
  melodies = malloc(memsize);
  if(melodies == 0) {
    printf("Could not allocate memory.\n");
    exit(1);
  }
  if(verbose)
    printf("clearing\n");
  memset(melodies, 0, memsize);

  check_file(filename_in);

  printf("variations: %d/%d\n", count_melodies(), ALL_MELODIES);

  if(filename_out) {
    export_flags(filename_out, melodies, MEM_SIZE);
  }

  free(melodies);


}

int main(int argc, char* const* argv)
{
  int opt;
  char* ifilename = NULL;
  char* ofilename = NULL;



  while ((opt = getopt (argc, (char* const*) argv, "i:o:v")) != -1)
  switch (opt)
    {
    case 'i':
      ifilename = optarg;
      break;
    case 'o':
      ofilename = optarg;
      break;
    case 'v':
      verbose = TRUE;
      break;
    default:
      abort ();
    }

  if(ifilename) {
    process_file(ifilename,ofilename);
  }
  


  exit(0);
}
