def romanToInt(s):
    roman = {'': 0, 'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    total, before = 0, ''

    for i in range(len(s) - 1, -1, -1):
        if roman[s[i]] < roman[before]:
            total = total - roman[s[i]]
        else:
            total = total + roman[s[i]]
        before = s[i]
    return total


print(romanToInt("MCMXCIV"))
