#include <vector> 
#include "Depot.h"

using namespace std;


class Individual {
public:

	// An individual consists of vectors with depots
	vector<Depot> depots;

	// Constructor that creates depots with vehicles in them from scratch
	Individual( int n_depots, int n_vehicles) {

		// Add depots according to the problem
		for (int depot = 0; depot < n_depots; depot++) {
			depots.push_back(Depot(n_vehicles));
		}
	}



};
