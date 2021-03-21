#include <vector> 
#include <math.h>     
#include <iostream>
#include <fstream>
#include <string>

#include "Depot.h"
#include "gfun.h"

using namespace std;
using namespace gfun;


class Individual {
public:

	// Parameters from the solution files for easy access
	int num_vehicles;
	int num_customers;
	int num_depots;

	// An individual consists of vectors with depotss
	vector<Depot> depots;

	// Randomness
	default_random_engine rng;


	// Data for printing
	vector<int> customer_data;

	// Constructors
	
	// Default Cosntructor
	Individual(){}

	// Constructor that creates depots with vehicles in them from scratch
	Individual(vector<int> mnt, vector<int> customer_data, vector<int> depot_data, vector<int> dur_load, default_random_engine rng ) {

		// Data for printing
		this->customer_data = customer_data;

		// Populate GA parameters 
		num_vehicles = mnt[0];
		num_customers = mnt[1];
		num_depots = mnt[2];

		// Randomness
		this->rng = rng;

		// Add depots according to the problem
		for (int depot = 0; depot < num_depots; depot++) {
			depots.push_back(Depot(num_vehicles, depot_data[0 + 3*depot], depot_data[1 + 3*depot], depot_data[2 + 3 * depot], dur_load, rng));
		}

		// Add and sort customers into the depots based on Euclidian distance
		for (int c = 0; c < num_customers; c++ ) {
			
			// Looking for the closest depot
			float depot_distance = 999999;
			int depot_index = 0;

			for (int d = 0; d < num_depots; d++) {
				float new_distance = distance(depots[d].x, depots[d].y, customer_data[1 + 5 * c], customer_data[2 + 5 * c] );

				// If the new distance is shorter, save that info
				if (new_distance < depot_distance) {
					depot_distance = new_distance;
					depot_index = d;
				}
			}

			// The customer c is added to the depots route (the +1 is needed because ids start at 1)
			depots[depot_index].add_customer(Customer(customer_data[5 * c], customer_data[1 + 5 * c], customer_data[2 + 5 * c] , customer_data[4 + 5 * c]));
		}

		// Now that everything is initialized, deploy the initial scheduler in Depots
		for (int d = 0; d < num_depots; d++) {
			depots[d].schedule();
		}

	}


	// Methods

	// Weighted-sum fitness scoring (adapted for this particular problem, takes into account only the total length of the )
	float get_fitness() {

		float total_travel = 0;

		// Lopp through all routes of the depots, and sum over the total travel distance an individual solution proposes
		for (int d = 0; d < depots.size(); d++) {
			for (int r = 0; r < depots[d].routes.size(); r++) {
				total_travel += depots[d].routes[r].total_distance;
			}
		}

		return total_travel;
	}

