#include <iostream>
#include <cmath>
using namespace std;

int main()
{
  int how_many;
  cout << "�аݭn�p��h�֭ӼƦr����N�δX�M�����G";
  cin >> how_many;

  double *dptr  = new double[how_many]; // �t�m���w�ƶq���O����

  for(int i=0;i<how_many;i++) {
    cout << "�п�J�� " << (i+1) << " �ӼƭȡG";
    cin >> *(dptr+i);
  }

  double sum = 0;
  for(int i=0;i<how_many;i++)        // �p��Ҧ��ƭȪ��`�M
    sum += *(dptr+i);
  cout << "��ƥ������G" << (sum / how_many) << endl;

  sum = 1;
  for(int i=0;i<how_many;i++)        // �p��Ҧ��ƭȪ����n
    sum *= *(dptr+i);
  cout << "�X�󥭧����G" << pow(sum,1.0/how_many);

  delete [] dptr;
}
