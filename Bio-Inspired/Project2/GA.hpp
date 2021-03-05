#include <iostream>
#include <vector>
#include "Individual.hpp"

using namespace std;


class GA {
public:

	// Parameters
	int population_size;
	float mutation_prob;
	float threshold;

	// Parameters from the solution files
	int num_vehicles;
	int num_customers;
	int num_depots;


	// Members
	vector<Individual> population;


	// Constructor
	GA (	
			float threshold, 
			int population_size,			
			float mutation_prob
		) {

		// Setting parameters for easy access 
		this->population_size = population_size;
		this->threshold = threshold;
		this->mutation_prob = mutation_prob;
	
	}

	// Methods used in the class
	void run();
	void generate_init_pop(int population_size);
	void parent_selection();
	void create_offspring();
	void survival_selection();
	void mutation();

	// Helper methods
	void generate_individual();
	void fitness();
	void read_problem_file();

};




