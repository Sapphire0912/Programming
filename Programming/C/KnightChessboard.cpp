# include<stdio.h>
# include<stdlib.h>

main(){
	int chess[8][8]; // �إߤ@�ӴѽL 
	int degree[8][8]; // �إߤ@�Ӷ��h��
	int x, y;
	printf("��J�_�l�y��(x y): ");
	scanf("%d %d", &y, &x);
	
	int i, j;
	// ��ѽL���C�ӭȳ]��0
	for(i = 0; i < 8; i++){
		for(j = 0; j < 8; j++){
			chess[i][j] = 0;
		}
	} 
	
	// �M�h�����k 8�Ӥ�V 
	int dx[8] = {2, 1, -1, -2, -2, -1, 1, 2};
	int dy[8] = {1, 2, 2, 1, -1, -2, -2, -1};
	int count = 0;
	
	// �ⶥ�h��(�C���I�i�H�����a��)�����Ʃ�i�h
	for(i = 0; i < 8; i++){
		for(j = 0; j < 8; j++){
			for(int k = 0; k < 8; k++){
				if (i + dx[k] >= 0 && i + dx[k] <= 7){
					if (j + dy[k] >= 0 && j + dy[k] <= 7){
						count++;
					}
				}	
			}
			degree[i][j] = count;
			count = 0;
		}
	}
	
	int times;
	int xcoord[8], ycoord[8]; // ���O�s��i�檺x, y�y�� 
	
	for(times = 0; times < 64; times++){
		// ���̫�@�B�������X�j�餣�Ω��U�P�_�F 
		if (chess[x][y] == 64)
			break;
		else{
			chess[x][y] = times + 1;
			degree[x][y] = 0;
		}
		
		// ����X�Ҧ��i�檺���|
		for(i = 0; i < 8; i++){
			if(x + dx[i] >= 0 && x + dx[i] <= 7){
				if (y + dy[i] >= 0 && y + dy[i] <= 7){
					xcoord[i] = x + dx[i]; // x�y�� 
					ycoord[i] = y + dy[i]; // y�y�� 
				}
				else{
					xcoord[i] = -1;
					ycoord[i] = -1;
				}
			}
			else{
				xcoord[i] = -1;
				ycoord[i] = -1;
			}
		}
		
		int value[8]; // �s�񶥼h��p��L�᪺�� 
		int position = 0; // ������m 
		
		// �p�ⶥ�h���� 
		for(i = 0; i < 8; i++){
			if(xcoord[i] >= 0 && ycoord[i] >= 0 && degree[xcoord[i]][ycoord[i]] > 0){
				degree[xcoord[i]][ycoord[i]]--;
				value[i] = degree[xcoord[i]][ycoord[i]];
			}
			else{ 
				value[i] = 9;
			}
		}

		// ��X���h��̤p��, �ç�X�����m 
		int mininum = value[0];
		for(i = 0; i < 8; i++){
			if (mininum > value[i]){
				mininum = value[i];
				position = i;
			}
		}
		
		// �̫�n���ʪ����G
		x = xcoord[position];
		y = ycoord[position]; 
	}
	
//	 ��X���G 
	for(i = 0; i < 8; i++){
		for(j = 0; j < 8; j++){
			printf("%3d", chess[i][j]);
		}
		printf("\n");
	} 
	system("pause");
	return 0;
} 

