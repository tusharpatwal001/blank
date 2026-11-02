# 4. Reverse each word in a sentence while keeping word order.


input= "Let's take LeetCode contest"
output= "s'teL ekat edoCteeL tsetnoc"


def reverse(s):
    return " ".join([word[::-1] for word in s.split(" ")])

print(output == reverse(input))

print(reverse(input))