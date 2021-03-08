#include <vector> 
#include "Depot.h"
#include <math.h>     
#include <iostream>
#include <fstream>
#include <string>

using namespace std;


class Individual {
public:

	// Parameters from the solution files for easy access
	int num_vehicles;
	int num_customers;
	int num_depots;

	// An individual consists of vectors with depots
	vector<Depot> depots;

	// Data for printing
	vector<int> customer_data;

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
				float new_distance = calc_distance(depots[d], customer_data[1 + 5 * c], customer_data[2 + 5 * c] );

				// If the new distance is shorter, save that info
				if (new_distance < depot_distance) {
					depot_distance = new_distance;
					depot_index = d;
				}
			}

			// The customer c is added to the depots route (the +1 is needed because ids start at 1)
			depots[depot_index].add_customer(Customer(customer_data[5 * c], customer_data[1 + 5 * c], customer_data[2 + 5 * c] , customer_data[4 + 5 * c]));

		}

		// Now that everything is initialized, deplot the initial scheduler in Depots
		for (int d = 0; d < num_depots; d++) {
			depots[d].schedule();
		}

		//print_simple();
		//plot_data();
		print_routes();
	}

	// Returns euclidian distance between the Depot and customer coordinates c_x and c_y
	float calc_distance(Depot depot, int c_x, int c_y) {
		return sqrt( pow(depot.x - c_x , 2) + pow(depot.y - c_y, 2) );
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
	void plot_data() {
		
		ofstream plot_file ("./plots/plot");

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
		for (int d = 0; d < num_depots; d++) {
			cout << "Depot ID: " << depots[d].id << "\n";
			for (int r = 0; r < depots[d].routes.size(); r++ ) {
				cout << "Route number: " << r << " Clients: ";
				for (int c = 0; c < depots[d].routes[r].customers.size(); c++) {
					cout << depots[d].routes[r].customers[c].id << " ";
				}
				cout << "\n";
			}
			cout << "\n\n";
		}
	}

};
