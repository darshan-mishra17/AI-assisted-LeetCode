import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
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
  Settings,
  ArrowLeft,
  CheckCircle,
  XCircle
} from 'lucide-react';
import GlassPanel from '../components/GlassPanel';
import AIMentorSidebar from '../components/AIMentorSidebar';
import { apiService } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

interface Problem {
  _id: string;
  title: string;
  slug: string;
  description: string;
  difficulty: 'easy' | 'medium' | 'hard';
  examples: Array<{
    input: string;
    output: string;
    explanation?: string;
  }>;
  constraints: string[];
  test_cases: Array<{
    input: string;
    expected_output: string;
  }>;
  acceptance_rate: number;
  tags: string[];
}

interface TestResult {
  passed: boolean;
  input: string;
  expected: string;
  actual: string;
  time: string;
  error?: string;
}

const ProblemDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [problem, setProblem] = useState<Problem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState('description');
  const [language, setLanguage] = useState('javascript');
  const [code, setCode] = useState('');
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showAIMentor, setShowAIMentor] = useState(false);

  // Language templates
  const getLanguageTemplate = (problemTitle: string, language: string) => {
    const functionName = problemTitle.replace(/[^a-zA-Z0-9]/g, '').toLowerCase();
    const templates = {
      javascript: `function ${functionName}(/* parameters */) {
    // Your solution here
    
}`,
      python: `def ${functionName}(/* parameters */):
    # Your solution here
    pass`,
      java: `class Solution {
    public /* return_type */ ${functionName}(/* parameters */) {
        // Your solution here
        
    }
}`,
      cpp: `class Solution {
public:
    /* return_type */ ${functionName}(/* parameters */) {
        // Your solution here
        
    }
};`
    };
    return templates[language as keyof typeof templates] || templates.javascript;
  };

  useEffect(() => {
    const fetchProblem = async () => {
      if (!id) return;
      
      try {
        setLoading(true);
        setError(null);
        const problemData = await apiService.getProblemBySlug(id);
        setProblem(problemData);
        setCode(getLanguageTemplate(problemData.title, language));
      } catch (error: any) {
        console.error('Failed to fetch problem:', error);
        setError('Failed to load problem. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchProblem();
  }, [id]);

  useEffect(() => {
    if (problem) {
      setCode(getLanguageTemplate(problem.title, language));
    }
  }, [language, problem]);

  const handleRunCode = async () => {
    if (!problem || !user) return;
    
    setIsRunning(true);
    setActiveTab('testcases');
    
    try {
      // Submit code for testing (not final submission)
      const submission = await apiService.submitCode({
        problem_id: problem._id,
        code: code,
        language: language
      });
      
      // Convert submission results to test results format
      const results: TestResult[] = problem.test_cases.map((testCase, index) => {
        const testResult = submission.test_results?.[index];
        return {
          passed: testResult?.status === 'accepted',
          input: testCase.input,
          expected: testCase.expected_output,
          actual: testResult?.actual_output || '',
          time: testResult?.execution_time || '0ms',
          error: testResult?.error_message
        };
      });
      
      setTestResults(results);
    } catch (error: any) {
      console.error('Failed to run code:', error);
      setTestResults([{
        passed: false,
        input: 'Error',
        expected: '',
        actual: '',
        time: '0ms',
        error: error.message || 'Failed to execute code'
      }]);
    } finally {
      setIsRunning(false);
    }
  };

  const handleSubmit = async () => {
    if (!problem || !user) return;
    
    setIsSubmitting(true);
    
    try {
      const submission = await apiService.submitCode({
        problem_id: problem._id,
        code: code,
        language: language
      });
      
      if (submission.status === 'accepted') {
        alert('🎉 Accepted! Great job!');
      } else {
        alert(`❌ ${submission.status.replace('_', ' ').toUpperCase()}`);
      }
    } catch (error: any) {
      console.error('Failed to submit code:', error);
      alert('Failed to submit solution. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty.toLowerCase()) {
      case 'easy': return 'text-green-400';
      case 'medium': return 'text-yellow-400';
      case 'hard': return 'text-red-400';
      default: return 'text-gray-400';
    }
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-white">
          <p className="text-xl mb-4">Please log in to solve problems</p>
          <Link 
            to="/login"
            className="bg-blue-500 hover:bg-blue-600 px-6 py-3 rounded-lg transition-colors"
          >
            Login
          </Link>
        </div>
      </div>
    );
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-white text-xl">Loading problem...</div>
      </div>
    );
  }

  if (error || !problem) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center text-white">
          <p className="text-xl mb-4">{error || 'Problem not found'}</p>
          <Link 
            to="/problems"
            className="bg-blue-500 hover:bg-blue-600 px-6 py-3 rounded-lg transition-colors"
          >
            Back to Problems
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex">
      {/* Problem Description Panel */}
      <div className="w-full lg:w-1/2 border-r border-white/20">
        <div className="p-6 h-screen overflow-y-auto">
          {/* Header */}
          <div className="mb-6">
            <div className="flex items-center space-x-3 mb-4">
              <Link
                to="/problems"
                className="p-2 hover:bg-white/10 rounded-lg transition-colors"
              >
                <ArrowLeft className="h-5 w-5 text-white" />
              </Link>
              <h1 className="text-2xl font-bold text-white">{problem.title}</h1>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(problem.difficulty)}`}>
                {problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1)}
              </span>
            </div>
            
            <div className="flex items-center space-x-6 text-sm text-gray-300">
              <div className="flex items-center space-x-1">
                <Users className="h-4 w-4" />
                <span>{problem.acceptance_rate}% Acceptance</span>
              </div>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-2 mt-3">
              {problem.tags.map((tag, index) => (
                <span key={index} className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Tabs */}
          <div className="border-b border-white/20 mb-6">
            <div className="flex space-x-6">
              {['description', 'solutions', 'submissions'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={`pb-3 px-1 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab
                      ? 'border-blue-500 text-blue-400'
                      : 'border-transparent text-gray-300 hover:text-white'
                  }`}
                >
                  <div className="flex items-center space-x-2">
                    {tab === 'description' && <BookOpen className="h-4 w-4" />}
                    {tab === 'solutions' && <Code className="h-4 w-4" />}
                    {tab === 'submissions' && <MessageCircle className="h-4 w-4" />}
                    <span className="capitalize">{tab}</span>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          {activeTab === 'description' && (
            <div className="space-y-6">
              {/* Problem Statement */}
              <div>
                <div className="prose prose-invert max-w-none">
                  <div className="whitespace-pre-wrap text-gray-300 leading-relaxed">
                    {problem.description}
                  </div>
                </div>
              </div>

              {/* Examples */}
              {problem.examples && problem.examples.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">Examples</h3>
                  {problem.examples.map((example, index) => (
                    <GlassPanel key={index} className="mb-4 p-4">
                      <div className="font-semibold text-white mb-2">Example {index + 1}:</div>
                      <div className="space-y-2 text-sm">
                        <div>
                          <span className="text-gray-400">Input: </span>
                          <code className="bg-gray-800 px-2 py-1 rounded text-green-400">{example.input}</code>
                        </div>
                        <div>
                          <span className="text-gray-400">Output: </span>
                          <code className="bg-gray-800 px-2 py-1 rounded text-blue-400">{example.output}</code>
                        </div>
                        {example.explanation && (
                          <div>
                            <span className="text-gray-400">Explanation: </span>
                            <span className="text-gray-300">{example.explanation}</span>
                          </div>
                        )}
                      </div>
                    </GlassPanel>
                  ))}
                </div>
              )}

              {/* Constraints */}
              {problem.constraints && problem.constraints.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">Constraints</h3>
                  <ul className="space-y-1 text-gray-300 text-sm">
                    {problem.constraints.map((constraint, index) => (
                      <li key={index} className="flex items-start space-x-2">
                        <span className="text-gray-500">•</span>
                        <code className="text-gray-300">{constraint}</code>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>

      {/* Code Editor Panel */}
      <div className="w-full lg:w-1/2 flex flex-col">
        {/* Editor Header */}
        <div className="p-4 border-b border-white/20">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-4">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="bg-gray-800 border border-white/20 text-white px-3 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="javascript">JavaScript</option>
                <option value="python">Python</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
              </select>
              
              <button
                onClick={() => setShowAIMentor(!showAIMentor)}
                className="p-2 hover:bg-white/10 rounded-lg transition-colors"
              >
                <Settings className="h-5 w-5 text-white" />
              </button>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={handleRunCode}
                disabled={isRunning}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 disabled:opacity-50 rounded-lg transition-colors"
              >
                <Play className="h-4 w-4" />
                <span>{isRunning ? 'Running...' : 'Run'}</span>
              </button>
              
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-500 disabled:opacity-50 rounded-lg transition-colors"
              >
                <Send className="h-4 w-4" />
                <span>{isSubmitting ? 'Submitting...' : 'Submit'}</span>
              </button>
            </div>
          </div>

          {/* Test Results Tabs */}
          <div className="flex space-x-4 text-sm">
            <button
              onClick={() => setActiveTab('testcases')}
              className={`flex items-center space-x-2 px-3 py-1 rounded transition-colors ${
                activeTab === 'testcases' 
                  ? 'bg-blue-500/20 text-blue-400' 
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              <TestTube className="h-4 w-4" />
              <span>Test Cases</span>
            </button>
          </div>
        </div>

        {/* Code Editor */}
        <div className="flex-1 flex flex-col">
          <div className="flex-1">
            <Editor
              height="50vh"
              language={language === 'cpp' ? 'cpp' : language}
              theme="vs-dark"
              value={code}
              onChange={(value) => setCode(value || '')}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                lineNumbers: 'on',
                roundedSelection: false,
                scrollBeyondLastLine: false,
                automaticLayout: true,
              }}
            />
          </div>

          {/* Test Results */}
          <div className="h-1/2 border-t border-white/20 overflow-y-auto">
            <div className="p-4">
              {activeTab === 'testcases' && (
                <div>
                  <h3 className="text-white font-semibold mb-3">Test Results</h3>
                  {testResults.length === 0 ? (
                    <p className="text-gray-400">Run your code to see test results</p>
                  ) : (
                    <div className="space-y-2">
                      {testResults.map((result, index) => (
                        <div key={index} className={`p-3 rounded-lg border ${
                          result.passed 
                            ? 'bg-green-500/10 border-green-500/30' 
                            : 'bg-red-500/10 border-red-500/30'
                        }`}>
                          <div className="flex items-center justify-between mb-2">
                            <div className="flex items-center space-x-2">
                              {result.passed ? (
                                <CheckCircle className="h-4 w-4 text-green-400" />
                              ) : (
                                <XCircle className="h-4 w-4 text-red-400" />
                              )}
                              <span className="font-medium text-white">Test Case {index + 1}</span>
                            </div>
                            <span className="text-sm text-gray-400">{result.time}</span>
                          </div>
                          
                          <div className="text-sm space-y-1">
                            <div>
                              <span className="text-gray-400">Input: </span>
                              <code className="text-gray-300">{result.input}</code>
                            </div>
                            <div>
                              <span className="text-gray-400">Expected: </span>
                              <code className="text-green-400">{result.expected}</code>
                            </div>
                            <div>
                              <span className="text-gray-400">Actual: </span>
                              <code className={result.passed ? 'text-green-400' : 'text-red-400'}>
                                {result.actual}
                              </code>
                            </div>
                            {result.error && (
                              <div>
                                <span className="text-gray-400">Error: </span>
                                <code className="text-red-400">{result.error}</code>
                              </div>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* AI Mentor Sidebar */}
      {showAIMentor && (
        <AIMentorSidebar 
          onClose={() => setShowAIMentor(false)}
          problemId={problem._id}
          code={code}
          language={language}
        />
      )}
    </div>
  );
};

export default ProblemDetail;