	// Apply mutation to the individual
	void mutation(float mutation_prob, int iteration) {

		// Testing grounds
		
		// Intra-depot mutation
		if (mutation_prob >= get_prob()) {

			// Choose one mutation with equal probability
			int mut_type = interval(0, 4);

			// Reversal Mutation ===================================
			if (mut_type == 0) {
				/*
				// Pick a depot
				int selected_depot = interval(0, num_depots);

				// Pick two points in the customers
				int cut1 = 0;
				int cut2 = 0;

				while (cut1 == cut2) {
					cut1 = interval(0, depots[selected_depot].customers.size());
					cut2 = interval(0, depots[selected_depot].customers.size());
				}

				// Remove the old routes
				depots[selected_depot].routes.clear();

				if (cut1 < cut2)
					shuffle(begin(depots[selected_depot].customers) + cut1, begin(depots[selected_depot].customers) + cut2, rng);
				else
					shuffle(begin(depots[selected_depot].customers) + cut2, begin(depots[selected_depot].customers) + cut1, rng);

				// Run scheduler
				depots[selected_depot].schedule(true, false);
				*/

				// Testing Random positive reversal mutation
				
				// Pick a depot
				int selected_depot = interval(0, num_depots);

				// Copy the depot
				Depot depot = depots[selected_depot];

				// Get old distance
				float old_distance = depot.total_distance();
				
				for (int i = 0; i < 30 ; i++ ) {
					shuffle(begin(depot.customers), end(depot.customers),rng);
					depot.schedule(true, true);

					if (old_distance > depot.total_distance()) {
						depots[selected_depot] = depot;
						break;
					}
				}
			}

			// Single customer re-routing ===================================
			else if (mut_type == 1) {
				/*
				// Randomly select a customer and remove it from the route 

				// Variables for best new home for the customer
				int best_depot = interval(0, depots.size());
				int best_route = interval(0, depots[best_depot].routes.size());
				int best_spot = interval(0, depots[best_depot].routes[best_route].customers.size());
				float best_distance = 99999999;

				// Pick a random customer from that depot
				Customer selected_customer = depots[best_depot].routes[best_route].customers[best_spot];

				// Remove the customer (updates happen in the background)
				depots[best_depot].remove_customer(selected_customer);

				// Loop thourgh depots
				for (int d = 0; d < depots.size(); d++) {
					// Loop through routes
					for (int r = 0; r < depots[d].routes.size(); r++) {
						// If the route has the capacity to handle a new customer
						if (depots[d].routes[r].check_capacity(selected_customer)) {

							// Find the most feasible location in that route
							for (int ii = 0; ii < depots[d].routes[r].customers.size(); ii++ ) {
								Route route = depots[d].routes[r];
								route.insert_customer(selected_customer, ii);
								float new_distance = depots[d].routes[r].calculate_total_distance(route.customers);
								if (best_distance > new_distance) {
									best_depot = d;
									best_route = r;
									best_spot = ii;
									best_distance = new_distance;
								}
							}
						}
					}
				}

				// Insert to best found location
				depots[best_depot].routes[best_route].insert_customer(selected_customer, best_spot);

				// And to the depot list
				depots[best_depot].add_customer(selected_customer);
				*/
			}
			
			// Random positive route reshuffle ===================================
			else if (mut_type == 2) {

				// Pick a depot
				int depot_i = interval(0, depots.size());

				// Pick and make a copy of a route
				int route_i = interval(0, depots[depot_i].routes.size());
				Route selected_route = depots[depot_i].routes[route_i];

				// Get the old distance
				float old_distance = selected_route.calculate_total_distance(selected_route.customers);

				for (int i = 0; i < 20; i++) {
					
					// Copy the old route
					Route route = selected_route;

					// Shuffle that route
					shuffle(begin(route.customers), end(route.customers), rng);

					// Get the new distance
					float new_distance = route.calculate_total_distance(route.customers);

					if (new_distance < old_distance) {

						depots[depot_i].routes[route_i] = route;
						depots[depot_i].routes[route_i].total_distance = depots[depot_i].routes[route_i].calculate_total_distance(depots[depot_i].routes[route_i].customers);
						break;
					}
				}
			}

			// Swapping ===================================
			else {
				// Pick a depot
				int selected_depot = interval(0, num_depots);

				// Return if there is only route in there
				if (depots[selected_depot].get_n_routes() <= 1) return;

				// Pick two routes
				int selected_route1 = 0;
				int selected_route2 = 0;

				while (selected_route1 == selected_route2) {
					selected_route1 = interval(0, depots[selected_depot].get_n_routes());
					selected_route2 = interval(0, depots[selected_depot].get_n_routes());
				}

				// Pick a customer in route
				int selected_customer_index = interval(0, depots[selected_depot].routes[selected_route1].customers.size());
				Customer customer = depots[selected_depot].routes[selected_route1].customers[selected_customer_index];

				// Check if feasibility maintained by this mutation
				// Do not mutate if feasibility is broken
				
				if (depots[selected_depot].routes[selected_route2].check_capacity(customer)) {
					// Add that customer to route2
					depots[selected_depot].routes[selected_route2].add_customer(customer);

					// Remove the customer from route1
					depots[selected_depot].routes[selected_route1].remove_customer_at(selected_customer_index);

					if (depots[selected_depot].routes[selected_route1].customers.empty()) depots[selected_depot].remove_route_at(selected_route1);
				}
				
			}
			
		}
		
		// Inter-depot
		if ( iteration % 10 == 0 ) 
			if (0.25 >= get_prob()) {
				// Hold the borderline customers
				vector <int> depot_list;

				// Look for a borderline customer in randomly chosen depot
				int selected_depot = interval(0, num_depots);

				// Find a customer that that might have a depot that is close by as well
				while (true) {

					// Pick a customer at random
					Customer customer = depots[selected_depot].customers[ interval(0, depots[selected_depot].customers.size()) ];

					// Go through other depots
					for (int d = 0; d < depots.size(); d++) {
						if (depots[d].id != depots[selected_depot].id) {

							float ratio = ( ( distance(customer.x, customer.y, depots[d].x, depots[d].y) - distance(customer.x, customer.y, depots[selected_depot].x, depots[selected_depot].y) ) / distance(customer.x, customer.y, depots[selected_depot].x, depots[selected_depot].y));
							
							if (abs(ratio) <= 0.2) depot_list.push_back(d);
							
						}
					}
					
					// We found another depot, hurray!
					if ( !depot_list.empty() ) {

						// PRandomly pick one from the list
						int new_depot = depot_list[ interval(0, depot_list.size())];
						
						// Push it into the new depot and schedule new routes
						depots[new_depot].routes.clear();
						depots[new_depot].add_customer(customer);
						depots[new_depot].schedule(true, true);

						// Remove the customer from the old depot
						depots[selected_depot].remove_customer(customer);
						clean_up();
						break;
					}
					else {
						break;
					}
				}
			
			}
	}

