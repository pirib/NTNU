#include <iostream>
#include "GA.hpp"



using namespace std;


int main()
{

	GA t = GA(0.6, 1, 0.1);
	t.run("p01");


	// Just so it is easier to read the terminal output
	cout << "\n\n";
}