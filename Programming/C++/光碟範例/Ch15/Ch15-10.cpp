#include <iostream>
#include "Ch15-10.h"

void main()
{
  Stack st;     // �w�q���|����

  try {
    for (int i=0; i<=20; i++)  // �ΰj���J 21 �����
      st.push(i);
  }
  catch (StackFull) {
    cerr << "�ާ@���~, ���|�w��\n";
  }

  try {
    for (int i=0; i<=20; i++)  // �ΰj����X 21 �����
      cout << st.pop() << '\t';
  }
  catch (StackEmpty) {
    cerr << "�ާ@���~, ���|�w�M��\n";
  }
}
