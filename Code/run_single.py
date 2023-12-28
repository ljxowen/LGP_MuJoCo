import parameters
import LGP
import warnings
import gym
import fitness
import ind_creation
import matplotlib.pyplot as plt 
import multiprocessing
import calc_fit

warnings.filterwarnings("ignore", category=DeprecationWarning)


def main() :

	#Instanciate an object of class Parameters
	params = parameters.Parameters()	

	#Instantiate and run the LGP algorithm
	LGPAlg = LGP.LGP(params)

	best_ind = LGPAlg.run()

	params.envv = gym.make("Ant-v4", render_mode= "human")

	fit = fitness.evaluate_ind(params.envv, best_ind)

	print("The fitness: ", fit)
	print("The ind: ")
	print(ind_creation.generate_program(best_ind, LGPAlg.params))
	plt.plot(LGPAlg.bestFit, color='r', label='best fit')
	plt.plot(LGPAlg.meanFit, color='b', label='mean fit')
	plt.xlabel('Generation')
	plt.ylabel('Fitness')
	plt.legend()
	plt.show()

if __name__ == '__main__' :
	main()    

