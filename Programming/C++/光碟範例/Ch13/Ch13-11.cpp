#include<iostream>
using namespace std;

class Flyable {      // ���檺�y�����z
public:
  virtual void takeoff() =0; // �_��
  virtual void flying()  =0; // ����
  virtual void landing() =0; // ����
};

class Bird : public Flyable {       // ��
public:
  void takeoff() { cout << "�i�}�ͻH, ���ʯͻH" << endl; }
  void flying()  { cout << "�i�ͷƵ�, ���ͥ[�t" << endl; }
  void landing() { cout << "��}�e��, ���͸��a" << endl; }
};

class Jetplane : public Flyable {   // �Q�g��
public:
  void takeoff() { cout << "�[�o��, ���_, ���_���[" << endl; }
  void flying()  { cout << "�[�o��" << endl; }
  void landing() { cout << "��t, ��_���[, �ۦa" << endl; }
};

int main()
{
  Bird egale;
  cout << "egale ��������{�G" << endl;
  egale.takeoff();
  egale.flying();
  egale.landing();

  Jetplane airbus;
  cout << "airbus ��������{�G" << endl;
  airbus.takeoff();
  airbus.flying();
  airbus.landing();
}
