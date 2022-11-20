#include <stdio.h>
#include <string.h>

typedef unsigned int WORD;

#define w        32             /* word size in bits                 */
#define r        12             /* number of rounds                  */
#define b        16             /* number of bytes in key            */
#define c         4             /* number  words in key = ceil(8*b/w)*/
#define t        26             /* size of table S = 2*(r+1) words   */
static WORD S[t] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};                      /* expanded key table                */
static WORD P = 0x00d220e3, Q = 0x0063438b;  /* magic constants             */
/* Rotation operators. x must be unsigned, to get logical right shift*/
#define ROTL(x,y) (((x)<<(y&(w-1))) | ((x)>>(w-(y&(w-1)))))
#define ROTR(x,y) (((x)>>(y&(w-1))) | ((x)<<(w-(y&(w-1)))))

void le(WORD *pt, WORD *ct) /* 2 WORD input pt/output ct    */
{ WORD i, A=pt[0]+S[0], B=pt[1]+S[1];
  for (i=1; i<=r; i++)
    { A = ROTL(A^B,B)+S[2*i];
      B = ROTL(B^A,A)+S[2*i+1];
    }
  ct[0] = A; ct[1] = B;
}

void de(WORD *ct, WORD *pt) /* 2 WORD input ct/output pt    */
{ WORD i, B=ct[1], A=ct[0];
  for (i=r; i>0; i--)
    { B = ROTR(B-S[2*i+1],A)^A;
      A = ROTR(A-S[2*i],B)^B;
    }
  pt[1] = B-S[1]; pt[0] = A-S[0];
}

void se(unsigned char *K) /* secret input key K[0...b-1]      */
{  WORD i, j, k, u=w/8, A, B, L[c];
   /* Initialize L, then S, then mix key into S */
   
   for (i = b - 1, L[c - 1] = 0; i != -1; i--)
   { 
		L[i/u] = (L[i/u] << 8) + K[i];
   }

   for (S[0]=P,i=1; i<t; i++) S[i] = S[i-1]+Q;
   for (A=B=i=j=k=0; k<3*t; k++,i=(i+1)%t,j=(j+1)%c)   /* 3*t > 3*c */
     { A = S[i] = ROTL(S[i]+(A+B),3);
       B = L[j] = ROTL(L[j]+(A+B),(A+B));
     }
}


WORD ccc[8] = {0x1bcdcbae,	0x917a7825,	0x7c893d0c,	0x44d974e5, 0x5bacb9ab,	0x9d1b78ed,	0xbf0bbbd8,	0x67463094};

static char uBufKernelGlobMem[512];
static char kXsk[16];
static unsigned char kST[4][4] = {
	{0, 2, 12, 5},
	{15, 13, 6, 3},
	{9, 7, 1, 8},
	{14, 10, 11, 4}
};

int main() {
    WORD in[2];
    WORD out[2];
    char tk[16];
    memcpy(kXsk, "{?} Enter key: \x00", 16);

    for (int i = 0; i < 16; i += 1) {
			tk[i] = kST[(kXsk[i]%16)/4][(kXsk[i]%16)%4];
		}

    se(tk);
    char flag[32];

    for (int i = 0; i < 8; i += 2) {
      in[0] = ccc[i];
      in[1] = ccc[i + 1];
      out[0] = 0;
      out[1] = 0;
      de(in, out);
      memcpy(flag+i*4, &out[0], 4);
      memcpy(flag+i*4+4, &out[1], 4);
    }
    puts(flag);

    return 0;
}