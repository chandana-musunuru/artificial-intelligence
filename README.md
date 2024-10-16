# artificial-intelligence (AI Search Algorithms Project)
# Pathfinding Algorithms for Shortest Travel Time
 
# Project Overview

This project implements four pathfinding algorithms—Breadth-First Search (BFS), Depth-First Search (DFS), Uniform Cost Search (UCS), and A*—to find the shortest path from a starting location to a goal location based on live traffic information and estimated Sunday traffic times.

1. Breadth-First Search (BFS)
BFS is an uninformed search algorithm that explores all possible paths level by level, starting from the root node. It uses a queue to ensure all nodes at the current level are explored before moving to the next level. BFS guarantees finding the shortest path in terms of the number of edges, but it doesn't consider travel times or costs.
Tie-breaking Strategy: When multiple children are at the same depth, nodes are expanded in the order they appear in the live traffic data.

2. Depth-First Search (DFS)
DFS explores as deep as possible along each branch before backtracking. It uses a stack to traverse the graph. While DFS is efficient in terms of space, it may not always find the optimal path, as it doesn't consider the cost of paths, and it may end up following a longer route.
Tie-breaking Strategy: When multiple children are at the same depth, nodes are expanded in the order they appear in the live traffic data.

3. Uniform Cost Search (UCS)
UCS is a cost-based search algorithm that explores the least-cost node first. It uses a priority queue, where nodes with the lowest cumulative cost are processed first. UCS guarantees finding the optimal path, as it always expands the least costly nodes.
Tie-breaking Strategy: When multiple children have the same path cost, nodes are expanded in the order they appear in the live traffic data. If a node with the same cost is already in the queue, the newly generated one is enqueued after the older one.

4.A*
A* is an informed search algorithm that combines the benefits of UCS with heuristics to guide the search. It uses both the actual travel cost and a heuristic estimate of the remaining distance to the goal (based on traffic-free estimates). A* tends to be faster than UCS due to this heuristic guidance but still guarantees the shortest path.
Tie-breaking Strategy: When multiple children have the same evaluation cost (path cost + heuristic), nodes are expanded in the order they appear in the live traffic data. If a node with the same evaluation cost is already in the queue, the newly generated one is enqueued after the older one.
