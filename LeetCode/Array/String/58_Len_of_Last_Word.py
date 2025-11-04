'''
https://leetcode.com/problems/length-of-last-word/description/?envType=study-plan-v2&envId=top-interview-150

58. Length of Last Word
Easy
Topics
premium lock icon
Companies
Given a string s consisting of words and spaces, return the length of the last word in the string.

A word is a maximal substring consisting of non-space characters only.

 

Example 1:

Input: s = "Hello World"
Output: 5
Explanation: The last word is "World" with length 5.
Example 2:

Input: s = "   fly me   to   the moon  "
Output: 4
Explanation: The last word is "moon" with length 4.
Example 3:

Input: s = "luffy is still joyboy"
Output: 6
Explanation: The last word is "joyboy" with length 6.


'''


class Solution:
    def lengthOfLastWord(self, s: str) -> int:

        counter = 0
        i = len(s) - 1

        #Case that ' ' is at the end
        while i >= 0 and s[i] == ' ':
            i = i - 1


        while i >= 0 and s[i] != ' ':
            counter = counter +1     
            i = i - 1 



        return counter
    



if __name__ == "__main__":
    solution = Solution()


    s = "   fly me   to   the moon  "

    print(solution.lengthOfLastWord(s))