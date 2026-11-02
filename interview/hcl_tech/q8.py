# 6. Second largest element in an array without sorting.


def second_largest(arr):
    first = second = float("-inf")
    for n in arr:
        if n > first:
            first, second = n, first
        elif first > n > second: second = n
    return second if second != float("-inf") else None

print(second_largest([1,2,3,4,5]))
