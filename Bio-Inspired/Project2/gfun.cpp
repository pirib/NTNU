#include <math.h> 
#include <random>
#include <vector>
#include <chrono>

#include "gfun.h"

using namespace std;


// Calculates and retusn euclidian distance
float gfun::distance(int x1, int y1, int x2, int y2) {
	return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
}

// Get a random int between min and max intervals (max not inclusive)
int gfun::interval(int min, int max)
{
	return min + (rand() % static_cast<int>(max - min ));
}

// Returns a random value between 0 and 1
float gfun::get_prob() {
	return ((double)rand() / (RAND_MAX));
}
