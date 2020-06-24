from helper import *
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

def personality_compatability(p1: str, p2: str):
	personality_index = {
		'Normal': 0,'Lazy': 1,'Peppy': 2,
		'Jock': 3,'Snooty': 4,'Cranky': 5,
		'Smug': 6,'Sisterly': 7}
	personality_compatability_matrix = [
		['♣','×','×','♦','♥','♣','♥','♦'],
		['×','♥','♦','×','♣','♦','♣','♥'],
		['×','♦','♥','♥','♦','×','♣','♣'],
		['♦','×','♥','♥','×','♣','♦','♣'],
		['♥','♣','♦','×','♣','♥','♦','×'],
		['♣','♦','×','♣','♥','♥','×','♦'],
		['♥','♣','♣','♦','♦','×','♥','×'],
		['♦','♥','♣','♣','×','♦','×','♥']]

	return personality_compatability_matrix[personality_index[p1]][personality_index[p2]]

def species_compatability(s1: str, s2: str):
	if s1 == s2:
		return '♦'
	elif {s1,s2} == {'Bear','Cub'} or {s1,s2} == {'Bull','Cow'} or {s1,s2} == {'Cat','Tiger'} or {s1,s2} == {'Dog','Wolf'} or {s1,s2} == {'Goat','Sheep'} or {s1,s2} == {'Kangaroo','Koala'}:
		return '♥'
	elif {s1,s2} == {'Deer','Horse'} or {s1,s2}.issubset({'Hamster','Squirrel','Mouse'}):
		return '♦'
	elif {s1,s2} == {'Cat','Mouse'} or {s1,s2} == {'Cat','Hamster'} or {s1,s2} == {'Dog','Gorilla'} or {s1,s2} == {'Dog','Monkey'} or {s1,s2} == {'Sheep','Wolf'}:
		return '×'
	else:
		return '♣'

def star_sign_compatability(sign1: str, sign2: str):
	def extract_star_sign(sign: str):
		if sign in {'Aries','Leo','Sagittarius'}:
			return 'Fire'
		elif sign in {'Taurus','Virgo','Capricorn'}:
			return 'Earth'
		elif sign in {'Gemini','Libra','Aquarius'}:
			return 'Air'
		elif sign in {'Cancer','Scorpio','Pisces'}:
			return 'Water'
		else:
			return ''

	star_sign1 = extract_star_sign(sign1)
	star_sign2 = extract_star_sign(sign2)

	if star_sign1 == '' or star_sign2 == '':
		return 0
	if star_sign1 == star_sign2:
		return '♥'
	elif {star_sign1,star_sign2} == {'Fire','Water'} or {star_sign1,star_sign2} == {'Earth','Air'}:
		return '×'
	else:
		return '♦'

def generate_score_matrix():
	size = len(villagers)
	score_matrix = np.zeros((size,size))
	for i in range(size):
		for j in range(size):
			if not i == j:
				score = score_to_int(personality_compatability(villagers[i]['Personality'],villagers[j]['Personality']))\
					+ score_to_int(species_compatability(villagers[i]['Species'],villagers[j]['Species']))\
					+ score_to_int(star_sign_compatability(villagers[i]['Sign'],villagers[j]['Sign']))
				score_matrix[i][j] = score

	return score_matrix

# --------------------------- Score Matrix Handling ---------------------------
def get_score_submatrix(names: list):
	score_matrix = generate_score_matrix()

	size = len(names)
	if size > 10:
		print ("Why you want to know the score matrix of a subset with more than 10 villagers? Return -1.")
		return -1
	indexes = [name_to_index(name) for name in names]
	for index in indexes:
		if not check_index(index):
			print ("Some of your name is not found in data! Return -1.")
			return -1

	score_submatrix = np.zeros((size,size))
	for i in range(size):
		for j in range(size):
			score_submatrix[i][j] = score_matrix[indexes[i]][indexes[j]]
	# print (score_submatrix)
	return score_submatrix

def find_best_pair():
	score_matrix = generate_score_matrix()

	best_pair_indexes = []
	indexes = np.where(score_matrix == score_matrix.max())
	row_indexes = indexes[0].tolist()
	column_indexes = indexes[1].tolist()
	if len(row_indexes) != len(column_indexes):
		print ("Something wrong in numpy! Return -1.")
		return -1
	for i in range(len(row_indexes)):
		if not {row_indexes[i],column_indexes[i]} in best_pair_indexes:
			best_pair_indexes.append({row_indexes[i],column_indexes[i]})
		else:
			continue
	# print (best_pair_indexes)
	return best_pair_indexes

def find_threshold_best_ten(threshold: int):
	score_matrix = generate_score_matrix()

	if threshold < 10:
		print ("Why the fuck setting your threshold that low? Return -1.")
		return -1
	def generate_threshold_score_matrix():
		size = len(villagers)
		threshold_score_matrix = np.zeros((size,size))

		for i in range(size):
			for j in range(size):
				if score_matrix[i][j] >= threshold:
					threshold_score_matrix[i][j] = score_matrix[i][j]

		return threshold_score_matrix
	threshold_score_matrix = generate_threshold_score_matrix()
	threshold_graph = nx.from_numpy_matrix(threshold_score_matrix, False)
	# nx.draw_networkx(threshold_graph, pos=nx.spring_layout(threshold_graph), with_labels = False, node_size = 10)
	# plt.show()
	best_ten_indexes = [s for s in nx.find_cliques(threshold_graph) if len(s) == 10]
	if not best_ten_indexes:
		print ("Seems you set your threshold too high! Nothing found, return -1.")
		return -1
	# print (best_ten_indexes)
	return best_ten_indexes

def find_threshold_best_left(names: list, threshold: int):
	score_matrix = generate_score_matrix()

	size = len(names)
	if size >= 10:
		print ("WTF, you already had 10 chosen villagers? Return -1.")
		return -1
	if size == 0:
		return find_threshold_best_ten(threshold)
	indexes = [name_to_index(name) for name in names]
	for index in indexes:
		if not check_index(index):
			print ("Some of your name is not found in data! Return -1.")
			return -1
	def generate_threshold_score_matrix():
		size = len(villagers)
		threshold_score_matrix = np.zeros((size,size))

		for i in range(size):
			for j in range(size):
				if i in indexes and j in indexes:
					threshold_score_matrix[i][j] = threshold
				elif score_matrix[i][j] >= threshold:
					threshold_score_matrix[i][j] = score_matrix[i][j]
				else:
					continue

		return threshold_score_matrix
	threshold_score_matrix = generate_threshold_score_matrix()
	threshold_graph = nx.from_numpy_matrix(threshold_score_matrix, False)
	candidates = [s for s in nx.find_cliques(threshold_graph) if len(s) == 10]
	if not candidates:
		print ("Seems you set your threshold too high! Nothing found, return -1.")
		return -1
	for candidate in candidates:
		# print (indexes)
		# print (candidate)
		if issublist(indexes, candidate):
			print (candidate)
			names = [index_to_name(index) for index in candidate]
			print (get_score_submatrix(names))

# --------------------------- Aborted ---------------------------
def find_overall_best_ten():
	overall_best_ten_indexes = []
	return overall_best_ten_indexes
# --------------------------- Aborted ---------------------------
