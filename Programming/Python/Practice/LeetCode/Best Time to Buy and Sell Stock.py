# You are given an array prices where prices[i] is the price of a given stock on the ith day.
#
# You want to maximize your profit by choosing a single day to buy one stock and
# choosing a different day in the future to sell that stock.
#
# Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

def maxProfit(prices):
    if len(prices) <= 1:
        return 0

    cur_min, max_pt = prices[0], 0
    for i in range(1, len(prices)):
        if prices[i] < cur_min:
            cur_min = prices[i]
            continue

        if prices[i] - cur_min > max_pt:
            max_pt = prices[i] - cur_min
            
    return max(max_pt, 0)


print(maxProfit([3, 2, 6, 5, 0, 3]))
