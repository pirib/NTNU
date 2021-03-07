#include <vector> 
#include "Depot.h"
#include <math.h>     
#include <iostream>
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
	Individual( vector<int> mnt, vector<int> customer_data, vector<int> depot_data ) {

		// Data for printing
		this->customer_data = customer_data;

		// Populate GA parameters 
		num_vehicles = mnt[0];
		num_customers = mnt[1];
		num_depots = mnt[2];


		// Add depots according to the problem
		for (int depot = 0; depot < num_depots; depot++) {
			depots.push_back(Depot(num_vehicles, depot_data[0 + 3*depot], depot_data[1 + 3*depot], depot_data[2 + 3 * depot]));
		}

		// Add and sort customers into the depots based on Euclidian distance
		for (int c = 0; c < num_customers; c++ ) {
			
			// Looking for the closest depot
			int depot_distance = 999999;
			int depot_index = 0;

			for (int d = 0; d < num_depots; d++) {
				int new_distance = calc_distance(depots[d], customer_data[1 + 5 * c], customer_data[2 + 5 * c] );

				// If the new distance is shorter, save that info
				if (new_distance < depot_distance) {
					depot_distance = new_distance;
					depot_index = d;
				}
			}

			// The customer c is added to the depots route (the +1 is needed because ids start at 1)
			depots[depot_index].add_customer(c+1);

		}
		print_data();
	}

	// Returns euclidian distance between the Depot and customer coordinates c_x and c_y
	float calc_distance(Depot depot, int c_x, int c_y) {
		return sqrt( pow(depot.x - c_x , 2) + pow(depot.y - c_y, 2) );
	}


	// Analytics
	void print_simple() {
		for (int d = 0; d < num_depots; d++) {
		
			cout << depots[d].id << " ";
		}
		cout << "\n";
	}

	// Prints information about each depot
	void print_data() {
		
		// Print information about the depots and which customers it serves
		for (int d = 0; d < num_depots; d++) {
			cout << "Depot ID:" << depots[d].id << " at " << depots[d].x << depots[d].y << "\n" << "Customers: ";

			for (int c = 0; c < depots[d].customers.size(); c++) {
				cout << "ID:" << depots[d].customers[c] << " ";
			}
			cout << "\n";
		}

		cout << "\n\n";

		// Printing the "grid"
		
		// Prep stuff
		int row = 100;
		int col = 100;

		vector<vector<string>> vec(row, vector<string>(col, "*"));

		for (int c = 0; c < num_customers; c++ ) {

			vec[customer_data[c * 5 + 1]][customer_data[c * 5 + 2]] = to_string(customer_data[c * 5]);

		}

		for (int d = 0; d < num_depots; d++) {
			vec[depots[d].x][depots[d].y] = "d";
		}

		// Prints the grid
		
		for (int v = 0; v < row; v++) {
			for (int vv = 0; vv < col; vv++) {
				cout << " " << vec[v][vv];
			}
			cout << "\n";
		}
		
	}

};
