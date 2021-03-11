#include <vector>

using namespace std;


namespace gfun {

	// Calculates and retusn euclidian distance
	float distance(int x1, int y1, int x2, int y2);

	// Get a random int between min and max intervals (both limits includsive) PS Not really uniform, but but 
	int interval(int min, int max);

	// Returns a random value between 0 and 1
	float get_prob();

}