from collections import defaultdict
from itertools import combinations

def get_local_itemsets(transactions, partition, min_support):
    local_itemsets = defaultdict(int)
    for transaction in transactions:
        if set(partition).issubset(transaction):
            for itemset in combinations(transaction, len(partition)):
                local_itemsets[itemset] += 1

    num_transactions = len(transactions)
    return {itemset: support/num_transactions for itemset, support in local_itemsets.items()
            if support/num_transactions >= min_support}

def apriori_partition(transactions, min_support, max_partition_size):
    all_itemsets = set(item for transaction in transactions for item in transaction)
    frequent_itemsets = defaultdict(list)

    # Generate frequent itemsets for each partition size
    for partition_size in range(1, max_partition_size+1):
        for partition in combinations(all_itemsets, partition_size):
            local_itemsets = get_local_itemsets(transactions, partition, min_support)
            if len(local_itemsets) > 0:
                frequent_itemsets[partition].append(local_itemsets)

    # Combine frequent itemsets to obtain global itemsets
    global_itemsets = defaultdict(float)
    for partition, partition_itemsets in frequent_itemsets.items():
        for itemsets in partition_itemsets:
            for itemset, support in itemsets.items():
                global_itemsets[itemset] += support

    return {itemset: support for itemset, support in global_itemsets.items()
            if support >= min_support}

transactions = [
    {1, 5, 6, 8},
    {2, 4, 8},
    {4, 5, 7},
    {2, 3},
    {5, 6, 7},
    {2, 3, 4},
    {2, 6, 7, 9},
    {5},
    {8},
    {3, 5, 7},
    {3, 5, 7},
    {5, 6, 8},
    {2, 4, 6, 7},
    {1, 3, 5, 7},
    {2, 3, 9},
]

min_support = 0.2
max_partition_size = 4

frequent_itemsets = apriori_partition(transactions, min_support, max_partition_size)

for itemset, support in frequent_itemsets.items():
    print("Frequent itemset {}: {}".format(itemset, support))
