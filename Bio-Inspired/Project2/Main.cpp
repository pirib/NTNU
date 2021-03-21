#include <iostream>
#include <vector>

#include <time.h>
#include "GA.h"
#include "gfun.h"


using namespace std;
using namespace gfun;

int main()
{
	clock_t start, end;

	GA t = GA(0.6, 400, 0.2);
	
	start = clock();
	t.run("p01");
	end = clock();

	cout << endl << "Time spent: " <<  double(end - start) / CLOCKS_PER_SEC << endl; 

	// Just so it is easier to read the terminal output
	cout << "\n\n";
}