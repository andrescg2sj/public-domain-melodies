
#include <stdio.h>
#include <unistd.h>
#include "util.h"

/**
 * @return bytes_written
 */
int export_flags(const char* filename, void* data, int size)
{

  FILE* f;
  int bytes_written = 0;
  unsigned char* dst = data;
  
  f = fopen(filename, "wb");
  if(f == NULL) {
    return 0;
  }

  while(bytes_written < size) {
    int block_size = min(IO_CHUNK, size-bytes_written);
    if(fwrite(dst, block_size, 1, f) > 0)
      bytes_written += block_size;
      dst += block_size;
  }

    return bytes_written;
}

