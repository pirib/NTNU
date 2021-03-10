#include <vector>
#include <string>
#include <iostream>
#include <fstream>

#include "GA.hpp"

using namespace std;


// Brings everything together
void GA::run(string file_name) {
	
	// Reads the specified problem file 
	read_problem_file(file_name);

	// Generate the inital population
	generate_init_pop();


	// Analytics
	for (int i = 0; i < population.size(); i++) {
		population[i].plot_data(to_string(i));
		population[i].print_routes();
	}
}


// Generates the initial population of size p_size
void GA::generate_init_pop( ) {

	// Generate population_size number of individuals
	for (int i = 0; i < population_size; i++) {
		population.push_back( Individual( mnt, customer_data, depot_data, dur_load ) );
	}

}


void GA::parent_selection() {

}

void GA::create_offspring() {

}

void GA::survival_selection() {

}

void GA::mutation() {

}



// Helpers ===================================================================

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



// Currently unused
void GA::print_simple() {
	for (int in = 0; in < population_size; in++) {
		for (int d = 0; d < population[in].num_depots; d++) {
			
			cout << population[in].depots[d].id << " ";
		}
		
	}
}