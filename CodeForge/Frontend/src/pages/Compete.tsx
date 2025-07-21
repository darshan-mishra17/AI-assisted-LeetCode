import React, { useState, useEffect } from 'react';
import { Trophy, Users, Clock, Zap, Play, Crown, Medal, Award } from 'lucide-react';
import GlassPanel from '../components/GlassPanel';
import Editor from '@monaco-editor/react';

const Compete: React.FC = () => {
  const [timeLeft, setTimeLeft] = useState(1800); // 30 minutes
  const [battleStarted, setBattleStarted] = useState(false);
  const [myCode, setMyCode] = useState('function solve(nums) {\n  // Your solution here\n  \n}');
  const [opponentCode, setOpponentCode] = useState('function solve(nums) {\n  // Opponent is coding...\n  \n}');
  const [myProgress, setMyProgress] = useState(45);
  const [opponentProgress, setOpponentProgress] = useState(38);

  const leaderboard = [
    { rank: 1, name: 'CodeNinja', score: 2450, avatar: '🥷', streak: 12 },
    { rank: 2, name: 'AlgoMaster', score: 2380, avatar: '🧠', streak: 8 },
    { rank: 3, name: 'ByteWarrior', score: 2340, avatar: '⚔️', streak: 15 },
    { rank: 4, name: 'You', score: 2280, avatar: '👤', streak: 7 },
    { rank: 5, name: 'DevPython', score: 2190, avatar: '🐍', streak: 4 }
  ];

  const currentBattle = {
    problem: 'Maximum Subarray Sum',
    difficulty: 'Medium',
    description: 'Find the contiguous subarray with the largest sum.',
    opponent: {
      name: 'AlgoMaster',
      avatar: '🧠',
      rating: 2380,
      wins: 156,
      losses: 43
    }
  };

  useEffect(() => {
    if (battleStarted && timeLeft > 0) {
      const timer = setTimeout(() => setTimeLeft(timeLeft - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [timeLeft, battleStarted]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1: return <Crown className="h-5 w-5 text-yellow-400" />;
      case 2: return <Medal className="h-5 w-5 text-gray-300" />;
      case 3: return <Award className="h-5 w-5 text-orange-400" />;
      default: return <span className="text-gray-400">#{rank}</span>;
    }
  };

  if (!battleStarted) {
    return (
      <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-orange-400 to-red-400 bg-clip-text text-transparent">
              Competition Arena
            </h1>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Challenge developers worldwide in real-time coding battles
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Quick Match */}
            <div className="lg:col-span-2">
              <GlassPanel className="p-8 mb-8">
                <div className="text-center">
                  <Trophy className="h-16 w-16 text-yellow-400 mx-auto mb-6" />
                  <h2 className="text-2xl font-bold text-white mb-4">Ready for Battle?</h2>
                  <p className="text-gray-300 mb-8">
                    You'll be matched with an opponent of similar skill level for a 30-minute coding challenge.
                  </p>
                  <button
                    onClick={() => setBattleStarted(true)}
                    className="flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-orange-600 to-red-600 hover:from-orange-500 hover:to-red-500 rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105 mx-auto"
                  >
                    <Play className="h-5 w-5" />
                    <span>Find Match</span>
                  </button>
                </div>
              </GlassPanel>

              {/* Match Preview */}
              <GlassPanel className="p-6">
                <h3 className="text-xl font-semibold text-white mb-4">Next Battle Preview</h3>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="text-4xl">{currentBattle.opponent.avatar}</div>
                    <div>
                      <div className="text-white font-semibold">{currentBattle.opponent.name}</div>
                      <div className="text-gray-400 text-sm">Rating: {currentBattle.opponent.rating}</div>
                      <div className="text-gray-400 text-sm">
                        {currentBattle.opponent.wins}W / {currentBattle.opponent.losses}L
                      </div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-lg font-semibold text-white">{currentBattle.problem}</div>
                    <div className="text-yellow-400 text-sm">{currentBattle.difficulty}</div>
                    <div className="text-gray-400 text-sm mt-1">{currentBattle.description}</div>
                  </div>
                </div>
              </GlassPanel>
            </div>

            {/* Leaderboard */}
            <div>
              <GlassPanel className="p-6">
                <h3 className="text-xl font-semibold text-white mb-6 flex items-center">
                  <Trophy className="h-5 w-5 mr-2 text-yellow-400" />
                  Global Leaderboard
                </h3>
                <div className="space-y-4">
                  {leaderboard.map((player) => (
                    <div
                      key={player.rank}
                      className={`flex items-center justify-between p-3 rounded-lg transition-all duration-300 ${
                        player.name === 'You' 
                          ? 'bg-blue-500/20 border border-blue-400/30' 
                          : 'bg-white/5 hover:bg-white/10'
                      }`}
                    >
                      <div className="flex items-center space-x-3">
                        <div className="flex items-center justify-center w-8">
                          {getRankIcon(player.rank)}
                        </div>
                        <div className="text-2xl">{player.avatar}</div>
                        <div>
                          <div className={`font-medium ${player.name === 'You' ? 'text-blue-400' : 'text-white'}`}>
                            {player.name}
                          </div>
                          <div className="text-xs text-gray-400">
                            🔥 {player.streak} streak
                          </div>
                        </div>
                      </div>
                      <div className="text-right">
                        <div className="text-white font-semibold">{player.score}</div>
                        <div className="text-xs text-gray-400">points</div>
                      </div>
                    </div>
                  ))}
                </div>
              </GlassPanel>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Battle View
  return (
    <div className="min-h-screen">
      {/* Battle Header */}
      <div className="p-4 border-b border-white/20 bg-black/30">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-6">
            <div className="flex items-center space-x-2">
              <Clock className="h-5 w-5 text-orange-400" />
              <span className="text-2xl font-bold text-white">{formatTime(timeLeft)}</span>
            </div>
            <div className="text-white">
              <span className="text-gray-400">Problem:</span> {currentBattle.problem}
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="text-center">
              <div className="text-sm text-gray-400">You</div>
              <div className="text-lg font-bold text-blue-400">{myProgress}%</div>
            </div>
            <div className="text-center">
              <div className="text-sm text-gray-400">{currentBattle.opponent.name}</div>
              <div className="text-lg font-bold text-red-400">{opponentProgress}%</div>
            </div>
          </div>
        </div>
      </div>

      {/* Battle Arena */}
      <div className="flex h-[calc(100vh-120px)]">
        {/* Your Code */}
        <div className="w-1/2 border-r border-white/20">
          <div className="p-3 bg-blue-500/20 border-b border-white/20">
            <h3 className="font-semibold text-white">Your Solution</h3>
          </div>
          <Editor
            height="100%"
            language="javascript"
            value={myCode}
            onChange={(value) => setMyCode(value || '')}
            theme="vs-dark"
            options={{
              fontSize: 14,
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
            }}
          />
        </div>

        {/* Opponent Code */}
        <div className="w-1/2">
          <div className="p-3 bg-red-500/20 border-b border-white/20">
            <h3 className="font-semibold text-white">{currentBattle.opponent.name}'s Solution</h3>
          </div>
          <div className="h-full bg-gray-900 relative">
            <div className="absolute inset-0 backdrop-blur-sm bg-black/50 flex items-center justify-center">
              <div className="text-center">
                <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-400">Opponent's code will be revealed when time ends</p>
              </div>
            </div>
            <Editor
              height="100%"
              language="javascript"
              value={opponentCode}
              theme="vs-dark"
              options={{
                readOnly: true,
                fontSize: 14,
                minimap: { enabled: false },
              }}
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Compete;