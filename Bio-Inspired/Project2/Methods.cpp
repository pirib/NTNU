#include <vector>
#include <string>
#include <iostream>
#include <fstream>

#include "GA.h"
#include "gfun.h"

using namespace std;
using namespace gfun;

// Brings everything together
void GA::run(string file_name) {
	
	// Reads the specified problem file 
	read_problem_file(file_name);

	// Generate the inital population
	generate_init_pop();
	
	
	for (int i = 0; i < 100 ; i++) {
		// Select parents
		parent_selection();

		// Create offspring using recombination 
		create_offspring();
	
		population.clear(); 
		population = selected_population;

		mutation();
		
		//cout << "Population size: " << population.size() << endl;
		//cout << "; Average fitness is: " << average_fitness() << endl;

		//best_solution().print_routes();

	}
	
}


// Generates the initial population of size p_size
void GA::generate_init_pop( ) {

	// Generate population_size number of individuals
	for (int i = 0; i < population_size; i++) {
		population.push_back( Individual( mnt, customer_data, depot_data, dur_load ) );
	}

}

// Tournament selection 
void GA::parent_selection() {

	// Clean up the old selected_population 
	selected_population.clear();

	// Select parenst for reproduction. Selected pool is roughly 50% of the original population size
	while (selected_population.size() < population_size/2) {

		// Pick two random individuals
		int index1 = 0;
		int index2 = 0;

		while (index1 == index2) {
			// Pick two random indexes
			index1 = interval(0, population_size );
			index2 = interval(0, population_size );
		}

		// Pick the fittest one with prob 0.8
		if (get_prob() < 0.8) {
			if (population[index1].get_fitness() >= population[index1].get_fitness()) 
				selected_population.push_back(population[index1]);
			else 
				selected_population.push_back(population[index2]);
		}
		// Else, pick one randomly
		else {
			if (get_prob() < 0.5) {
				selected_population.push_back(population[index1]);
			}
			else {
				selected_population.push_back(population[index2]);
			}
		}
	}
		
}

