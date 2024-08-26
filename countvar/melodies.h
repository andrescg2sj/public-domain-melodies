#ifndef _MELODIES_H_
#define _MELODIES_H_

#define MELODY_NODES 8
#define NOTE_BITS 3
#define NOTE_MASK 0x7
#define MELODY_BYTES 3
#define MELODY_BITS (MELODY_BYTES*8)
#define ALL_MELODIES (1<<24)
#define MEM_SIZE (ALL_MELODIES/8)

typedef unsigned char byte;

typedef unsigned int melody;


#endif
