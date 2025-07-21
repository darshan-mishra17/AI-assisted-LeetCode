import React, { useState } from 'react';
import { X, Send, Bot, User, Lightbulb, Code, HelpCircle } from 'lucide-react';
import GlassPanel from './GlassPanel';

interface AIMentorSidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const AIMentorSidebar: React.FC<AIMentorSidebarProps> = ({ isOpen, onClose }) => {
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState([
    {
      type: 'ai',
      content: "👋 Hi! I'm your AI coding mentor. I can help you with hints, explain concepts, or review your approach. What would you like assistance with?",
      timestamp: new Date()
    }
  ]);

  const suggestions = [
    { icon: Lightbulb, text: "Give me a hint for this problem" },
    { icon: Code, text: "Explain the optimal approach" },
    { icon: HelpCircle, text: "What data structure should I use?" }
  ];

  const handleSendMessage = () => {
    if (!message.trim()) return;

    const userMessage = {
      type: 'user',
      content: message,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = {
        type: 'ai',
        content: getAIResponse(message),
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
    }, 1000);

    setMessage('');
  };

  const getAIResponse = (userMessage: string) => {
    if (userMessage.toLowerCase().includes('hint')) {
      return "💡 Here's a hint: Think about using a hash map to store the numbers you've seen and their indices. For each number, check if its complement (target - current number) exists in the hash map.";
    } else if (userMessage.toLowerCase().includes('approach')) {
      return "🎯 The optimal approach is:\n\n1. Create a hash map to store number → index pairs\n2. Iterate through the array once\n3. For each number, calculate its complement (target - num)\n4. Check if complement exists in hash map\n5. If yes, return [complement_index, current_index]\n6. If no, add current number and index to hash map\n\nTime complexity: O(n), Space complexity: O(n)";
    } else if (userMessage.toLowerCase().includes('data structure')) {
      return "📊 For the Two Sum problem, use a **Hash Map** (or dictionary in Python, Map in JavaScript):\n\n• **Key**: The number from the array\n• **Value**: The index of that number\n\nThis allows O(1) lookup time to check if the complement exists, making the overall solution O(n) instead of O(n²) with nested loops.";
    } else {
      return "🤔 I understand you're working on the Two Sum problem. Could you be more specific about what you'd like help with? I can provide hints, explain approaches, or help with implementation details.";
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    setMessage(suggestion);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed right-0 top-16 h-[calc(100vh-4rem)] w-80 z-40 border-l border-white/20">
      <GlassPanel className="h-full rounded-none flex flex-col">
        {/* Header */}
        <div className="p-4 border-b border-white/20 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-blue-500 rounded-lg">
              <Bot className="h-5 w-5 text-white" />
            </div>
            <div>
              <h3 className="font-semibold text-white">AI Mentor</h3>
              <p className="text-xs text-green-400">● Online</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-all duration-300"
          >
            <X className="h-5 w-5 text-gray-400" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, index) => (
            <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-[80%] p-3 rounded-lg ${
                msg.type === 'user' 
                  ? 'bg-blue-600 text-white' 
                  : 'bg-white/10 text-gray-300'
              }`}>
                <div className="flex items-start space-x-2">
                  {msg.type === 'ai' && (
                    <Bot className="h-4 w-4 text-purple-400 mt-0.5 flex-shrink-0" />
                  )}
                  <div className="flex-1">
                    <div className="whitespace-pre-wrap text-sm">{msg.content}</div>
                    <div className="text-xs opacity-70 mt-1">
                      {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Quick Suggestions */}
        <div className="p-4 border-t border-white/20 space-y-2">
          <div className="text-sm text-gray-400 mb-2">Quick suggestions:</div>
          {suggestions.map((suggestion, index) => {
            const Icon = suggestion.icon;
            return (
              <button
                key={index}
                onClick={() => handleSuggestionClick(suggestion.text)}
                className="w-full flex items-center space-x-2 p-2 text-left text-sm bg-white/5 hover:bg-white/10 rounded-lg transition-all duration-300"
              >
                <Icon className="h-4 w-4 text-blue-400 flex-shrink-0" />
                <span className="text-gray-300">{suggestion.text}</span>
              </button>
            );
          })}
        </div>

        {/* Input */}
        <div className="p-4 border-t border-white/20">
          <div className="flex space-x-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
              placeholder="Ask for help..."
              className="flex-1 px-3 py-2 bg-black/20 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-400 text-sm"
            />
            <button
              onClick={handleSendMessage}
              disabled={!message.trim()}
              className="p-2 bg-blue-600 hover:bg-blue-500 disabled:bg-blue-600/50 disabled:cursor-not-allowed rounded-lg transition-all duration-300"
            >
              <Send className="h-4 w-4 text-white" />
            </button>
          </div>
        </div>
      </GlassPanel>
    </div>
  );
};

export default AIMentorSidebar;