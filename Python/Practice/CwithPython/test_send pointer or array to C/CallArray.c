# include<stdio.h>
# include<stdlib.h>
# include "CallArray.h"

int c[5];

void handleArray(int *p, int size){	
	for (int k=0;k<size;k++){
		*(p + k) = *(p + k) + 1;
		c[k] = *(p + k);
	}
}

