#!/bin/bash

#swig -python -c++ calc_fit.i
#c++ -flto -Ofast -mtune=native -march=native -fPIC -c calc_fit.cpp calc_fit_wrap.cxx -I/Users/ljxowen/opt/anaconda3_arm64/anaconda3/include/python3.11
#c++ -shared calc_fit.o calc_fit_wrap.o -o _calc_fit.so -L/Users/ljxowen/opt/anaconda3_arm64/anaconda3/lib -lpython3.11

swig -python -c++ calc_fit.i

c++ -flto -Ofast -mtune=native -march=native -fPIC -c calc_fit.cpp calc_fit_wrap.cxx \
    -I/Users/ljxowen/opt/anaconda3_arm64/anaconda3/envs/swig_env/include/python3.11

c++ -shared calc_fit.o calc_fit_wrap.o -o _calc_fit.so -undefined dynamic_lookup

    
