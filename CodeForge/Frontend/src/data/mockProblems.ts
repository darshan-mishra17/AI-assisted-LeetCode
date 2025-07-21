import { Problem } from '../services/api';

// Mock problems data for demo purposes when backend is not available
export const mockProblems: Problem[] = [
  {
    _id: 'two-sum-id',
    title: 'Two Sum',
    slug: 'two-sum',
    difficulty: 'easy',
    description: 'Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.',
    examples: [
      { input: 'nums = [2,7,11,15], target = 9', output: '[0,1]' },
      { input: 'nums = [3,2,4], target = 6', output: '[1,2]' }
    ],
    constraints: '2 <= nums.length <= 10^4, -10^9 <= nums[i] <= 10^9',
    tags: ['Array', 'Hash Table'],
    acceptance_rate: 65.5,
    test_cases: [
      { input: '[2,7,11,15]\n9', expected_output: '[0,1]' },
      { input: '[3,2,4]\n6', expected_output: '[1,2]' }
    ],
    total_submissions: 1000,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'valid-parentheses-id',
    title: 'Valid Parentheses',
    slug: 'valid-parentheses',
    difficulty: 'easy',
    description: 'Given a string s containing just the characters \'(\', \')\', \'{\', \'}\', \'[\' and \']\', determine if the input string is valid.',
    examples: [
      { input: 's = "()"', output: 'true' },
      { input: 's = "()[]{}"', output: 'true' },
      { input: 's = "(]"', output: 'false' }
    ],
    constraints: '1 <= s.length <= 10^4, s consists of parentheses only',
    tags: ['String', 'Stack'],
    acceptance_rate: 72.3,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'palindromic-substring-id',
    title: 'Longest Palindromic Substring',
    slug: 'longest-palindromic-substring',
    difficulty: 'medium',
    description: 'Given a string s, return the longest palindromic substring in s.',
    examples: [
      { input: 's = "babad"', output: '"bab"' },
      { input: 's = "cbbd"', output: '"bb"' }
    ],
    constraints: '1 <= s.length <= 1000, s consist of only digits and English letters',
    tags: ['String', 'Dynamic Programming'],
    acceptance_rate: 45.2,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'reverse-integer-id',
    title: 'Reverse Integer',
    slug: 'reverse-integer',
    difficulty: 'easy',
    description: 'Given a signed 32-bit integer x, return x with its digits reversed.',
    examples: [
      { input: 'x = 123', output: '321' },
      { input: 'x = -123', output: '-321' },
      { input: 'x = 120', output: '21' }
    ],
    constraints: '-2^31 <= x <= 2^31 - 1',
    tags: ['Math', 'Integer Manipulation'],
    acceptance_rate: 25.6,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'maximum-subarray-id',
    title: 'Maximum Subarray',
    slug: 'maximum-subarray',
    difficulty: 'medium',
    description: 'Given an integer array nums, find the contiguous subarray with the largest sum.',
    examples: [
      { input: 'nums = [-2,1,-3,4,-1,2,1,-5,4]', output: '6' },
      { input: 'nums = [1]', output: '1' }
    ],
    constraints: '1 <= nums.length <= 10^5, -10^4 <= nums[i] <= 10^4',
    tags: ['Array', 'Dynamic Programming'],
    acceptance_rate: 49.1,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'climbing-stairs-id',
    title: 'Climbing Stairs',
    slug: 'climbing-stairs',
    difficulty: 'easy',
    description: 'You are climbing a staircase. It takes n steps to reach the top. Each time you can either climb 1 or 2 steps.',
    examples: [
      { input: 'n = 2', output: '2' },
      { input: 'n = 3', output: '3' }
    ],
    constraints: '1 <= n <= 45',
    tags: ['Math', 'Dynamic Programming'],
    acceptance_rate: 49.5,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'best-time-buy-sell-id',
    title: 'Best Time to Buy and Sell Stock',
    slug: 'best-time-to-buy-and-sell-stock',
    difficulty: 'easy',
    description: 'You are given an array prices where prices[i] is the price of a given stock on the ith day.',
    examples: [
      { input: 'prices = [7,1,5,3,6,4]', output: '5' },
      { input: 'prices = [7,6,4,3,1]', output: '0' }
    ],
    constraints: '1 <= prices.length <= 10^5, 0 <= prices[i] <= 10^4',
    tags: ['Array', 'Dynamic Programming'],
    acceptance_rate: 52.5,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'container-with-water-id',
    title: 'Container With Most Water',
    slug: 'container-with-most-water',
    difficulty: 'medium',
    description: 'You are given an integer array height. Find two lines that form a container with the most water.',
    examples: [
      { input: 'height = [1,8,6,2,5,4,8,3,7]', output: '49' },
      { input: 'height = [1,1]', output: '1' }
    ],
    constraints: 'n >= 2, 1 <= height[i] <= 10^4',
    tags: ['Array', 'Two Pointers'],
    acceptance_rate: 54.9,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'three-sum-id',
    title: '3Sum',
    slug: '3sum',
    difficulty: 'medium',
    description: 'Given an integer array nums, return all the triplets that sum to zero.',
    examples: [
      { input: 'nums = [-1,0,1,2,-1,-4]', output: '[[-1,-1,2],[-1,0,1]]' },
      { input: 'nums = [0,1,1]', output: '[]' }
    ],
    constraints: '3 <= nums.length <= 3000, -10^5 <= nums[i] <= 10^5',
    tags: ['Array', 'Two Pointers', 'Sorting'],
    acceptance_rate: 32.4,
    created_at: '2025-01-01T00:00:00Z'
  },
  {
    _id: 'median-sorted-arrays-id',
    title: 'Median of Two Sorted Arrays',
    slug: 'median-of-two-sorted-arrays',
    difficulty: 'hard',
    description: 'Given two sorted arrays nums1 and nums2, return the median of the two sorted arrays.',
    examples: [
      { input: 'nums1 = [1,3], nums2 = [2]', output: '2.00000' },
      { input: 'nums1 = [1,2], nums2 = [3,4]', output: '2.50000' }
    ],
    constraints: '0 <= m <= 1000, 0 <= n <= 1000',
    tags: ['Array', 'Binary Search'],
    acceptance_rate: 35.4,
    created_at: '2025-01-01T00:00:00Z'
  }
];

// Initialize mock solved problems (simulate some completed problems)
export const initializeMockSolvedProblems = () => {
  const solvedIds = ['two-sum-id', 'valid-parentheses-id'];
  return new Set(solvedIds);
};
