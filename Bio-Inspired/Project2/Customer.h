#pragma once

class Customer {
public:

	// Customer has information about their id and x/y coordinates
	int id;
	int x;
	int y;
	int demand;

	// Constructor
	Customer(int id, int x, int y, int demand) {
		this->id = id;
		this->x = x;
		this->y = y;
		this->demand = demand;
	}

	// Overloading equality to easily compare Customer objects
	bool operator==(Customer A) {
		return this->id == A.id;
	}
};