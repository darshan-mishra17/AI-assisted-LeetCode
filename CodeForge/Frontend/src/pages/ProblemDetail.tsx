import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import Editor from '@monaco-editor/react';
import { 
  Play, 
  Send, 
  Settings,
  ArrowLeft,
  CheckCircle,
  XCircle
} from 'lucide-react';
import AIMentorSidebar from '../components/AIMentorSidebar';
import { apiService, Problem } from '../services/api';
import { useAuth } from '../contexts/AuthContext';

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
  const { user } = useAuth();
  const [problem, setProblem] = useState<Problem | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Left panel tabs
  const [leftActiveTab, setLeftActiveTab] = useState('description');
  
  // Right panel editor
  const [language, setLanguage] = useState('javascript');
  const [code, setCode] = useState('');
  
  // Bottom panel tabs
  const [bottomActiveTab, setBottomActiveTab] = useState('testcase');
  const [testResults, setTestResults] = useState<TestResult[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showAIMentor, setShowAIMentor] = useState(false);

  // Language templates
  const getLanguageTemplate = (problemTitle: string, language: string) => {
    const functionName = problemTitle ? problemTitle.replace(/[^a-zA-Z0-9]/g, '').toLowerCase() : 'solution';
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
        console.log('Fetching problem with slug:', id);
        const problemData = await apiService.getProblemBySlug(id);
        console.log('Problem data received:', problemData);
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
    if (!problem) return;
    
    if (!user) {
      alert('Please log in to run code');
      return;
    }
    
    setIsRunning(true);
    setBottomActiveTab('testresult');
    
    try {
      const submission = await apiService.submitCode({
        problem_id: problem._id,
        code: code,
        language: language
      });
      
      const results: TestResult[] = [{
        passed: submission.status === 'accepted',
        input: 'All test cases',
        expected: `${submission.total_test_cases} test cases`,
        actual: `${submission.test_cases_passed} passed`,
        time: submission.runtime ? `${submission.runtime}ms` : '0ms',
        error: submission.error_message
      }];
      
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
    if (!problem) return;
    
    if (!user) {
      alert('Please log in to submit code');
      return;
    }
    
    setIsSubmitting(true);
    
    try {
      const submission = await apiService.submitCode({
        problem_id: problem._id,
        code: code,
        language: language
      });
      
      if (submission.status === 'accepted') {
        alert('🎉 Accepted! Great job!');
        
        // Dispatch problem solved event for other components
        window.dispatchEvent(new CustomEvent('problemSolved', {
          detail: { problemId: problem._id }
        }));
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
      case 'easy': return 'text-green-400 bg-green-400/10';
      case 'medium': return 'text-yellow-400 bg-yellow-400/10';
      case 'hard': return 'text-red-400 bg-red-400/10';
      default: return 'text-gray-400 bg-gray-400/10';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-white text-xl">Loading problem...</div>
      </div>
    );
  }

  if (error || !problem) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
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
    <div className="min-h-screen bg-gray-900 flex">
      {/* Left Panel - Problem Description */}
      <div className="w-1/2 border-r border-gray-700">
        <div className="p-6 h-screen overflow-y-auto">
          {/* Header */}
          <div className="mb-6">
            <div className="flex items-center space-x-3 mb-4">
              <Link
                to="/problems"
                className="p-2 hover:bg-gray-700 rounded-lg transition-colors"
              >
                <ArrowLeft className="h-5 w-5 text-white" />
              </Link>
              <h1 className="text-xl font-bold text-white">{problem.title}</h1>
              <span className={`px-3 py-1 rounded-full text-sm font-medium ${getDifficultyColor(problem.difficulty)}`}>
                {problem.difficulty.charAt(0).toUpperCase() + problem.difficulty.slice(1)}
              </span>
            </div>

            {/* Tags */}
            <div className="flex flex-wrap gap-2">
              {problem.tags?.map((tag, index) => (
                <span key={index} className="px-2 py-1 bg-gray-700 text-gray-300 rounded text-xs">
                  {tag}
                </span>
              ))}
            </div>
          </div>

          {/* Left Panel Tabs */}
          <div className="border-b border-gray-700 mb-6">
            <div className="flex space-x-6">
              {['description', 'editorial', 'solutions', 'submissions'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setLeftActiveTab(tab)}
                  className={`pb-3 px-1 border-b-2 font-medium text-sm transition-colors capitalize ${
                    leftActiveTab === tab
                      ? 'border-orange-500 text-orange-400'
                      : 'border-transparent text-gray-300 hover:text-white'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          {leftActiveTab === 'description' && (
            <div className="space-y-6">
              {/* Problem Statement */}
              <div className="text-gray-300 leading-relaxed whitespace-pre-wrap">
                {problem.description}
              </div>

              {/* Examples */}
              {problem.examples && problem.examples.length > 0 && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">Examples</h3>
                  {problem.examples.map((example, index) => (
                    <div key={index} className="mb-4 p-4 bg-gray-800 rounded-lg">
                      <div className="font-semibold text-white mb-2">Example {index + 1}:</div>
                      <div className="space-y-2 text-sm">
                        <div>
                          <span className="text-gray-400">Input: </span>
                          <code className="bg-gray-700 px-2 py-1 rounded text-green-400">{example.input}</code>
                        </div>
                        <div>
                          <span className="text-gray-400">Output: </span>
                          <code className="bg-gray-700 px-2 py-1 rounded text-blue-400">{example.output}</code>
                        </div>
                        {example.explanation && (
                          <div>
                            <span className="text-gray-400">Explanation: </span>
                            <span className="text-gray-300">{example.explanation}</span>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Constraints */}
              {problem.constraints && (
                <div>
                  <h3 className="text-lg font-semibold text-white mb-3">Constraints</h3>
                  <div className="text-gray-300 text-sm whitespace-pre-wrap bg-gray-800 p-4 rounded-lg">
                    {problem.constraints}
                  </div>
                </div>
              )}
            </div>
          )}

          {leftActiveTab === 'editorial' && (
            <div className="text-center text-gray-400 py-8">
              Editorial coming soon...
            </div>
          )}

          {leftActiveTab === 'solutions' && (
            <div className="text-center text-gray-400 py-8">
              Community solutions coming soon...
            </div>
          )}

          {leftActiveTab === 'submissions' && (
            <div className="text-center text-gray-400 py-8">
              Your submissions will appear here...
            </div>
          )}
        </div>
      </div>

      {/* Right Panel - Code Editor */}
      <div className="w-1/2 flex flex-col bg-gray-800">
        {/* Editor Header */}
        <div className="p-4 border-b border-gray-700">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="bg-gray-700 border border-gray-600 text-white px-3 py-2 rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
              >
                <option value="javascript">JavaScript</option>
                <option value="python">Python</option>
                <option value="java">Java</option>
                <option value="cpp">C++</option>
              </select>
              
              <button
                onClick={() => setShowAIMentor(!showAIMentor)}
                className="p-2 hover:bg-gray-700 rounded transition-colors"
              >
                <Settings className="h-5 w-5 text-white" />
              </button>
            </div>

            <div className="flex items-center space-x-3">
              <button
                onClick={handleRunCode}
                disabled={isRunning}
                className="flex items-center space-x-2 px-4 py-2 bg-gray-700 hover:bg-gray-600 disabled:opacity-50 rounded transition-colors text-white font-medium"
              >
                <Play className="h-4 w-4" />
                <span>{isRunning ? 'Running...' : 'Run'}</span>
              </button>
              
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 hover:bg-green-500 disabled:opacity-50 rounded transition-colors text-white font-medium"
              >
                <Send className="h-4 w-4" />
                <span>{isSubmitting ? 'Submitting...' : 'Submit'}</span>
              </button>
            </div>
          </div>
        </div>

        {/* Code Editor */}
        <div className="flex-1">
          <Editor
            height="60%"
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
              padding: { top: 10, bottom: 10 }
            }}
          />
        </div>

        {/* Bottom Panel - Test Cases */}
        <div className="h-2/5 border-t border-gray-700">
          <div className="border-b border-gray-700">
            <div className="flex space-x-6 px-4">
              {['testcase', 'testresult'].map((tab) => (
                <button
                  key={tab}
                  onClick={() => setBottomActiveTab(tab)}
                  className={`py-3 px-1 border-b-2 font-medium text-sm transition-colors capitalize ${
                    bottomActiveTab === tab
                      ? 'border-orange-500 text-orange-400'
                      : 'border-transparent text-gray-300 hover:text-white'
                  }`}
                >
                  {tab === 'testcase' ? 'Testcase' : 'Test Result'}
                </button>
              ))}
            </div>
          </div>

          <div className="p-4 h-full overflow-y-auto">
            {bottomActiveTab === 'testcase' && (
              <div>
                <h3 className="text-white font-semibold mb-3">Test Cases</h3>
                {problem.test_cases && problem.test_cases.length > 0 ? (
                  <div className="space-y-4">
                    {problem.test_cases.slice(0, 3).map((testCase, index) => (
                      <div key={index} className="bg-gray-900 p-4 rounded-lg">
                        <div className="font-medium text-white mb-2">Case {index + 1}</div>
                        <div className="space-y-2 text-sm">
                          <div>
                            <span className="text-gray-400">Input: </span>
                            <code className="bg-gray-700 px-2 py-1 rounded text-green-400">
                              {testCase.input}
                            </code>
                          </div>
                          <div>
                            <span className="text-gray-400">Expected: </span>
                            <code className="bg-gray-700 px-2 py-1 rounded text-blue-400">
                              {testCase.expected_output}
                            </code>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="text-gray-400">No test cases available</div>
                )}
              </div>
            )}

            {bottomActiveTab === 'testresult' && (
              <div>
                <h3 className="text-white font-semibold mb-3">Test Results</h3>
                {testResults.length === 0 ? (
                  <div className="text-gray-400">Run your code to see test results</div>
                ) : (
                  <div className="space-y-3">
                    {testResults.map((result, index) => (
                      <div key={index} className={`p-4 rounded-lg border ${
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
                            <span className="font-medium text-white">Test Result {index + 1}</span>
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

      {/* AI Mentor Sidebar */}
      {showAIMentor && (
        <AIMentorSidebar 
          isOpen={showAIMentor}
          onClose={() => setShowAIMentor(false)}
        />
      )}
    </div>
  );
};

export default ProblemDetail;
