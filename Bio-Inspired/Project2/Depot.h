#include <vector>

using namespace std;

class Depot {
public:

	// Depot knows the customers it should be serving, number of vehicles it has, and the routes specific to the current solution
	vector<int> customers;
	int n_vehicles;

	// The order in the vector is the order of service as well
	vector<vector<int>> routes;

	// Constructor
	Depot(int n_vechicles) {
		this->n_vehicles = n_vechicles;
	}


	// Cleans up and then adds a list of customers
	void set_customers(vector<int> customers) {

		this->customers.clear();

		this->customers = customers;
	}


};

