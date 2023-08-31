# Medium
# Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]],
# such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0.
# Notice that the solution set must not contain duplicate triplets.

import time


def threeSum(nums):
    if len(nums) < 3:
        return []

    reg = list()
    nums.sort()
    for st in range(len(nums) - 2):
        nd = st + 1
        rd = len(nums) - 1  # 最大值

        while nd < rd:
            total = nums[st] + nums[nd] + nums[rd]
            if total == 0:
                reg.append([nums[st], nums[nd], nums[rd]])
                nd += 1
                rd -= 1

            elif total > 0:
                rd -= 1

            elif total < 0:
                nd += 1

    # 符合條件且不重複的答案放到 ans 裡面
    ans = list()
    for i in reg:
        if i not in ans:
            ans.append(i)
    return ans


st = time.time()
s = [-1, 0, 1, 2, -1, -4]
print(s)
res = threeSum(s)
end = time.time()
print(res)
print("%.5f" % (end - st))

