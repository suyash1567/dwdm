from itertools import combinations

def generateMFCS(MFCS, infrequent_itemsets):
    for infrequent_itemset in infrequent_itemsets:
        for MFCS_itemset in MFCS.copy():
            if set(infrequent_itemset).issubset(set(MFCS_itemset)):
                MFCS.remove(MFCS_itemset)
                for item in infrequent_itemset:
                    updated_MFCS_itemset = list(set(MFCS_itemset) - set([item]))
                    if not any(set(updated_MFCS_itemset).issubset(set(_MFCS_itemset)) for _MFCS_itemset in MFCS):
                        MFCS.append(updated_MFCS_itemset)
    return MFCS





def pruneCandidatesUsingMFS(candidate_itemsets, MFS):
	candidate_itemsets = candidate_itemsets.copy()

	for itemset in candidate_itemsets.copy():
		if any(all(_item in _MFS_itemset for _item in itemset) for _MFS_itemset in MFS):
			candidate_itemsets.remove(itemset)

	return candidate_itemsets


def generateCandidateItemsets(level_k, level_frequent_itemsets):
    candidate_frequent_itemsets = []
    n_frequent_itemsets = len(level_frequent_itemsets)

    for i in range(n_frequent_itemsets):
        for j in range(i+1, n_frequent_itemsets):
            itemset_1 = level_frequent_itemsets[i]
            itemset_2 = level_frequent_itemsets[j]

            # Check if the first k-1 elements match
            if itemset_1[:level_k-1] == itemset_2[:level_k-1]:
                candidate_itemset = itemset_1[:level_k-1] + [itemset_1[-1], itemset_2[-1]]
                candidate_frequent_itemsets.append(candidate_itemset)
    
    return candidate_frequent_itemsets


def pruneCandidatesUsingMFCS(candidate_itemsets, MFCS):
	candidate_itemsets = candidate_itemsets.copy()

	for itemset in candidate_itemsets.copy():
		if not any(all(_item in _MFCS_itemset for _item in itemset) for _MFCS_itemset in MFCS):
			candidate_itemsets.remove(itemset)

	return candidate_itemsets


def pincerSearch(transactions, min_support):
	# Extract the list of items in the transactions
	items = set()
	for transaction in transactions:
		items.update(transaction)
	items = sorted(list(items))
	
	level_k = 1 # The current level number

	level_frequent_itemsets = [] # Level 0: Frequent itemsets
	candidate_frequent_itemsets = [[item] for item in items] # Level 1: Candidate itemsets
	level_infrequent_itemsets = [] # Level 0: Infrequent itemsets

	MFCS = [items.copy()] # Maximal Frequent Candidate Sets
	MFS = [] # Maximal Frequent Sets

	print("MFCS = {}".format(MFCS))
	print("MFS = {}\n".format(MFS))

	while candidate_frequent_itemsets:
		
		print("LEVEL {}: ".format(level_k))
		print("C{} = {}".format(level_k, candidate_frequent_itemsets))

		candidate_freq_itemsets_cnts = [0]*len(candidate_frequent_itemsets)
		MFCS_itemsets_cnts = [0]*len(MFCS)

		# Step 1: Read the database and count supports for Ck and MFCS
		for transaction in transactions:
			
			for i, itemset in enumerate(candidate_frequent_itemsets):
				if all(_item in transaction for _item in itemset):
					candidate_freq_itemsets_cnts[i] += 1

			for i, itemset in enumerate(MFCS):
				if all(_item in transaction for _item in itemset):
					MFCS_itemsets_cnts[i] += 1

		for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts):
			print("{} -> {}".format(itemset, support), end=', ')
		print()

		for itemset, support in zip(MFCS, MFCS_itemsets_cnts):
			print("{} -> {}".format(itemset, support), end=', ')
		print()

		# Step 2: MFS := MFS U {frequent itemsets in MFCS}
		MFS.extend([itemset for itemset, support in zip(MFCS, MFCS_itemsets_cnts) if ((support >= min_support) and (itemset not in MFS))])
		print("MFS = {}".format(MFS))

		# Step 3: Sk := {infrequent itemsets in Ck}
		level_frequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support >= min_support]
		level_infrequent_itemsets = [itemset for itemset, support in zip(candidate_frequent_itemsets, candidate_freq_itemsets_cnts) if support < min_support]

		print("L{} = {}".format(level_k, level_frequent_itemsets))
		print("S{} = {}".format(level_k, level_infrequent_itemsets))

		# Step 4: call MFCS-gen algorithm if Sk != NULL
		MFCS = generateMFCS(MFCS, level_infrequent_itemsets)
		print("MFCS = {}".format(MFCS))

		# Step 5: call MFS-pruning procedure
		level_frequent_itemsets = pruneCandidatesUsingMFS(level_frequent_itemsets, MFS)
		print("After Pruning: L{} = {}\n".format(level_k, level_frequent_itemsets))

		# Step 6: Generate candidates Ck+1 from Ck (using generate and prune)
		candidate_frequent_itemsets = generateCandidateItemsets(level_k, level_frequent_itemsets)

		# Step 7: If any frequents itemsets in Ck is removed in MFS-pruning procedure
		# Call the recovery procedure to recover candidates to Ck+1

		# Step 8: call MFCS-prune procedure to prune candidates in Ck+1
		candidate_frequent_itemsets = pruneCandidatesUsingMFCS(candidate_frequent_itemsets, MFCS)

		# Step 9: k := k+1
		level_k += 1

	return MFS

if __name__ == '__main__':
	transactions = [
		{1,3,4},
		{2,3,5},
		{1,2,3,5},
		{2,5}
	]

	min_support_count = 2

	MFS = pincerSearch(transactions, min_support_count)
	print("MFS = {}".format(MFS))