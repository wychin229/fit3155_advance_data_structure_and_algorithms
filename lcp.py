# Name: Chin Wen Yuan
# Student ID : 29975239
import sys


def read_file(filename):
    file = open(filename, "r")
    return file.read().strip("\n")


def read_pairs_from_file(filename):
    file = open(filename, "r")
    lines = file.readlines()
    pairs_arr = []
    for line in lines:
        line = line.strip("\n")
        line = line.split(" ")
        pair = (int(line[0]), int(line[1]))
        pairs_arr.append(pair)
    return pairs_arr


def write_file(content_arr):
    to_write = ""
    file = open("output_lcp.txt", "w")
    for item in content_arr:
        to_write += " ".join(str(elem) for elem in item) + "\n"
    file.write(to_write)
    file.close()


def get_post(char):
    return ord(char) - 35  # "#" -> 0, z -> 87


class Node:
    def __init__(self, start, end, suffix_index):
        self.child = [None] * 88  # as ord("z") - ord("$") + 1 = 88
        self.start_ind = start
        self.end_ind = end
        self.suffix_link = None
        self.suffix_index = suffix_index

    def get_detail(self):
        return self.start_ind, self.get_end_index(), self.child

    def get_end_index(self):
        if isinstance(self.end_ind, End):
            return self.end_ind.end_pointer
        else:
            return self.end_ind


class End:
    def __init__(self):
        self.end_pointer = -1  # initiate at root

    def increment(self):
        self.end_pointer += 1  # increment by 1 for Rule 1


