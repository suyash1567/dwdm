import itertools
import numpy as np

def create_candidates(dataset, length):

    candidates = []
    for transaction in dataset:
        for item in transaction:
            if not any([set([item]) == c for c in candidates]):
                candidates.append(set([item]))
    return [set(c) for c in itertools.combinations(sorted(set.union(*candidates)), length)]

def prune(dataset, candidates, min_support):
  
    supports = {}
    for transaction in dataset:
        for candidate in candidates:
            if candidate.issubset(set(transaction)):
                supports[tuple(candidate)] = supports.get(tuple(candidate), 0) + 1
    return {k: v for k, v in supports.items() if v >= min_support}

def apriori(dataset, min_support=2):
    """
    Generate frequent itemsets using the Apriori algorithm.
    """
    dataset = [set(transaction) for transaction in dataset]
    length = 1
    supports = {}
    while True:
        candidates = create_candidates(dataset, length)
        if not candidates:
            break
        supports.update(prune(dataset, candidates, min_support))
        length += 1
    return supports

# Example usage:


dataset = []
n = int(input("Enter the number of transactions: "))
for i in range(n):
    transaction = input("Enter items in transaction separated by space: ").split()
    dataset.append(transaction)

supports = apriori(dataset, min_support=2)
print(supports)
