#include<iostream>
#include<string>
#include<cctype>
using namespace std;

int main()
{
  string idStr;      // �O���ϥΪ̿�J���
  bool isID = false; // �ϥΪ̿�J���榡�O�_���T
  string num = "0123456789";  // �Ψ����ҬO�_���Ʀr���r��

  do {
    cout << "�п�J�����Ҧr���G";
    cin >> idStr;
    if(idStr.size()!=10) {
      cout << "�����Ҧr���@�Q�Ӧr���A�Ф��n��J�ťաI" << endl;
      continue;
    }
    if (isalpha(idStr[0]))  // �� 1 �r�O�_���j�g�Τp�g�^��r��
       if (idStr.substr(1,9).find_first_not_of("0123456789")
             == string::npos)  // �ˬd�� 9 �r�O�_�t�Ʀr�H�~���r��
         isID = true;
       else
         cout << "�����Ҧr���᭱9�Ӧr���O�Ʀr�I" << endl;
    else
      cout << "�����Ҧr���� 1 �Ӧr�����^��r���I" << endl;
  } while (!isID);
}
