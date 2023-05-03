import numpy as np
import random

def k_means(data, k, max_iterations=100):
    # Initialize k centroids randomly
    centroids = data[np.random.choice(range(len(data)), k, replace=False)]
    
    for i in range(max_iterations):
        # Assign each data point to the closest centroid
        distances = np.sqrt(((data - centroids[:, np.newaxis])**2).sum(axis=2))
        labels = np.argmin(distances, axis=0)
        
        # Update centroids to the mean of their assigned data points
        new_centroids = np.array([data[labels == j].mean(axis=0) for j in range(k)])
        
        # Stop if centroids have not moved
        if np.all(centroids == new_centroids):
            break
        
        centroids = new_centroids
    
    return centroids, labels


# Ask the user to input the data points
n = int(input("Enter the number of data points: "))
data = np.zeros((n, 2))
for i in range(n):
    print(f"Enter data point: ")
    data[i,0] = float(input("Input x "))
    data[i,1] = float(input("Input y "))

# Cluster the data into k clusters
k = int(input("Enter the number of clusters: "))
clusters, centroids = k_means(data, k)

# Print the clusters and centroids
for i, cluster in enumerate(clusters):
    print(f"Cluster {i}: {len(cluster)} points")
print(f"Centroids: {centroids}")
