def help_michael(mafia_tree, savings):
	if sum_wp(mafia_tree) - sum_cp(mafia_tree) <= savings: 
		return "Yes"
	reduc_needed = sum_wp(mafia_tree) - sum_cp(mafia_tree) - savings
	sacrifices = [] #list of all people whose rp > 1 and whose wp>cp
	for person in tree_flattener(mafia_tree):
		if find_rp(mafia_tree, person) > 1 and node_wp(person) > node_cp(person):
			sacrifices.append(person)
	total = 0
	for person in sacrifices: 
		total += max_reduc(mafia_tree,person)
	if total < reduc_needed:
		return "No" 	
	total = []
	for person in sacrifices:
		total.append([node_name(person) , node_wp(person), max_reduc(mafia_tree,person)])
	return ["Possible"] + possible_returner(total ,reduc_needed)

def datum(tree):
	return tree[0]

def node_name(node):
	return node[0]

def node_cp(node):
	return node[1]

def node_wp(node):
	return node[2]

def children(tree):
	return tree[1:]

def isleaf(tree):
	return len(children(tree)) == 0

def sorter(lst):
	swapped = 1
	while swapped:
		swapped = 0
		i = 0
		while i < len(lst) - 1:
			if lst[i][2] < lst[i+1][2]:
				(lst[i],lst[i+1]) = (lst[i+1],lst[i])
				swapped = 1
			i +=1
	return lst

def possible_returner(lst, numb):
	sorted_list = sorter(lst)
	if sorted_list[0][2] >= numb:
		l = [[sorted_list[0][0], sorted_list[0][1] - numb]]
		return l
	l = [[sorted_list[0][0], sorted_list[0][1]-sorted_list[0][2]]]
	return l + possible_returner(lst[1:], numb-sorted_list[0][2])

def tree_flattener(tree):
	tree_flattened = [datum(tree)]
	if isleaf(tree):
		return tree_flattened
	for child in children(tree):
		tree_flattened += tree_flattener(child)
	return tree_flattened 

def sum_wp(tree):
	if isleaf(tree):
		return node_wp(datum(tree))
	totalwp = node_wp(datum(tree))
	for child in children(tree):
			totalwp += sum_wp(child)
	return totalwp 

def sum_cp(tree):
	if isleaf(tree):
		return node_cp(datum(tree))
	totalcp = node_cp(datum(tree))
	for child in children(tree):
			totalcp += sum_cp(child)
	return totalcp 

def find_rp(tree, node): #This function finds the rp (depth) of the given person.
    if datum(tree) == node:
        return 0
    for child in children(tree):
        rp = find_rp(child, node)
        if rp != None:
            return rp + 1

def max_reduc(tree, node): 
#This function calculates the maximum amount of reduction that can be made from the given person.
	if node_wp(node) - find_rp(tree,node)*100 > 0:
		return find_rp(tree,node)*100
	return node_wp(node) - 1