#include "GA.hpp"

#include <vector>
#include <string>
#include <iostream>
#include <fstream>

using namespace std;



void GA::run() {

}


// Generates the initial population of size p_size
void GA::generate_init_pop( int p_size) {

}


void GA::parent_selection() {

}

void GA::create_offspring() {

}

void GA::survival_selection() {

}

void GA::mutation() {

}



// Helpers
void GA::generate_individual() {
}

void GA::fitness() {

}

void GA::read_problem_file() {

	// Helper stuff
	int temp;
	vector<int> mnt;
	vector<int> dur_load;
	vector<int> customer_data;
	vector<int> depot_data;

	// Open the file using relative path
	ifstream problem_file;
	problem_file.open("./Data/DataFiles/p01");

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