%module calc_fit
%{
#include "calc_fit.h"
%}

%include "std_vector.i"
%include "std_string.i"

namespace std {
    %template(VecString) vector<string>;
    %template(VecFloat) vector<float>;
    %template(VecVecFloat) vector<vector<float>>;
    %template(VecVecString) vector<vector<string>>;
}

using namespace std;

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

