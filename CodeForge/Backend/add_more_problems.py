#!/usr/bin/env python3
"""
Script to add more coding problems to the CodeForge database
"""

import asyncio
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# MongoDB connection
MONGODB_URL = "mongodb+srv://harshpatel:Harsh2005@cluster0.d9fud.mongodb.net/codeforge?retryWrites=true&w=majority&appName=Cluster0"

problems_to_add = [
    {
        "title": "Reverse Integer",
        "slug": "reverse-integer",
        "difficulty": "easy",
        "description": "Given a signed 32-bit integer x, return x with its digits reversed. If reversing x causes the value to go outside the signed 32-bit integer range [-2^31, 2^31 - 1], then return 0.",
        "examples": [
            {"input": "x = 123", "output": "321"},
            {"input": "x = -123", "output": "-321"},
            {"input": "x = 120", "output": "21"}
        ],
        "constraints": ["-2^31 <= x <= 2^31 - 1"],
        "tags": ["Math", "Integer Manipulation"],
        "acceptance_rate": 25.6,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Palindrome Number",
        "slug": "palindrome-number",
        "difficulty": "easy",
        "description": "Given an integer x, return true if x is palindrome integer. An integer is a palindrome when it reads the same backward as forward.",
        "examples": [
            {"input": "x = 121", "output": "true"},
            {"input": "x = -121", "output": "false"},
            {"input": "x = 10", "output": "false"}
        ],
        "constraints": ["-2^31 <= x <= 2^31 - 1"],
        "tags": ["Math", "Palindrome"],
        "acceptance_rate": 49.6,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Roman to Integer",
        "slug": "roman-to-integer",
        "difficulty": "easy",
        "description": "Roman numerals are represented by seven different symbols: I, V, X, L, C, D and M. Given a roman numeral, convert it to an integer.",
        "examples": [
            {"input": "s = \"III\"", "output": "3"},
            {"input": "s = \"LVIII\"", "output": "58"},
            {"input": "s = \"MCMXC\"", "output": "1994"}
        ],
        "constraints": ["1 <= s.length <= 15", "s contains only the characters ('I', 'V', 'X', 'L', 'C', 'D', 'M')"],
        "tags": ["Hash Table", "Math", "String"],
        "acceptance_rate": 58.1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Longest Common Prefix",
        "slug": "longest-common-prefix",
        "difficulty": "easy",
        "description": "Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string \"\".",
        "examples": [
            {"input": "strs = [\"flower\",\"flow\",\"flight\"]", "output": "\"fl\""},
            {"input": "strs = [\"dog\",\"racecar\",\"car\"]", "output": "\"\""}
        ],
        "constraints": ["1 <= strs.length <= 200", "0 <= strs[i].length <= 200"],
        "tags": ["String", "Array"],
        "acceptance_rate": 38.9,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses-2",
        "difficulty": "easy",
        "description": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.",
        "examples": [
            {"input": "s = \"()\"", "output": "true"},
            {"input": "s = \"()[]{}\"", "output": "true"},
            {"input": "s = \"(]\"", "output": "false"}
        ],
        "constraints": ["1 <= s.length <= 10^4", "s consists of parentheses only '()[]{}'."],
        "tags": ["String", "Stack"],
        "acceptance_rate": 40.7,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "difficulty": "easy",
        "description": "You are given the heads of two sorted linked lists list1 and list2. Merge the two lists in a one sorted list.",
        "examples": [
            {"input": "list1 = [1,2,4], list2 = [1,3,4]", "output": "[1,1,2,3,4,4]"},
            {"input": "list1 = [], list2 = []", "output": "[]"}
        ],
        "constraints": ["The number of nodes in both lists is in the range [0, 50]", "-100 <= Node.val <= 100"],
        "tags": ["Linked List", "Recursion"],
        "acceptance_rate": 59.8,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Remove Duplicates from Sorted Array",
        "slug": "remove-duplicates-from-sorted-array",
        "difficulty": "easy",
        "description": "Given an integer array nums sorted in non-decreasing order, remove the duplicates in-place such that each unique element appears only once.",
        "examples": [
            {"input": "nums = [1,1,2]", "output": "2, nums = [1,2,_]"},
            {"input": "nums = [0,0,1,1,1,2,2,3,3,4]", "output": "5, nums = [0,1,2,3,4,_,_,_,_,_]"}
        ],
        "constraints": ["1 <= nums.length <= 3 * 10^4", "-100 <= nums[i] <= 100"],
        "tags": ["Array", "Two Pointers"],
        "acceptance_rate": 50.8,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Search Insert Position",
        "slug": "search-insert-position",
        "difficulty": "easy",
        "description": "Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.",
        "examples": [
            {"input": "nums = [1,3,5,6], target = 5", "output": "2"},
            {"input": "nums = [1,3,5,6], target = 2", "output": "1"}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 <= nums[i] <= 10^4"],
        "tags": ["Array", "Binary Search"],
        "acceptance_rate": 42.1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "difficulty": "medium",
        "description": "Given an integer array nums, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6"},
            {"input": "nums = [1]", "output": "1"},
            {"input": "nums = [5,4,-1,7,8]", "output": "23"}
        ],
        "constraints": ["1 <= nums.length <= 10^5", "-10^4 <= nums[i] <= 10^4"],
        "tags": ["Array", "Divide and Conquer", "Dynamic Programming"],
        "acceptance_rate": 49.1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Length of Last Word",
        "slug": "length-of-last-word",
        "difficulty": "easy",
        "description": "Given a string s consisting of words and spaces, return the length of the last word in the string.",
        "examples": [
            {"input": "s = \"Hello World\"", "output": "5"},
            {"input": "s = \"   fly me   to   the moon  \"", "output": "4"}
        ],
        "constraints": ["1 <= s.length <= 10^4", "s consists of only English letters and spaces ' '."],
        "tags": ["String"],
        "acceptance_rate": 35.9,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Plus One",
        "slug": "plus-one",
        "difficulty": "easy",
        "description": "You are given a large integer represented as an integer array digits, where each digits[i] is the ith digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading zero, except the number 0 itself. Increment the large integer by one and return the resulting array of digits.",
        "examples": [
            {"input": "digits = [1,2,3]", "output": "[1,2,4]"},
            {"input": "digits = [4,3,2,1]", "output": "[4,3,2,2]"},
            {"input": "digits = [9]", "output": "[1,0]"}
        ],
        "constraints": ["1 <= digits.length <= 100", "0 <= digits[i] <= 9"],
        "tags": ["Array", "Math"],
        "acceptance_rate": 43.3,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Add Binary",
        "slug": "add-binary",
        "difficulty": "easy",
        "description": "Given two binary strings a and b, return their sum as a binary string.",
        "examples": [
            {"input": "a = \"11\", b = \"1\"", "output": "\"100\""},
            {"input": "a = \"1010\", b = \"1011\"", "output": "\"10101\""}
        ],
        "constraints": ["1 <= a.length, b.length <= 10^4", "a and b consist only of '0' or '1' characters."],
        "tags": ["Math", "String", "Bit Manipulation", "Simulation"],
        "acceptance_rate": 49.0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Climbing Stairs",
        "slug": "climbing-stairs",
        "difficulty": "easy",
        "description": "You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?",
        "examples": [
            {"input": "n = 2", "output": "2"},
            {"input": "n = 3", "output": "3"}
        ],
        "constraints": ["1 <= n <= 45"],
        "tags": ["Math", "Dynamic Programming", "Memoization"],
        "acceptance_rate": 49.5,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Remove Duplicates from Sorted List",
        "slug": "remove-duplicates-from-sorted-list",
        "difficulty": "easy",
        "description": "Given the head of a sorted linked list, delete all duplicates such that each element appears only once. Return the linked list sorted as well.",
        "examples": [
            {"input": "head = [1,1,2]", "output": "[1,2]"},
            {"input": "head = [1,1,2,3,3]", "output": "[1,2,3]"}
        ],
        "constraints": ["The number of nodes in the list is in the range [0, 300]", "-100 <= Node.val <= 100"],
        "tags": ["Linked List"],
        "acceptance_rate": 47.4,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Merge Sorted Array",
        "slug": "merge-sorted-array",
        "difficulty": "easy",
        "description": "You are given two integer arrays nums1 and nums2, sorted in non-decreasing order, and two integers m and n, representing the number of elements in nums1 and nums2 respectively. Merge nums1 and nums2 into a single array sorted in non-decreasing order.",
        "examples": [
            {"input": "nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3", "output": "[1,2,2,3,5,6]"},
            {"input": "nums1 = [1], m = 1, nums2 = [], n = 0", "output": "[1]"}
        ],
        "constraints": ["nums1.length == m + n", "nums2.length == n", "0 <= m, n <= 200"],
        "tags": ["Array", "Two Pointers", "Sorting"],
        "acceptance_rate": 42.9,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Same Tree",
        "slug": "same-tree",
        "difficulty": "easy",
        "description": "Given the roots of two binary trees p and q, write a function to check if they are the same or not. Two binary trees are considered the same if they are structurally identical, and the nodes have the same values.",
        "examples": [
            {"input": "p = [1,2,3], q = [1,2,3]", "output": "true"},
            {"input": "p = [1,2], q = [1,null,2]", "output": "false"}
        ],
        "constraints": ["The number of nodes in both trees is in the range [0, 100]", "-10^4 <= Node.val <= 10^4"],
        "tags": ["Tree", "Depth-First Search", "Binary Tree"],
        "acceptance_rate": 55.6,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Symmetric Tree",
        "slug": "symmetric-tree",
        "difficulty": "easy",
        "description": "Given the root of a binary tree, check whether it is a mirror of itself (i.e., symmetric around its center).",
        "examples": [
            {"input": "root = [1,2,2,3,4,4,3]", "output": "true"},
            {"input": "root = [1,2,2,null,3,null,3]", "output": "false"}
        ],
        "constraints": ["The number of nodes in the tree is in the range [1, 1000]", "-100 <= Node.val <= 100"],
        "tags": ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"],
        "acceptance_rate": 49.4,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Maximum Depth of Binary Tree",
        "slug": "maximum-depth-of-binary-tree",
        "difficulty": "easy",
        "description": "Given the root of a binary tree, return its maximum depth. A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.",
        "examples": [
            {"input": "root = [3,9,20,null,null,15,7]", "output": "3"},
            {"input": "root = [1,null,2]", "output": "2"}
        ],
        "constraints": ["The number of nodes in the tree is in the range [0, 10^4]", "-100 <= Node.val <= 100"],
        "tags": ["Tree", "Depth-First Search", "Breadth-First Search", "Binary Tree"],
        "acceptance_rate": 73.8,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Convert Sorted Array to Binary Search Tree",
        "slug": "convert-sorted-array-to-binary-search-tree",
        "difficulty": "easy",
        "description": "Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.",
        "examples": [
            {"input": "nums = [-10,-3,0,5,9]", "output": "[0,-3,9,-10,null,5]"},
            {"input": "nums = [1,3]", "output": "[3,1]"}
        ],
        "constraints": ["1 <= nums.length <= 10^4", "-10^4 <= nums[i] <= 10^4"],
        "tags": ["Array", "Divide and Conquer", "Tree", "Binary Search Tree", "Binary Tree"],
        "acceptance_rate": 63.8,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-and-sell-stock",
        "difficulty": "easy",
        "description": "You are given an array prices where prices[i] is the price of a given stock on the ith day. You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock. Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5"},
            {"input": "prices = [7,6,4,3,1]", "output": "0"}
        ],
        "constraints": ["1 <= prices.length <= 10^5", "0 <= prices[i] <= 10^4"],
        "tags": ["Array", "Dynamic Programming"],
        "acceptance_rate": 52.5,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Add Two Numbers",
        "slug": "add-two-numbers",
        "difficulty": "medium",
        "description": "You are given two non-empty linked lists representing two non-negative integers. The digits are stored in reverse order, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.",
        "examples": [
            {"input": "l1 = [2,4,3], l2 = [5,6,4]", "output": "[7,0,8]"},
            {"input": "l1 = [0], l2 = [0]", "output": "[0]"}
        ],
        "constraints": ["The number of nodes in each linked list is in the range [1, 100]", "0 <= Node.val <= 9"],
        "tags": ["Linked List", "Math", "Recursion"],
        "acceptance_rate": 36.9,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "difficulty": "medium",
        "description": "Given a string s, find the length of the longest substring without repeating characters.",
        "examples": [
            {"input": "s = \"abcabcbb\"", "output": "3"},
            {"input": "s = \"bbbbb\"", "output": "1"},
            {"input": "s = \"pwwkew\"", "output": "3"}
        ],
        "constraints": ["0 <= s.length <= 5 * 10^4", "s consists of English letters, digits, symbols and spaces."],
        "tags": ["Hash Table", "String", "Sliding Window"],
        "acceptance_rate": 33.8,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "difficulty": "medium",
        "description": "You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]). Find two lines that together with the x-axis form a container such that the container contains the most water. Return the maximum amount of water a container can store.",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49"},
            {"input": "height = [1,1]", "output": "1"}
        ],
        "constraints": ["n >= 2", "1 <= height[i] <= 10^4"],
        "tags": ["Array", "Two Pointers", "Greedy"],
        "acceptance_rate": 54.9,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "3Sum",
        "slug": "3sum",
        "difficulty": "medium",
        "description": "Given an integer array nums, return all the triplets [nums[i], nums[j], nums[k]] such that i != j, i != k, and j != k, and nums[i] + nums[j] + nums[k] == 0. Notice that the solution set must not contain duplicate triplets.",
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"},
            {"input": "nums = [0,1,1]", "output": "[]"},
            {"input": "nums = [0,0,0]", "output": "[[0,0,0]]"}
        ],
        "constraints": ["3 <= nums.length <= 3000", "-10^5 <= nums[i] <= 10^5"],
        "tags": ["Array", "Two Pointers", "Sorting"],
        "acceptance_rate": 32.4,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Letter Combinations of a Phone Number",
        "slug": "letter-combinations-of-a-phone-number",
        "difficulty": "medium",
        "description": "Given a string containing digits from 2-9 inclusive, return all possible letter combinations that the number could represent. Return the answer in any order.",
        "examples": [
            {"input": "digits = \"23\"", "output": "[\"ad\",\"ae\",\"af\",\"bd\",\"be\",\"bf\",\"cd\",\"ce\",\"cf\"]"},
            {"input": "digits = \"\"", "output": "[]"},
            {"input": "digits = \"2\"", "output": "[\"a\",\"b\",\"c\"]"}
        ],
        "constraints": ["0 <= digits.length <= 4", "digits[i] is a digit in the range ['2', '9']."],
        "tags": ["Hash Table", "String", "Backtracking"],
        "acceptance_rate": 56.1,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Generate Parentheses",
        "slug": "generate-parentheses",
        "difficulty": "medium",
        "description": "Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.",
        "examples": [
            {"input": "n = 3", "output": "[\"((()))\",\"(()())\",\"(())()\",\"()(())\",\"()()()\"]"},
            {"input": "n = 1", "output": "[\"()\"]"}
        ],
        "constraints": ["1 <= n <= 8"],
        "tags": ["String", "Dynamic Programming", "Backtracking"],
        "acceptance_rate": 70.5,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Swap Nodes in Pairs",
        "slug": "swap-nodes-in-pairs",
        "difficulty": "medium",
        "description": "Given a linked list, swap every two adjacent nodes and return its head. You must solve the problem without modifying the values in the list's nodes (i.e., only nodes themselves may be changed.)",
        "examples": [
            {"input": "head = [1,2,3,4]", "output": "[2,1,4,3]"},
            {"input": "head = []", "output": "[]"},
            {"input": "head = [1]", "output": "[1]"}
        ],
        "constraints": ["The number of nodes in the list is in the range [0, 100]", "0 <= Node.val <= 100"],
        "tags": ["Linked List", "Recursion"],
        "acceptance_rate": 58.3,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Remove Nth Node From End of List",
        "slug": "remove-nth-node-from-end-of-list",
        "difficulty": "medium",
        "description": "Given the head of a linked list, remove the nth node from the end of the list and return its head.",
        "examples": [
            {"input": "head = [1,2,3,4,5], n = 2", "output": "[1,2,3,5]"},
            {"input": "head = [1], n = 1", "output": "[]"},
            {"input": "head = [1,2], n = 1", "output": "[1]"}
        ],
        "constraints": ["The number of nodes in the list is sz.", "1 <= sz <= 30", "0 <= Node.val <= 100", "1 <= n <= sz"],
        "tags": ["Linked List", "Two Pointers"],
        "acceptance_rate": 37.2,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Median of Two Sorted Arrays",
        "slug": "median-of-two-sorted-arrays",
        "difficulty": "hard",
        "description": "Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).",
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.00000"},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.50000"}
        ],
        "constraints": ["nums1.length == m", "nums2.length == n", "0 <= m <= 1000", "0 <= n <= 1000"],
        "tags": ["Array", "Binary Search", "Divide and Conquer"],
        "acceptance_rate": 35.4,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    },
    {
        "title": "Regular Expression Matching",
        "slug": "regular-expression-matching",
        "difficulty": "hard",
        "description": "Given an input string s and a pattern p, implement regular expression matching with support for '.' and '*' where: '.' Matches any single character. '*' Matches zero or more of the preceding element.",
        "examples": [
            {"input": "s = \"aa\", p = \"a\"", "output": "false"},
            {"input": "s = \"aa\", p = \"a*\"", "output": "true"},
            {"input": "s = \"ab\", p = \".*\"", "output": "true"}
        ],
        "constraints": ["1 <= s.length <= 20", "1 <= p.length <= 30"],
        "tags": ["String", "Dynamic Programming", "Recursion"],
        "acceptance_rate": 27.7,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
]

async def add_problems():
    """Add problems to the MongoDB database"""
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGODB_URL)
        db = client.codeforge
        problems_collection = db.problems
        
        print(f"Adding {len(problems_to_add)} problems to the database...")
        
        # Insert all problems
        result = await problems_collection.insert_many(problems_to_add)
        
        print(f"Successfully added {len(result.inserted_ids)} problems!")
        
        # Print summary
        total_problems = await problems_collection.count_documents({})
        easy_count = await problems_collection.count_documents({"difficulty": "easy"})
        medium_count = await problems_collection.count_documents({"difficulty": "medium"}) 
        hard_count = await problems_collection.count_documents({"difficulty": "hard"})
        
        print(f"\nDatabase Summary:")
        print(f"Total problems: {total_problems}")
        print(f"Easy: {easy_count}")
        print(f"Medium: {medium_count}")
        print(f"Hard: {hard_count}")
        
    except Exception as e:
        print(f"Error adding problems: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    asyncio.run(add_problems())
