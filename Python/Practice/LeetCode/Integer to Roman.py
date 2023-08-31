# Median
# Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M.
# Symbol Value
# I 1, V 5, X 10, L 50, C 100, D 500, M 1000
# Example 1:
# Input: num = 3
# Output: "III"
# Example 2:
# Input: num = 4
# Output: "IV"
# Example 3:
# Input: num = 9
# Output: "IX"
# Example 4:
# Input: num = 58
# Output: "LVIII"
# Explanation: L = 50, V = 5, III = 3.
# Example 5:
# Input: num = 1994
# Output: "MCMXCIV"
# Explanation: M = 1000, CM = 900, XC = 90 and IV = 4.

# myself
def intToRoman(num):
    if 0 <= num <= 3999:
        sp = {4: 'IV', 9: 'IX', 40: 'XL', 90: 'XC', 400: 'CD', 900: 'CM'}
        one = num % 10
        ten = num % 100 - one
        hundred = num % 1000 - ten - one
        thousand = num // 1000

        res = ''
        if thousand > 0:
            for i in range(thousand):
                res += 'M'

        if hundred in sp.keys():
            res += sp[hundred]
        else:
            if hundred < 500:
                for i in range(0, hundred, 100):
                    res += 'C'
            elif hundred > 5:
                res += 'D'
                for i in range(0, hundred - 500, 100):
                    res += 'C'
            else:
                res += 'D'

        if ten in sp.keys():
            res += sp[ten]
        else:
            if ten < 50:
                for i in range(0, ten, 10):
                    res += 'X'
            elif ten > 50:
                res += 'L'
                for i in range(0, ten - 50, 10):
                    res += 'X'
            else:
                res += 'L'

        if one in sp.keys():
            res += sp[one]
        else:
            if one < 5:
                for i in range(one):
                    res += 'I'
            elif one > 5:
                res += 'V'
                for i in range(one - 5):
                    res += 'I'
            else:
                res += 'V'
        return res
    return None


# others
VALUES = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
CODES = ['M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']


def intToRoman2(num) -> str:
    # Constraint 1 <= num <= 3999
    # Max chars are 15 with 3888 number
    str_list = 15 * ['']
    str_index = 0

    # O(1 * log N)
    for i in range(len(VALUES)):
        while num >= VALUES[i]:
            str_list[str_index] = CODES[i]
            str_index += 1
            num -= VALUES[i]

    # O(1)
    return str.join("", str_list)


for test in [3, 4, 9, 58, 1994, 3999]:
    print(intToRoman2(test))
