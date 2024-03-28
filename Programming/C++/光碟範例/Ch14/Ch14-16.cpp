#include<iostream>
#include<fstream>
#include<string>
using namespace std;

class Entry {   // �q�T���������O
friend istream& operator>>(istream&, Entry&);
friend ostream& operator<<(ostream&, Entry&);
public:
  void keyin();
  string getname() { return name;}
  string getphone() { return phone;}
private:
  string name;  // �m�W
  string phone; // �q��
};

void Entry::keyin()     // �ШϥΪ̿�J�s��ƪ��禡
{
  cin.get();    // �M���w�İϤ�������r��
  cout << "�п�J�s�ض��ت��m�W�G";
  getline(cin,name);
  cout << "�п�J�s�ض��ت��q�ܸ��X�G";
  getline(cin,phone);
}

ostream& operator<<(ostream& os, Entry &e)
{ // �s�ɮ�, �C����Ʀs�@��, �m�W�P�q�ܥγr�����}
  return os << e.name << ',' << e.phone << endl;
}

istream& operator>>(istream& is, Entry &e)
{
  getline(is,e.name,',');       // ��Ū�r�����e���m�W
  getline(is,e.phone,'\n');     // �AŪ����r�����e���q��
  return is;
}

void addone(fstream& file)      // ��J�s���ت��禡
{
  Entry newone;
  newone.keyin();
  file.seekp(0,ios_base::end);  // �����ɮ׳̫�g�J�s���
  file << newone;
  cout << "�w�s��!\n";
}

void lookup(fstream& file)      // �j�M���禡
{
  cout << "�n��֪��q�ܡG";
  string name;
  cin.get();            // �M���w�İϤ�������r��
  getline(cin,name);    // ����L���o�m�W�r��

  Entry who;            // �Ψ��x�s���ɮ�Ū�J�����
  file.seekg(0,ios_base::beg);  // �q�YŪ��
  while(!file.eof()) {
    file >> who;
    if(name == who.getname()) { // ���m�W
      cout << "�q�ܸ��X�O " << who.getphone() << '\n';
      return;           // �w�g���, �i���X�禡
    }
  }
  file.clear();         // �M�� eof() �����A
  cout << "�S���o�ӤH�����\n";
}

int main()
{
  fstream file = fstream("TelBook.txt", ios_base::in|ios_base::out);
  if (!file)
    cerr <<"�ɮ׶}�ҥ���!!\n";
  else {
    char choice;
    do {
      cout << "�п�ܥ\��(0)�����{��(1)��J���(2)�j�M��ơG";
      cin >> choice;
      if (choice == '1')        // �ϥΪ̭Y�� 1
        addone(file);
      else if (choice == '2')   // �ϥΪ̭Y�� 2
        lookup(file);
    } while (choice != '0');
    cout << "...Goodbye...";
  }
}
