# Given a string s containing just the characters '(', ')', '{', '}', '[' and ']',
# determine if the input string is valid.
# An input string is valid if:
#
# Open brackets must be closed by the same type of brackets.
# Open brackets must be closed in the correct order.


def isValid(s):
    bracket_map = {'(': ')', '[': ']', '{': '}'}
    keys = ['(', '[', '{']
    stack = list()

    if len(s) % 2 != 0:
        return False

    for i in s:
        if i in keys:
            stack.append(i)
            print("append: ", stack)

        elif stack and bracket_map[stack[-1]] == i:
            stack.pop(-1)
            print("remove: ", stack)
        else:
            return False

    return stack == []


a = isValid("[([]])")
print(a)
