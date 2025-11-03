'''
https://leetcode.com/problems/linked-list-cycle/description/?envType=study-plan-v2&envId=top-interview-150

141. Linked List Cycle
Easy
Topics
premium lock icon
Companies
Given head, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the next pointer. Internally, pos is used to denote the index of the node that tail's next pointer is connected to. Note that pos is not passed as a parameter.

Return true if there is a cycle in the linked list. Otherwise, return false.

 

Example 1:


Input: head = [3,2,0,-4], pos = 1
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).
Example 2:


Input: head = [1,2], pos = 0
Output: true
Explanation: There is a cycle in the linked list, where the tail connects to the 0th node.
Example 3:


Input: head = [1], pos = -1
Output: false
Explanation: There is no cycle in the linked list.
 

'''


from typing import Optional

# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None



def hasCycle(head: Optional[ListNode]) -> bool:

    #Edge case
    if not head or not head.next:
        return False
    
    #Using 2 pointers
    slow = head
    fast = head.next


    while fast and fast.next:
        if slow == fast:
            return True
    
        slow = slow.next
        fast = fast.next.next

    return False



#Test
def create_linked_list(nodes_val: list, pos: int) -> Optional[ListNode]:
    if not nodes_val:
        return None
    nodes = [ListNode(val) for val in nodes_val]
    head = nodes[0]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i+1]
    if pos != -1:
        nodes[-1].next = nodes[pos]
    return head


head = [3,2,0,-4]
pos = 1


print(hasCycle(None))