def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i



print(two_sum([1, 2, 3, 5], 6))

def func(nums, t):
    seen = {}
    for i, n in enumerate(nums):
        if t - n in seen:
            return [seen[t-n], i]
        seen[n] = i