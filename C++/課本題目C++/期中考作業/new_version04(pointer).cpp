#include<iostream>
#define students 10
#define score 3

using namespace std; 
float avg(float*);
float sum(float*);

main(){
	float mean[students], total[students];
	float grade[score];
	float *p = grade;
	
	for(int i=0;i<students;i++){
		cout << "�п�J�� " << i+1 << " �Ӿǥͪ����Z(�� �^ ��): ";
		for(int j=0;j<score;j++)
			cin >> *(p+j);
		total[i] = sum(p);
		mean[i] = avg(p);
	}
	cout << endl;
	for(int i=0;i<students;i++)
		cout << "�� " << i+1 << " ��ǥͪ����Z(����,�`�M): "
			 << mean[i] << " , " << total[i] << endl;
}

float avg(float *total){
	return sum(total)/score;
}

float sum(float *sscore){
	float total;
	for(int i=0;i<score;i++)
		total += *(sscore+i);
	return total;
}
