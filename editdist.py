# Name: Chin Wen Yuan
# Student ID : 29975239
import sys


def read_file(filename):
    file = open(filename,"r")
    text = file.read()
    file.close()
    return text


def write_file(result_arr):
    content = ""
    for i in range(0,len(result_arr)):
        content += str(result_arr[i][0]) + " " + str(result_arr[i][1]) + "\n"
    file = open("output_editdist.txt","w")
    file.write(content)
    file.close()


def z_algo(text, pattern):
    string = pattern + "$" + text
    z_arr = [0]*len(string)
    n = len(string)

    l, r = 0, 0

    for i in range(1, n):
        # Case 1 : where current i is outside of the Z-box
        if i > r:
            l, r = i, i

            while r < n and string[r - l] == string[r]:
                r += 1
            z_arr[i] = r - l
            r -= 1
        # Case 2 : where current i is within the Z-box
        else:
            # find the corresponding index from the prefix of the string

            k = i - l

            # Case 2a : Z[k] is less than remaining
            if z_arr[k] < r - i + 1:
                z_arr[i] = z_arr[k]
            # Case 2b : Z[k] is larger than remaining
            elif z_arr[k] > r - i + 1:
                z_arr[i] = r - i + 1
            # Case 2c : Z[k] is equal to remaining
            else:
                l = i
                while r < n and string[r - l] == string[r]:
                    r += 1
                z_arr[i] = r - l
                r -= 1
    return z_arr


# can reverse string or array
def get_reversed(str_or_arr):
    return str_or_arr[::-1]


def get_edit_dist(prefix_z_arr, suffix_z_arr, pattern_len):
    edit_dist = [-1]*len(prefix_z_arr)

    for i in range(0,len(prefix_z_arr)):
        if prefix_z_arr[i] == pattern_len:
            edit_dist[i] = 0
        else:
            deletion = i + pattern_len
            if deletion < len(prefix_z_arr):
                if prefix_z_arr[i] + suffix_z_arr[deletion] >= pattern_len:
                    edit_dist[i] = 1
            substitution = i + pattern_len - 1
            if substitution < len(prefix_z_arr):
                if prefix_z_arr[i] + suffix_z_arr[substitution] == pattern_len - 1:
                    edit_dist[i] = 1
            insertion = i + pattern_len - 2
            if insertion < len(prefix_z_arr):
                if prefix_z_arr[i] + suffix_z_arr[insertion] > insertion - i and pattern_len-2 >= 0:
                    edit_dist[i] = 1

    # remove redundant match
    for i in range(0,len(edit_dist)-1):
        if edit_dist[i] == 0:
            if edit_dist[i+1] == 1:
                edit_dist[i+1] = -1
            if edit_dist[i-1] == 1:
                edit_dist[i-1] = -1

    return edit_dist


def edit_dist_driver(text, pattern):

    reversed_text = get_reversed(text)
    reversed_pattern = get_reversed(pattern)

    prefix_z_arr = z_algo(text, pattern)
    prefix_z_arr = prefix_z_arr[len(pattern) + 1:]

    suffix_z_arr = z_algo(reversed_text, reversed_pattern)
    suffix_z_arr = suffix_z_arr[len(pattern) + 1:]
    suffix_z_arr = get_reversed(suffix_z_arr)

    edit_dist = get_edit_dist(prefix_z_arr, suffix_z_arr, len(pattern))
    result = []
    for i in range(0, len(edit_dist)):
        if edit_dist[i] != -1:
            result.append((i,edit_dist[i]))

    write_file(result)
    return result


if __name__ == "__main__":
    argument_00 = sys.argv[0]   # Assignment_Run.py
    argument_01 = sys.argv[1]   # argument_01 = "text.txt"
    argument_02 = sys.argv[2]   # argument_02 = "pattern.lol"

    text = read_file(argument_01)
    pattern = read_file(argument_02)
    # text = "abcddabccda"
    # pattern = "c"

    edit_dist_driver(text,pattern)

