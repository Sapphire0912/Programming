#include<stdio.h>
main()
{
	int hr,min,sec;
	int year,mon,day;
	char week[50];
	printf("���G�Y�����0�I�Х�00�A�H�νп�J2��ơC(�ҡG3�I4��8��h�п�J03:04:08)\n");
	printf("�п�J�{�b���ɶ�(24�p�ɨ�)�G(hr:min:sec)\n");
	scanf("%d:%d:%d",&hr,&min,&sec);
	
    if(hr>23) 
    printf("�I�H�A���D�O�³J�ܡH�I�I�ĢI�A�O�L�����P�y���ɶ��ڡH�H�H�@�Ѣ����p�ɤ����H�I\n");
    else
    if(min>59)
    printf("�I�H�A���D�O�³J�ܡH�I�I�ĢI�A�O�ݭ����P�y�������ڡH�H�H��צh�F�@��O�_�H�I\n");
    else
    if(sec>59)
    printf("�I�H�A���D�O�³J�ܡH�I�I�ĢI�A�O�ݭ����P�y����w�ڡH�H�H�q���O�_�Ӧ��O�F�H�I\n");
    else
    printf("�п�J�{�b������G(year-mon-day-week)\n");
    scanf("%d-%d-%d-%s",&year,&mon,&day,&week);
    
    if(year>2017) 
    printf("�I�H�A���D�O�̤l�ܡH�I�I�ĢI�X�~�F�������D�H�I\n");
    else
    if(mon>13)
    printf("�I�H�A���D�O��è�ܡH�I�I�ĢI���P�H���~��ܡH�I\n");
    else
    if(day>31)
    printf("�I�H�A���D����ê�ܡH�I�I�ĢI�ڷQ�j���O�C�C�C\n"); 
    else
    printf("�{�b���ɶ����G%d�I %d�� %d��\n���Ѫ�������G�褸 %d�~ %d�� %d�� �P��%s\n",hr,min,sec,year,mon,day,week);

	return 0;
 } 
