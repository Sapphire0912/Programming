class ListNode:
    def __init__(self, val=0, Next=None):
        self.val = val
        self.next = Next


class Solution:
    def addTwoNumbers(self, l1, l2):
        sum_head = ListNode()
        p, q, curr_sum = l1, l2, sum_head
        carry = 0
        while p or q or carry:
            p, p_val = (p.next, p.val) if p else (p, 0)
            q, q_val = (q.next, q.val) if q else (q, 0)
            carry, sum_ = divmod(p_val + q_val + carry, 10)
            curr_sum.next = ListNode(sum_)
            curr_sum = curr_sum.next

        return sum_head.next


q1 = [2, 4, 3]
q2 = [5, 6, 4]
L1, L2 = None, None

for index, value in enumerate(q1):
    L1 = ListNode(val=value)
    if index + 1 == len(q1):
        L1.next = ListNode(0)
    else:
        L1.next = ListNode(q1[index + 1])
    L1 = L1.next

for index, value in enumerate(q2):
    L2 = ListNode(val=value)
    if index + 1 == len(q2):
        L2.next = ListNode(0)
    else:
        L2.next = ListNode(q2[index + 1])
    L2 = L2.next


S = Solution()
S.addTwoNumbers(L1, L2)

# unfinish

