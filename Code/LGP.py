from math import isinf
from random import sample
import numpy as np
import csv, sys, getopt
import gym
from tqdm import tqdm
import time


import ind_creation
import mutation
import fitness

def mean(vet) :
	if len(vet) > 0 :
		return (sum(vet))/len(vet)
	else :
		return float('+inf')

class LGP() :

	def __init__(self, params) :
		self.params = params

	def init_logs(self) :
		self.meanFit = []
		self.bestFit = []
		self.meanSizes = []
		self.bestSizes = []
		self.meanEffSizes = []
		self.bestEffSizes = []

	def update_logs(self) :

		sizes = [len(ind) for ind in self.pop]
		effSizes = [len(effInd) for effInd in self.effPop]

		npFit = np.array(self.fit)

		self.meanFit.append(np.nanmean(npFit))

		self.bestFit.append(self.fit[self.idxBestInd])

		self.meanSizes.append(mean(sizes))
		self.meanEffSizes.append(mean(effSizes))

		self.bestSizes.append(sizes[self.idxBestInd])
		self.bestEffSizes.append(effSizes[self.idxBestInd])

	def write_line_log(self, line, arqName) :
		archive = open(arqName, 'a', newline='')
		writer = csv.writer(archive, delimiter=',')
		writer.writerow(line)
		archive.close()

	def save_logs(self, gen) :

		#Find best individual found in the run
		bestEffInd = self.effPop[self.idxBestInd]
		bestEffProg = ind_creation.generate_program(bestEffInd, self.params)

		#Save found solution to logs
		archive = open(self.params.logDir + 'solutions', 'a')
		archive.write(bestEffProg + '\n' + '#'*80 + '\n')
		archive.close()

		#Save number of individual and instruction evaluations to optimum
		if (self.fit[self.idxBestInd][0] < self.params.stopValue) : 
			evals = gen*self.params.mi*self.params.lambd + self.params.mi
		else : evals = -1

		archive = open(self.params.logDir+'evaluations.csv', 'a')
		archive.write('%d\n' % evals)
		archive.close()

		archive = open(self.params.logDir+'instEvaluations.csv', 'a')
		if evals == -1 :
			archive.write('%d\n' % -1)
		else :
			archive.write('%d\n' % self.instEvals)
		archive.close()

		#Save fitness measures
		for i in range(len(self.params.fitMeasures)) :

			meanI = [x[i] for x in self.meanFit[len(self.meanFit)-1:]]
			bestI = [x[i] for x in self.bestFit[len(self.bestFit)-1:]]

			self.write_line_log(meanI, self.params.logDir+'mean_train_%s.csv'%self.params.fitMeasures[i])
			self.write_line_log(bestI, self.params.logDir+'best_train_%s.csv'%self.params.fitMeasures[i])

		#Save sizes
		self.write_line_log(self.meanSizes[len(self.meanSizes)-1:], self.params.logDir+'meanSizes.csv')
		self.write_line_log(self.bestSizes[len(self.bestSizes)-1:], self.params.logDir+'bestSizes.csv')
		self.write_line_log(self.meanEffSizes[len(self.meanEffSizes)-1:], self.params.logDir+'meanEffSizes.csv')
		self.write_line_log(self.bestEffSizes[len(self.bestEffSizes)-1:], self.params.logDir+'bestEffSizes.csv')

		if self.params.verbose :
			print('\nLogs saved in %s' % self.params.logDir)

	def info(self, gen) :
		if self.params.verbose :
			print('\nBest individual:')
			print(ind_creation.generate_program(self.effPop[self.idxBestInd], self.params))
			time.sleep(1)
			print('Generation %d' % gen)
			print('Best fitness : %.20f' % self.fit[self.idxBestInd])
			fits = self.fit
			print('Mean fitness train: %.20f' % mean(fits))
			print('Worst fitness train: %.20f' % min(fits))


	def tournament(self):

		#Select tournSize random individuals from population
		selected = sample(range(self.params.popSize), self.params.tournSize)
		fits = [self.fit[i] for i in selected]

		#Find winner and loser
		winner = max(range(len(fits)), key = lambda k: fits[k])
		loser = min(range(len(fits)), key = lambda k: fits[k])

		#Return winner and loser
		return selected[winner], selected[loser]

	def update_pop(self, idxWinner, idxLoser, newInd) :

		#Replace loser by copy of winner
		indCopywinner = self.pop[idxWinner]
		effIndCopyWinner = self.effPop[idxWinner]
		effInstsCopyWinner = self.effInsts[idxWinner]
		self.pop[idxLoser] = indCopywinner
		self.effPop[idxLoser] = effIndCopyWinner
		self.effInsts[idxLoser] = effInstsCopyWinner
		self.fit[idxLoser] = self.fit[idxWinner]

		#Replace winner by new
		effNewInd, effNewInsts = ind_creation.remove_introns(newInd, self.params)
		newFit = fitness.evaluate_ind(self.params.env, effNewInd)
		#self.instEvals = self.instEvals + len(effNewInd)

		if isinf(newFit) :
			return

		self.pop[idxWinner] = newInd
		self.effPop[idxWinner] = effNewInd
		self.effInsts[idxWinner] = effNewInsts
		self.fit[idxWinner] = newFit

	# def loop_gen(self) :

	# 	#Initialize new pop with the best current individual (elitism)
	# 	newPop = [self.pop[self.idxBestInd]]
	# 	newEffPop = [self.effPop[self.idxBestInd]]
	# 	newEffInsts = [self.effInsts[self.idxBestInd]]
	# 	newFitTrain = [self.fitTrain[self.idxBestInd]]
	# 	newFitTest = [self.fitTest[self.idxBestInd]]

	# 	for i in range(self.params.popSize-1) :

	# 		#Perform tournament
	# 		idxWinner = self.tournament()[0]

	# 		#Apply mutations
	# 		if self.params.singleActiveMut :
	# 			newInd = mutation.apply_mutations_single(self.pop[idxWinner], self.effInsts[idxWinner], self.params)
	# 		else :
	# 			newInd = mutation.apply_mutations_rate(self.pop[idxWinner], self.params)

	# 		newEffInd, effInstsNewInd = ind_creation.remove_introns(newInd, self.params)
	# 		newIndFitTrain = fitness.fit_ind(newEffInd, 'train', self.params)
	# 		newIndFitTest = fitness.fit_ind(newEffInd, 'test', self.params)
	# 		self.instEvals = self.instEvals + len(newEffInd)

	# 		#Add mutated ind in the new population
	# 		newPop.append(newInd)
	# 		newEffPop.append(newEffInd)
	# 		newEffInsts.append(effInstsNewInd)
	# 		newFitTrain.append(newIndFitTrain)
	# 		newFitTest.append(newIndFitTest)

	# 	#Replace current population
	# 	self.pop = newPop
	# 	self.effPop = newEffPop
	# 	self.effInsts = newEffInsts
	# 	self.fitTrain = newFitTrain
	# 	self.fitTest = newFitTest

	def loop_steady(self) :

		for i in range(int(self.params.popSize/2)) :

			#Perform two tournaments
			idxWinner1, idxLoser1 = self.tournament()
			idxWinner2, idxLoser2 = self.tournament()

			#Apply mutations
			if self.params.singleActiveMut :
				newInd1 = mutation.apply_mutations_single(self.pop[idxWinner1], self.effInsts[idxWinner1], self.params)
				newInd2 = mutation.apply_mutations_single(self.pop[idxWinner2], self.effInsts[idxWinner2], self.params)
			else :
				newInd1 = mutation.apply_mutations_rate(self.pop[idxWinner1], self.params)
				newInd2 = mutation.apply_mutations_rate(self.pop[idxWinner2], self.params)

			#Update of population
			self.update_pop(idxWinner1, idxLoser1, newInd1)
			self.update_pop(idxWinner2, idxLoser2, newInd2)

	# def loop_mi_lambda(self) :

	# 	for idx in range(self.params.mi) :

	# 		parent = self.pop[idx]
	# 		effParent = self.effPop[idx]
	# 		effInstsParent = self.effInsts[idx]

	# 		#Generate lambda offsprings
	# 		for i in range(self.params.lambd) :

	# 			#Apply mutations
	# 			if self.params.singleActiveMut :
	# 				newInd = mutation.apply_mutations_single(parent, effInstsParent, self.params)
	# 			else :
	# 				newInd = mutation.apply_mutations_rate(parent, self.params)
	# 			effNewInd, effNewInsts = ind_creation.remove_introns(newInd, self.params)
	# 			newIndFit = fitness.evaluate_ind(self.params.env, effNewInd)

	# 			#Replace original individual if offspring is better
	# 			if newIndFit <= self.fit[idx] :
	# 				self.pop[idx] = newInd
	# 				self.effPop[idx] = effNewInd
	# 				self.effInsts[idx] = effNewInsts
	# 				self.fit[idx] = newIndFit

	def run(self):

		#Set number of registers
		#Load dataset
		fitness.load_data(self.params)

		#Initialize population and fitness
		self.pop = ind_creation.create_pop(self.params)
		tuples = [ind_creation.remove_introns(ind, self.params) for ind in self.pop]
		self.effPop = [x[0] for x in tuples]
		self.effInsts = [x[1] for x in tuples]
		self.fit = fitness.evaluate_pop(self.params.env, self.effPop)
		#self.fitTest = fitness.evaluate_pop(self.effPop, 'test', self.params)

		#Initialize log variables
		self.init_logs()

		#Calculate index of best individual
		self.idxBestInd = max(range(len(self.fit)), key=lambda k: self.fit[k])

		#Initialize number of instruction evaluations
		#self.instEvals = sum([len(effInd) for effInd in self.effPop])

		#Update log data and show info
		self.update_logs()
		self.info(gen=0)

		#Loop for number of generations or number of instruction evaluations
		#gen = 0
		#while self.instEvals < self.params.maxInstEvals :
		for gen in tqdm(range(self.params.nGenerations), desc='Processing') :

			#Increment number of generations (only when using the budget on instruction evaluations)
			#gen = gen + 1
			#Stopping criterium
			if (self.fit[self.idxBestInd] > self.params.stopValue): break

			#Evolutionary loop
			if self.params.evoLoop == 'gen' :
				self.loop_gen()
			elif self.params.evoLoop == 'steady' :
				self.loop_steady()
			elif self.params.evoLoop == 'lambda' :
				self.loop_mi_lambda()

			#Calculate index of best individual
			self.fit = fitness.evaluate_pop(self.params.env, self.effPop)
			self.idxBestInd = max(range(len(self.fit)), key=lambda k: self.fit[k])

			#Update log data and show info
			self.update_logs()
			self.info(gen=gen+1)

		#self.save_logs(gen=gen)
		return self.pop[self.idxBestInd]
