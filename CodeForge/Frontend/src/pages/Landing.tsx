import React from 'react';
import { Link } from 'react-router-dom';
import { 
  Code2, 
  Zap, 
  Users, 
  BookOpen, 
  Trophy, 
  Brain,
  ArrowRight,
  CheckCircle,
  Star,
  Sparkles,
  User
} from 'lucide-react';
import GlassPanel from '../components/GlassPanel';

const Landing: React.FC = () => {
  const features = [
    {
      icon: Brain,
      title: 'AI Mentor',
      description: 'Get personalized hints and explanations from our intelligent coding assistant'
    },
    {
      icon: Users,
      title: 'Peer-vs-Peer Mode',
      description: 'Challenge friends and developers worldwide in real-time coding battles'
    },
    {
      icon: BookOpen,
      title: 'Roadmap Learning',
      description: 'Follow structured learning paths tailored to your goals and skill level'
    },
    {
      icon: Trophy,
      title: 'Gamified Progress',
      description: 'Earn XP, unlock badges, and track your coding journey with detailed analytics'
    }
  ];

  const stats = [
    { value: '50K+', label: 'Active Coders' },
    { value: '1000+', label: 'Problems' },
    { value: '98%', label: 'Success Rate' },
    { value: '24/7', label: 'AI Support' }
  ];

  return (
    <div className="relative">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute top-20 left-10 w-72 h-72 bg-blue-500/20 rounded-full blur-3xl animate-pulse"></div>
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-cyan-500/20 rounded-full blur-3xl animate-pulse delay-500"></div>
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="mb-8">
            <div className="inline-flex items-center space-x-2 px-4 py-2 rounded-full bg-gradient-to-r from-blue-500/20 to-purple-500/20 border border-white/20 mb-6">
              <Sparkles className="h-4 w-4 text-yellow-400" />
              <span className="text-sm font-medium text-gray-300">New: AI-Powered Code Reviews</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-cyan-400 bg-clip-text text-transparent">
              Master Coding
              <br />
              <span className="text-white">at CodeForge</span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Level up your programming skills with AI-powered mentoring, 
              competitive coding battles, and personalized learning roadmaps.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
              <Link
                to="/problems"
                className="group flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                <Zap className="h-5 w-5" />
                <span>Start Coding</span>
                <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              
              <Link
                to="/dashboard"
                className="flex items-center space-x-2 px-8 py-4 border border-white/20 hover:bg-white/10 rounded-xl font-semibold transition-all duration-300"
              >
                <User className="h-5 w-5" />
                <span>View Dashboard</span>
              </Link>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16">
            {stats.map((stat, index) => (
              <GlassPanel key={index} className="p-6 text-center">
                <div className="text-3xl font-bold text-blue-400 mb-2">{stat.value}</div>
                <div className="text-gray-300 text-sm">{stat.label}</div>
              </GlassPanel>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              Why Choose CodeForge?
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto">
              Experience the future of coding education with cutting-edge features 
              designed to accelerate your programming journey.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <GlassPanel key={index} className="p-8" hover>
                  <div className="flex items-start space-x-4">
                    <div className="p-3 rounded-lg bg-gradient-to-r from-blue-500 to-purple-600">
                      <Icon className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <h3 className="text-xl font-semibold mb-3 text-white">{feature.title}</h3>
                      <p className="text-gray-300 leading-relaxed">{feature.description}</p>
                    </div>
                  </div>
                </GlassPanel>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center">
          <GlassPanel className="p-12">
            <Code2 className="h-16 w-16 text-blue-400 mx-auto mb-6" />
            <h2 className="text-3xl md:text-4xl font-bold mb-6 text-white">
              Ready to Transform Your Coding Skills?
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Join thousands of developers who are already mastering algorithms, 
              data structures, and competitive programming.
            </p>
            <Link
              to="/problems"
              className="inline-flex items-center space-x-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 rounded-xl font-semibold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
            >
              <span>Begin Your Journey</span>
              <ArrowRight className="h-5 w-5" />
            </Link>
          </GlassPanel>
        </div>
      </section>
    </div>
  );
};

export default Landing;