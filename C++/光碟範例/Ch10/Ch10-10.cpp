#include <iostream>
using namespace std;

class ByteInt {
public:
  ByteInt(int i) { c = (char) i; }  // �غc�禡
  void show()    { cout << (int) c << endl; }
  operator int() { return (int) c; }  // �N�����૬�����
  ByteInt &operator++();        // �e�m���W�禡
  ByteInt operator++(int);      // ��m���W�禡
private:
  char c;       // �ΨӦs��ƭȪ���Ʀ���
};

ByteInt& ByteInt::operator++()   // �e�m���W�禡
{
  c++;
  return *this;
}

ByteInt ByteInt::operator++(int) // ��m���W�禡
{
  ByteInt tmp = *this;           // �O�s���W�e����
  c++;
  return tmp;                    // �Ǧ^���W�e����
}

void main()
{
  ByteInt b(0);
  for(;b<5;b++)      // ����λ��W����
    b.show();
  cout << "�b�|�� " << b << " ����, �P���� " // ������X����
       << 2 * b * 3.14159;                   // �Ϊ���ѻP���k�p��
}
