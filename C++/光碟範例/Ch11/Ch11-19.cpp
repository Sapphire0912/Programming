#include<iostream>
#include<string>
#include<cctype>
using namespace std;

bool checkID (string idStr)          // �d�稭���Ҧr�����禡
{
  int letterNums[] = {10,11,12,13,14,15,16,17,34,18,
                      19,20,21,22,35,23,24,25,26,27,
                      28,29,32,30,31,33};

  if (islower(idStr[0]))        // ���N�Ĥ@�ӭ^��r���ର�j�g
    idStr[0] = toupper(idStr[0]);

  int total = (letterNums[idStr[0] - 'A'] / 10) +
              (letterNums[idStr[0] - 'A'] % 10) * 9;
  for(int i = 1;i < 9;i++)
    total += (idStr[i] - '0') * (9 - i); // �̧ǥ[�`

  // �H10��h�[�`�Ȥ��Ӧ�ƫ�A���Ӧ��
  int checkNum = (10 - total % 10) % 10;

  if(checkNum == (idStr[9] - '0'))  //�P�����Ҧr���̫�@�X��
    return true;
  else
    return false;
}

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
           == string::npos)    // �ˬd�� 9 �r�O�_�t�Ʀr�H�~���r��
        if (isID = checkID(idStr))   // �I�s checkID() �i��d��
          cout << "�d��q�L" << endl;
        else
          cout << "���O�X�k�������Ҧr��" << endl;
      else
        cout << "�����Ҧr���᭱9�Ӧr���O�Ʀr�I" << endl;
    else
      cout << "�����Ҧr���� 1 �Ӧr�����^��r���I" << endl;
  } while (!isID);
}
