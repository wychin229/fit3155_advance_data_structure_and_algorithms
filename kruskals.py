# Name: Chin Wen Yuan
# Student ID : 29975239
import sys


def read_file_line_by_line(filename):
    file = open(filename, "r")
    lines = file.readlines()
    graph = []
    for line in lines:
        line = line.strip("\n")
        line = line.split(" ")
        graph.append(line)
    return graph


def write_file(total_weight, content_arr):
    to_write = str(total_weight) + "\n"
    file = open("output_kruskals.txt", "w")
    for i in range(len(content_arr)):
        int_to_str = [str(item) for item in content_arr[i]]
        converted = " ".join(int_to_str)
        to_write += converted + "\n"
    file.write(to_write)
    file.close()


# weighted undirected graph
class Graph:

    def __init__(self, num_of_vertices):
        self.num_of_v = num_of_vertices
        self.graph = []

    # add an Edge to this graph
    def add_edge(self, u, v, w):
        self.graph.append((int(u), int(v), int(w)))

    # sort the edges of the graph according to weight
    def sort_edge(self):
        self.graph = sorted(self.graph, key=lambda item: item[2])

    # find set of an element i (uses path compression technique)
    def find(self, i, parent_arr):
        if parent_arr[i] == i:
            return i
        return self.find(parent_arr[i], parent_arr)

    # does the union of two sets (x and y) (uses union by rank)
    def union(self, x, y, parent_arr, rank_arr):
        # find the two of 2 element
        x_root = self.find(x, parent_arr)
        y_root = self.find(y, parent_arr)

        # compare the rank of the roots of x and y to determine the union
        # implements Union by Rank
        if rank_arr[x_root] < rank_arr[y_root]:
            parent_arr[x_root] = y_root
        elif rank_arr[x_root] > rank_arr[y_root]:
            parent_arr[y_root] = x_root
        # if the rank is the same
        # make y merge under x and increase x's root rank
        else:
            parent_arr[y_root] = x_root
            rank_arr[x_root] += 1

    def kruskal_mst(self):

        mst = []  # store the result minimum spanning tree of Graph

        edge_ind = 0  # use for indicating element in sorted edges of Graph

        mst_ind = 0  # use for indicating index in result mst (to make sure all vertices is accounted for)

        parent_arr = []

        rank_arr = []

        # initiate parent and rank array
        for node in range(self.num_of_v):
            parent_arr.append(node)
            rank_arr.append(0)

        # Step 1. sort the edges
        self.sort_edge()

        # Step 2. start from the smallest weight edge
        # and continuously picking edge until all vertices is included in mst
        while mst_ind < self.num_of_v - 1:
            # Step 2a. choose the smallest (weight) edge
            (u, v, w) = self.graph[edge_ind]
            # print("u: ", u)
            # print("v: ", v)
            # print("weight: ", w)
            # print("parent_arr: ", parent_arr)
            # print("rank_arr: ", rank_arr)
            x = self.find(u, parent_arr)
            y = self.find(v, parent_arr)

            # Step 2b. check if edge can be included into mst
            # -> not in the same tree (not same root)
            if x != y:
                mst_ind += 1
                mst.append([u, v, w])
                self.union(x, y, parent_arr, rank_arr)

            # go to next iteration
            edge_ind += 1

        # Calculate the total weight
        minimum_cost = 0
        for u, v, w in mst:
            minimum_cost += w
            # print("%d -- %d == %d" % (u, v, w))
        # print("Cost: ",minimum_cost)

        return minimum_cost, mst


def run(graph_representation, num_of_vertices):
    g = Graph(num_of_vertices)
    for u, v, w in graph_representation:
        g.add_edge(u, v, w)
    # g.kruskal_mst()
    total_cost, mst = g.kruskal_mst()
    write_file(total_cost, mst)


if __name__ == "__main__":
    # argument_00 = sys.argv[0]  # kruskals.py
    # argument_01 = sys.argv[1]  # argument_01 = "7"
    # argument_02 = sys.argv[2]  # argument_02 = "edge_file.txt"
    #
    # num_of_vertices = argument_01
    # graph_representation = read_file_line_by_line(argument_02)
    # run(graph_representation, num_of_vertices)

    num_of_vertices = 7
    graph_representation =  read_file_line_by_line("G.txt")
    run(graph_representation,num_of_vertices)
