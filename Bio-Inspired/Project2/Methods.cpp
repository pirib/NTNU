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
	
	for (int i = 0; i < 10 ; i++) {
	// Select parents
		parent_selection();

		// Create offspring using recombination 
		create_offspring();
	
		population.clear(); 
		population = selected_population;
		
		//cout << "Population size: " << population.size() << endl;
		//cout << "Average fitness is: " << average_fitness() << endl;

		best_solution().print_routes();
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
		int index_depot = interval(0, mnt[2]);
	
		// Randomly select a route from each parent's depot
		int index_route_1 = interval(0, p1.depots[index_depot].routes.size());
		int index_route_2 = interval(0, p2.depots[index_depot].routes.size());

		// Remove all customers that route1 in parent 1 is in parent2
	
		// Looping through customers in route1 for parent1
		for (int c = 0; c < p1.depots[index_depot].routes[index_route_1].customers.size(); c++) {		
		
			// Removing that customer from all the routes
			// Looping throughs Depots
			for (int d = 0; d < p2.depots.size(); d++) {
				// Looping through Routes
				for (int r = 0; r < p2.depots[d].routes.size(); r++) {
					// Loooping through customers in the routes
					for (int cc = 0; cc < p2.depots[d].routes[r].customers.size(); cc ++) {
						// Remove the specified customer
						p2.depots[d].routes[r].remove_customer( p1.depots[index_depot].routes[index_route_1].customers[c].id );
					}
				}
			}
		
		}

		// Looping through customers in route2 of parent2
		for (int c = 0; c < p2.depots[index_depot].routes[index_route_2].customers.size(); c++) {

			// Removing that customer from all the routes
			// Looping throughs Depots
			for (int d = 0; d < p1.depots.size(); d++) {
				// Looping through Routes
				for (int r = 0; r < p1.depots[d].routes.size(); r++) {
					// Loooping through customers in the routes
					for (int cc = 0; cc < p1.depots[d].routes[r].customers.size(); cc++) {
						// Remove the specified customer
						p1.depots[d].routes[r].remove_customer(p2.depots[index_depot].routes[index_route_2].customers[c].id);
					}
				}
			}
		}

	
		// For each customer in route1
		for (Customer customer : p1.depots[index_depot].routes[index_route_1].customers) {

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

			// Temp vector to store all the information about insertion positions
			vector<Loc> insertion_positions;
		

			// ============================== Finding the best spots for insertion

			// For each route in p2
			int index = 0;
			for (Route route : p2.depots[index_depot].routes) {
			
				// For each possible insertion position
				for (int i = 0; i <= route.customers.size() ; i++ ) {

				// Create a new insertion_position
				insertion_positions.push_back( Loc() );

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
				

			}
			else {
				p2.depots[index_depot].routes[insertion_positions[0].route].insert_customer(customer, 0);
			}
			
			for (Loc loc : insertion_positions) {
				if (loc.feas) {
					p2.depots[index_depot].routes[insertion_positions[0].route].insert_customer(customer, insertion_positions[0].index);
					break;
				}	
			}
			
		}



		selected_population.push_back(p1);
		selected_population.push_back(p2);
	}
}

void GA::survival_selection() {

}

void GA::mutation() {

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

