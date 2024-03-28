/* 
	Introduction of algorithms 3rd.
	Chapter 2. Getting Started
	2.1 Insertion sort P.16
	
	target: Insertion sort
	input: any length of array.
	output: sorted array.	
	
	Languages: C
*/

# include<stdio.h>
# include<stdlib.h>
# define MAXSIZE 10

int *InsertionSort(int *Array, int length, int sorted=0){
	/* if sorted is 0, sort from smallest to largest.
	   if sorted is 1, sort from largest to smallest.
	*/
	
	int j, i;   // control array index
	int key; // save current element.
	
	for (j=1;j<length;j++){
		key = Array[j];
		i = j - 1;
		
		if (sorted == 0){
			while (i > 0 && Array[i] > key){
				Array[i + 1] = Array[i];
				i = i - 1;
			}
		}

		else{
			if (sorted == 1){
				while (i > 0 && Array[i] < key){
					Array[i + 1] = Array[i];
					i = i - 1;
				}				
			}
			else{
				printf("the parameter of sorted is malformed.\n");
			}
		}

		Array[i + 1] = key;
	}
	
	return Array;
}

int main(){
	int A[MAXSIZE];
	
	int i=0;
	char y;
	do{
		scanf("%d", &A[i]);
		i++;
	}while (y = getchar() != '\n');
	
	int *ptr = A;
	InsertionSort(ptr, i, 0);
	
	// sorted result
	for (int k=0;k<i;k++){
		printf("%d ", ptr[k]);
	}
	printf("\n");
	return 0;	
}


