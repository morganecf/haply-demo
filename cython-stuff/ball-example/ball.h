namespace shapes {
	class Ball {
		public: 
			int cx, cy;
			float r, v, m;
			int p[2];
			Ball(int cx, int cy, float r, float m);
			~Ball();
			int* getPos();
			float getRadius();
			float getVel();
			float getMass();
			void accelerate();
			void move(int dx, int dy);
	};
}