import gym
from math import isnan
import numpy as np
import matplotlib.pyplot as plt
import time

import ind_creation
import calc_fit

#Parameters class
class Parameters() :

	def __init__(self) :

		#Non-terminal functions (implemented in calc_fit.cpp).
#		self.functions = 
#		self.functions = ['AND','NAND','OR','NOR']
		self.functions = ['AND','AND_INV1','XOR','OR'] + ['+', '-', '*', '/', 'sin', 'cos', 'e', 'ln']

		#Problem properties, path to directory where the data files are, and log directory.
		self.nDim = 27
		self.nOut = 8
		self.nRegisters = self.nDim + self.nOut
		#self.dataPath = '../datasets/benchmarks_regression/pagie1'
		#self.dataPath = '../datasets/benchmarks_circuits/mult3'
		self.env = gym.make('Ant-v4')
		self.logDir = '../logs/'

		#Fitness measures to be computed (first one is used for evolution).
#		self.fitMeasures = ['MAE']#, 'RMSE', 'SSE']
		#self.fitMeasures = ['PERC']

		#If validation is True, best ind in last generation is chosen using validation data.
		self.validation = False

		#Threshold for optimal solution.
		self.stopValue = 999999999

		self.verbose = True

		#Total number of registers used is equal to nDim + nExtraRegisters.
		self.nExtraRegisters = 10

		#When only micro-mutations are used, program size is constant and equal to initIndSize.
		self.initIndSize = 25
		self.maxIndSize = 50

		#popSize is used by generational and steady-state EAs, mi and lambd for (1+\lambda).
		self.popSize = 50
		self.mi = 50
		self.lambd = 1

		#Current implementation in LGP.py uses a budget on the number of effective instructions evaluated.
		self.nGenerations = 20
		self.maxInstEvals = 20

		#Tournament size, when it applies.
		self.tournSize = 10

		#Evolutionary scheme to be used (generational, steady-state, 1+\lambda).
#		self.evoLoop = 'gen'
		self.evoLoop = 'steady'
#		self.evoLoop = 'lambda'

		#Probability that a second argument will be a constant and the possible constants.
		self.probCons = 0.5
		self.consts = [float(const) for const in range(1,10)]

		#Mutation rate and probabilities of macro- and micro-mutations.
		self.mutRate = 0.01
		self.probMacroMut = 1.0
		self.probMicroMut = 1.0

		#If singleActiveMut is True, mutRate is ignored and single active mutation is applied.
		self.singleActiveMut = False

		self.funcArity = {'+':2,
			          '-':2,
			          '*':2,
			          '/':2,
			          'sin':1,
			          'cos':1,
			          'tan':1,
			          'htan':1,
			          'pow':2,
			          'sqrt':1,
			          'e':1,
			          'ln':1,
			          'AND':2,
			          'NAND':2,
			          'OR':2,
			          'NOR':2,
			          'AND_INV1':2,
			          'XOR':2,
			          'XNOR':2,
			          'NOT':1}

		self.funcPrint = {'+': ['', '+', ''],
			          '-': ['', '-', ''],
			          '*': ['', '*', ''],
			          '/': ['', '/', ''],
			          'sin': ['sin(', '', ')'],
			          'cos': ['cos(', '', ')'],
			          'tan': ['tan(', '', ')'],
			          'htan': ['htan(', '', ')'],
			          'pow': ['pow(', '', '', ')'],
			          'sqrt': ['sqrt(', '', ')'],
			          'e': ['e(', '', ')'],
			          'ln': ['ln(', '', ')'],
			          'AND': ['', 'AND', ''],
			          'NAND': ['', 'NAND', ''],
			          'OR': ['', 'OR', ''],
			          'NOR': ['', 'NOR', ''],
			          'AND_INV1': ['', 'AND_INV1', ''],
			          'XOR': ['', 'XOR', ''],
			          'XNOR': ['', 'XNOR', ''],
			          'NOT': ['', 'NOT', '']}

##
def auto_test() :
	#params = Parameters()
	#params.env.reset()
	#img = plt.imshow(params.env.render())
	env = gym.make("Swimmer-v4",render_mode= "human")
	observation = env.reset()
	print("Length of observation: ", len(observation[0]))
	time.sleep(5)
	#Auto-test
if __name__ == '__main__' :
	auto_test()