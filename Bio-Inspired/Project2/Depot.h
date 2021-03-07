#include <vector>

using namespace std;


class Depot {
public:

	// Depot knows the customers it should be serving, number of vehicles it has, and the routes specific to the current solution
	vector<int> customers;
	int n_vehicles;

	// The order in the vector is the order of service as well
	vector<vector<int>> routes;

	// Additional parameters
	int id;
	int x;
	int y;

	// Constructor
	Depot(int n_vechicles, int id, int x, int y) {
		this->n_vehicles = n_vechicles;
		this->id = id;
		this->x = x;
		this->y = y;
	}


	// Cleans up and then adds a list of customers
	void set_customers(vector<int> customers) {

		this->customers.clear();

		this->customers = customers;
	}

	// Add one new customer to the end of the vector
	void add_customer( int customer_id ) {
		this->customers.push_back(customer_id);
	}


};

