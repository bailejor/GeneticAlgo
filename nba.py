from bs4 import BeautifulSoup 
import requests
import pandas as pd
import numpy as np
import random as rnd

#######GET SEASON PLAYER DATA###################################################
'''url = "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"

page = requests.get(url)

soup = BeautifulSoup(page.content, 'html.parser')

soup.findAll('tr', limit=2)
headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]
headers = headers[1:]

rows = soup.findAll('tr')[1:]
player_stats = [[td.getText() for td in rows[i].findAll('td')]
            for i in range(len(rows))]
stats = pd.DataFrame(player_stats, columns = headers)
print(stats.head(10))'''

#######GET SEASON PLAYER DATA###################################################

#######Fitness Function#########################################################

#Bonus points for average opponent rank lower than X
#Bonus points for home court advantage higher than X
#Bonus points for avg minutes

#Points for each point +1
#Points for 3PT shot +0.5
#Points for Rebounds +1.25
#Points for assists +1.5
#Points for Steals +2
#Points for blocks +2
#Points for turnover -0.5
#Points for double-double +1.5
#Points for triple-double +3

#Lineup requirements: 1PG, 1SG, 1SF, 1PF, 1C, 1G(PG, SG), 1F (SF, PF), 1 UTIL (PG, SG, SF, PF, C)

df = pd.read_csv('dksalaries-3.csv', header = 0)

point_guard = pd.DataFrame()
shooting_guard = pd.DataFrame()
guard = pd.DataFrame()
small_fwd = pd.DataFrame()
power_fwd = pd.DataFrame()
center = pd.DataFrame()
fwd = pd.DataFrame()
util = pd.DataFrame()

#Put all PG candidates in list
point_guard = df.loc[df['Position'].isin(['PG', 'PG/SG', 'PG/SF'])]

#Put all SG candidates in list
shooting_guard = df.loc[df['Position'].isin(['SG', 'PG/SG', 'SG/SF'])]

#Put all G candidates in list
guard = df.loc[df['Position'].isin(['PG', 'PG/SG', 'PG/SF', 'SG', 'PG/SF', 'SG/SF'])]

#Put all SF candidates in list
small_fwd = df.loc[df['Position'].isin(['SF', 'PG/SF', 'SG/SF', 'SF/PF'])]

#Put all PF in list
power_fwd = df.loc[df['Position'].isin(['PF', 'PF/C', 'SF/PF'])]

#Put all C in list
center = df.loc[df['Position'].isin(['C', 'PF/C'])]

#Put all FWD in list
fwd = df.loc[df['Position'].isin(['PF', 'PF/C', 'SF/PF', 'SF', 'PG/SF', 'SG/SF', 'SF/PF'])]

#Put all util in list
util = df


def subsequent_fitness_func(fittest_chroms, child_gen, under_cost):
	child_max = child_gen
	parent_max = fittest_chroms
	child_score = []
	parent_score = []
	non_identical_children = []

	#Append items to list if the total is not above $50k
	child_max = [x for x in child_max if (x[0][5] + x[1][5] + x[2][5] + x[3][5] + x[4][5] + x[5][5] + x[6][5] + x[7][5]) < 50000]
	
	for i in child_max:
		ident_list = []
		for j in range(0, 8):
			ident_list.append(i[j][2])
			#print(ident_list)
		#Check if there are any identicals in the player names if not, append to list
		if len(set(ident_list)) != len(ident_list):
			#print("duplicate found")
			pass
		else:
			non_identical_children.append(i)
	#print(non_identical_children)
	child_max = non_identical_children

	#FIGURE OUT HOW TO MAKE SURE THERE ARE NO DUPLICATE PLAYERS
	#seen = set()
	#child_max = [x for x in child_max if not (x[0][2] + x[1][2] + x[2][2] + x[3][2] + x[4][2] + x[5][2] + x[6][2] + x[7][2]) < 50000]

	score_parent = 0
	score_child = 0
	for index, chromosome in enumerate(parent_max):
		score_parent = 0
		for i in range(0, 7):
			score_parent = chromosome[i][8] + score_parent
			index = index
		parent_score.append(score_parent)

	for index, chromosome in enumerate(child_max):
		score_child = 0
		for i in range(0, 7):
			score_child = chromosome[i][8] + score_child
			index = index
		child_score.append(score_child)

	#Select top N children
	ranked_child_indices = sorted(range(len(child_score)), key=lambda i: child_score[i])[-10:]
	
	max_child_score = max(child_score)
	max_parent_score = max(parent_score)
	max_child_index = child_score.index(max(child_score))
	max_parent_index = parent_score.index(max(parent_score))
	#print("child score is " + str(max(child_score)))
	#print("parent score is " + str(max(parent_score)))

	#Keep top N children based on indices in population
	child_max = [child_max[i] for i in ranked_child_indices]

	return(max_child_score, max_parent_score, child_max, max_child_index)


def initial_fitness_func(under_cost, population):
#Calculate the scores of each lineup that is under $50,000 salary cap
	fittest = []
	fittest_chroms = []
	score = 0
	for index, chromosome in enumerate(under_cost):
		score = 0
		for i in range(0, 7):
			score = chromosome[i][8] + score
			index = index
		fittest.append(score)
		#fittest.append(index)
	#print(fittest)
	#print(under_cost)
	#Get indices of n greatest fitness scores (currently 100)
	max_scores = sorted(range(len(fittest)), key=lambda i: fittest[i])[-200:]
	#print(max_scores)
	for i in range(0, len(max_scores)):
		fittest_chroms.append(under_cost[max_scores[i]])
	return fittest_chroms, under_cost

