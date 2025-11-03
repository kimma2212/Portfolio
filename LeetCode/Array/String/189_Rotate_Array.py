'''
https://leetcode.com/problems/rotate-array/description/?envType=study-plan-v2&envId=top-interview-150

189. Rotate Array
Medium
Topics
premium lock icon
Companies
Hint
Given an integer array nums, rotate the array to the right by k steps, where k is non-negative.

 

Example 1:

Input: nums = [1,2,3,4,5,6,7], k = 3
Output: [5,6,7,1,2,3,4]
Explanation:
rotate 1 steps to the right: [7,1,2,3,4,5,6]
rotate 2 steps to the right: [6,7,1,2,3,4,5]
rotate 3 steps to the right: [5,6,7,1,2,3,4]
Example 2:

Input: nums = [-1,-100,3,99], k = 2
Output: [3,99,-1,-100]
Explanation: 
rotate 1 steps to the right: [99,-1,-100,3]
rotate 2 steps to the right: [3,99,-1,-100]

'''

from typing import List


class Solution:
    def rotate(self, nums: List[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        nums[:] = nums[-k:] + nums[:-k]
        


if __name__ == "__main__":

    solution = Solution()

    nums = [1,2,3,4,5,6,7]
    k = 3


    #before
    print(f"Before: {nums}")

    solution.rotate(nums, k)

    #after
    print(f"After: {nums}")