class ImplicitSuffixTree:
    def __init__(self, text):
        self.end_pointer = End()
        self.root = None
        self.text = text
        self.previous_node = None
        self.active_node = Node
        self.active_length = 0
        self.active_edge = -1
        self.j = 0

        self.generate_by_ukkonen()

    def create_node(self, start, end, suffix_ind):
        node = Node(start, end, suffix_ind)
        # new node's suffix link by default is the root node
        node.suffix_link = self.root
        return node

    def phrase(self, i):
        # print("Phrase ", i)
        # Trick + Rule 1 : rapid leaf extension, will automatically handles adding new character to a leaf
        self.end_pointer.increment()

        while self.j <= i:
            # suffix_to_process = self.text[self.j:i + 1]
            # print("Iteration ", self.j, " ", suffix_to_process)

            if self.active_length == 0:
                self.active_edge = i

            position = get_post(self.text[self.active_edge])

            # Rule 2 : branch out
            # if current leaf does not exists, create a new one
            if self.active_node.child[position] is None:
                self.active_node.child[position] = self.create_node(i, self.end_pointer, self.j)

                # check if previously created another node in the same phrase
                if self.previous_node is not None:
                    self.previous_node.suffix_link = self.active_node
                    self.previous_node = None

            else:
                child_node = self.active_node.child[get_post(self.text[self.active_edge])]
                child_node_edge_length = child_node.get_end_index() - child_node.start_ind + 1

                # check if able to apply Trick 3: Skip Count
                if self.active_length >= child_node_edge_length:
                    # apply skip count
                    self.active_node = child_node  # change active node to its child (current_node)
                    self.active_length -= child_node_edge_length  # reset active length
                    self.active_edge += child_node_edge_length  # update active edge
                    continue  # reject all remaining statement and return to the top of while loop

                # Trick 4 : show stopper
                # if current character is present on the edge (Rule 3: already exist)
                # self.j will not be incremented in this phrase (freezed)
                if self.text[i] == self.text[self.active_node.child[position].start_ind + self.active_length]:
                    # update the suffix link of the previously created node to the current created node
                    if self.active_node != self.root and self.previous_node is not None:
                        self.previous_node.suffix_link = self.active_node
                        self.previous_node = None
                    self.active_length += 1
                    break  # break the loop and move to the next phrase

                # if current character is not present on the edge (Rule 2: branch out)
                # might happen in the middle of an existing edge
                else:
                    # starting index of the first part of the original edge (the matched prefix)
                    internal_start = self.active_node.child[position].start_ind
                    # the new node created is an internal node
                    # therefore, suffix_index = -1, indicates that its not a leaf
                    self.active_node.child[position] = self.create_node(internal_start,
                                                                        internal_start + self.active_length - 1, -1)

                    # check for any previously created node in the same i phrase but different j iteration
                    # required to update its suffix link
                    if self.previous_node is not None:
                        self.previous_node.suffix_link = self.active_node.child[position]

                    # save the new node to be the previous created node for the coming j iterations (in same i phrase)
                    self.previous_node = self.active_node.child[position]

                    # create a new node (leaf) for the second part of the original edge (unmatched suffix)
                    second_start = get_post(self.text[internal_start + self.active_length])
                    # update the new starting point of this edge
                    child_node.start_ind += self.active_length
                    self.active_node.child[position].child[second_start] = child_node
                    # the new node that holds the new character
                    new_leaf = get_post(self.text[i])
                    self.active_node.child[position].child[new_leaf] = self.create_node(i, self.end_pointer, self.j)

            # update the active length and active edge for next phrase
            # only the active node is updated as active edge and length remains unchanges as it is
            # referring to the same char in the text
            if self.active_node != self.root:
                self.active_node = self.active_node.suffix_link
            else:
                if self.active_length > 0:
                    self.active_edge = self.j + 1
                    self.active_length -= 1

            self.j += 1

            # if i == j, increment both, so that redundant work is avoided
            # this ensures O(n+n)
            if i == self.j - 1:
                self.j = i + 1

        # reset variable that stores previously created node
        self.previous_node = None

    def generate_by_ukkonen(self):
        self.root = self.create_node(-1, -1, -1)
        self.active_node = self.root  # traverse from root
        for i in range(len(self.text)):
            self.phrase(i)

    def traverse_tree_for_lcp(self, s1, index1, s2, index2):
        lcp = 0
        if index1 < len(s1) and index2 < len(s2):
            pos_s1 = get_post(s1[index1])
            pos_s2 = get_post(s2[index2])
            current_node = self.root.child[pos_s1]
            while pos_s1 == pos_s2:  # the 2 character matches
                # check if the children consist of children from both strings
                in_s1, in_s2 = self.check_if_both(current_node, len(s1))
                is_both = in_s1 and in_s2
                if is_both:
                    current_edge_length = current_node.get_end_index() - current_node.start_ind + 1
                    index1 += current_edge_length
                    index2 += current_edge_length
                    lcp += current_edge_length
                    if index1 < len(s1) and index2 < len(s2):
                        pos_s1 = get_post(s1[index1])
                        pos_s2 = get_post(s2[index2])
                        current_node = current_node.child[pos_s1]
                    else:
                        break
                else:
                    break
        return lcp

    # check if the current edge appears in both strings
    def check_if_both(self, node, len_s1):
        belong_s1 = False
        belong_s2 = False
        i = 0
        while i < 87:
            if node.child[i] is not None and node.child[i].suffix_index >= 0:  # is leaf
                # check if is leaf
                if node.child[i].start_ind > len_s1 + 1:  # belong to string 2
                    belong_s2 = True
                else:
                    belong_s1 = True
            elif node.child[i] is not None and node.child[i].suffix_index < 0:  # is not a leaf
                belong_s1, belong_s2 = self.check_if_both(node.child[i], len_s1)
            # if already checked that this node has children that belong to both strings, break the loop
            if belong_s1 and belong_s2:
                break
            i += 1
        return belong_s1, belong_s2

    # helper function for display()
    def display_child(self, child_list, lvl, parent_start, parent_end):
        j = 0
        got_child = False
        while j <= 87:
            if j < 87:
                if child_list[j] is not None:
                    got_child = True
                    node_start, node_end, depp_node_child = child_list[j].get_detail()
                    print("Lvl", lvl, " Child", node_start, " ", node_end, " ", parent_start, " ", parent_end, "index:",
                          child_list[j].suffix_index)
                    self.display_child(depp_node_child, lvl + 1, node_start, node_end)

            if j == 87 and got_child is False:  # no children (leaf)
                print("Lvl", lvl - 1, " is Leaf", parent_start, " ", parent_end)
            j += 1

    # function to display the implicit tree produced
    def display(self):
        root_start, root_end, root_child = self.root.get_detail()
        print("Root", root_start, " ", root_end, " ", self.root.suffix_index, "\n", root_child)
        self.display_child(root_child, 0, root_start, root_end)


def run(s1, s2, pairs):
    generalised_suffix_tree = ImplicitSuffixTree(s1 + "#" + s2 + "$")
    # generalised_suffix_tree.display()
    lcps = []
    for pair in pairs:
        lcp = generalised_suffix_tree.traverse_tree_for_lcp(s1, pair[0], s2, pair[1])
        # print("lcp: ", lcp, "  str1: ", s1[pair[0]:], "  str2:", s2[pair[1]:])
        lcps.append((pair[0], pair[1], lcp))
    write_file(lcps)


if __name__ == "__main__":
    argument_00 = sys.argv[0]  # lcp.py
    argument_01 = sys.argv[1]  # argument_01 = "s1.txt"
    argument_02 = sys.argv[2]  # argument_01 = "s2.txt"
    argument_03 = sys.argv[3]  # argument_01 = "pairs.txt"

    s1 = read_file(argument_01)
    s2 = read_file(argument_02)
    pairs = read_pairs_from_file(argument_03)
    # s1 = read_file("s1.txt")
    # s2 = read_file("s2.txt")
    # pairs = read_pairs_from_file("lcp_pairs.txt")
    run(s1,s2,pairs)
    # run("abcdacbdab","dacbdabc",[(3,0),(4,2),(0,5)])
    # run("abc", "abc", [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)])