	// Analytics

	// Prints the Depot IDs and assigned customers to it
	void print_simple() {
		// Print information about the depots and which customers it serves
		for (int d = 0; d < num_depots; d++) {
			cout << "Depot ID:" << depots[d].id << " at " << depots[d].x << depots[d].y << "\n";

			for (int r = 0; r < depots[d].routes.size(); r++) {
				cout << "Route " << r << "\n";
				for (int c = 0; c < depots[d].routes[r].customers.size(); c++) {
					cout << "ID:" << depots[d].routes[r].customers[c].id << " " << depots[d].routes[r].customers[c].demand << " ";
				}
				cout << "\n";
			}
			cout << "\n";
		}

		cout << "\n\n";

	}

	// Saves the information about the individual into a file to be plotted by python
	void plot_data(string filename = "") {
		
		string file = "./plots/plot";

		ofstream plot_file(file.append(filename));

		// Save information about the depots and which customers it serves
		// The format is: 
		// DepotID, depotX, depotY, newline
		// All customers:
		// CustomerID, CustomerX, customerY, newline
		// |
		
		for (int d = 0; d < num_depots; d++) {
	
			plot_file << depots[d].id << " " << depots[d].x << " " << depots[d].y << "\n";

			for (int r = 0; r < depots[d].routes.size(); r++) {
				for (int c = 0; c < depots[d].routes[r].customers.size(); c++) {
					plot_file << depots[d].routes[r].customers[c].id << " " << depots[d].routes[r].customers[c].x << " " << depots[d].routes[r].customers[c].y << "\n";
				}
				plot_file << "|\n";
			}

			plot_file << "/";
		}
		
	}

	// Prints out routes per depot
	void print_routes() {

		cout << "Fitness: " << get_fitness() << "\n";

		for (int d = 0; d < num_depots; d++) {
			cout << "Depot ID: " << depots[d].id << "\n";
			for (int r = 0; r < depots[d].routes.size(); r++ ) {
				cout << "Route number: " << r << " Length: "<< depots[d].routes[r].total_distance << "; Capacity: " << depots[d].routes[r].vehicle_capacity << "; Clients: ";
				for (int c = 0; c < depots[d].routes[r].customers.size(); c++) {
					cout << depots[d].routes[r].customers[c].id << " ";
				}
				cout << "\n";
			}
			cout << "\n\n";
		}
	}


	// Helpers

	// Returns True if there is no problem with feasibility in every route of every depot
	bool is_feasible() {
		for (Depot depot : depots) {
			for (Route route : depot.routes) {
				if (route.vehicle_capacity < 0) {
					return false;
				}
			}
		}
		return true;
	}

	// Cleans up empty routes in all the depots
	void clean_up() {
		for (Depot & depot : depots) {
			depot.remove_empty_routes();
		}
	}

	// Overloading equality to easily compare Individual objects
	bool operator==(Individual A) {
		
		string ind1 = "";
		string ind2 = "";

		for (Depot &depot : this->depots) {
			for (Route &route : depot.routes) {
				for (Customer &customer : route.customers)
				ind1 += to_string(customer.id);
			}
		}

		for (Depot& depot : A.depots) {
			for (Route& route : depot.routes) {
				for (Customer& customer : route.customers)
					ind2 += to_string(customer.id);
			}
		}

		return ind1 == ind2;
	}

};
