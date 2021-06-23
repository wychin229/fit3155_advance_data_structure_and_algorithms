# Name: Chin Wen Yuan
# Student ID : 29975239
import sys
import csv


def read_file(filename):
    file = open(filename, "r")
    return file.read().strip("\n")


def write_file(content_arr):
    to_write = ""
    file = open("output_suffix_array.txt", "w")
    for i in range(len(content_arr)):
        to_write += str(content_arr[i]) + "\n"
    file.write(to_write)
    file.close()


def get_post(char):
    return ord(char) - 36  # $ -> 0, z -> 86


class Node:
    def __init__(self, start, end, suffix_index):
        self.child = [None] * 87  # as ord("z") - ord("$") + 1 = 87
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

    def generate_suffix_arr(self):
        suffix_arr = []
        current = self.root  # enter the Tree from the root
        suffix_arr += self.generate_suffix_aux(current)
        return suffix_arr

    def generate_suffix_aux(self, current_node):
        temp_arr = []
        if current_node.suffix_index != -1:  # a leaf
            temp_arr += [current_node.suffix_index]
        else:
            for i in range(87):
                if current_node.child[i] is not None:
                    temp_arr += self.generate_suffix_aux(current_node.child[i])
        return temp_arr

    # helper function for display()
    def display_child(self, child_list, lvl, parent_start, parent_end):
        j = 0
        got_child = False
        while j <= 87:
            if j < 87:
                if child_list[j] is not None:
                    got_child = True
                    node_start, node_end, depp_node_child = child_list[j].get_detail()
                    print("Lvl", lvl, " Child", node_start, " ", node_end, " ", parent_start, " ", parent_end)
                    self.display_child(depp_node_child, lvl + 1, node_start, node_end)

            if j == 87 and got_child is False:  # no children (leaf)
                print("Lvl", lvl - 1, " is Leaf", parent_start, " ", parent_end)
            j += 1

    # function to display the implicit tree produced
    def display(self):
        root_start, root_end, root_child = self.root.get_detail()
        print("Root", root_start, " ", root_end, "\n", root_child)
        self.display_child(root_child, 0, root_start, root_end)


def run(string):
    suffix_tree = ImplicitSuffixTree(string + "$")  # append terminal
    suffix_arr = suffix_tree.generate_suffix_arr()
    # print(suffix_arr)
    write_file(suffix_arr)
    # suffix_tree.display()


def test():
    file = open("test_ans.txt", "r")
    lines = file.readlines()
    ans = []
    for line in lines:
        line = line.strip("\n")
        line = line.split(" ")
        line = line[:len(line) - 1]
        ans.append(line)

    strings = []
    with open('strings.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            strings += row

    success = 0
    for i in range(min(len(ans), len(strings))):
        suffix_tree = ImplicitSuffixTree(strings[i] + "$")
        suffix_arr = suffix_tree.generate_suffix_arr()
        if len(suffix_arr) == len(ans[i]):
            for j in range(len(suffix_arr)):
                if suffix_arr[j] != int(ans[i][j]):
                    print("String: ", strings[i])
                    print("Found  : ", suffix_arr)
                    print("Correct: ", ans[i])
                    break
            success += 1

        else:
            print("Found  : ", suffix_arr)
            print("Correct: ", ans[i])
            break
    print(success)


if __name__ == "__main__":
    argument_00 = sys.argv[0]  # suffix_array.py
    argument_01 = sys.argv[1]  # argument_01 = "string.txt"

    string = read_file(argument_01)
    # string = read_file("s.txt")
    run(string)
    # run("abcababcacbccbab")
    # test()
