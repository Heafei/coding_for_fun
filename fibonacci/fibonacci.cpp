#include <iostream>
#include <fstream>
#include <vector>
#include <cstdio>

//#define _DEBUG_

#ifdef _DEBUG_
#define log_e(...) fprintf(stderr, __VA_ARGS__)
#define log_d(...) fprintf(stdout, __VA_ARGS__)
#else
#define log_e(...)
#define log_d(...)
#endif

using namespace std;

/**
 *
 */
long fibonacci_number(int n){
	long fib_num_n = 1;
	if(n>2){
		fib_num_n = fibonacci_number(n-1) + fibonacci_number(n-2);
	}else{
		fib_num_n = 1;
	}
	return fib_num_n;
}

long* fibonacci_sequence(int n){
	long *fib_seq = new long[n];
	int idx = 0;
	while(idx < n){
		if(idx > 1){
			fib_seq[idx] = fib_seq[idx-1] + fib_seq[idx-2];
		}else{
			fib_seq[idx] = 1;
		}
		log_d("fibonacci[%3d]=%ld\n", idx+1, fib_seq[idx]);
		idx++;
	}
	return fib_seq;
}

int fibonacci_sequence(int n, long* &fib_seq){
	fib_seq = new long[n];
	int idx = 0;
	while(idx < n){
		if(idx > 1){
			fib_seq[idx] = fib_seq[idx-1] + fib_seq[idx-2];
		}else{
			fib_seq[idx] = 1;
		}
		log_d("fibonacci[%3d]=%ld\n", idx+1, fib_seq[idx]);
		idx++;
	}
	return 0;
}

int main(int argc, char* argv[]){
	int n = 10;
	long * fib_seq_a;
	long* fib_seq_b;
	fib_seq_a = fibonacci_sequence(n);
	fibonacci_sequence(n, fib_seq_b);
	cout << "fibonacci_sequence = " << fib_seq_a[n-1] << endl;
	cout << "fibonacci_sequence = " << fib_seq_b[n-1] << endl;
	std::cout << fibonacci_number(n) << std::endl;
	return 0;
}
