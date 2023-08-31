# easy
# Write a function to find the longest common prefix string amongst an array of strings.
# If there is no common prefix, return an empty string "".

# Example 1:
# Input: strs = ["flower","flow","flight"]
# Output: "fl"

# Example 2:
# Input: strs = ["dog","racecar","car"]
# Output: ""
# Explanation: There is no common prefix among the input strings.

def longestCommonPrefix(strs):
    match = ""
    res = ""
    if 0 < len(strs) <= 200:
        if len(strs) == 1:
            return strs[-1]

        else:
            sample = strs[0]
            for index in range(1, len(strs)):
                i = 0
                while i < min(len(sample), len(strs[index])) and strs[index][i] == sample[i]:
                    match += sample[i]
                    i += 1

                res = match
                sample = match
                match = ""
    return res


print(longestCommonPrefix(["flower", "flow", "flight"]))
