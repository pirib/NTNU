using namespace std;

class Customer {
public:

	// Customer has information about their id and x/y coordinates
	int id;
	int x;
	int y;

	// Constructor
	Customer(int id, int x, int y) {
		this->id = id;
		this->x = x;
		this->y = y;
	}

};