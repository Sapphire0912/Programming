#include<iostream>
#include<string>
using namespace std;

int main()
{
  char ss[30];
  cout << "�п�J�@�Ӧr��G";
  cin.getline(ss, 10, '$');
  cout << ss << endl;

  cout << "�п�J�@�Ӧr��G";
  cin.get(ss, 30);
  cout << ss << endl;
  cout << "�п�J�@�Ӧr��G";
  cin.get(ss, 30);
  cout << ss << endl;
}
