#!/usr/bin/env python3
"""
freightNetworkPlanner.py
------------------------
Build a minimum-cost transportation network (Minimum Spanning Tree)
connecting all warehouses with Kruskal’s algorithm.

Time  : O(E log E)   (sorting edges)
Space : O(E + V)     (edge list + Union-Find)

Author : <your-name>
Date   : <today’s date>
"""
from typing import List, Tuple
import sys

Edge = Tuple[int, int, int]  # (u, v, weight)

# ------------------------------------------------------------------ #
#  Union–Find (Disjoint Set Union)                                   #
# ------------------------------------------------------------------ #
class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.rank   = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # union by rank
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1
        return True

# ------------------------------------------------------------------ #
#  Kruskal’s Algorithm                                               #
# ------------------------------------------------------------------ #
def kruskal_mst(num_vertices: int, edges: List[Edge]) -> Tuple[List[Edge], int]:
    edges_sorted = sorted(edges, key=lambda e: e[2])     # by weight
    uf = UnionFind(num_vertices)
    mst:   List[Edge] = []
    total: int        = 0

    for u, v, w in edges_sorted:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w
            if len(mst) == num_vertices - 1:
                break

    if len(mst) != num_vertices - 1:
        raise ValueError("Graph is disconnected; MST impossible.")
    return mst, total

# ------------------------------------------------------------------ #
#  Input Helpers                                                     #
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

def build_graph_interactively() -> Tuple[int, List[Edge]]:
    print("\nEnter graph data:")
    n = prompt_int("  Number of warehouses (vertices): ", lambda x: x >= 2)
    m = prompt_int("  Number of transportation lines (edges): ", lambda x: x >= n - 1)

    edges: List[Edge] = []
    print("  Enter each edge as: src dst cost   (0-based indices)")
    for i in range(1, m + 1):
        while True:
            raw = input(f"    Edge {i}: ").strip().split()
            if len(raw) != 3:
                print("      ⚠️  Provide exactly 3 integers.")
                continue
            try:
                u, v, w = map(int, raw)
                if not (0 <= u < n and 0 <= v < n and u != v and w >= 0):
                    raise ValueError
                edges.append((u, v, w))
                break
            except ValueError:
                print("      ⚠️  Invalid edge. Try again.")
    return n, edges

def load_demo_graph() -> Tuple[int, List[Edge]]:
    demo_edges: List[Edge] = [
        (0, 1, 7), (0, 2, 3), (0, 3, 8), (0, 4, 5),
        (1, 2, 4), (1, 4, 6),
        (2, 3, 4), (2, 4, 2),
        (3, 4, 1),
        (1, 3, 9)
    ]
    return 5, demo_edges

# ------------------------------------------------------------------ #
#  Main Driver                                                       #
# ------------------------------------------------------------------ #
def main() -> None:
    print("=== Freight Network Planner (MST) ===")
    use_demo = input("Load demo graph? [Y/n]: ").strip().lower()
    if use_demo in ("", "y", "yes"):
        n, edges = load_demo_graph()
        print("Loaded demo graph with 5 warehouses and 10 edges.")
    else:
        n, edges = build_graph_interactively()

    try:
        mst, total = kruskal_mst(n, edges)
    except ValueError as e:
        print(f"\n❌ {e}")
        sys.exit(1)

    print("\n Minimum-Cost Lines:")
    for u, v, w in mst:
        print(f"  {u} — {v}   cost = {w}")
    print(f"\n Total construction cost: {total}")

if __name__ == "__main__":
    main()
