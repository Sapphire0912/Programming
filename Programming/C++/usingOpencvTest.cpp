# include <opencv2\opencv.hpp>


using namespace cv;
using namespace std;

int main(){
	Mat srcImg = imread("background.jpg");
	
	imshow("Test Bg", srcImg);
	waitKey(0);
	system("pause");
	return 0;
}
