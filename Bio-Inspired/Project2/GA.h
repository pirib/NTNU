#include <iostream>
#include <vector>

#include "Individual.h"

using namespace std;


class GA {
public:

	// Parameters
	int population_size;
	float mutation_prob;
	float threshold;

	// Data from the problem file
	vector<int> mnt;
	vector<int> dur_load;
	vector<int> customer_data;
	vector<int> depot_data;

	// Members
	vector<Individual> population;
	vector<Individual> selected_population;

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
	void run(string file_name);
	void generate_init_pop();
	void parent_selection();
	void create_offspring();
	void survival_selection();
	void mutation();

	// Helper methods
	float average_fitness();
	Individual best_solution();
	void read_problem_file(string file_name);

	

};




