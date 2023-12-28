#ifndef CALC_FIT_H__
#define CALC_FIT_H__

#include <stdlib.h>
#include <stdio.h>

#include <vector>
#include <string>
#include <numeric>
#include <cmath>

using namespace std;


extern vector<float> r;

void set_params(vector<float> r_aux, vector<float> observation_aux);
void update_r(vector<float> observation_aux);
void clean_r();
void print_r();
float division(float x, float y);
float square(float x);
float natLog(float x);
float tangent(float x);

vector<float> calc_vector(vector< vector<string> > ind);
//vector<float> calc_fit(vector< vector<string> > ind, string type, vector<string> measures);

#endif /* CALC_FIT__ */