def subsequent_mating(fittest_chroms, under_cost, child_max):
#pick positions from two parents at random. Add them to child generation. 
	#SELECT THE NUMBER OF CHILDREN
	child_gen = []
	cross_over = 100
	for i in range(0, cross_over):
		prob = rnd.random()
		parent1, parent2 = rnd.sample(child_max, 2)
		#print(parent1)
		if prob < 0.20:
			child_gen.append(parent1[0:4] + parent2[4:8])
			#GET the first half of parent 1 genes, 2nd half of parent 2 genes
			#print(child_gen)

		elif prob < 0.40:
			child_gen.append(parent2[0:4] + parent1[4:8])
			#GET the second half of parent 1 genes, 1st half of parent 2 genes
			#print(child_gen)
		elif prob < 60:
			child_gen.append(parent1[0:2] + parent2[2:4] + parent1[4:6] + parent2[4:8])

		elif prob < 80:
			child_gen.append(parent2[0:2] + parent1[2:4] + parent2[4:6] + parent1[4:8])

		else:
			#Mutation. Mutate random position from fittest sample
			rand_position_change = rnd.randint(0, 7)
			parent1[rand_position_change] = under_cost[rand_position_change][rand_position_change]
			parent1.append(child_gen)
	return(fittest_chroms, child_gen, under_cost)

def mating(fittest_chroms, under_cost):
#pick positions from two parents at random. Add them to child generation. 
	child_gen = []
	#SELECT THE NUMBER OF CHILDREN
	cross_over = 500
	for i in range(0, cross_over):
		prob = rnd.random()
		parent1, parent2 = rnd.sample(fittest_chroms, 2)

		if prob < 0.40:
			child_gen.append(parent1[0:4] + parent2[4:8])
			#GET the first half of parent 1 genes, 2nd half of parent 2 genes
			#print(child_gen)

		elif prob < 0.80:
			child_gen.append(parent2[0:4] + parent1[4:8])
			#GET the second half of parent 1 genes, 1st half of parent 2 genes
			#print(child_gen)

		else:
			#Mutation. Mutate random position from fittest sample
			rand_position_change = rnd.randint(0, 7)
			parent1[rand_position_change] = under_cost[rand_position_change][rand_position_change]
			parent1.append(child_gen)
	return(fittest_chroms, child_gen, under_cost)


def initial_func():
	population = 1000
	under_cost = []
	while len(under_cost) < 1000:
		pg_sample = point_guard.sample(n=1)
		sg_sample = shooting_guard.sample(n=1)
		g_sample = guard.sample(n=1)
		sfwd_sample = small_fwd.sample(n=1)
		pwfd_sample = power_fwd.sample(n=1)
		center_sample = center.sample(n=1)
		fwd_sample = fwd.sample(n=1)
		util_sample = util.sample(n=1)

		chromosome = [pg_sample.values.flatten(), sg_sample.values.flatten(), g_sample.values.flatten(),
		sfwd_sample.values.flatten(), pwfd_sample.values.flatten(), center_sample.values.flatten(),
		fwd_sample.values.flatten(), util_sample.values.flatten()]

		fitness = chromosome[0][8] + chromosome[1][8] + chromosome[2][8] + chromosome[3][8] + chromosome[4][8] + chromosome[5][8] + chromosome[6][8] + chromosome[7][8]
		cost = chromosome[0][5] + chromosome[1][5] + chromosome[2][5] + chromosome[3][5] + chromosome[4][5] + chromosome[5][5] + chromosome[6][5] + chromosome[7][5]

	#Include only if cost is under salary cap
		if cost < 50000:
			under_cost.append(chromosome)
	return(under_cost, population)
#initial_fitness_func(under_cost)


#Run to initialize population and evaluate, then cross and evaluate
under_cost, population = initial_func()
fittest_chroms, under_cost = initial_fitness_func(under_cost, population)
fittest_chroms, child_gen, under_cost = mating(fittest_chroms, under_cost)
i = 0
while i < 500:
	max_child_score, max_parent_score, child_max, max_child_index = subsequent_fitness_func(fittest_chroms, child_gen, under_cost)
	fittest_chroms, child_gen, under_cost = subsequent_mating(fittest_chroms, under_cost, child_max)
	i = i + 1
	max_child_score, max_parent_score, child_max, max_child_index = subsequent_fitness_func(fittest_chroms, child_gen, under_cost)



print("Best Lineup: " + str(child_max[0][0][2] + ", " +  child_max[0][1][2] + ", " + child_max[0][2][2] + ", " + child_max[0][3][2] + ", " + child_max[0][4][2]+ ", " + child_max[0][5][2] + ", " + child_max[0][6][2]+ ", " + child_max[0][7][2]))
print("Projected points: " + str(child_max[0][0][8] + child_max[0][1][8] + child_max[0][2][8] + child_max[0][3][8] + child_max[0][4][8] + child_max[0][5][8] + child_max[0][6][8] + child_max[0][7][8]))
print("Cost: $" + str(child_max[0][0][5] + child_max[0][1][5] + child_max[0][2][5] + child_max[0][3][5] + child_max[0][4][5] + child_max[0][5][5] + child_max[0][6][5] + child_max[0][7][5]))



	#TERMINATE WHEN THE NEW POPULATION ARE NOT SIGNIFICANTLY DIFFERENT FROM THE LAST


#The effect of having three or more days rest compared to playing back to back games is estimated to be 2.26 points; compared to having one day rest is estimated to be 1.09 points and compared to having two days rest is estimated to be 0.58 points.
#Home court advantage results in teams winning by 3.62 points. They win 61% of the time
