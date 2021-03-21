#include <vector>
#include <algorithm>
#include <random>

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

	// Randomness
	default_random_engine rng;

	// The order in the vector is the order of service as well
	vector<Route> routes;

	// Constructor
	Depot(int n_vechicles, int id, int x, int y, vector<int> dur_load, default_random_engine & rng) {
		this->n_vehicles = n_vechicles;
		this->id = id;
		this->x = x;
		this->y = y;

		veh_dur = dur_load[0];
		veh_load = dur_load[1];

		// Shuffle the customers in the route
		this->rng = rng;
	}

	// Add one new customer to the end of the vector
	void add_customer( Customer customer) {
		this->customers.push_back(customer);
	}

	// Two part scheduler that sets the routes and takes into acount the duration of the routes + capacity of the car
	// p 84
	void schedule(bool use_two_phases = true, bool randomize = true) {

		// Remove old routes if still exist
		routes.clear();

		int veh_used = 0;

		// Create an empty route with specified vehicle duration/load capabilities
		add_route();

		// Randomize the routes
		if (randomize) {
			shuffle(begin(customers), end(customers), rng);
		}
	
		// Phase 1

		// Iterate through the customers, and add them to a route, or create a new route if the demand is not met
		for (int c = 0; c < customers.size(); c++) {
			
			// Push the customer into the route if that route's vechile's capacity can handle it
			if ( routes.back().check_capacity(customers[c])) {
				routes.back().add_customer(customers[c]);
			}
			else {

				// If the depot has more disposable vehicles, create a new delivery route, and add the customer there.
				if (routes.size() <= n_vehicles ) {
					add_route();
					routes.back().add_customer(customers[c]);
				}
				else {
					// Add a customer still
					routes.back().add_customer(customers[c]);

					// This will decrease the behicle capacity, but could be redeemed by phase 2
				}
			}			
		}
		
		if (use_two_phases) {
		// Phase 2
			for (int r = 0; r < routes.size(); r++) {

				if ( routes[r].customers.size() > 1) {
					// Find the route to swap with
					int next_route = r + 1;

					// In case the index is outside the vector, swap with the the first route
					if (next_route == routes.size()) {
						next_route = 0;
					}
			
					// Check if the move does not overburden the capacity of the next route 
					if	( routes[next_route].check_capacity( routes[r].customers.back() ) ) {

						// temp copies for proposes route and next route
						vector<Customer> prop_r = routes[r].customers;
						vector<Customer> prop_next_r = routes[next_route].customers;

						// Insert the last customer of prop_r into the first spot of prop_next_r
						prop_next_r.insert(prop_next_r.begin() + 0, prop_r.back() );

						// Remove the last customer from the cur_r
						prop_r.pop_back();

						// Check if this change results in less distance travelled
						if (routes[r].calculate_total_distance(routes[r].customers) + routes[next_route].calculate_total_distance(routes[next_route].customers) <
							routes[r].calculate_total_distance(prop_next_r) +  routes[next_route].calculate_total_distance(prop_r ) ) {
					
							// Append the last customer from r to the next route
							routes[next_route].add_customer(routes[r].customers.back(), false);

							// Remove the last customer from route r
							routes[r].remove_customer_at( routes[r].customers.size() - 1 );

							// Check if removal left the route empty, then remove the route
							if (routes[r].customers.empty())
								remove_empty_routes();
						}
					}
				}
			}
		}
	}

	// Adds a route with specified vechicle capacities
	void add_route() {
		routes.push_back(Route(veh_dur, veh_load, x, y));
	}

	// Returns number of routes this depot has
	int get_n_routes() {
		return routes.size();
	}
	
	// Removes the customer from the customers list, and from the route that had that customer. Update the customer list and recalculates the new route length
	void remove_customer(Customer customer) {

		int i = 0;
		
		for (Customer& c : customers) {
			if (c == customer) {
				customers.erase(customers.begin() + i);
				break;
			}
			i++;
		}

		// Find the customer at the route
		int r = -1;
		for (Route& route : routes) {
			r++;
			for (Customer& c : route.customers) {
				if (c == customer) {
					route.remove_customer(customer.id);
					
					if (route.customers.size() == 0) {
						routes.erase( begin(routes) + r);
					}

					return;
				}
			}
		}

	}

	// Removes the route at index
	void remove_route_at(int index) {
		routes.erase(begin(routes) + index);
	}

	// Removes all empty routes form the 
	void remove_empty_routes() {

		vector<int> routes_to_delete;

		for (int r = 0; r < routes.size(); r++) {
			if (routes[r].customers.size() == 0) {
				routes_to_delete.insert(begin(routes_to_delete), r);
			}
		}

		for (int r : routes_to_delete) {
			remove_route_at(r);
		}
	}

	// Calculate the total distance travelled in this depot
	float total_distance() {
		float distance = 0;
		for (Route route : routes) {
			distance += route.calculate_total_distance(route.customers);
		}
		return distance;
	}

};