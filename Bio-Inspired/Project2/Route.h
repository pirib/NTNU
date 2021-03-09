#include <vector>
#include <iostream>

#include "gfun.h"

using namespace std;
using namespace gfun;


class Route {
public:

	// Customers along the route
	vector<Customer> customers;

	// Vehicle information
	int vehicle_duration;
	int vehicle_capacity;

	// Route distance
	float total_distance;

	// Depot info
	int d_x;
	int d_y;

	// Constructor
	Route(int veh_dur, int veh_load, int d_x, int d_y) {
		vehicle_duration = veh_dur;
		vehicle_capacity = veh_load;
		total_distance = 0;
		this->d_x = d_x;
		this->d_y = d_y;
	}

	// Adds a customer to the route. 
	void add_customer(Customer customer, bool back = true) {

		// Reduce the capacity of the vehicle of this route and add the customer to the route
		vehicle_capacity -= customer.demand;

		// Calculate and add the distance this route covers
		total_distance += distance(customer.x, customer.y, d_x, d_y);
		
		// Insert the new customer either into the back or front of the route
		if ( not back ) 
			customers.insert(customers.begin(), customer);
		else
			customers.push_back(customer);		

		// Recalculate the total distance
		total_distance = calculate_total_distance(customers);

	}


	// Removes customer at index index
	void remove_customer_at(int index) {

		// Remove the customer at the index
		customers.erase(customers.begin() + index);

		// Recalculate the total distance
		total_distance = calculate_total_distance(customers);
	}

	// Currently unused
	// Remove and return the customer from the vector based on its ID
	Customer remove_customer(int customer_id) {

		// Loop through the customers looking for the one with specified ID
		for (int c = 0; c < customers.size(); c++) {
			if (customers[c].id == customer_id) {

				// Add the vehicla cpaacity back
				vehicle_capacity += customers[c].demand;
				
				// Save the data about the customer
				Customer removed_customer = customers[c];

				// Remove the customer
				customers.erase(customers.begin() + c);

				// Return the previously saved one
				return removed_customer;
			}
		}

		cout << "Shit went wrong in remove_custoer in Route object";
	}

	// Returns true if the capacity of the route is fine given that the customer specified will be added
	bool check_capacity(Customer customer) {
		if (customer.demand <= vehicle_capacity) {
			return true;
		}
		return false;
	}

	float calculate_total_distance( vector<Customer> customers_list) {

		// Reset the total distance to 0
		int new_distance = 0;

		// Add distance between the depot to the first customer
		new_distance += distance(d_x, d_y, customers_list[0].x, customers_list[0].y);

		// Add distance between each customer as in order presented
		for (int c = 0; c < customers_list.size()-1; c++) {
			new_distance += distance(customers_list[c].x, customers_list[c].y, customers_list[c].y, customers_list[c+1].y);
		}

		// Add distance between last customer to the depot
		new_distance += distance(d_x, d_y, customers_list.back().x, customers_list.back().y);

		return new_distance;
	}

};