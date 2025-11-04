'''
https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/description/?envType=study-plan-v2&envId=top-interview-150

28. Find the Index of the First Occurrence in a String
Easy
Topics
premium lock icon
Companies
Given two strings needle and haystack, return the index of the first occurrence of needle in haystack, or -1 if needle is not part of haystack.

 

Example 1:

Input: haystack = "sadbutsad", needle = "sad"
Output: 0
Explanation: "sad" occurs at index 0 and 6.
The first occurrence is at index 0, so we return 0.
Example 2:

Input: haystack = "leetcode", needle = "leeto"
Output: -1
Explanation: "leeto" did not occur in "leetcode", so we return -1.

'''


class Solution:
    def strStr(self, haystack: str, needle: str) -> int:

        window_size = len(needle)

        #Check expection
        if window_size > len(haystack):
            return -1




        for i in range (len(haystack) - window_size + 1):
            curr = haystack[i:i+window_size]
            print(curr)

            if curr == needle:
                return i
            
        return -1

    def KPM_algo(self, haystack: str, needle: str) -> int:

        '''
        슬라이딩 윈도우'를 개선한 **"더 똑똑한 슬라이딩 윈도우"**라고 생각하시면 됩니다.
        아이디어: needle("찾을 문자열")을 미리 분석해서 '패턴 테이블'을 만들어 둡니다.
        예시: haystack = "abacaabac", needle = "abac"needle의 "aba"까지 일치했는데, 4번째 글자('c')가 틀렸다고 가정해봅시다.
        단순 슬라이딩 윈도우: needle을 한 칸만 이동해서 haystack의 두 번째 글자부터 다시 비교합니다. 
        (비효율적)KMP: "aba"라는 패턴을 분석한 결과, 다음 비교는 2칸을 건너뛰고 haystack의 3번째 글자부터 시작해도 된다는 것을 미리 알고 있습니다.
        장점: 불필요한 비교를 건너뛰기 때문에 훨씬 빠릅니다.시간 복잡도: $O(H + N)$needle 분석에 $O(N)$, haystack 검색에 $O(H)$가 걸립니다.
        '''

        #Create Pattern Table





        return None


    def simple_ver(self, haystack: str, needle: str) -> int:
        return haystack.find(needle)




if __name__ == "__main__":

    solution = Solution()

    haystack = "badbutsad"
    needle = "cad"

    # haystack_2 = "leetcode", 
    # needle_2 = "leeto"

    print(solution.simple_ver(haystack, needle))
    