void GA::create_offspring() {

	while (selected_population.size() < population_size ) {
		// Recombination
	
		// Randomly pick parents for mating
		int index1 = 0;
		int index2 = 0;

		while (index1 == index2) {
			// Pick two random indexes
			index1 = interval(0, selected_population.size());
			index2 = interval(0, selected_population.size());
		}

		// Pick and copy two parents. These are the ones that will mate
		Individual p1 = selected_population[index1];
		Individual p2 = selected_population[index2];

		// Pick a depot for recombination
		int selected_depot = interval(0, mnt[2]);
	
		// Randomly select a route from each parent's depot
		int selected_route_p1 = interval(0, p1.depots[selected_depot].routes.size());
		int selected_route_p2 = interval(0, p2.depots[selected_depot].routes.size());

		// The customers that are to be deleted from p2 and p1
		vector<Customer> customersFromP1 = p1.depots[selected_depot].routes[selected_route_p1].customers;
		vector<Customer> customersFromP2 = p2.depots[selected_depot].routes[selected_route_p2].customers;
		

		// Old Debugging, delete when done
		/*
		cout << endl << "Customers from p1 are: " << endl;
		for (Customer customer : p1.depots[selected_depot].routes[selected_route_p1].customers) {
			cout << customer.id << " ";
		}
		cout << endl;
	
		cout << endl << "Customers from p2 are: " << endl;
		for (Customer customer : p2.depots[selected_depot].routes[selected_route_p2].customers) {
			cout << customer.id << " ";
		}
		cout << endl;

		cout << "P1 before recombination " << endl;
		p1.print_routes();
		cout << endl;


		cout << "P2 before recombination " << endl;
		p2.print_routes();
		cout << endl;
		*/

		// ================== Remove all customers that route1 in parent 1 is in parent2


		// Removing that customer from all the routes
		// Looping throughs Depots in p2
		for (int d = 0; d < p2.depots.size(); d++) {
			// Looping through Routes
			for (int r = 0; r < p2.depots[d].routes.size(); r++) {
				// Loooping through customers in the routes
				for (Customer c : customersFromP1) {
					p2.depots[d].routes[r].remove_customer(c.id);
				}
				
			}
		}
		
		// Looping throughs Depots in p1
		for (int d = 0; d < p1.depots.size(); d++) {
			// Looping through Routes
			for (int r = 0; r < p1.depots[d].routes.size(); r++) {
				// Loooping through customers in the routes
				for (Customer c : customersFromP2) {
					p1.depots[d].routes[r].remove_customer(c.id);
				}

			}
		}
			
		// ================== Compute the insertion cost

		// Struct for deciding where to insert the new customers
		struct Loc {
			int index;
			bool feas;
			int cost;
			int route;
		};

		// Comparator function for sorting the insertion_positions
		auto comp = [](Loc one, Loc two) {
			return (one.cost < two.cost);
		};

		
		// For each customer that needs to be inserted from P1
		for (Customer customer : customersFromP1) {

			// Temp vector to store all the information about insertion positions
			vector<Loc> insertion_positions;
		
			// ============================== Finding the best spots for insertion

			// For each route in p2
			int route_index = 0;
			for (Route route : p2.depots[selected_depot].routes) {
			
				// For each possible insertion position
				for (int i = 0; i <= route.customers.size() ; i++ ) {

					// Create a new insertion_position
					insertion_positions.push_back( Loc() );

					// Populate data
					insertion_positions.back().feas = route.check_capacity(customer);
					insertion_positions.back().index = i;
					insertion_positions.back().route = route_index;

					vector<Customer> temp = route.customers;

					temp.insert(temp.begin() + i, customer);

					insertion_positions.back().cost = route.calculate_total_distance(temp);
				
				}

				// Lazy way of finding the route's index
				route_index++;

			}
	
			// Sort the list using lambda comp (the location that leads to smallest travel cost added is used).
			sort(insertion_positions.begin(), insertion_positions.end(), comp);
		

			// =================== Insert the customers back into the individuals
			
			if (get_prob() <= 0.8) {

				// Choose the first feasible insertion location.
				bool inserted = false;

				for (Loc loc : insertion_positions) {
					if (loc.feas) {
						p2.depots[selected_depot].routes[insertion_positions[0].route].insert_customer(customer, insertion_positions[0].index);
						inserted = true;
						break;
					}
				}

				// If there are no feasible locations, create a new route and add the customer in there
				if (inserted == false) {
					p2.depots[selected_depot].add_route();
					p2.depots[selected_depot].routes.back().add_customer(customer);
				}

			}
			// Just shove the customer into the
			else {
				p2.depots[selected_depot].routes[insertion_positions[0].route].insert_customer(customer, 0);
			}
			
		}

		
		// For each customer in route2
		for (Customer customer : customersFromP2) {

			// Temp vector to store all the information about insertion positions
			vector<Loc> insertion_positions;

			// ============================== Finding the best spots for insertion

			// For each route in p2
			int index = 0;
			for (Route route : p1.depots[selected_depot].routes) {

				// For each possible insertion position
				for (int i = 0; i <= route.customers.size(); i++) {

					// Create a new insertion_position
					insertion_positions.push_back(Loc());

					// Populate data
					insertion_positions.back().feas = route.check_capacity(customer);
					insertion_positions.back().index = i;
					insertion_positions.back().route = index;

					vector<Customer> temp = route.customers;
					temp.insert(temp.begin() + i, customer);

					insertion_positions.back().cost = route.calculate_total_distance(temp);

				}

				// Lazy way of finding the route's index
				index++;

			}

			// Sort the list using lambda comp (the location that leads to smallest travel cost added is used).
			sort(insertion_positions.begin(), insertion_positions.end(), comp);


			// =================== Insert the customers back into the individuals

			if (get_prob() <= 0.8) {

				// Choose the first feasible insertion location.
				bool inserted = false;

				for (Loc loc : insertion_positions) {
					if (loc.feas) {
						p1.depots[selected_depot].routes[insertion_positions[0].route].insert_customer(customer, insertion_positions[0].index);
						inserted = true;
						break;
					}
				}

				// If there are no feasible locations, create a new route and add the customer in there
				if (inserted == false) {
					p1.depots[selected_depot].add_route();
					p1.depots[selected_depot].routes.back().add_customer(customer);
				}

			}
			// Just shove the customer into the
			else {
				p1.depots[selected_depot].routes[insertion_positions[0].route].insert_customer(customer, 0);
			}

		}

		// Old debugging code, remove when done
		/*
		cout << "P1 after recombination " << endl;
		p1.print_routes();
		cout << endl;

		cout << "P2 after recombination " << endl;
		p2.print_routes();
		cout << endl;
		*/


		// Add the newly created children into the selection_population if they are feasible
		if (p1.is_feasible())
			selected_population.push_back(p1);
		
		if (p2.is_feasible())
			selected_population.push_back(p2);
	}

}

