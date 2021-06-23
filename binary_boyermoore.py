# Name: Chin Wen Yuan
# Student ID : 29975239
import sys


def read_file(filename):
    file = open(filename,"r")
    return file.read()


def write_file(content_arr):
    to_write = ""
    file = open("output_binary_boyermoore.txt","w")
    for i in range(len(content_arr)):
        to_write += str(content_arr[i]) + "\n"
    file.write(to_write)
    file.close()


# Gusfield's Z-algorithm from task 1
def z_algo(string):
    n = len(string)
    z_arr = [0]*n
    z_arr[0] = n

    l, r = 0, 0

    for i in range(1, n):
        if i > r:
            l, r = i, i

            while r < n and string[r - l] == string[r]:
                r += 1
            z_arr[i] = r - l
            r -= 1
        else:
            k = i - l

            if z_arr[k] < r - i + 1:
                z_arr[i] = z_arr[k]
            elif z_arr[k] > r - i + 1:
                z_arr[i] = r - i + 1
            else:
                l = i
                while r < n and string[r - l] == string[r]:
                    r += 1
                z_arr[i] = r - l
                r -= 1
    return z_arr


def get_reversed(str_or_arr):
    return str_or_arr[::-1]


# Bad Character: the position of the RIGHTMOST char of the alphabets that is to the left of the mismatch index
# characters is sorted using their ascii value
# first row R1(x) saves the alphabet's ascii value
def get_bad_char_arr(alphas,pattern):
    bad_char_arr = [[-1 for _ in range(len(alphas))] for _ in range(len(pattern))]
    for i in range(len(pattern)):
        count = i - 0
        for j in range(count):
            if get_ascii_value(pattern[j]) == get_ascii_value(str(0)): # equals to 0
                bad_char_arr[i][0] = j
            elif get_ascii_value(pattern[j]) == get_ascii_value(str(1)): # equals to 1
                bad_char_arr[i][1] = j
    return bad_char_arr


# Good Suffix: for each suffix starting at position j in pat, store the RIGHTMOST position p such that
# 1: pat[j..m] == pat[p-reverse_z_arr[p]+1..p]
# 2: pat[j-1] != pat[p-reverse_z_arr[p]]
def get_good_suffix(reverse_z_arr, pattern_len):
    good_suffix = [0]*(pattern_len+1)
    for j in range(pattern_len-1):
        k = pattern_len -1 - reverse_z_arr[j] + 1
        good_suffix[k] = j

    return good_suffix


def get_ascii_value(character):
    return ord(character)


def get_matched_prefix(z_arr, pattern_len):
    matched_prefix_arr = [0]*(pattern_len+1)

    for i in range(pattern_len):
        x = z_arr[pattern_len-i-1] + pattern_len-i-1
        y = pattern_len
        if x != y and pattern_len-i < pattern_len:
            matched_prefix_arr[pattern_len-i-1] = matched_prefix_arr[pattern_len-i]
        else:
            matched_prefix_arr[pattern_len-i-1] = z_arr[pattern_len-i-1]

    return matched_prefix_arr


class BinaryBoyerMoore(object):

    def __init__(self,pattern):
        self.alphabets = ["0","1"]
        self.z_arr = z_algo(pattern)
        self.pat_len = len(pattern)

        # pre-processing
        self.bad_char_arr = get_bad_char_arr(self.alphabets,pattern)
        suffix_z_arr = z_algo(get_reversed(pattern))
        self.suffix_z_arr = get_reversed(suffix_z_arr[1:])
        self.good_suffix_arr = get_good_suffix(self.suffix_z_arr, len(pattern))
        self.matched_prefix_arr = get_matched_prefix(self.z_arr, len(pattern))


    # should return the number of shifts for this rule
    def bad_char_rule(self,mismatch_pat_index,mismatch_txt_char):
        # get the closest match char for the mismatch character in the text
        closest_match = self.bad_char_arr[mismatch_pat_index][get_ascii_value(mismatch_txt_char)-48]
        pos_to_shift = mismatch_pat_index-closest_match

        return pos_to_shift

    # should return the number of shifts for this rule
    def good_suffix_rule(self,mismatch_pat_index):
        # case 1a : if a mismatch occurs at k and good_suffix(k+1) > 0
        if self.good_suffix_arr[mismatch_pat_index+1] > 0:
            return self.pat_len -1 - self.good_suffix_arr[mismatch_pat_index+1]
        # case 1b : if a mismatch occurs at k and good_suffix(k+1) = 0
        elif self.good_suffix_arr[mismatch_pat_index+1] == 0:
            return self.pat_len - self.matched_prefix_arr[mismatch_pat_index+1]

    def matched(self):
        if self.pat_len > 1:
            return self.pat_len - self.matched_prefix_arr[1]
        else:
            return 0

    def check_good_suffix_rule(self,mismatch_pat_index):
        return self.good_suffix_arr[mismatch_pat_index+1] > 0

