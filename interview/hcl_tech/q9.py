# 7. Count character frequency and return the top-k most frequent characters.

from collections import Counter


def top_k_chars(s, k):
    return Counter(s).most_common(k)

print(top_k_chars("abcabcfbhslfkfnlcfjb", 2))


