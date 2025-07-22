import React, { useState } from 'react';
import { X, Send, Bot, Lightbulb, Bug, BookOpen, Route } from 'lucide-react';
import API_BASE_URL from '../config/api';

interface AIMentorSidebarProps {
  isOpen: boolean;
  onClose: () => void;
  currentProblem: {
    id: string;
    title: string;
    difficulty: string;
    description: string;
  };
  userCode: string;
  language: string;
}

interface Message {
  type: 'user' | 'ai';
  content: string;
  timestamp: Date;
}

const AIMentorSidebar: React.FC<AIMentorSidebarProps> = ({
  isOpen,
  onClose,
  currentProblem,
  userCode,
  language
}) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const API_BASE = API_BASE_URL; // Use the configured API URL

  const sendMessage = async (message: string, type: 'chat' | 'hint' | 'analyze' | 'explain' | 'debug' | 'learning-path' = 'chat') => {
    if (!message.trim() && type === 'chat') return;

    const userMessage: Message = {
      type: 'user',
      content: message || getQuickActionText(type),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      let endpoint = '';
      let payload: any = {
        problem_id: currentProblem.id,
        user_code: userCode,
        language: language,
        hint_type: 'explanation'
      };

      switch (type) {
        case 'hint':
          endpoint = '/ai/hint';
          payload.hint_type = 'hint';
          break;
        case 'analyze':
          endpoint = '/ai/analyze';
          // For analyze endpoint, use different payload structure
          payload = {
            code: userCode,
            language: language,
            problem_description: currentProblem.description
          };
          break;
        case 'explain':
          endpoint = '/ai/explain-concept';
          // For explain endpoint
          payload = {
            concept: message || 'current problem approach',
            user_level: 'intermediate',
            include_examples: true,
            programming_language: language
          };
          break;
        case 'debug':
          endpoint = '/ai/debug';
          // For debug endpoint
          payload = {
            code: userCode,
            language: language,
            error_message: message || 'Code debugging needed',
            expected_behavior: 'Correct algorithm implementation'
          };
          break;
        case 'learning-path':
          endpoint = '/ai/learning-path';
          // For learning path endpoint
          payload = {
            current_problem_id: currentProblem.id,
            user_strengths: ['problem-solving'],
            user_weaknesses: ['optimization']
          };
          break;
        default:
          endpoint = '/ai/hint'; // Default to hint for chat
          payload.hint_type = 'explanation';
      }

      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      
      const aiMessage: Message = {
        type: 'ai',
        content: data.response || data.hint || data.analysis || data.explanation || data.debug_suggestion || data.learning_path || 'Sorry, I couldn\'t process your request.',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error('AI Mentor Error:', error);
      const errorMessage: Message = {
        type: 'ai',
        content: `Sorry, I'm having trouble connecting to the AI service. Error: ${error instanceof Error ? error.message : 'Unknown error'}`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const getQuickActionText = (type: string): string => {
    switch (type) {
      case 'hint': return 'Can you give me a hint for this problem?';
      case 'analyze': return 'Please analyze my current code';
      case 'explain': return 'Explain the key concepts for this problem';
      case 'debug': return 'Help me debug my code';
      case 'learning-path': return 'What should I learn to master this type of problem?';
      default: return '';
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-y-0 right-0 w-96 bg-slate-900 border-l border-slate-700 z-50 flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-slate-700">
        <div className="flex items-center gap-2">
          <Bot className="w-5 h-5 text-blue-400" />
          <h2 className="text-white font-semibold">AI Mentor</h2>
        </div>
        <button
          onClick={onClose}
          className="text-slate-400 hover:text-white transition-colors"
        >
          <X className="w-5 h-5" />
        </button>
      </div>

      {/* Problem Context */}
      <div className="p-3 bg-slate-800 border-b border-slate-700">
        <div className="text-sm text-slate-300">
          <p className="font-medium text-white">{currentProblem.title}</p>
          <p className="text-xs text-slate-400">Difficulty: {currentProblem.difficulty}</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="p-3 border-b border-slate-700">
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={() => sendMessage('', 'hint')}
            disabled={isLoading}
            className="flex items-center gap-2 p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-sm disabled:opacity-50"
          >
            <Lightbulb className="w-4 h-4" />
            Hint
          </button>
          <button
            onClick={() => sendMessage('', 'analyze')}
            disabled={isLoading}
            className="flex items-center gap-2 p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-sm disabled:opacity-50"
          >
            <BookOpen className="w-4 h-4" />
            Analyze
          </button>
          <button
            onClick={() => sendMessage('', 'debug')}
            disabled={isLoading}
            className="flex items-center gap-2 p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-sm disabled:opacity-50"
          >
            <Bug className="w-4 h-4" />
            Debug
          </button>
          <button
            onClick={() => sendMessage('', 'learning-path')}
            disabled={isLoading}
            className="flex items-center gap-2 p-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-sm disabled:opacity-50"
          >
            <Route className="w-4 h-4" />
            Learn
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-slate-400 py-8">
            <Bot className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>Hi! I'm your AI mentor.</p>
            <p className="text-sm mt-1">Ask me anything about this problem or use the quick actions above!</p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] p-3 rounded-lg ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-800 text-slate-200'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className="text-xs opacity-60 mt-1">
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-slate-800 text-slate-200 p-3 rounded-lg">
              <div className="flex items-center gap-2">
                <Bot className="w-4 h-4 animate-pulse" />
                <span>AI is thinking...</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-slate-700">
        <div className="flex gap-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Ask me anything about this problem..."
            className="flex-1 bg-slate-800 text-white placeholder-slate-400 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !inputMessage.trim()}
            className="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed text-white p-2 rounded-lg transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
};

export default AIMentorSidebar;