void GA::mutation() {

		// Loop through each individual and apply mutation
		for (Individual & individual : selected_population ) { 
			if (mutation_prob >= get_prob()) {

				// Inter-Depot Mutation 
	
				// Choose one mutation with equal probability
				int mut_type = interval(0,3);

				// Reversal Mutation ===================================
				if (mut_type == 0) {


				}

				// Single customer re-routing ===================================

				// Swapping ===================================
				if (mut_type == 2) {
			
					cout << endl << "Mutation! " << endl;
			
					// Pick a depot
					int selected_depot = interval(0, mnt[2]);

					// Return if there is only route in there
					if (individual.depots[selected_depot].get_n_routes() <= 1) return;

					// Pick two routes
					int selected_route1 = 0;
					int selected_route2 = 0;

					while (selected_route1 == selected_route2) {
						selected_route1 = interval(0, individual.depots[selected_depot].get_n_routes());
						selected_route2 = interval(0, individual.depots[selected_depot].get_n_routes());
					}

					// Debugging
					cout << "Selected routes are " << selected_route1 << " " << selected_route2 << endl;
					cout << "Routes in the Depot " << individual.depots[selected_depot].id << " before mutation: " << endl;
					individual.print_routes();

					// Pick a customer in route1
					int selected_customer_index = interval(0, individual.depots[selected_depot].routes[selected_route1].customers.size());
					Customer customer = individual.depots[selected_depot].routes[selected_route1].customers[selected_customer_index];

					// Check if feasibility maintained by this mutation
					// Do not mutate if feasibility 
					if (individual.depots[selected_depot].routes[selected_route2].check_capacity(customer) ) {
						// Add that customer to route2
						individual.depots[selected_depot].routes[selected_route2].add_customer(customer);

						// Remove the customer from route1
						individual.depots[selected_depot].routes[selected_route1].remove_customer_at(selected_customer_index);

						cout << endl << "Routes in the Depot after mutation: " << endl;
						individual.print_routes();
					}
				}
			}

		}

}

void GA::survival_selection() {
	// TODO recombination can create infeasible individueals - remove them

}





// Helpers ===================================================================

// Analytics
 
// Returns the average fitness of the population
float GA::average_fitness() {

	float total_fitness = 0;

	for (int i = 0; i < population.size(); i++) {
		total_fitness += population[i].get_fitness();
	}

	return total_fitness / population.size();

}

// Returns the individual with the best solution (e.g. min fitness)
Individual GA::best_solution() {

	// Assign the first individual as the current best one
	Individual best_individual = population[0];

	for (int i = 1; i < population.size(); i++) {
		if (population[i].get_fitness() < best_individual.get_fitness()) {
			best_individual = population[i];
		}
	}

	return best_individual;

}


// Others

// Reads the problem file
void GA::read_problem_file(string file_name) {

	// Helper stuff
	int temp;

	// Open the file using relative path
	ifstream problem_file;
	problem_file.open("./Data/DataFiles/" + file_name);

	// Debugging purposes
	if (!problem_file) std::cerr << "Could not open the file!" << std::endl;

	// Getting the first three values num_vehicles, num_customers, num_depots
	for (int i = 0; i < 3; i ++ ) {
		problem_file >> temp;
		mnt.push_back(temp);
	}
	
	// Getting the next depot_num of values into dur_load
	for (int i = 0; i < mnt[0]; i++) {
		for (int n = 0; n < 2; n++ ) {
			problem_file >> temp;
			dur_load.push_back(temp);
		}
	}
	
	// Getting the next customer_number of values into customer_data
	for (int i = 0; i < mnt[1]; i++) {
		for (int n = 0; n < 5; n++) {
			problem_file >> temp;
			customer_data.push_back(temp);
		}
		problem_file.ignore(255,'\n');
	}

	// Getting depot_data
	for (int i = 0; i < mnt[2]; i++) {
		for (int n = 0; n < 3; n++) {
			problem_file >> temp;
			depot_data.push_back(temp);
		}
		problem_file.ignore(255, '\n');	
	}
	
	// Close the file
	problem_file.close();
}

