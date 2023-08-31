#include <iostream>
using namespace std;

class ByteInt {
public:
  ByteInt(int i) { c = (char) i; }  // �غc�禡
  void show()    { cout << (int) c << endl; }
  ByteInt &operator++();         // �e�m���W�禡
  ByteInt operator++(int);       // ��m���W�禡
private:
  char c;       // �ΨӦs��ƭȪ���Ʀ���
};

ByteInt& ByteInt::operator++()   // �e�m���W�禡
{
  c++;
  cout << "�e�m ++" << endl;     // ����i�R��
  return *this;
}

ByteInt ByteInt::operator++(int) // ��m���W�禡
{
  ByteInt tmp = *this;           // �O�s���W�e����
  c++;
  cout << "��m ++" << endl;     // ����i�R��
  return tmp;                    // �Ǧ^���W�e����
}

void main()
{
  ByteInt b(5);
  (++b).show(); // �[ 1 ����ܨ��
  (b++).show(); // �A�[ 1, ����ܥ[ 1 ���e����
  b.show();     // ��̫ܳᵲ�G
}
