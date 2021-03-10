#pragma once

#include <math.h> 

namespace gfun {

	// TODO check that this actually returns floats
	// Calculates and retusn euclidian distance
	inline float distance(int x1, int y1, int x2, int y2){
		return sqrt( pow( x1 - x2 , 2) + pow(y1 - y2, 2) );

	}


}