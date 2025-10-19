'''
121. Best Time to Buy and Sell Stock
Easy
Topics
premium lock icon
Companies
You are given an array prices where prices[i] is the price of a given stock on the ith day.

You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.

Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/?envType=study-plan-v2&envId=top-interview-150

'''


# If next value is smaller, update
# else try subtract



from typing import List

def maxProfit(prices: List[int]) -> int:
    min = prices[0]
    diff = 0
    best = 0
    
    #Iterate
    for price in prices:

        #Update minimum price
        if price < min:
            min = price
        
        #최대 수익 갱신
        if price - min > diff:
            diff = price - min
            best = price
            
    
    if best - min < 0:
        return 0
    else:
        return diff











prices = [7,1,5,3,6,4]
prices_2 = [2,4,1]

print(maxProfit(prices_2))