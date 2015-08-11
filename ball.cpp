#include <stdio.h>
#include <iostream>
#include <string>
#include <vector>
#include "ball.h"

using namespace std;

namespace shapes {

	Ball::Ball(int center_x, int center_y, float radius, float mass) {
		cx = center_x;
		cy = center_y;
		r = radius;
		m = mass;
		p[0] = cx;
		p[1] = cy;
		v = 0.0;
	}

	Ball::~Ball() {}

	int *Ball::getPos() { return p; }
	float Ball::getRadius () { return r; }
	float Ball::getVel() { return v; }
	float Ball::getMass() { return m; }

	void Ball::accelerate() {
		cout << "accelerating";
	}
	void Ball::move(int dx, int dy) {
		cout << "moving";
	}

}