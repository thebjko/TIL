---
created_at : 2023-07-11, Tue
유효기록일 : 2023-07-11, Tue
topics : 
context : 
tags : algorithm BST
related : 
---
# Binary Search Tree
```python
class Node:
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None


class BinarySearchTree:
	def __init__(self):
		self.root = None

	def insert(self, value):
		# create new_node
		new_node = Node(value)

		# edge case 1: self.root is None
		if self.root is None:
			self.root = new_node
			return True

		temp = self.root

		# while loop
		while True:
			# if new_node == temp return False
			if new_node.value == temp.value:
				return False
			# if < left else > right
			if new_node.value < temp.value:
				# if None insert new_node else move to next
				if temp.left is None:
					temp.left = new_node
					return True
				temp = temp.left
			else:
				# if None insert new_node else move to next
				if temp.right is None:
					temp.right = new_node
					return True
				temp = temp.right

	def contains(self, value):
		# if self.root is None:
		#	return False

		temp = self.root
		while temp is not None:
			if value < temp.value:
				temp = temp.left
			elif value > temp.value:
				temp = temp.right
			else:
				return True
		return False

```



---
# 참고자료
- Python Data Structures & Algorithms + LEETCODE Exercises


[^1]: 
