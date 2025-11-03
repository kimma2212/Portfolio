'''
https://leetcode.com/problems/majority-element/description/?envType=study-plan-v2&envId=top-interview-150

169. Majority Element
Easy
Topics
premium lock icon
Companies
Given an array nums of size n, return the majority element.

The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

'''



from typing import List




def majorityElement(nums: List[int]) -> int:
    counter = {}
    for num in nums:
        if num in counter:
            counter[num] += 1
        else:
            counter[num] = 1
    


    return max(counter, key=counter.get)




nums = [3,2,3]

print(majorityElement(nums))