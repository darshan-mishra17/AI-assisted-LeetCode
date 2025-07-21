import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Search, 
  Filter, 
  CheckCircle, 
  X,
  ChevronDown,
  Building,
  Tag,
  BarChart3,
  Loader2
} from 'lucide-react';
import GlassPanel from '../components/GlassPanel';
import { apiService, Problem, Submission } from '../services/api';
import { initializeMockSolvedProblems } from '../data/mockProblems';

const Problems: React.FC = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    difficulty: '',
    topic: '',
    company: '',
    status: ''
  });
  const [showFilters, setShowFilters] = useState(false);
  const [problems, setProblems] = useState<Problem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [solvedProblems, setSolvedProblems] = useState<Set<string>>(new Set());

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        setLoading(true);
        
        // Try to fetch from API first
        try {
          const fetchedProblems = await apiService.getProblems(
            0, 
            50, 
            filters.difficulty || undefined,
            filters.topic ? [filters.topic] : undefined
          );
          setProblems(fetchedProblems);
        } catch (apiError) {
          console.warn('API failed, using mock data:', apiError);
          // Fallback to mock data with simplified structure
          const mockProblems: Problem[] = [
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
              constraints: '2 <= nums.length <= 10^4',
              tags: ['Array', 'Hash Table'],
              acceptance_rate: 65.5,
              test_cases: [
                { input: '[2,7,11,15]\n9', expected_output: '[0,1]', is_hidden: false }
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
                { input: 's = "()[]{}"', output: 'true' }
              ],
              constraints: '1 <= s.length <= 10^4',
              tags: ['String', 'Stack'],
              acceptance_rate: 72.3,
              test_cases: [
                { input: '"()"', expected_output: 'true', is_hidden: false }
              ],
              total_submissions: 800,
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
              constraints: '1 <= s.length <= 1000',
              tags: ['String', 'Dynamic Programming'],
              acceptance_rate: 45.2,
              test_cases: [
                { input: '"babad"', expected_output: '"bab"', is_hidden: false }
              ],
              total_submissions: 600,
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
              constraints: '1 <= nums.length <= 10^5',
              tags: ['Array', 'Dynamic Programming'],
              acceptance_rate: 49.1,
              test_cases: [
                { input: '[-2,1,-3,4,-1,2,1,-5,4]', expected_output: '6', is_hidden: false }
              ],
              total_submissions: 900,
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
              test_cases: [
                { input: '2', expected_output: '2', is_hidden: false }
              ],
              total_submissions: 750,
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
              test_cases: [
                { input: '[1,8,6,2,5,4,8,3,7]', expected_output: '49', is_hidden: false }
              ],
              total_submissions: 650,
              created_at: '2025-01-01T00:00:00Z'
            },
            {
              _id: '3sum-id',
              title: '3Sum',
              slug: '3sum',
              difficulty: 'medium',
              description: 'Given an integer array nums, return all the triplets that sum to zero.',
              examples: [
                { input: 'nums = [-1,0,1,2,-1,-4]', output: '[[-1,-1,2],[-1,0,1]]' },
                { input: 'nums = [0,1,1]', output: '[]' }
              ],
              constraints: '3 <= nums.length <= 3000',
              tags: ['Array', 'Two Pointers', 'Sorting'],
              acceptance_rate: 32.4,
              test_cases: [
                { input: '[-1,0,1,2,-1,-4]', expected_output: '[[-1,-1,2],[-1,0,1]]', is_hidden: false }
              ],
              total_submissions: 850,
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
              test_cases: [
                { input: '[1,3]\n[2]', expected_output: '2.00000', is_hidden: false }
              ],
              total_submissions: 400,
              created_at: '2025-01-01T00:00:00Z'
            }
          ];
          setProblems(mockProblems);
        }
        
        // Fetch user submissions to determine solved problems (using mock data if API fails)
        try {
          const currentUser = localStorage.getItem('currentUser');
          if (currentUser) {
            const user = JSON.parse(currentUser);
            const submissions = await apiService.getUserSubmissions(user.id || user.username);
            
            // Find successful submissions and track solved problems
            const solved = new Set<string>();
            submissions.forEach((submission: Submission) => {
              if (submission.status === 'accepted') {
                solved.add(submission.problem_id);
              }
            });
            setSolvedProblems(solved);
          }
        } catch (submissionError) {
          console.warn('Could not fetch user submissions, using mock solved problems:', submissionError);
          // Initialize with mock solved problems
          setSolvedProblems(initializeMockSolvedProblems());
        }
        
      } catch (err: any) {
        console.error('Error fetching problems:', err);
        setError(err.message || 'Failed to fetch problems');
      } finally {
        setLoading(false);
      }
    };

    fetchProblems();
  }, [filters.difficulty, filters.topic]);

  // Listen for problem solved events
  useEffect(() => {
    const handleProblemSolved = (event: CustomEvent) => {
      const { problemId } = event.detail;
      setSolvedProblems(prev => new Set([...prev, problemId]));
    };

    window.addEventListener('problemSolved', handleProblemSolved as EventListener);
    return () => {
      window.removeEventListener('problemSolved', handleProblemSolved as EventListener);
    };
  }, []);

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'text-green-400 bg-green-400/10';
      case 'medium': return 'text-yellow-400 bg-yellow-400/10';
      case 'hard': return 'text-red-400 bg-red-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  const filteredProblems = problems.filter(problem =>
    problem.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    problem.description?.toLowerCase().includes(searchTerm.toLowerCase())
  );
  
  const topics = ['Array', 'String', 'Linked List', 'Tree', 'Graph', 'Dynamic Programming', 'Binary Search'];
  const companies = ['Google', 'Amazon', 'Microsoft', 'Facebook', 'Apple', 'Netflix', 'Adobe'];
  const difficulties = ['Easy', 'Medium', 'Hard'];
  const statuses = ['Not Attempted', 'Attempted', 'Solved'];

  const clearFilters = () => {
    setFilters({
      difficulty: '',
      topic: '',
      company: '',
      status: ''
    });
    setSearchTerm('');
  };

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold mb-2 text-white">
            Practice <span className="text-blue-400">Problems</span>
          </h1>
          <p className="text-gray-300">Sharpen your skills with curated coding challenges</p>
          
          {/* Demo Button */}
          <button
            onClick={() => {
              // Demo: Mark first problem as solved
              const firstProblem = problems[0];
              if (firstProblem) {
                setSolvedProblems(prev => new Set([...prev, firstProblem._id]));
                // Also dispatch the event
                window.dispatchEvent(new CustomEvent('problemSolved', {
                  detail: { problemId: firstProblem._id }
                }));
              }
            }}
            className="mt-4 px-4 py-2 bg-green-500/20 hover:bg-green-500/30 border border-green-500/30 rounded-lg transition-all duration-300 text-green-400 text-sm"
          >
            🎯 Demo: Mark First Problem as Solved
          </button>
        </div>

        {/* Search and Filters */}
        <GlassPanel className="p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Bar */}
            <div className="flex-1 relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search problems..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-400 transition-all duration-300"
              />
            </div>

            {/* Filter Toggle */}
            <button
              onClick={() => setShowFilters(!showFilters)}
              className="flex items-center space-x-2 px-6 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-lg transition-all duration-300"
            >
              <Filter className="h-5 w-5" />
              <span>Filters</span>
              <ChevronDown className={`h-4 w-4 transition-transform ${showFilters ? 'rotate-180' : ''}`} />
            </button>

            {/* Clear Filters */}
            {(Object.values(filters).some(f => f !== '') || searchTerm) && (
              <button
                onClick={clearFilters}
                className="flex items-center space-x-2 px-4 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 rounded-lg transition-all duration-300"
              >
                <X className="h-4 w-4" />
                <span>Clear</span>
              </button>
            )}
          </div>

          {/* Expandable Filters */}
          {showFilters && (
            <div className="mt-6 pt-6 border-t border-white/20">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {/* Difficulty Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    <BarChart3 className="inline h-4 w-4 mr-1" />
                    Difficulty
                  </label>
                  <select
                    value={filters.difficulty}
                    onChange={(e) => setFilters({...filters, difficulty: e.target.value})}
                    className="w-full px-3 py-2 bg-black/20 border border-white/20 rounded-lg text-white focus:outline-none focus:border-blue-400"
                  >
                    <option value="">All Levels</option>
                    {difficulties.map(diff => (
                      <option key={diff} value={diff}>{diff}</option>
                    ))}
                  </select>
                </div>

                {/* Topic Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    <Tag className="inline h-4 w-4 mr-1" />
                    Topic
                  </label>
                  <select
                    value={filters.topic}
                    onChange={(e) => setFilters({...filters, topic: e.target.value})}
                    className="w-full px-3 py-2 bg-black/20 border border-white/20 rounded-lg text-white focus:outline-none focus:border-blue-400"
                  >
                    <option value="">All Topics</option>
                    {topics.map(topic => (
                      <option key={topic} value={topic}>{topic}</option>
                    ))}
                  </select>
                </div>

                {/* Company Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    <Building className="inline h-4 w-4 mr-1" />
                    Company
                  </label>
                  <select
                    value={filters.company}
                    onChange={(e) => setFilters({...filters, company: e.target.value})}
                    className="w-full px-3 py-2 bg-black/20 border border-white/20 rounded-lg text-white focus:outline-none focus:border-blue-400"
                  >
                    <option value="">All Companies</option>
                    {companies.map(company => (
                      <option key={company} value={company}>{company}</option>
                    ))}
                  </select>
                </div>

                {/* Status Filter */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    <CheckCircle className="inline h-4 w-4 mr-1" />
                    Status
                  </label>
                  <select
                    value={filters.status}
                    onChange={(e) => setFilters({...filters, status: e.target.value})}
                    className="w-full px-3 py-2 bg-black/20 border border-white/20 rounded-lg text-white focus:outline-none focus:border-blue-400"
                  >
                    <option value="">All Status</option>
                    {statuses.map(status => (
                      <option key={status} value={status}>{status}</option>
                    ))}
                  </select>
                </div>
              </div>
            </div>
          )}
        </GlassPanel>

        {/* Problems List */}
        <div className="space-y-4">
          {loading && (
            <div className="flex items-center justify-center py-8">
              <Loader2 className="h-8 w-8 animate-spin text-blue-400" />
              <span className="ml-2 text-gray-400">Loading problems...</span>
            </div>
          )}

          {error && (
            <div className="flex items-center justify-center py-8">
              <div className="text-red-400 text-center">
                <p className="font-semibold mb-2">Error loading problems</p>
                <p className="text-sm">{error}</p>
              </div>
            </div>
          )}

          {!loading && !error && filteredProblems.map((problem) => (
            <GlassPanel 
              key={problem._id} 
              className="p-6 hover:bg-white/15 transition-all duration-300 cursor-pointer"
              onClick={() => navigate(`/problems/${problem.slug}`)}
            >
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-4 flex-1">
                  {/* Status Icon */}
                  <div className="flex-shrink-0">
                    {solvedProblems.has(problem._id) ? (
                      <CheckCircle className="h-5 w-5 text-green-400" />
                    ) : (
                      <div className="h-5 w-5 rounded-full border-2 border-gray-600"></div>
                    )}
                  </div>

                  {/* Problem Info */}
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-semibold text-white hover:text-blue-400 transition-colors duration-300">
                      {problem.title}
                    </h3>
                    <p className="text-gray-300 text-sm mt-1 line-clamp-1">{problem.description}</p>
                    
                    {/* Tags */}
                    <div className="flex items-center space-x-2 mt-2">
                      <span className={`px-2 py-1 rounded text-xs font-medium ${getDifficultyColor(problem.difficulty)}`}>
                        {problem.difficulty}
                      </span>
                      {problem.tags.slice(0, 2).map((tag: string, index: number) => (
                        <span key={index} className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs font-medium">
                          {tag}
                        </span>
                      ))}
                      {problem.tags.length > 2 && (
                        <span className="text-gray-400 text-xs">+{problem.tags.length - 2} more</span>
                      )}
                    </div>
                  </div>

                  {/* Acceptance Rate */}
                  <div className="hidden md:block text-right">
                    <div className="text-sm text-gray-300">Acceptance</div>
                    <div className="text-lg font-semibold text-green-400">{problem.acceptance_rate}%</div>
                  </div>
                </div>
              </div>
            </GlassPanel>
          ))}
        </div>

        {filteredProblems.length === 0 && (
          <GlassPanel className="p-12 text-center">
            <Search className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">No problems found</h3>
            <p className="text-gray-300">Try adjusting your search terms or filters</p>
          </GlassPanel>
        )}
      </div>
    </div>
  );
};

export default Problems;