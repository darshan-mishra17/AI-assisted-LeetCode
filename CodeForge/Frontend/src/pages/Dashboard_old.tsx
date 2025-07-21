import React, { useState, useEffect } from 'react';
import { 
  Trophy, 
  Zap, 
  CheckCircle,
  Flame,
  Target,
  Award,
  Clock,
  TrendingUp
} from 'lucide-react';
import GlassPanel from '../components/GlassPanel';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';

interface UserStats {
  xp_points: number;
  problems_solved: number;
  streak: number;
  easy_solved: number;
  medium_solved: number;
  hard_solved: number;
  total_submissions: number;
}

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const [userStats, setUserStats] = useState<UserStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDashboardData = async () => {
      if (!user) return;
      
      try {
        setLoading(true);
        
        // Try to fetch user stats, but use fallback if it fails
        try {
          const stats = await apiService.getUserStats(user._id);
          setUserStats(stats);
        } catch (error) {
          console.error('Failed to fetch user stats:', error);
          // Use user data as fallback
          setUserStats({
            xp_points: user.xp_points || 0,
            problems_solved: user.problems_solved || 0,
            streak: user.streak || 0,
            easy_solved: 0,
            medium_solved: 0,
            hard_solved: 0,
            total_submissions: 0
          });
        }
        
      } finally {
        setLoading(false);
      }
    };

    fetchDashboardData();
  }, [user]);

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Please log in to view dashboard</div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-white text-xl">Loading dashboard...</div>
      </div>
    );
  }

  const currentLevel = Math.floor((userStats?.xp_points || 0) / 100) + 1;
  const badges = [
    { name: 'First Steps', icon: '🎯', earned: (userStats?.problems_solved || 0) > 0 },
    { name: 'Streak Master', icon: '🔥', earned: (userStats?.streak || 0) >= 5 },
    { name: 'Problem Solver', icon: '🧩', earned: (userStats?.problems_solved || 0) >= 10 },
    { name: 'Speed Demon', icon: '⚡', earned: (userStats?.problems_solved || 0) >= 50 },
    { name: 'Algorithm Expert', icon: '🧠', earned: (userStats?.hard_solved || 0) >= 5 },
    { name: 'Competition Winner', icon: '🏆', earned: (userStats?.xp_points || 0) >= 1000 }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <div className="container mx-auto px-6 py-8">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">
            Welcome back, {user.username}! 👋
          </h1>
          <p className="text-purple-200">Ready to solve some problems today?</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {/* XP Points */}
          <GlassPanel className="text-center">
            <div className="flex flex-col items-center">
              <Zap className="h-8 w-8 text-yellow-400 mb-2" />
              <div className="text-sm text-purple-200 mb-1">XP Points</div>
              <div className="text-2xl font-bold text-white">{userStats?.xp_points || 0}</div>
            </div>
          </GlassPanel>

          {/* Level */}
          <GlassPanel className="text-center">
            <div className="flex flex-col items-center">
              <Trophy className="h-8 w-8 text-purple-400 mb-2" />
              <div className="text-sm text-purple-200 mb-1">Level</div>
              <div className="text-2xl font-bold text-white">Level {currentLevel}</div>
            </div>
          </GlassPanel>

          {/* Streak */}
          <GlassPanel className="text-center">
            <div className="flex flex-col items-center">
              <Flame className="h-8 w-8 text-orange-400 mb-2" />
              <div className="text-sm text-purple-200 mb-1">Streak</div>
              <div className="text-2xl font-bold text-white">{userStats?.streak || 0}</div>
            </div>
          </GlassPanel>

          {/* Problems Solved */}
          <GlassPanel className="text-center">
            <div className="flex flex-col items-center">
              <CheckCircle className="h-8 w-8 text-green-400 mb-2" />
              <div className="text-sm text-purple-200 mb-1">Problems Solved</div>
              <div className="text-2xl font-bold text-white">{userStats?.problems_solved || 0}</div>
            </div>
          </GlassPanel>
        </div>

        {/* Progress Overview */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Problem Difficulty Breakdown */}
          <GlassPanel>
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
              <Target className="h-6 w-6 mr-2" />
              Problem Breakdown
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-400 rounded-full mr-3"></div>
                  <span className="text-purple-200">Easy</span>
                </div>
                <span className="text-white">{userStats?.easy_solved || 0} solved</span>
              </div>
              <div className="flex justify-between items-center">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-yellow-400 rounded-full mr-3"></div>
                  <span className="text-purple-200">Medium</span>
                </div>
                <span className="text-white">{userStats?.medium_solved || 0} solved</span>
              </div>
              <div className="flex justify-between items-center">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-red-400 rounded-full mr-3"></div>
                  <span className="text-purple-200">Hard</span>
                </div>
                <span className="text-white">{userStats?.hard_solved || 0} solved</span>
              </div>
            </div>
          </GlassPanel>

          {/* Achievements */}
          <GlassPanel>
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
              <Award className="h-6 w-6 mr-2" />
              Achievements
            </h2>
            <div className="grid grid-cols-3 gap-3">
              {badges.map((badge, index) => (
                <div 
                  key={index}
                  className={`text-center p-2 rounded-lg ${
                    badge.earned 
                      ? 'bg-yellow-400/20 border border-yellow-400/30' 
                      : 'bg-gray-700/50 border border-gray-600/30 opacity-50'
                  }`}
                >
                  <div className="text-2xl mb-1">{badge.icon}</div>
                  <div className="text-xs text-purple-200">{badge.name}</div>
                </div>
              ))}
            </div>
          </GlassPanel>

          {/* Recent Activity */}
          <GlassPanel>
            <h2 className="text-xl font-semibold text-white mb-4 flex items-center">
              <Clock className="h-6 w-6 mr-2" />
              Quick Stats
            </h2>
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-purple-200">Total Submissions</span>
                <span className="text-white">{userStats?.total_submissions || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-purple-200">Success Rate</span>
                <span className="text-white">
                  {userStats?.total_submissions ? 
                    Math.round(((userStats.problems_solved || 0) / userStats.total_submissions) * 100) 
                    : 0}%
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-purple-200">Current Level</span>
                <span className="text-white">Level {currentLevel}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-purple-200">Next Level</span>
                <span className="text-white">{100 - ((userStats?.xp_points || 0) % 100)} XP</span>
              </div>
            </div>
          </GlassPanel>
        </div>

        {/* Call to Action */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <GlassPanel className="text-center">
            <TrendingUp className="h-12 w-12 text-blue-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">Continue Learning</h3>
            <p className="text-purple-200 mb-4">Practice makes perfect! Keep solving problems to improve your skills.</p>
            <button 
              className="bg-gradient-to-r from-blue-500 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-blue-600 hover:to-purple-700 transition-all duration-200"
              onClick={() => window.location.href = '/problems'}
            >
              Browse Problems
            </button>
          </GlassPanel>

          <GlassPanel className="text-center">
            <Trophy className="h-12 w-12 text-yellow-400 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-white mb-2">Challenge Yourself</h3>
            <p className="text-purple-200 mb-4">Ready for a challenge? Compete with others and climb the leaderboard!</p>
            <button 
              className="bg-gradient-to-r from-yellow-500 to-orange-600 text-white px-6 py-3 rounded-lg hover:from-yellow-600 hover:to-orange-700 transition-all duration-200"
              onClick={() => window.location.href = '/compete'}
            >
              Start Competing
            </button>
          </GlassPanel>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
