/*
	Introduction of algorithms 3rd.
	Chapter 2. Getting Started
	2.3 Merge sort P.31
	
	target: Merge sort
	input: any length of array.
	output: sorted array.
	
	Languages: C++
*/

# include<iostream>
# define MAXSIZE 10
using namespace std;

int main(){
	int A[MAXSIZE];
	
	int i=0;
	char y;
	do{
		scanf("%d", &A[i]);
		i++;
	}while (y = getchar() != '\n');
	
	int *ptr = A;
	MergeSort(ptr, 0, i, 0);
	
	// sorted result
	for (int k=0;k<i;k++){
		printf("%d ", ptr[k]);
	}
	printf("\n");
	return 0;	
}