def bm_driver(text,pattern):
    driver = BinaryBoyerMoore(pattern)

    m = len(pattern)
    n = len(text)
    comparison = 0
    occurs = []
    pointer = 0 # initial pointer in text
    pause = -1
    resume = -1
    while pointer <= n-m:

        to_shift = 1
        k = m-1 # pointer for pattern
        mismatched = False
        while k >= 0 and k < m:

            if k >= pause or k <= resume:
                if text[pointer + k] != pattern[k]:

                    n_bad_char = driver.bad_char_rule(k, text[pointer + k])
                    n_good_suffix = driver.good_suffix_rule(k)
                    to_shift = max(to_shift,n_bad_char, n_good_suffix)

                    # Galil's Optimization
                    if n_good_suffix >= n_bad_char:
                        if driver.check_good_suffix_rule(k):  # uses good suffix
                            pause = driver.good_suffix_arr[k + 1]
                            resume = driver.good_suffix_arr[k + 1] - (m - 1) + k + 1  # resume comparison here
                        else:
                            pause = driver.matched_prefix_arr[k + 1] - 1
                            resume = 0
                    mismatched = True
                    pointer += to_shift
                    break
                else:
                    k -= 1
            else:
                k = resume - 1

            comparison += 1

        if not mismatched:
            occurs.append(pointer)
            pointer += driver.matched()
            # Galil's Optimization
            pause = m - 1 - driver.matched()
            resume = 0

    return comparison, occurs


def test_bm():
    text_file = open("test_binary.txt","r")
    test_text = text_file.readlines()
    texts = []
    for line in test_text:
        texts.append(line.strip("\n"))
    pat_file = open("test_pattern.txt","r")
    test_pat = pat_file.readlines()
    patterns = []
    for line in test_pat:
        patterns.append(line.strip("\n"))
    ans_file = open("output_BM.txt","r")
    ans = ans_file.readlines()
    expected = []
    for line in ans:
        line = line.strip("\n")
        if len(line) > 0:
            line = line.split(" ")
            res = []
            for i in range(len(line)):
                if len(line[i]) > 0:
                    res.append(int(line[i]))
            expected.append(res)
        else:
            expected.append([])
    print(len(texts),len(patterns),len(expected))

    success = 0
    failed = 0
    for i in range(len(texts)):
        compare, result = bm_driver(texts[i],patterns[i])
        if result == expected[i]:
            success += 1
        else:
            print("successed so far : ",success)
            print("string: ",texts[i])
            print("pattern: ",patterns[i])
            print("expected: ",expected[i])
            print("result  : ",result)
            print("comparison took ",compare)
            break

    print("Succeed test cases: ",success)
    print("Failed test cases: ",failed)
    # compare num of comparison before and after optimization
    no_opti_file = open("no_opti.txt","r")
    no_opti_num = no_opti_file.readlines()
    no_opti = []
    for line in no_opti_num:
        line = line.strip(" ")
        line = line.split(":")
        no_opti.append(line[1])
    opti_file = open("opti.txt","r")
    opti_num = opti_file.readlines()
    opti = []
    for line in opti_file:
        line = line.strip(" ")
        line = line.split(":")
        opti.append(line[1])
    bad = 0
    for i in range(len(opti)):
        if opti[i] > no_opti[i]:
            bad += 1
    print("Bad : ",bad)


if __name__ == "__main__":
    argument_00 = sys.argv[0]   # Assignment_Run.py
    argument_01 = sys.argv[1]   # argument_01 = "text.txt"
    argument_02 = sys.argv[2]   # argument_02 = "pattern.lol"

    # text = "0011010101111001001101100"
    # pattern = "010"

    text = read_file(argument_01)
    pattern = read_file(argument_02)

    comparison, occurs = bm_driver(text,pattern)
    write_file(occurs)
    print(comparison)
    # test_bm() #
