'''
https://leetcode.com/problems/merge-sorted-array/description/?envType=study-plan-v2&envId=top-interview-150
88. Merge Sorted Array
Solved
Easy
Topics
premium lock icon
Companies
Hint
You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively.

Merge nums1 and nums2 into a single array sorted in non-decreasing order.

The final sorted array should not be returned by the function, but instead be stored inside the array nums1. To accommodate this, nums1 has a length of m + n, where the first m elements denote the elements that should be merged, and the last n elements are set to 0 and should be ignored. nums2 has a length of n.
'''

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
