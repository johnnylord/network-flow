class Edge:

    def __init__(self, src, dst, capacity):
        # Edge information
        self.src = src
        self.dst = dst
        self.flow = 0
        self.capacity = capacity
        # Residual Edge
        self.residual = None

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f"{self.src} -> {self.dst}"

    def is_residual(self):
        return self.capacity == 0

    def remain_capacity(self):
        return self.capacity - self.flow

    def augment(self, bottleneck):
        self.flow += bottleneck
        self.residual.flow -= bottleneck


class FordFulkersonDfsSolver:
    FLOW_INFINITY = 100000

    def __init__(self, n, s, t):
        self.n = n
        self.s = s
        self.t = t
        self.round = 0
        self.graph = [ [] for _ in range(n) ]
        self.visited = [ self.round for _ in range(n) ]
        self.max_flow = 0

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        content = ""
        for node, edges in enumerate(self.graph):
            state = f"Node {node}"
            for edge in edges:
                state += (
                        f"\n\t{edge.src} to {edge.dst},"
                        f" flow: {edge.flow}, capacity: {edge.capacity}"
                        )
                if edge.capacity == 0:
                    state += " (Residual)"
                else:
                    state += " (Normal)"
            content += ("\n"+state)
        return content

    def add_edge(self, src, dst, capacity):
        e1 = Edge(src, dst, capacity)
        e2 = Edge(dst, src, 0)
        e1.residual = e2
        e2.residual = e1
        self.graph[src].append(e1)
        self.graph[dst].append(e2)

    def solve(self):
        bottleneck = self._dfs(self.s, FordFulkersonDfsSolver.FLOW_INFINITY)
        while bottleneck != 0:
            print(f"Round {self.round}")
            self.max_flow += bottleneck
            self._reset_visited()
            bottleneck = self._dfs(self.s, FordFulkersonDfsSolver.FLOW_INFINITY)

    def _dfs(self, node, flow):
        # Reach sink node
        if node == self.t:
            return flow
        # DFS find minimum flow along augment path
        self._visit_node(node)
        edges = self.graph[node]
        for edge in edges:
            rcap = edge.remain_capacity()
            if (rcap > 0) and not self._is_visited(edge.dst):
                bottleneck = self._dfs(edge.dst, min([flow, rcap]))
                if bottleneck > 0:
                    edge.augment(bottleneck)
                    return bottleneck
        return 0

    def _reset_visited(self):
        self.round += 1
        self.visited = [ self.round for _ in range(self.n) ]

    def _visit_node(self, node):
        self.visited[node] = (self.round + 1)

    def _is_visited(self, node):
        return self.visited[node] == (self.round + 1)


def main():
    n = 11      # Number of node in the graph
    s = n - 2   # Source node index
    t = n - 1   # Sink node index

    # Create max flow solver
    solver = FordFulkersonDfsSolver(n, s, t)

    # Edges from source
    solver.add_edge(s, 0, 10)
    solver.add_edge(s, 1, 5)
    solver.add_edge(s, 2, 10)

    # Middle Edges
    solver.add_edge(0, 3, 10)
    solver.add_edge(1, 2, 10)
    solver.add_edge(2, 5, 15)
    solver.add_edge(3, 1, 20)
    solver.add_edge(3, 6, 15)
    solver.add_edge(4, 1, 15)
    solver.add_edge(4, 3, 3)
    solver.add_edge(5, 4, 4)
    solver.add_edge(5, 8, 10)
    solver.add_edge(6, 7, 10)
    solver.add_edge(7, 4, 10)
    solver.add_edge(7, 5, 7)

    # Edges to sink
    solver.add_edge(6, t, 15)
    solver.add_edge(8, t, 10)

    # Solve the problem
    solver.solve()
    print(solver)
    print("="*20)
    print("Max Flow:", solver.max_flow)

if __name__ == "__main__":
    main()
