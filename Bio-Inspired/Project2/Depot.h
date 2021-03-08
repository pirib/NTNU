#include <vector>
#include "Customer.h"

using namespace std;

class Depot {
public:

	// Depot knows the customers it should be serving, number of vehicles it has, and the routes specific to the current solution
	vector<Customer> customers;
	int n_vehicles;
	int veh_dur;
	int veh_load;

	// The order in the vector is the order of service as well
	vector<vector<int>> routes;

	// Additional parameters
	int id;
	int x;
	int y;

	// Constructor
	Depot(int n_vechicles, int id, int x, int y, vector<int> dur_load) {
		this->n_vehicles = n_vechicles;
		this->id = id;
		this->x = x;
		this->y = y;
		veh_dur = dur_load[0];
		veh_load = dur_load[1];
	}

	// Add one new customer to the end of the vector
	void add_customer( Customer customer) {
		this->customers.push_back(customer);
	}

	// Two part scheduler that sets the routes and takes into acount the duration of the routes + capacity of the car
	// p 84
	void schedule() {

		// Part 1

	}

};
