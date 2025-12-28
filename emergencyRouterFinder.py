#!/usr/bin/env python3
"""
emergencyRouteFinder.py
=======================
Compute the fastest road-network routes from a disaster zone (source)
to one or more hospitals using Dijkstra's algorithm.

Features
--------
1.  Interactive input of a weighted graph, the disaster-zone vertex,
    and one or more hospital vertices; OR load a built-in demo graph
    with ≥ 6 nodes / ≥ 10 edges.
2.  Encapsulated `dijkstra()` function that returns the shortest
    distance to every vertex and enables path reconstruction.
3.  Clear output: distance table for all hospitals and the
    step-by-step optimal path to a chosen hospital.

Complexity
----------
Time  : O(E log V)  using a binary heap
Space : O(E + V)

Author : <your-name>
Date   : <today'ys date>
"""
from typing import List, Tuple, Dict
import heapq
import sys

Edge = Tuple[int, int, int]             # (u, v, weight)
Adj  = List[List[Tuple[int, int]]]      # adjacency list


# ------------------------------------------------------------------ #
#  Dijkstra’s algorithm                                              #
# ------------------------------------------------------------------ #
def dijkstra(n: int, adj: Adj, src: int) -> Tuple[List[int], List[int]]:
    """
    Return (dist, prev) where
      dist[v] = shortest distance src→v  (inf if unreachable)
      prev[v] = predecessor of v in the shortest path (-1 if none)

    Raises ValueError if any edge weight is negative.
    """
    # Detect negative edge weights up front
    if any(w < 0 for neigh in adj for _, w in neigh):
        raise ValueError("Graph contains negative edge weights; "
                         "Dijkstra's algorithm is invalid.")

    INF = 10**15
    dist = [INF] * n
    prev = [-1] * n
    dist[src] = 0

    pq: List[Tuple[int, int]] = [(0, src)]  # (distance, vertex)

    while pq:
        d, u = heapq.heappop(pq)
        if d != dist[u]:      # stale entry
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                heapq.heappush(pq, (dist[v], v))
    return dist, prev


def reconstruct_path(prev: List[int], target: int) -> List[int]:
    """Return list of vertices from source to target (inclusive)."""
    path = []
    cur = target
    while cur != -1:
        path.append(cur)
        cur = prev[cur]
    path.reverse()
    return path


# ------------------------------------------------------------------ #
#  Input helpers                                                     #
# ------------------------------------------------------------------ #
def prompt_int(prompt: str, cond=lambda x: True) -> int:
    while True:
        try:
            val = int(input(prompt).strip())
            if not cond(val):
                raise ValueError
            return val
        except ValueError:
            print("  ⚠️  Enter a valid integer.")


def build_graph_interactively() -> Tuple[int, Adj]:
    print("\nEnter graph data:")
    n = prompt_int("  Number of intersections (vertices): ", lambda x: x >= 2)
    m = prompt_int("  Number of roads (edges): ", lambda x: x >= n - 1)

    adj: Adj = [[] for _ in range(n)]
    print("  Enter each road as: src dst travel_time   (0-based indices)")
    for i in range(1, m + 1):
        while True:
            raw = input(f"    Road {i}: ").strip().split()
            if len(raw) != 3:
                print("      ⚠️  Provide exactly 3 integers.")
                continue
            try:
                u, v, w = map(int, raw)
                if not (0 <= u < n and 0 <= v < n and u != v and w >= 0):
                    raise ValueError
                adj[u].append((v, w))
                adj[v].append((u, w))    # undirected
                break
            except ValueError:
                print("      ⚠️  Invalid road. Try again.")
    return n, adj


def load_demo_graph() -> Tuple[int, Adj, int, List[int]]:
    """
    Returns (n, adj, source, hospitals)
    Demo city map with 7 intersections (0-6) and 12 roads.
    Hospitals are at vertices 4 and 6, disaster zone at 0.
    """
    n = 7
    edge_list: List[Edge] = [
        (0, 1, 4), (0, 2, 3), (0, 3, 10),
        (1, 2, 2), (1, 4, 7),
        (2, 4, 4), (2, 5, 3),
        (3, 5, 6),
        (4, 5, 2), (4, 6, 5),
        (5, 6, 1),
        (3, 6, 12)
    ]
    adj: Adj = [[] for _ in range(n)]
    for u, v, w in edge_list:
        adj[u].append((v, w))
        adj[v].append((u, w))
    source = 0
    hospitals = [4, 6]
    return n, adj, source, hospitals


# ------------------------------------------------------------------ #
#  Main driver                                                       #
# ------------------------------------------------------------------ #
def main() -> None:
    print("=== Emergency Route Finder (Shortest Paths) ===")
    use_demo = input("Load demo graph? [Y/n]: ").strip().lower()
    if use_demo in ("", "y", "yes"):
        n, adj, source, hospitals = load_demo_graph()
        print("Loaded demo map (7 intersections, 12 roads).")
        print(f"Disaster zone at vertex {source}; hospitals at {hospitals}.")
    else:
        n, adj = build_graph_interactively()
        source = prompt_int("\nEnter disaster-zone vertex index: ",
                            lambda x: 0 <= x < n)
        hospitals_input = input("Enter hospital vertex indices "
                                "(space-separated): ").strip().split()
        hospitals = []
        for h in hospitals_input:
            try:
                idx = int(h)
                if 0 <= idx < n:
                    hospitals.append(idx)
            except ValueError:
                continue
        if not hospitals:
            print("⚠️  No valid hospitals entered. Exiting.")
            sys.exit(1)

    # Compute shortest paths
    try:
        dist, prev = dijkstra(n, adj, source)
    except ValueError as e:
        print(f"\n {e}")
        sys.exit(1)

    # Show distance table
    print("\n🩺 Fastest travel times to hospitals:")
    for h in hospitals:
        if dist[h] == 10**15:
            print(f"  Hospital {h}: UNREACHABLE")
        else:
            print(f"  Hospital {h}: {dist[h]} time units")

    # Show step-by-step path to a selected hospital
    target = prompt_int("\nWhich hospital’s path to display? ",
                        lambda x: x in hospitals)
    if dist[target] == 10**15:
        print("No path available.")
        sys.exit(0)

    path = reconstruct_path(prev, target)
    print("\n Optimal route:")
    print("  → ".join(map(str, path)))
    print(f"Total travel time: {dist[target]}")

if __name__ == "__main__":
    main()
