import math
import csv

def readData(filename):
	reader = csv.reader(open(filename, 'r'))
	transactions = []
	for row in reader:
		transactions.append(row)
	return transactions

def gain_category(col, dataset):
	total = list(row[col] for row in dataset)
	len_total = len(total)
	att_dict = {}
	for i in total:
		if i in att_dict:
			att_dict[i] += 1
		else:
			att_dict[i] = 1
	gain = 0
	for i in att_dict.keys():
		p = (att_dict[i] / float(len_total))
		gain += -p * math.log(p, 2)
	return gain

def gain_attribute_category(col, dataset):
	gain = 0
	p = 0
	classes = list(set(row[col] for row in dataset))
	for i in classes:
		len_total = len(dataset)
		new_dataset = [row for row in dataset if i == row[col]]
		new_len_total = len(new_dataset)
		p += (new_len_total / float(len_total)) * gain_category(len(dataset[0]) - 1, new_dataset)
	return p

def split_attribute(dataset):
	classes = list(set(row[-1] for row in dataset[1:]))
	info_gain = gain_category(len(dataset[0])-1, dataset[1:])
	best_gain = 0
	for col in range(len(dataset[0]) - 1):
		gainA = gain_attribute_category(col, dataset[1:])
		dgain = info_gain - gainA
		if dgain > best_gain or best_gain == 0:
			b_col, best_gain = col, dgain
	links = list(set(val[b_col] for val in dataset[1:]))
	ret = {}
	for i in links:
		ret[i] = [dataset[0]] + [row for row in dataset if i == row[b_col]]
	return {'b_col': b_col, 'best_gain': best_gain, 'data': ret}

def prune(sub_dataset):
	outcomes = [row[-1] for row in sub_dataset[1:]]
	max_val = max(set(outcomes), key=outcomes.count)
	for i in sub_dataset[1:]:
		if i[-1] != max_val:
			return False
	return True

def to_terminal(sub_dataset):
	outcomes = [row[-1] for row in sub_dataset[1:]]
	return max(set(outcomes), key=outcomes.count)

def split(node, max_depth, min_size, depth):
	ret = node['data']
	del (node['data'])
	for i in ret.keys():
		check = prune(ret[i])
		if check:
			node[i] = to_terminal(ret[i])
			continue
		if depth >= max_depth:
			node[i] = to_terminal(ret[i])
			continue
		if len(ret[i]) <= min_size:
			node[i] = to_terminal(ret[i])
		else:
			node[i] = split_attribute(ret[i])
			split(node[i], max_depth, min_size, depth + 1)

def create_tree(data):
	root = split_attribute(data)
	split(root, 4, 1, 1)
	return root

def print_tree(root, n=1):
	s = set()
	s.add('b_col')
	s.add('best_gain')
	val = set(root.keys()) - s
	for i in val:	
		if type(root[i]) == type('str'):
			print("level : " + str(n), "col: " + str(root['b_col']), "gain: " + str(root['best_gain']), "outcome: " + i + ":" + root[i])
		else:
			print("level : " + str(n), "col: " + str(root['b_col']), "value: " + i, "gain: " + str(root['best_gain']))
			print_tree(root[i], n + 1)
		if n == 1:
			print()

data = readData("data.csv")
root = create_tree(data)
print(root)
print_tree(root)