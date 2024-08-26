

#define min(a, b) ((a>b)? (a): (b))

#define BYTE_INDEX_MASK 0x7
#define BYTE_INDEX_BITS 3

#define IO_CHUNK 4096

int export_flags(const char* filename, void* data, int size);

typedef enum {TRUE=-1, FALSE=0} bool;

