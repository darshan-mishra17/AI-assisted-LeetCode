import React, { useState } from 'react';
import { 
  MessageSquare, 
  ThumbsUp, 
  ThumbsDown, 
  Reply, 
  Search,
  Plus,
  Clock,
  User,
  Tag,
  TrendingUp,
  Eye
} from 'lucide-react';
import GlassPanel from '../components/GlassPanel';

const Forum: React.FC = () => {
  const [activeTab, setActiveTab] = useState('trending');
  const [searchTerm, setSearchTerm] = useState('');

  const posts = [
    {
      id: 1,
      title: 'Dynamic Programming vs Memoization - When to use which?',
      author: 'CodeMaster',
      avatar: '👨‍💻',
      timeAgo: '2 hours ago',
      content: 'I\'ve been working on DP problems and I\'m confused about when to use bottom-up vs top-down approaches. Can someone explain the key differences?',
      tags: ['Dynamic Programming', 'Algorithms', 'Interview Prep'],
      upvotes: 24,
      downvotes: 2,
      replies: 8,
      views: 156,
      hasCode: true
    },
    {
      id: 2,
      title: 'Two Sum - Multiple approaches comparison',
      author: 'AlgoNinja',
      avatar: '🥷',
      timeAgo: '4 hours ago',
      content: 'Just solved Two Sum in 4 different ways. Here\'s a comparison of time/space complexity for each approach.',
      tags: ['Arrays', 'Hash Map', 'Beginner'],
      upvotes: 45,
      downvotes: 1,
      replies: 12,
      views: 289,
      hasCode: true
    },
    {
      id: 3,
      title: 'Tips for optimizing recursive solutions',
      author: 'RecursionQueen',
      avatar: '👑',
      timeAgo: '6 hours ago',
      content: 'Share your best practices for writing efficient recursive algorithms. What techniques do you use to avoid TLE?',
      tags: ['Recursion', 'Optimization', 'Performance'],
      upvotes: 18,
      downvotes: 0,
      replies: 6,
      views: 98,
      hasCode: false
    },
    {
      id: 4,
      title: 'Graph algorithms study guide',
      author: 'GraphGuru',
      avatar: '🌐',
      timeAgo: '1 day ago',
      content: 'Comprehensive guide covering BFS, DFS, Dijkstra, and Union-Find. Perfect for interview preparation!',
      tags: ['Graphs', 'BFS', 'DFS', 'Study Guide'],
      upvotes: 67,
      downvotes: 3,
      replies: 15,
      views: 445,
      hasCode: true
    }
  ];

  const trendingTags = [
    { name: 'Dynamic Programming', count: 234 },
    { name: 'Binary Trees', count: 189 },
    { name: 'Arrays', count: 167 },
    { name: 'Hash Map', count: 145 },
    { name: 'Graphs', count: 132 },
    { name: 'Recursion', count: 98 }
  ];

  const getTagColor = (tag: string) => {
    const colors = [
      'bg-blue-500/20 text-blue-400',
      'bg-purple-500/20 text-purple-400',
      'bg-green-500/20 text-green-400',
      'bg-yellow-500/20 text-yellow-400',
      'bg-red-500/20 text-red-400',
      'bg-cyan-500/20 text-cyan-400'
    ];
    return colors[tag.length % colors.length];
  };

  const filteredPosts = posts.filter(post =>
    post.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
  );

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl md:text-4xl font-bold mb-2 text-white">
            Community <span className="text-blue-400">Forum</span>
          </h1>
          <p className="text-gray-300">Share knowledge, ask questions, and learn together</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-3 space-y-6">
            {/* Search and Actions */}
            <GlassPanel className="p-6">
              <div className="flex flex-col md:flex-row gap-4">
                <div className="flex-1 relative">
                  <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search discussions..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    className="w-full pl-10 pr-4 py-3 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-400 transition-all duration-300"
                  />
                </div>
                <button className="flex items-center space-x-2 px-6 py-3 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 rounded-lg font-semibold transition-all duration-300">
                  <Plus className="h-5 w-5" />
                  <span>New Post</span>
                </button>
              </div>

              {/* Tabs */}
              <div className="flex space-x-4 mt-6 border-b border-white/20">
                {[
                  { id: 'trending', label: 'Trending', icon: TrendingUp },
                  { id: 'recent', label: 'Recent', icon: Clock },
                  { id: 'unanswered', label: 'Unanswered', icon: MessageSquare }
                ].map((tab) => {
                  const Icon = tab.icon;
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`flex items-center space-x-2 px-4 py-2 border-b-2 transition-all duration-300 ${
                        activeTab === tab.id
                          ? 'border-blue-400 text-blue-400'
                          : 'border-transparent text-gray-400 hover:text-white'
                      }`}
                    >
                      <Icon className="h-4 w-4" />
                      <span>{tab.label}</span>
                    </button>
                  );
                })}
              </div>
            </GlassPanel>

            {/* Posts */}
            <div className="space-y-4">
              {filteredPosts.map((post) => (
                <GlassPanel key={post.id} className="p-6 hover:bg-white/15 transition-all duration-300">
                  <div className="flex items-start space-x-4">
                    {/* Author Avatar */}
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-2xl">
                        {post.avatar}
                      </div>
                    </div>

                    {/* Post Content */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="text-lg font-semibold text-white hover:text-blue-400 cursor-pointer transition-colors duration-300">
                            {post.title}
                          </h3>
                          <div className="flex items-center space-x-2 text-sm text-gray-400 mt-1">
                            <span>by {post.author}</span>
                            <span>•</span>
                            <span>{post.timeAgo}</span>
                            {post.hasCode && (
                              <>
                                <span>•</span>
                                <span className="text-green-400 text-xs">📝 Code included</span>
                              </>
                            )}
                          </div>
                        </div>
                      </div>

                      <p className="text-gray-300 mt-3 line-clamp-2">{post.content}</p>

                      {/* Tags */}
                      <div className="flex flex-wrap gap-2 mt-4">
                        {post.tags.map((tag, index) => (
                          <span
                            key={index}
                            className={`px-2 py-1 rounded text-xs font-medium ${getTagColor(tag)}`}
                          >
                            {tag}
                          </span>
                        ))}
                      </div>

                      {/* Actions */}
                      <div className="flex items-center justify-between mt-4">
                        <div className="flex items-center space-x-6">
                          <button className="flex items-center space-x-1 text-gray-400 hover:text-green-400 transition-colors duration-300">
                            <ThumbsUp className="h-4 w-4" />
                            <span className="text-sm">{post.upvotes}</span>
                          </button>
                          <button className="flex items-center space-x-1 text-gray-400 hover:text-red-400 transition-colors duration-300">
                            <ThumbsDown className="h-4 w-4" />
                            <span className="text-sm">{post.downvotes}</span>
                          </button>
                          <button className="flex items-center space-x-1 text-gray-400 hover:text-blue-400 transition-colors duration-300">
                            <Reply className="h-4 w-4" />
                            <span className="text-sm">{post.replies} replies</span>
                          </button>
                          <div className="flex items-center space-x-1 text-gray-400">
                            <Eye className="h-4 w-4" />
                            <span className="text-sm">{post.views} views</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </GlassPanel>
              ))}
            </div>

            {filteredPosts.length === 0 && (
              <GlassPanel className="p-12 text-center">
                <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">No posts found</h3>
                <p className="text-gray-300">Try adjusting your search terms</p>
              </GlassPanel>
            )}
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Trending Tags */}
            <GlassPanel className="p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <Tag className="h-5 w-5 mr-2 text-blue-400" />
                Trending Topics
              </h3>
              <div className="space-y-3">
                {trendingTags.map((tag, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-gray-300 hover:text-blue-400 cursor-pointer transition-colors duration-300">
                      {tag.name}
                    </span>
                    <span className="text-sm text-gray-400">{tag.count}</span>
                  </div>
                ))}
              </div>
            </GlassPanel>

            {/* Community Stats */}
            <GlassPanel className="p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Community Stats</h3>
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Total Posts</span>
                  <span className="text-white font-semibold">12,456</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Active Members</span>
                  <span className="text-green-400 font-semibold">2,891</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">Solved Today</span>
                  <span className="text-blue-400 font-semibold">456</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-300">New Posts</span>
                  <span className="text-purple-400 font-semibold">89</span>
                </div>
              </div>
            </GlassPanel>

            {/* Guidelines */}
            <GlassPanel className="p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Community Guidelines</h3>
              <div className="space-y-2 text-sm text-gray-300">
                <p>• Be respectful and constructive</p>
                <p>• Include code snippets when relevant</p>
                <p>• Search before posting duplicates</p>
                <p>• Use descriptive titles</p>
                <p>• Help others learn and grow</p>
              </div>
            </GlassPanel>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Forum;