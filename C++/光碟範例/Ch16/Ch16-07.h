using namespace std;

template<class T,int MaxSize = 20>
class Stack {
public:
  void init() { sp = 0; }  // 初始化的成員函式
  void push(T data);       // 宣告存入一個整數的函式
  T pop();               // 宣告取出一個整數的函式
private:
  int sp;             // 用來記錄目前堆疊中已存幾筆資料
  T buffer[MaxSize];  // 代表堆疊的陣列
  static void Error() { cout << "\nStack Error\n"; }
};

template<class T,int MaxSize>
void Stack<T,MaxSize>::push(T data)  // 將一個整數『堆』入堆疊
{
   if(sp == MaxSize)      // 若已達最大值, 則不能再放資料進來
     Error();
   else
     buffer[sp++] = data; // 將資料存入 sp 所指元素, 並將 sp 加 1
}                         // 表示所存的資料多了一筆

template<class T,int MaxSize>
T Stack<T,MaxSize>::pop()            // 從堆疊中取出一個整數
{
   if(sp == 0) {          // 若已經到底了表示堆疊中應無資料
     Error();
     return 0;
   }
   return buffer[--sp];   // 傳回 sp 所指的元素, 並將 sp 減 1
}                         // 表示所存的資料少了一筆