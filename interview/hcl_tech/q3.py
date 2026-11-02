# 12. Write a function that reverses the characters of each word in a string while preserving word order.
from q2 import timed
str1 = "How would you design a retryable LLM API call function"



def reverse(s):
    return " ".join(w[::-1] for w in s.split())


print(reverse(str1))