# include<stdio.h>
# include<stdlib.h>
# include<time.h>

# define width 800
# define height 600


int **calc(int **mat){
	int **arr = (int **)malloc(width * sizeof(int *));
	
	for (int i=0; i < width; i++){
		arr[i] = (int *)malloc(height * sizeof(int));
	}
	
	for (int i=0; i < width; i++){
		for (int j=0; j < height; j++){
			arr[j][i] = mat[j][i] * 2;
		}
	}
	return arr;
}

int main(){
	srand(time(NULL));
	int matrix[height][width] = {};
	int i, j;
	int* p[width];
	
	for (i = 0; i < width; i++){
		p[i] = matrix[i];
		
		for (j = 0; j < height; j++){
			matrix[j][i] = rand() % 256;
		}
	}
	printf("ori: %3d ", matrix[0][0]);
	
	int **res = calc(p);
	
	for (i = 0; i < width; i++){		
		for (j = 0; j < height; j++){
			if (i == 0 & j == 0)
				printf("calc: %3d", res[j][i]);
		}
	}
	
	return 0;
}

