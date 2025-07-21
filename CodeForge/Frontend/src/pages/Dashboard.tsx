import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  BookOpen, 
  Trophy, 
  TrendingUp,
  Code,
  CheckCircle,
  Clock,
  Star,
  Zap,
  Calendar,
  Award,
  Target,
  Activity
} from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';

interface DashboardStats {
  totalProblems: number;
  problemsSolved: number;
  easyProblems: { solved: number; total: number };
  mediumProblems: { solved: number; total: number };
  hardProblems: { solved: number; total: number };
  currentStreak: number;
  maxStreak: number;
  xpPoints: number;
  recentSubmissions: any[];
  upcomingContests: any[];
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState<DashboardStats>({
    totalProblems: 0,
    problemsSolved: 0,
    easyProblems: { solved: 0, total: 0 },
    mediumProblems: { solved: 0, total: 0 },
    hardProblems: { solved: 0, total: 0 },
    currentStreak: 0,
    maxStreak: 0,
    xpPoints: 0,
    recentSubmissions: [],
    upcomingContests: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        setLoading(true);
        
        // Fetch real problems from the API
        const problems = await apiService.getProblems(0, 1000);
        
        // Group problems by difficulty
        const problemsByDifficulty = problems.reduce((acc, problem) => {
          if (!acc[problem.difficulty]) {
            acc[problem.difficulty] = [];
          }
          acc[problem.difficulty].push(problem);
          return acc;
        }, { easy: [], medium: [], hard: [] } as any);

        // For now, use mock solved data until we have proper user submissions
        const mockSolvedProblems = Math.floor(problems.length * 0.15); // 15% solved
        const mockEasySolved = Math.floor(problemsByDifficulty.easy.length * 0.3);
        const mockMediumSolved = Math.floor(problemsByDifficulty.medium.length * 0.1);
        const mockHardSolved = Math.floor(problemsByDifficulty.hard.length * 0.05);
        
        setStats({
          totalProblems: problems.length,
          problemsSolved: mockSolvedProblems,
          easyProblems: { solved: mockEasySolved, total: problemsByDifficulty.easy.length },
          mediumProblems: { solved: mockMediumSolved, total: problemsByDifficulty.medium.length },
          hardProblems: { solved: mockHardSolved, total: problemsByDifficulty.hard.length },
          currentStreak: 5,
          maxStreak: 12,
          xpPoints: user?.stats?.xp || 450,
          recentSubmissions: [],
          upcomingContests: [
            { id: 1, name: 'Weekly Challenge', date: '2024-01-15' },
            { id: 2, name: 'Algorithm Sprint', date: '2024-01-22' }
          ]
        });
        
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
        // Fallback to mock data if API fails
        setStats({
          totalProblems: 3,
          problemsSolved: 1,
          easyProblems: { solved: 1, total: 2 },
          mediumProblems: { solved: 0, total: 1 },
          hardProblems: { solved: 0, total: 0 },
          currentStreak: 1,
          maxStreak: 3,
          xpPoints: user?.stats?.xp || 50,
          recentSubmissions: [],
          upcomingContests: []
        });
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();

    // Listen for problem solved events
    const handleProblemSolved = (event: any) => {
      const problemData = event.detail;
      console.log('Problem solved:', problemData);
      // Refetch dashboard data
      fetchDashboardData();
    };

    window.addEventListener('problemSolved', handleProblemSolved);
    return () => {
      window.removeEventListener('problemSolved', handleProblemSolved);
    };
  }, [user]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 p-6">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-700 rounded w-1/3 mb-4"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              {[1, 2, 3, 4].map(i => (
                <div key={i} className="bg-gray-800 rounded-lg p-6 h-24"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">
            Welcome back, {user?.username}! 👋
          </h1>
          <p className="text-gray-300">
            You've solved {stats.problemsSolved} problems so far. Keep going!
          </p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          {/* Total Problems */}
          <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100 text-sm">Total Problems</p>
                <p className="text-2xl font-bold">{stats.totalProblems}</p>
              </div>
              <BookOpen className="h-8 w-8 text-blue-200" />
            </div>
          </div>

          {/* Problems Solved */}
          <div className="bg-gradient-to-r from-green-600 to-green-700 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100 text-sm">Problems Solved</p>
                <p className="text-2xl font-bold">{stats.problemsSolved}</p>
              </div>
              <CheckCircle className="h-8 w-8 text-green-200" />
            </div>
          </div>

          {/* Current Streak */}
          <div className="bg-gradient-to-r from-orange-600 to-orange-700 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100 text-sm">Current Streak</p>
                <p className="text-2xl font-bold">{stats.currentStreak}</p>
              </div>
              <Star className="h-8 w-8 text-orange-200" />
            </div>
          </div>

          {/* XP Points */}
          <div className="bg-gradient-to-r from-purple-600 to-purple-700 rounded-lg p-6 text-white shadow-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 text-sm">XP Points</p>
                <p className="text-2xl font-bold">{stats.xpPoints}</p>
              </div>
              <Trophy className="h-8 w-8 text-purple-200" />
            </div>
          </div>
        </div>

        {/* Progress Section */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Progress by Difficulty */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg">
            <h2 className="text-xl font-bold text-white mb-6 flex items-center">
              <TrendingUp className="h-5 w-5 mr-2 text-blue-400" />
              Progress by Difficulty
            </h2>
            
            <div className="space-y-6">
              {/* Easy */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-green-400 font-medium">Easy</span>
                  <span className="text-gray-300 text-sm">
                    {stats.easyProblems.solved}/{stats.easyProblems.total}
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-green-400 to-green-500 h-3 rounded-full transition-all duration-500 ease-in-out"
                    style={{ 
                      width: `${stats.easyProblems.total > 0 ? (stats.easyProblems.solved / stats.easyProblems.total) * 100 : 0}%` 
                    }}
                  ></div>
                </div>
              </div>

              {/* Medium */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-yellow-400 font-medium">Medium</span>
                  <span className="text-gray-300 text-sm">
                    {stats.mediumProblems.solved}/{stats.mediumProblems.total}
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-yellow-400 to-yellow-500 h-3 rounded-full transition-all duration-500 ease-in-out"
                    style={{ 
                      width: `${stats.mediumProblems.total > 0 ? (stats.mediumProblems.solved / stats.mediumProblems.total) * 100 : 0}%` 
                    }}
                  ></div>
                </div>
              </div>

              {/* Hard */}
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-red-400 font-medium">Hard</span>
                  <span className="text-gray-300 text-sm">
                    {stats.hardProblems.solved}/{stats.hardProblems.total}
                  </span>
                </div>
                <div className="w-full bg-gray-700 rounded-full h-3">
                  <div 
                    className="bg-gradient-to-r from-red-400 to-red-500 h-3 rounded-full transition-all duration-500 ease-in-out"
                    style={{ 
                      width: `${stats.hardProblems.total > 0 ? (stats.hardProblems.solved / stats.hardProblems.total) * 100 : 0}%` 
                    }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Upcoming Contests */}
          <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg">
            <h2 className="text-xl font-bold text-white mb-4 flex items-center">
              <Calendar className="h-5 w-5 mr-2 text-purple-400" />
              Upcoming Contests
            </h2>
            <div className="space-y-4">
              {stats.upcomingContests.length > 0 ? (
                stats.upcomingContests.map((contest: any) => (
                  <div key={contest.id} className="flex items-center justify-between p-3 bg-gray-700 rounded-lg">
                    <div>
                      <h3 className="text-white font-medium">{contest.name}</h3>
                      <p className="text-gray-400 text-sm">{contest.date}</p>
                    </div>
                    <Award className="h-5 w-5 text-yellow-400" />
                  </div>
                ))
              ) : (
                <div className="text-gray-400 text-center py-4">
                  <Calendar className="h-8 w-8 mx-auto mb-2 opacity-50" />
                  <p>No upcoming contests</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 shadow-lg mb-8">
          <h2 className="text-xl font-bold text-white mb-6 flex items-center">
            <Target className="h-5 w-5 mr-2 text-green-400" />
            Quick Actions
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Link 
              to="/problems" 
              className="flex items-center justify-center p-4 bg-blue-600 hover:bg-blue-700 rounded-lg text-white font-medium transition-colors"
            >
              <Code className="h-5 w-5 mr-2" />
              Solve Problems
            </Link>
            <Link 
              to="/compete" 
              className="flex items-center justify-center p-4 bg-orange-600 hover:bg-orange-700 rounded-lg text-white font-medium transition-colors"
            >
              <Trophy className="h-5 w-5 mr-2" />
              Join Contest
            </Link>
            <Link 
              to="/forum" 
              className="flex items-center justify-center p-4 bg-purple-600 hover:bg-purple-700 rounded-lg text-white font-medium transition-colors"
            >
              <Activity className="h-5 w-5 mr-2" />
              Visit Forum
            </Link>
          </div>
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
