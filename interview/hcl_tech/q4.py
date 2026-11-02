# 2. Moving average of a time series given a window size.

def moving_avg(arr, w):
    return [sum(arr[i:i+w])/w for i in range(len(arr)-w+1)]

print(moving_avg([1,2,3,4,5], 2))