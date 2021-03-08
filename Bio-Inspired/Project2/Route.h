using namespace std;
#include <vector>
#include <iostream>

class Route {
public:

	// Customers along the route
	vector<Customer> customers;

	// Vehicle information
	int vehicle_duration;
	int vehicle_capacity;

	// Constructor
	Route(int veh_dur, int veh_load) {
		vehicle_duration = veh_dur;
		vehicle_capacity = veh_load;
	}

	// Adds a customer to the route. 
	// Returns true if the customer was added with no problem, returns false if any constraints were violated
	bool add_customer(Customer customer) {

		// Check with the constraints first
		if (customer.demand > vehicle_capacity)
			return false;
		else {
			// Reduce the capacity of the vehicle of this route and add the customer to the route
			vehicle_capacity = vehicle_capacity - customer.demand;
			customers.push_back(customer);
		}
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

};