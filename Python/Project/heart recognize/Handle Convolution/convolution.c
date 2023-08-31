# include "convolutionH.h"

# include<stdio.h>
# include<stdlib.h>
# include<math.h>
# define width 800 // 800 
# define height 600  // 600

double u[256];
double ux[256];
int result[height][width];

int gL, gLM, gM, gMH, gH;

double handle(int low, int med, int high, int scale){
	double curr_u;
	
	double left, right;
	double alpha, beta;
	
	alpha = med - low;
	beta = high - med;
	
	if (med >= scale)
		left = med - scale;
	else
		left = 0;
		
	if (scale >= med)
		right = scale - med;
	else
		right = 0;
	
	curr_u = left / alpha + right / beta;
	if (curr_u <= 1)
		curr_u = 1.0 - curr_u;
	else
		curr_u = 0;
	
	return curr_u;
}

void U(int L, int LM, int M, int MH, int H, float uLPowScale, float uMPowScale, float uHPowScale){
	int i;
	for (i=0; i<256; i++){		
		if (0 <= i && i < LM)
			u[i] = pow(handle(0, L, LM, i), uLPowScale);		
		if (LM <= i && i < MH)
			u[i] = pow(handle(LM, M, MH, i), uMPowScale);		
		if (MH <= i)
			u[i] = pow(handle(MH, H, 255, i), uHPowScale);
		ux[i] = i * u[i];
	}
	
	gL = L;
	gLM = LM;
	gM = M;
	gMH = MH;
	gH = H;
}

void CMultiThreshold(int src[height][width]){
	int h, w; // control loop
	int m, n; // control matrix
	
	double TotuL=0, TotuXL=0;
	double TotuM=0, TotuXM=0;
	double TotuH=0, TotuXH=0; 
	int avg, ML, MM, MH;
	int dL, dM, dH;
	
	int val;
		
	// control loop
	for (h=1; h < height-1; h++){
		for (w=1; w < width-1; w++){
			// control matrix
			for (m=h-1; m <= h+1; m++){
				for (n=w-1; n <= w+1; n++){
					// calculation
					val = src[m][n];
					if (val < gLM){
						TotuL += u[val];
						TotuXL += ux[val];
					}
					if (gLM <= val && val < gMH){
						TotuM += u[val];
						TotuXM += ux[val];	
					}
					if (gMH <= val && val < 256){
						TotuH += u[val];
						TotuXH += ux[val];		
					}
					avg += val;
				}
			}
			// control matrix end.
			
			// calculation avg, ML, MM, MH
			if (avg != 0){
				avg = avg / 9;
				if (TotuL != 0)
					ML = TotuXL / TotuL;
				if (TotuM != 0)
					MM = TotuXM / TotuM;
				if (TotuH != 0)
					MH = TotuXH / TotuH;
				
				// calculation diff
				dL = (avg < ML)?ML - avg:avg - ML;
				dM = (avg < MM)?MM - avg:avg - MM;
				dH = (avg < MH)?MH - avg:avg - MH;
				
				// return gray value
				if ((dL < dM && dL < dH) || ((dL == dM || dL == dH))) // 假如 dL 最小, 或者有兩個相等值時取較小灰階值 
					result[h][w] = 0;
				else{
					if ((dM < dL && dM < dH) || (dM == dH))
						result[h][w] = 128;
					else
						result[h][w] = 255;
				}
			}
			else
				result[h][w] = 0;
		}
	}
	// control loop end.
}


