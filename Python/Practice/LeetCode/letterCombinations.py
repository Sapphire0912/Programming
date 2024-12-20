# Given a string containing digits from 2-9 inclusive, return all possible letter combinations
# that the number could represent.
# Return the answer in any order.

# A mapping of digit to letters (just like on the telephone buttons) is given below.
# Note that 1 does not map to any letters.


def letterCombinations(digits):
    result = []
    dicts = {
        '2': ['a', 'b', 'c'],
        '3': ['d', 'e', 'f'],
        '4': ['g', 'h', 'i'],
        '5': ['j', 'k', 'l'],
        '6': ['m', 'n', 'o'],
        '7': ['p', 'q', 'r', 's'],
        '8': ['t', 'u', 'v'],
        '9': ['w', 'x', 'y', 'z']
    }

    if 0 < len(digits) <= 4 and digits.isdigit():
        if len(digits) == 1:
            return dicts[digits]
        else:
            result = [s for s in dicts[digits[0]]]
            for key in digits:
                if key not in dicts.keys():
                    return result

                else:
                    reg = list()
                    for f in result:
                        for d in dicts[key]:
                            reg.append(f+d)
                    result = reg
    return result


a = letterCombinations("23")
print(a)


