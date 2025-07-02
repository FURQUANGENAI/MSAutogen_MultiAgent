
def max_subarray_sum(arr):
    if not arr:
        return 0
    
    max_current = max_global = arr[0]
    for num in arr[1:]:
        max_current = max(num, max_current + num)
        if max_current > max_global:
            max_global = max_current
    return max_global

# Test cases
print(max_subarray_sum([1, -3, 2, 1, -1])) # Test Case 1: Output should be 3 (subarray [2, 1])
print(max_subarray_sum([-2, -3, 4, -1, -2, 1, 5, -3])) # Test Case 2: Output should be 7 (subarray [4, -1, -2, 1, 5])
print(max_subarray_sum([-1, -1, -1, -1])) # Test Case 3: Output should be -1 (subarray [-1])
