# include<stdio.h>
# include<unistd.h>

int main() {
	int A;
	A = fork();  /* fork another proces */
	
	if (A == 0){
		printf("This is child process\n");
		execlp("/bin/dir", "dir", NULL);
	}
	else{
		printf("This is from parent process\n");
		int pid = wait(&status);
		printf("Child %d completes", pid);
	}
	printf("process ends %d\n", A);
	
	system("PAUSE");
	return 0;
}
