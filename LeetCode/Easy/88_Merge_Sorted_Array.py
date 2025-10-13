from typing import List

def merge(nums1: List[int], m: int, nums2: List[int], n: int) -> None:

    """
    Do not return anything, modify nums1 in-place instead.
    
    """

    num1_len = len(nums1)

    while n > 0:
        if nums1[m-1] > nums2[n-1] and m > 0:
            nums1[num1_len-1] = nums1[m-1]
            nums1[m-1] = 0
            m = m - 1
        else: 
            nums1[num1_len-1] = nums2[n-1]
            nums2[n-1] = 0
            n = n - 1
        num1_len -= 1


nums1 = [1]
m = 1
nums2 = []
n = 0


merge(nums1, m, nums2, n)
print(nums1)
