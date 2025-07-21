import React, { useState } from 'react';
import { Bot, X, Send, Lightbulb, Code, HelpCircle, Minimize2, Maximize2 } from 'lucide-react';

interface FloatingAIButtonProps {
  problemTitle?: string;
  currentCode?: string;
}

const FloatingAIButton: React.FC<FloatingAIButtonProps> = ({ problemTitle, currentCode }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<Array<{ type: 'user' | 'ai', content: string }>>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!message.trim()) return;

    const userMessage = message;
    setMessage('');
    setMessages(prev => [...prev, { type: 'user', content: userMessage }]);
    setIsLoading(true);

    // Simulate AI response (in real implementation, this would call your AI service)
    setTimeout(() => {
      let aiResponse = '';
      
      if (userMessage.toLowerCase().includes('hint')) {
        aiResponse = `For the ${problemTitle || 'current problem'}, try using a HashMap to store numbers you've seen and their indices. This allows O(1) lookup time for the complement.`;
      } else if (userMessage.toLowerCase().includes('debug') || userMessage.toLowerCase().includes('error')) {
        if (currentCode) {
          aiResponse = `I can help debug your code! Looking at your current solution, common issues include: 1) Off-by-one errors in loops, 2) Not handling edge cases, 3) Incorrect return types. Share your specific error and I'll help!`;
        } else {
          aiResponse = "I can help debug your code! Common issues include: 1) Off-by-one errors in loops, 2) Not handling edge cases, 3) Incorrect return types. Share your code and specific error!";
        }
      } else if (userMessage.toLowerCase().includes('explain')) {
        aiResponse = "I'll explain the solution approach: Use a hash map to store each number and its index as you iterate. For each number, calculate its complement (target - current number) and check if it exists in the map.";
      } else if (userMessage.toLowerCase().includes('optimize')) {
        aiResponse = "To optimize: 1) Use HashMap for O(1) lookups instead of nested loops, 2) Single pass through array, 3) Early return when solution found. Time: O(n), Space: O(n).";
      } else {
        aiResponse = `I'm here to help with ${problemTitle || 'your coding problem'}! Ask me for:\n• Hints about the approach\n• Code explanations\n• Debugging help\n• Optimization tips\n• Test case insights`;
      }

      setMessages(prev => [...prev, { type: 'ai', content: aiResponse }]);
      setIsLoading(false);
    }, 1000);
  };

  const quickActions = [
    { icon: Lightbulb, text: 'Get Hint', action: () => setMessage('Can you give me a hint?') },
    { icon: Code, text: 'Explain Solution', action: () => setMessage('Can you explain the solution approach?') },
    { icon: HelpCircle, text: 'Debug Help', action: () => setMessage('Help me debug my code') }
  ];

  if (!isOpen) {
    return (
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={() => setIsOpen(true)}
          className="bg-gradient-to-r from-blue-500 to-purple-600 text-white p-4 rounded-full shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-200 group"
        >
          <Bot className="w-6 h-6 group-hover:animate-pulse" />
        </button>
        <div className="absolute bottom-16 right-0 bg-gray-800 text-white px-3 py-2 rounded-lg text-sm whitespace-nowrap opacity-0 group-hover:opacity-100 transition-opacity">
          AI Assistant
        </div>
      </div>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      <div className={`bg-gray-900 border border-gray-700 rounded-xl shadow-2xl transition-all duration-300 ${
        isMinimized ? 'w-80 h-16' : 'w-96 h-[500px]'
      }`}>
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-700 bg-gradient-to-r from-blue-600 to-purple-600 rounded-t-xl">
          <div className="flex items-center gap-2">
            <Bot className="w-5 h-5 text-white" />
            <span className="text-white font-medium">AI Assistant</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setIsMinimized(!isMinimized)}
              className="text-white hover:bg-white/20 p-1 rounded transition-colors"
            >
              {isMinimized ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
            </button>
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:bg-white/20 p-1 rounded transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {!isMinimized && (
          <div className="flex flex-col h-[calc(500px-64px)]">
            {/* Messages */}
            <div className="flex-1 p-4 overflow-y-auto bg-gray-900 min-h-0">
              {messages.length === 0 ? (
                <div className="text-center text-gray-400 mt-8">
                  <Bot className="w-12 h-12 mx-auto mb-4 text-gray-500" />
                  <p className="text-sm">Hi! I'm your AI coding assistant.</p>
                  <p className="text-xs mt-2">Ask me for hints, explanations, or debugging help!</p>
                </div>
              ) : (
                <div className="space-y-3">
                  {messages.map((msg, index) => (
                    <div key={index} className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`max-w-[80%] p-3 rounded-lg text-sm ${
                        msg.type === 'user' 
                          ? 'bg-blue-600 text-white' 
                          : 'bg-gray-800 text-gray-100 border border-gray-700'
                      }`}>
                        {msg.content}
                      </div>
                    </div>
                  ))}
                  {isLoading && (
                    <div className="flex justify-start">
                      <div className="bg-gray-800 text-gray-100 p-3 rounded-lg text-sm border border-gray-700">
                        <div className="flex items-center gap-2">
                          <div className="flex gap-1">
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce"></div>
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                            <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                          </div>
                          <span>AI is thinking...</span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Quick Actions */}
            {messages.length === 0 && (
              <div className="px-4 py-2 border-t border-gray-700">
                <div className="grid grid-cols-3 gap-2">
                  {quickActions.map((action, index) => (
                    <button
                      key={index}
                      onClick={action.action}
                      className="flex flex-col items-center gap-1 p-2 bg-gray-800 hover:bg-gray-700 rounded-lg transition-colors text-xs"
                    >
                      <action.icon className="w-4 h-4 text-blue-400" />
                      <span className="text-gray-300">{action.text}</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input - Fixed at bottom */}
            <div className="p-4 border-t border-gray-700 bg-gray-900 rounded-b-xl">
              <div className="flex gap-2">
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                  placeholder="Ask me anything..."
                  className="flex-1 bg-gray-800 text-white px-3 py-2 rounded-lg border border-gray-600 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-sm"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!message.trim() || isLoading}
                  className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:cursor-not-allowed text-white p-2 rounded-lg transition-colors"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FloatingAIButton;
