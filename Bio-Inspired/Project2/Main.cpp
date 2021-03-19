#include <iostream>
#include <vector>

#include "GA.h"
#include "gfun.h"


using namespace std;
using namespace gfun;

int main()
{

	GA t = GA(0.6, 100, 0.5);

	t.run("p01");


	// Just so it is easier to read the terminal output
	cout << "\n\n";
}