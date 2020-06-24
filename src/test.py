from compatability import *

# score_matrix = generate_score_matrix()
# np.savetxt('score_matrix.csv', score_matrix, delimiter=',', fmt='%d')

# find_best_pair()
# get_score_submatrix(['Sylvana','Maple','Zell','Beardo','sdad'])
# best_tens = find_threshold_best_ten(12)
# print (best_tens)

# for best_ten in best_tens:
# 	for index in best_ten:
# 		print (villagers[index]['Name'])
# get_score_submatrix(['Tammy','Stitches','Chester','Nate','Charlise','Barold'])

# print (name_to_index('Tammy'))
names = ['Mitzi','Olaf','Pango','Roald','Tybalt','Tipper','Renée','Nate','Stitches']
indexes = [name_to_index(name) for name in names]
best_left_indexes = find_threshold_best_left(names, threshold=8, switch=1, between_score_threshold=8)
for best_left in best_left_indexes:
    ten = indexes + best_left
    temp = [index_to_name(index) for index in ten]
    score_submatrix = get_score_submatrix(temp)
    between_score_submatrix = score_submatrix[np.ix_(range(len(names)),range(len(names),10))]
    print (temp[len(names):], between_score_submatrix.min())
    print (score_submatrix[np.ix_(range(len(names)),range(len(names),10))])

# i1 = name_to_index('Boris')
# i2 = name_to_index('Eugene')
# print (villagers[i1])
# print (villagers[i2])

# best_ten = [87, 95, 355, 357, 362, 365, 243, 109, 104, 113]
# names = [index_to_name(index) for index in best_ten]
# print (get_score_submatrix(names))
