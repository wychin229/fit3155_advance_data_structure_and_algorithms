from editdist import edit_dist_driver  # TODO: import your own edit dist -> modify function name below if necessary
import unittest


# TODO: expect output to be list of tuples in the form (index, edit distance)
class TestEditDistance(unittest.TestCase):
    def test_edit_zero(self):
        edit_zero_cases = [("abcd", "abcdabcdabcdabcd"), ("abc", "abcabcabc")]
        ans = [[(0, 0), (4, 0), (8, 0), (12, 0)], [(0, 0), (3, 0), (6, 0)]]
        for i in range(len(edit_zero_cases)):
            pat, text = edit_zero_cases[i]
            self.assertEqual(edit_dist_driver(text, pat), ans[i], "Case:\n" + "text: " + str(text) + "\npat: " + str(pat))

    def test_insertion(self):
        insertion_cases = [("abcd", "abdyabxdcyabcdz"), ("abc", "abdabdabcbcd")
            , ("abcd", "abdabdabcbcd"), ("abb", "abcasnfljacaqalabdoab")
            , ("bcb", "bbacbcaaacbbjalbb"), ("aaba", "ababa")
            , ("bcab", "bcbaccbabbbcb"), ("qqcda", "qqdaajfnqdqcdaaqqaaqqca"),
                           ("bbbc", "bbcalnbbcccbbc"), ("bcd", "cdelasbc"),
                           ("adcds", "dcdsaadcdcadcd"), ("aaa", "aaaaaaaa"), ("aa", "aaaaaaaa")
                           ]
        ans = [[(0, 1), (4, 1), (10, 0)], [(0, 1), (3, 1), (6, 0), (8, 1), (9, 1)],
               [(0, 1), (3, 1), (6, 1), (8, 1), (9, 1)], [(0, 1), (15, 1), (19, 1)],
               [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (8, 1), (9, 1), (10, 1), (15, 1)],
               [(0, 1), (1, 1), (2, 1)], [(0, 1), (6, 1), (10, 1)], [(0, 1), (8, 1), (9, 1), (10, 1), (19, 1)],
               [(0, 1), (5, 1), (6, 1), (10, 1), (11, 1)], [(0, 1), (6, 1)], [(0, 1), (5, 1), (10, 1)],
               [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)],
               [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)]]

        for i in range(len(insertion_cases)):
            pat, text = insertion_cases[i]
            self.assertEqual(edit_dist_driver(text, pat), ans[i],
                             "\nCase:\n" + "text: " + str(text) + "\npat: " + str(pat))

    def test_removal(self):
        removal_cases = [("bcda", "abcddabccda"), ("bcda", "abcdxabcgda"), ("acad", "acaxddcdadcaddacdad"),
                         ("aaxaa", "aadxaasaxaaaxdaa"), ("bbcbba", "bxbcbbacbbaabdbbcbsba"),
                         ("abcba", "abccbaabbcbaabcbba"), ("babb", "baabbbabbbbaxbbaabb")
                         ]
        ans = [[(1, 1), (6, 1), (7, 1), (8, 1)], [(1, 1), (6, 1)], [(0, 1), (8, 1), (9, 1), (10, 1), (14, 1)],
               [(0, 1), (1, 1), (5, 1), (6, 1), (7, 1), (10, 1)], [(0, 1), (1, 1), (2, 1), (4, 1), (5, 1), (14, 1)],
               [(0, 1), (6, 1), (7, 1), (8, 1), (12, 1)], [(0, 1), (1, 1), (2, 1), (3, 1), (5, 0), (7, 1), (8, 1),
                                                           (10, 1), (14, 1), (15, 1), (16, 1)]]

        for i in range(len(removal_cases)):
            pat, text = removal_cases[i]
            self.assertEqual(edit_dist_driver(text, pat), ans[i],
                             "\nCase:\n" + "text: " + str(text) + "\npat: " + str(pat))

    def test_substitution(self):
        substitution_cases = [("ab", "aaaaaaaaaaaa"), ("abcdd", "axcddabxddeababedd"),
                              ("ccedec", "cqedecccqdecccdddccefec")]
        ans = [[(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1)],
               [(0, 1), (5, 1), (13, 1)], [(0, 1), (6, 1), (17, 1)]]
        for i in range(len(substitution_cases)):
            pat, text = substitution_cases[i]
            self.assertEqual(edit_dist_driver(text, pat), ans[i], "Case:\n" + "text: " + str(text) + "\npat: " + str(pat))

    def test_edge_cases(self):
        edge_cases = [("bb", "b"), ("bb", "c"), ("acbdsfs", "acbdsf"), ("acbdsfsx", "acbdsd"),
                      ("aaaaaaaa", "a"),  # pattern longer than match
                      ("aaaaaaaaa", "aaaaaaaaa"), ("bbbbaabb", "bbbbbbbb"), ("akjdhsdab", "akjdhedab"),
                      ("akjhsdab", "akdhedab"),  # pattern same length
                      ("a", "aaaaaaaa"), ("a", "aaaaaaa"), ("b", "aaaaaaaa"), ("c", "b"), ("c", "c")]  # len(pat) = 1
        ans = [[(0, 1)], [], [(0, 1)], [], [], [(0, 0)], [], [(0, 1)], [],
               [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)],
               [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)],
               [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)], [(0, 1)], [(0, 0)]]
        for i in range(len(edge_cases)):
            pat, text = edge_cases[i]
            self.assertEqual(edit_dist_driver(text, pat), ans[i], "Case:"+str(i)+"\n" + "text: " + str(text) + "\npat: " + str(pat))

    def test_before_after_edit_zero(self):
        before_after_cases = [("ababa", "bababa"), ("ababa", "ababab"), ("ababa", "bbbabbabababbb"),
                              ("aadc", "aaaaaadc")]
        ans = [[(1, 0)], [(0, 0), (2, 1)], [(3, 1), (4, 1), (6, 0), (8, 1)], [(4, 0)]]
        for i in range(len(before_after_cases)):
            pat, text = before_after_cases[i]
            self.assertEqual(edit_dist_driver(text, pat), ans[i], "Case:\n" + "text: " + str(text) + "\npat: " + str(pat))


if __name__ == "__main__":
    unittest.main()