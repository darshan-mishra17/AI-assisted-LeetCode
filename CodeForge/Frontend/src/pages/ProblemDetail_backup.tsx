import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { 
  Play, 
  Send, 
  ChevronRight, 
  Clock, 
  Users, 
  ThumbsUp,
  MessageCircle,
  BookOpen,
  Code,
  TestTube,
  Settings
} from 'lucide-react';
import GlassPanel from '../components/GlassPanel';
import AIMentorSidebar from '../components/AIMentorSidebar';

const ProblemDetail: React.FC = () => {
  const { id } = useParams();
  const [activeTab, setActiveTab] = useState('description');
  const [language, setLanguage] = useState('javascript');
  const [code, setCode] = useState(`function twoSum(nums, target) {
    // Your solution here
    
}`);
  const [testResults, setTestResults] = useState<any[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [showAIMentor, setShowAIMentor] = useState(false);

  const problem = {
    id: 1,
    title: 'Two Sum',
    difficulty: 'Easy',
    description: `Given an array of integers \`nums\` and an integer \`target\`, return indices of the two numbers such that they add up to \`target\`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.`,
    examples: [
      {
        input: 'nums = [2,7,11,15], target = 9',
        output: '[0,1]',
        explanation: 'Because nums[0] + nums[1] == 9, we return [0, 1].'
      },
      {
        input: 'nums = [3,2,4], target = 6',
        output: '[1,2]',
        explanation: 'Because nums[1] + nums[2] == 6, we return [1, 2].'
      }
    ],
    constraints: [
      '2 ≤ nums.length ≤ 10⁴',
      '-10⁹ ≤ nums[i] ≤ 10⁹',
      '-10⁹ ≤ target ≤ 10⁹',
      'Only one valid answer exists.'
    ],
    stats: {
      acceptance: '49.2%',
      submissions: '15.2M',
      likes: 45623,
      dislikes: 1547
    }
  };

  const languages = [
    { value: 'javascript', label: 'JavaScript' },
    { value: 'python', label: 'Python' },
    { value: 'java', label: 'Java' },
    { value: 'cpp', label: 'C++' },
    { value: 'typescript', label: 'TypeScript' }
  ];

  const testCases = [
    { input: '[2,7,11,15]\n9', output: '[0,1]', expected: '[0,1]' },
    { input: '[3,2,4]\n6', output: '[1,2]', expected: '[1,2]' },
    { input: '[3,3]\n6', output: '[0,1]', expected: '[0,1]' }
  ];

  const handleRunCode = () => {
    setIsRunning(true);
    setActiveTab('testcases');
    
    // Simulate test execution
    setTimeout(() => {
      setTestResults([
        { passed: true, input: '[2,7,11,15], 9', expected: '[0,1]', actual: '[0,1]', time: '2ms' },
        { passed: true, input: '[3,2,4], 6', expected: '[1,2]', actual: '[1,2]', time: '1ms' },
        { passed: false, input: '[3,3], 6', expected: '[0,1]', actual: '[1,0]', time: '1ms' }
      ]);
      setIsRunning(false);
    }, 2000);
  };

  const handleSubmit = () => {
    // Handle submission logic
    console.log('Submitting solution...');
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'Easy': return 'text-green-400';
      case 'Medium': return 'text-yellow-400';
      case 'Hard': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  return (
    <div className="min-h-screen flex">
      {/* Problem Description Panel */}
      <div className="w-full lg:w-1/2 border-r border-white/20">
        <div className="p-6 h-screen overflow-y-auto">
          {/* Header */}
          <div className="mb-6">
            <div className="flex items-center space-x-3 mb-4">
              <h1 className="text-2xl font-bold text-white">{problem.title}</h1>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(problem.difficulty)}`}>
                {problem.difficulty}
              </span>
            </div>
            
            {/* Stats */}
            <div className="flex items-center space-x-6 text-sm text-gray-400">
              <div className="flex items-center space-x-1">
                <ThumbsUp className="h-4 w-4" />
                <span>{problem.stats.likes}</span>
              </div>
              <div className="flex items-center space-x-1">
                <Users className="h-4 w-4" />
                <span>{problem.stats.submissions} submissions</span>
              </div>
              <div className="flex items-center space-x-1">
                <span>Acceptance: {problem.stats.acceptance}</span>
              </div>
            </div>
          </div>

          {/* Tabs */}
          <div className="flex space-x-4 mb-6 border-b border-white/20">
            {[
              { id: 'description', label: 'Description', icon: BookOpen },
              { id: 'solutions', label: 'Solutions', icon: Code },
              { id: 'discuss', label: 'Discuss', icon: MessageCircle }
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

          {/* Content */}
          {activeTab === 'description' && (
            <div className="space-y-6">
              {/* Problem Description */}
              <div className="text-gray-300 leading-relaxed">
                <div dangerouslySetInnerHTML={{ __html: problem.description.replace(/`([^`]+)`/g, '<code class="bg-gray-800 px-2 py-1 rounded text-blue-400">$1</code>') }} />
              </div>

              {/* Examples */}
              <div>
                <h3 className="text-white font-semibold mb-4">Examples:</h3>
                {problem.examples.map((example, index) => (
                  <GlassPanel key={index} className="p-4 mb-4">
                    <div className="space-y-2">
                      <div>
                        <span className="text-gray-400">Input: </span>
                        <code className="text-blue-400">{example.input}</code>
                      </div>
                      <div>
                        <span className="text-gray-400">Output: </span>
                        <code className="text-green-400">{example.output}</code>
                      </div>
                      <div className="text-sm text-gray-300">{example.explanation}</div>
                    </div>
                  </GlassPanel>
                ))}
              </div>

              {/* Constraints */}
              <div>
                <h3 className="text-white font-semibold mb-4">Constraints:</h3>
                <ul className="space-y-1 text-gray-300">
                  {problem.constraints.map((constraint, index) => (
                    <li key={index} className="flex items-start space-x-2">
                      <span className="text-blue-400 mt-1">•</span>
                      <code className="text-sm">{constraint}</code>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {activeTab === 'testcases' && (
            <div className="space-y-4">
              <h3 className="text-white font-semibold">Test Results:</h3>
              {testResults.map((result, index) => (
                <GlassPanel key={index} className="p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className={`font-medium ${result.passed ? 'text-green-400' : 'text-red-400'}`}>
                      Test Case {index + 1}: {result.passed ? 'Passed' : 'Failed'}
                    </span>
                    <span className="text-gray-400 text-sm">{result.time}</span>
                  </div>
                  <div className="text-sm space-y-1">
                    <div><span className="text-gray-400">Input:</span> <code>{result.input}</code></div>
                    <div><span className="text-gray-400">Expected:</span> <code className="text-green-400">{result.expected}</code></div>
                    <div><span className="text-gray-400">Actual:</span> <code className={result.passed ? 'text-green-400' : 'text-red-400'}>{result.actual}</code></div>
                  </div>
                </GlassPanel>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Code Editor Panel */}
      <div className="w-full lg:w-1/2 flex flex-col">
        {/* Editor Header */}
        <div className="p-4 border-b border-white/20 flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="px-3 py-2 bg-black/20 border border-white/20 rounded-lg text-white focus:outline-none focus:border-blue-400"
            >
              {languages.map((lang) => (
                <option key={lang.value} value={lang.value}>{lang.label}</option>
              ))}
            </select>
            
            <button
              onClick={() => setShowAIMentor(!showAIMentor)}
              className="flex items-center space-x-2 px-3 py-2 bg-gradient-to-r from-purple-500/20 to-blue-500/20 border border-purple-400/30 rounded-lg hover:from-purple-500/30 hover:to-blue-500/30 transition-all duration-300"
            >
              <MessageCircle className="h-4 w-4" />
              <span>AI Mentor</span>
            </button>
          </div>

          <div className="flex items-center space-x-2">
            <button
              onClick={handleRunCode}
              disabled={isRunning}
              className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-500 disabled:bg-green-600/50 disabled:cursor-not-allowed rounded-lg transition-all duration-300"
            >
              <Play className="h-4 w-4" />
              <span>{isRunning ? 'Running...' : 'Run'}</span>
            </button>
            
            <button
              onClick={handleSubmit}
              className="flex items-center space-x-2 px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg transition-all duration-300"
            >
              <Send className="h-4 w-4" />
              <span>Submit</span>
            </button>
          </div>
        </div>

        {/* Editor */}
        <div className="flex-1">
          <Editor
            height="100%"
            language={language}
            value={code}
            onChange={(value) => setCode(value || '')}
            theme="vs-dark"
            options={{
              fontSize: 14,
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              wordWrap: 'on',
              automaticLayout: true
            }}
          />
        </div>

        {/* Test Cases Panel */}
        <div className="h-48 border-t border-white/20 p-4 overflow-y-auto">
          <div className="flex items-center space-x-4 mb-4">
            <button
              onClick={() => setActiveTab('testcases')}
              className={`flex items-center space-x-2 px-3 py-1 rounded-lg transition-all duration-300 ${
                activeTab === 'testcases' ? 'bg-blue-500/20 text-blue-400' : 'text-gray-400 hover:text-white'
              }`}
            >
              <TestTube className="h-4 w-4" />
              <span>Test Cases</span>
            </button>
          </div>

          {/* Test Cases */}
          <div className="space-y-2">
            {testCases.map((testCase, index) => (
              <div key={index} className="p-3 bg-black/20 rounded-lg">
                <div className="text-sm">
                  <div className="text-gray-400 mb-1">Test Case {index + 1}:</div>
                  <div className="text-white font-mono text-xs">{testCase.input}</div>
                  <div className="text-gray-400 mt-1">Expected: <span className="text-green-400">{testCase.expected}</span></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* AI Mentor Sidebar */}
      <AIMentorSidebar isOpen={showAIMentor} onClose={() => setShowAIMentor(false)} />
    </div>
  );
};

export default ProblemDetail;