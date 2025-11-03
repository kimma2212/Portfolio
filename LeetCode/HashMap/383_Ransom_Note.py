'''
https://leetcode.com/problems/ransom-note/description/?envType=study-plan-v2&envId=top-interview-150


383. Ransom Note
Easy
Topics
premium lock icon
Companies
Given two strings ransomNote and magazine, return true if ransomNote can be constructed by using the letters from magazine and false otherwise.

Each letter in magazine can only be used once in ransomNote.

 

Example 1:

Input: ransomNote = "a", magazine = "b"
Output: false
Example 2:

Input: ransomNote = "aa", magazine = "ab"
Output: false
Example 3:

Input: ransomNote = "aa", magazine = "aab"
Output: true

'''




# def canConstruct(ransomNote: str, magazine: str) -> bool:
#     first = {}

#     for letter in magazine:
#         if letter in first:
#             first[letter] += 1
#         else:
#             first[letter] = 1

#     for i in ransomNote:
#         if i in first:
#             first[i] -= 1
#             if first[i] < 0:
#                 return False
#         else:
#             return False
        
    
#     return True



#Using collection

import collections
def canConstruct(ransomNote: str, magazine: str) -> bool:
    first = {}

    mag = collections.Counter(magazine)

    rans = collections.Counter(ransomNote)

    for i, count in rans.items():
        if mag[i] < count:
            return False
        
    
    return True




ransomNote = "a"
magazine = "b"


ransomNote_2 = "aa"
magazine_2 = "aab"

print(canConstruct(ransomNote, magazine))