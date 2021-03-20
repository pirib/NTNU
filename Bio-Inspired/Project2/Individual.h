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

	// Data for printing
	vector<int> customer_data;

	// Cosntructors
	
	// Default Cosntructor
	Individual(){}

	// Constructor that creates depots with vehicles in them from scratch
	Individual(vector<int> mnt, vector<int> customer_data, vector<int> depot_data, vector<int> dur_load ) {

		// Data for printing
		this->customer_data = customer_data;

		// Populate GA parameters 
		num_vehicles = mnt[0];
		num_customers = mnt[1];
		num_depots = mnt[2];

		// Add depots according to the problem
		for (int depot = 0; depot < num_depots; depot++) {
			depots.push_back(Depot(num_vehicles, depot_data[0 + 3*depot], depot_data[1 + 3*depot], depot_data[2 + 3 * depot], dur_load));
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
	void mutation(float mutation_prob, default_random_engine & rng, int iteration) {

		// Intra-depot mutation
		if (mutation_prob >= get_prob()) {

			// Choose one mutation with equal probability
			int mut_type = interval(0, 2);

			// Reversal Mutation ===================================
			if (mut_type == 0) {

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

			}

			// Single customer re-routing ===================================
			/*
			else if (mut_type == 1) {

			}
			*/

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
				//cout << depots[selected_depot].routes[selected_route1].customers.size() << endl;
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
		if ( iteration % 5 == 0 ) 
			if (0.25 >= get_prob()) {
				// Hold the borderline customers
				vector <int> depot_list;

				// Look for a borderline customer in randomly chosen depot

				int selected_depot = interval(0, num_depots);

				int selected_route = interval(0, depots[selected_depot].routes.size());

				// For each customer, find a depot that is close by as well
				for (Customer& customer : depots[selected_depot].customers) {
					
					depot_list.clear();

					for (int d = 0; d < depots.size(); d++) {
						if (depots[d].id != depots[selected_depot].id) {
							float ratio = ((distance(customer.x, customer.y, depots[d].x, depots[d].y) - distance(customer.x, customer.y, depots[selected_depot].x, depots[selected_depot].y)) / distance(customer.x, customer.y, depots[selected_depot].x, depots[selected_depot].y));
							
							if (ratio <= 0.5) depot_list.push_back(d);
						
						}
					}
					
					// We found another depot, hurray!
					if (!depot_list.empty()) {

						// Randomly pick one from the list
						int new_depot = depot_list[0];
						
						// Push it into the new depot and schedule new routes
						depots[new_depot].routes.clear();
						depots[new_depot].add_customer(customer);
						depots[new_depot].schedule(true, false);

						// Remove the customer from the old depot
						depots[selected_depot].remove_customer(customer);
						clean_up();
						break;
					};
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
