#include <vector>
#include "Customer.h"
#include "Route.h"


using namespace std;

class Depot {
public:

	// Params
	int id;
	int x;
	int y;

	// Depot knows the customers it should be serving, number of vehicles it has, and the routes specific to the current solution
	vector<Customer> customers;
	int n_vehicles;
	int veh_dur;
	int veh_load;

	// The order in the vector is the order of service as well
	vector<Route> routes;

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

		int veh_used = 0;

		// Create an empty route with specified vehicle duration/load capabilities
		add_route();

		// Phase 1

		// Iterate through the customers, and add them to a route, or create a new route if the demand is not met
		for (int c = 0; c < customers.size(); c++) {
			
			// Push the customer into the route
			if (! routes[routes.size() - 1].add_customer(customers[c])) {
								
				// Since the customer was not added, we need to decrement the index, to re-assign the customer on the next step
				c--;

				// If we have available vehicles, deploy them
				if (veh_used < n_vehicles) {
					add_route();

					// If a customer was not added, it means that the vehicle has reached its max capacity
					veh_used += 1;
				}
				else {
					cout << "ERROR:\n ";
					cout << "The depot " << id << " does not have the capacity to handle the customers assigned! \n\n";
					break;
				}
			}
				
		}

		// Phase 2


	}

	// Adds a route with specified vechicle capcities
	void add_route() {
		routes.push_back(Route(veh_dur, veh_load));
	}

};
