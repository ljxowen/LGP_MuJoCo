from math import isnan
import numpy as np
import parameters
import ind_creation
import calc_fit
import multiprocessing
import cv2

def load_data_aux(params) :
	observation = params.env.reset()
	global observation_mat
	observation_mat = np.array(observation[0])

def set_params_calc_fit() :

	r_aux = calc_fit.VecVecFloat()
	observation_aux = calc_fit.VecVecFloat()

	sizeJ = len(observation_mat)

	r_aux = [0 for j in range(sizeJ+8)] 
	observation_aux = observation_mat

	calc_fit.set_params(r_aux, observation_aux)


def load_data(params) :
	load_data_aux(params)
	set_params_calc_fit()

def action_wrapper(action):
	# Use numpy. tanh() to map the values in the list to the range of [-1, 1]
	return np.tanh(action).tolist()
	#return [max(-1.0, min(1.0, a)) for a in action]


#evaluates the fitness of an individual 
def evaluate_ind(env, ind):
	num_episode = 20
	fitness = 0
	for x in range(0, num_episode):
		done = False
		truncated = False
		observation = env.reset()
		observation = observation[0]
		#print("obser: ", observation)
		episode_reward = 0
		num_step = 0
		# evaluation episode
		while not (done or truncated):
			get_action = calc_fit.calc_vector(ind)
			#get_aciton = np.random.choice(get_action, size = 8, replace=False)
			get_action = get_action[-8:]
			action = action_wrapper(get_action)
			#print("action: ", action)
			try:
				observation, reward, done, truncated, info = env.step(action)
				#print("observation: ", observation)
				calc_fit.update_r(observation)
			except:
				return 0
			episode_reward += reward
			num_step += 1
		fitness += episode_reward
	#calc_fit.print_r()
	return (fitness/num_episode)



def evaluate_pop(env, pop):
	#fits = pool.map(evaluate_helper, [(env, ind) for ind in pop])
	return [evaluate_ind(env, ind) for ind in pop]


def auto_test() :

	ind = [['pow', '0', 'r0', 'c3.0'],
	       ['pow', '1', 'r1', 'c2.0'],
	       ['+', '0', 'r0', 'r1'],
	       ['+', '0', 'r0', 'r2']]

	# ind = [['AND', '4', 'r0', 'r1'],
	#        ['NOR', '5', 'r0', 'r1'],
	#        ['OR', '0', 'r4', 'r5'],
	#        ['AND', '4', 'r2', 'r3'],
	#        ['NOR', '5', 'r2', 'r3'],
	#        ['OR', '1', 'r4', 'r5'],
	#        ['AND', '4', 'r0', 'r1'],
	#        ['NOR', '5', 'r0', 'r1'],
	#        ['OR', '0', 'r4', 'r5']]

#	ind = ind_creation.create_ind(params)
#	ind, effInsts = ind_creation.remove_introns(ind, params)

	function = 'nguyen1'
#	function = 'par4'
	params = parameters.Parameters()
	load_data(params)
	fit = evaluate_ind(params.env, ind)
	print("The individual fitness: ", fit)

	pop = ind_creation.create_pop(params)
	fits = evaluate_pop(params.env, pop)
	print("The populaiton fitness: ", fits)


#Auto-test
if __name__ == '__main__' :
	auto_test()

