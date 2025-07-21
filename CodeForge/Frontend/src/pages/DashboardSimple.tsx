import React from 'react';
import { Link } from 'react-router-dom';
import { 
  BookOpen, 
  Trophy, 
  Target, 
  TrendingUp,
  Code,
  CheckCircle,
  Clock,
  Star,
  Zap
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Welcome back, {user?.username}! 👋
          </h1>
          <p className="text-gray-300">
            Ready to sharpen your coding skills? Let's get started!
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Problems Solved</p>
                <p className="text-2xl font-bold text-green-400">
                  {user?.stats?.total_problems_solved || 0}
                </p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-400" />
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Current Streak</p>
                <p className="text-2xl font-bold text-orange-400">
                  {user?.stats?.current_streak || 0}
                </p>
              </div>
              <TrendingUp className="h-8 w-8 text-orange-400" />
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">XP Points</p>
                <p className="text-2xl font-bold text-blue-400">
                  {user?.stats?.xp || 0}
                </p>
              </div>
              <Star className="h-8 w-8 text-blue-400" />
            </div>
          </div>

          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Rank</p>
                <p className="text-2xl font-bold text-purple-400">
                  {user?.role === 'admin' ? 'Admin' : 'Coder'}
                </p>
              </div>
              <Trophy className="h-8 w-8 text-purple-400" />
            </div>
          </div>
        </div>

        {/* Action Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <Link 
            to="/problems"
            className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-xl p-6 text-white hover:from-blue-700 hover:to-blue-800 transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-white/20 rounded-lg p-3">
                <BookOpen className="h-8 w-8" />
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-1">Practice Problems</h3>
                <p className="text-blue-100">
                  Solve coding challenges and improve your skills
                </p>
              </div>
            </div>
          </Link>

          <Link 
            to="/compete"
            className="bg-gradient-to-br from-green-600 to-green-700 rounded-xl p-6 text-white hover:from-green-700 hover:to-green-800 transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-white/20 rounded-lg p-3">
                <Trophy className="h-8 w-8" />
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-1">Competitions</h3>
                <p className="text-green-100">
                  Join contests and compete with others
                </p>
              </div>
            </div>
          </Link>

          <Link 
            to="/forum"
            className="bg-gradient-to-br from-purple-600 to-purple-700 rounded-xl p-6 text-white hover:from-purple-700 hover:to-purple-800 transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            <div className="flex items-center space-x-4">
              <div className="bg-white/20 rounded-lg p-3">
                <Code className="h-8 w-8" />
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-1">Discussion Forum</h3>
                <p className="text-purple-100">
                  Connect with other developers
                </p>
              </div>
            </div>
          </Link>
        </div>

        {/* Recent Activity */}
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg">
          <h2 className="text-xl font-bold text-white mb-4 flex items-center">
            <Clock className="h-5 w-5 mr-2 text-blue-400" />
            Recent Activity
          </h2>
          <div className="text-gray-400 text-center py-8">
            <Zap className="h-12 w-12 mx-auto mb-3 opacity-50" />
            <p className="text-lg">No recent activity yet.</p>
            <p className="text-sm mt-1">Start solving problems to see your progress here!</p>
            <Link 
              to="/problems" 
              className="inline-block mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition-colors"
            >
              Get Started
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
