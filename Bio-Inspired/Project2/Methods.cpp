#include <vector>
#include <string>
#include <iostream>
#include <fstream>
#include <chrono>
#include <thread>

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
	
	// Create generations
	for (int i = 0; i < 50; i++) {

		// Clean up the old selected_population 
		selected_population.clear();
		parents.clear();

		// Select parents - populates parents vector
		parent_selection(true);

		// Create offspring using recombination - populates selected_population
		create_offspring();

		// Elitism
		Individual best = best_solution();
		for (int i = 0; i < population_size / 100; i++) {
			selected_population[interval(0, selected_population.size())] = best;
		}		
		
		// Replace the old population with new offspring + elitist parents
		population.clear();
		population = selected_population;

		// Mutation
		for (Individual& individual : population) individual.mutation(mutation_prob, i);

		// Retain only good ones from the big chunk of the population
		survival_selection();

		// Decaying mutation
		//mutation_prob *= 0.99;
		
		//cout << "Average: " << average_fitness() << endl;
		cout << i << "Best Solution so far: " << best_solution().get_fitness() << endl;
		//cout << "Population size: " << population.size() << endl;
	}
	cout << best_solution().get_fitness();
	best_solution().plot_data();
	best_solution().print_routes();
}


// Generates the initial population of size p_size
void GA::generate_init_pop() {

	// Generate population_size number of individuals
	for (int i = 0; i < population_size; i++) {
		population.push_back( Individual( mnt, customer_data, depot_data, dur_load, rng ) );
	}

}

// Tournament selection 
void GA::parent_selection(bool binary) {

	// Select parenst for reproduction. 
	while (parents.size() < population_size/2) {
		
		// Binary tournament selection
		if (binary) {
		
			// Pick two random individuals
			int index1 = 0;
			int index2 = 0;

			while (index1 == index2) {
				// Pick two random indexes
				index1 = interval( 0, population.size() );
				index2 = interval( 0, population.size());
			}

			// Pick the fittest one with prob 0.8
			if (get_prob() <= 0.8) {
				if (population[index1].get_fitness() >= population[index1].get_fitness()) 
					parents.push_back(population[index1]);
				else 
					parents.push_back(population[index2]);
			}
			// Else, pick one randomly
			else {
				if (get_prob() <= 0.5) {
					parents.push_back(population[index1]);
				}
				else {
					parents.push_back(population[index2]);
				}
			}

		} 
		// k-Tournament selection with 10 spots

		else {
			vector <Individual> selected;

			// Get 10 random individuals into the selected
			while (selected.size() <= 10) {
				selected.push_back(population[interval(0, population.size())]);
			}

			// Comparison functiosn for finding the fittest ones
			auto comp = [](Individual & one, Individual & two) {
				return (one.get_fitness() < two.get_fitness());
			};

			// Pick the fittest one with prob 0.8
			if (get_prob() <= 0.8) {
				/*
				sort(begin(selected), end(selected), comp);
				parents.push_back(selected[0]);
				*/
				float best_fitness = selected[0].get_fitness();
				Individual best_parent = selected[0];

				for (int p = 1; p < selected.size(); p++) {
					float new_fitness = selected[p].get_fitness();
					if (new_fitness < best_fitness) {
						best_parent = selected[p];
						best_fitness = new_fitness;
					}
				}
				parents.push_back( best_parent);

			}
			else {
				parents.push_back( selected[interval(0, selected.size())] );
			}
		}
	}
		
}

void GA::create_offspring() {

	// Mating with incest prevention
	while (selected_population.size() < population_size) {
		
		// Recombination

		// Randomly pick parents for mating
		int index1 = 0;
		int index2 = 0;

		while (index1 == index2 && parents[index1] == parents[index2] )  {
			// Pick two random indexes
			index1 = interval(0, parents.size());
			index2 = interval(0, parents.size());
		}

		// Pick and copy two parents. These are the ones that will mate
		Individual p1 = parents[index1];
		Individual p2 = parents[index2];

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
		auto comp = [](Loc &one, Loc &two) {
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
				for (int i = 0; i <= route.customers.size(); i++) {

					// Create a new insertion_position
					insertion_positions.push_back(Loc());

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
		if (p1.is_feasible()) {
			p1.clean_up();
			selected_population.push_back(p1);
		}

		if (p2.is_feasible()) {
			p2.clean_up();
			selected_population.push_back(p2);
		}
	}

}

void GA::survival_selection() {
	
	// Erase infeasible individuals
	population.erase(
		remove_if(
			population.begin(), population.end(),
			[](Individual & ind) { return ! ind.is_feasible(); }),
		population.end());	


	// Filter out the clones
	/*
	vector <Individual> unique;
	unique.push_back(population[0]);

	for (Individual& individual : population) {
		bool is_copy = false;
		for (Individual & ind : unique) {

			if (individual == ind) {
				is_copy = true;
				break;
			}
		}
		if (!is_copy) unique.push_back(individual);
	}
	
	population.clear();
	population = unique;
	*/


	// Comparator lambda for sorting 
	auto comp = [](Individual& one, Individual& two) {
		return (one.get_fitness() < two.get_fitness());
	};
	
	// Keep only the best ones - survival pressure	
	
	//sort(population.begin(), population.end(), comp);

	// Trim the eccess	
	if (population.size() > population_size)
		population.erase( population.begin() + population_size, population.end());
	
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
	float best_fitness = population[0].get_fitness();

	for (Individual& individual : population) {
		float new_fitness = individual.get_fitness();
		if (new_fitness < best_fitness) {
			best_individual = individual;
			best_fitness = new_fitness;
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

