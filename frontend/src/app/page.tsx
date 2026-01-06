'use client';

import Link from 'next/link';
import { CheckCircle2, Users, Shield, Zap, ArrowRight } from 'lucide-react';
import { useState } from 'react';
import { signup, signin, User } from '@/lib/api-client';
import { setAuthUser } from '@/lib/auth-client';
import { useRouter, redirect } from 'next/navigation';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      {/* Header/Nav */}
      <header className="border-b bg-white/80 backdrop-blur-sm sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-6 h-6 text-blue-600" />
            <span className="text-xl font-bold">TaskFlow</span>
          </div>
          <nav className="hidden md:flex items-center gap-6">
            <a href="#features" className="text-sm text-slate-600 hover:text-slate-900">Features</a>
            <a href="#auth" className="text-sm text-slate-600 hover:text-slate-900">Get Started</a>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <div className="max-w-4xl mx-auto text-center space-y-8">
          <div className="inline-block px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-sm font-medium mb-4">
            ✨ Your Personal Task Management Solution
          </div>
          <h1 className="text-5xl md:text-6xl font-bold tracking-tight text-slate-900">
            Organize Your Life,
            <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent"> One Task at a Time</span>
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto">
            A secure, intuitive todo app designed for individuals who want to stay on top of their tasks without the complexity.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center pt-4">
            <a href="#auth" className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors">
              Get Started Free
              <ArrowRight className="w-4 h-4" />
            </a>
            <a href="#features" className="inline-flex items-center justify-center gap-2 px-6 py-3 border-2 border-slate-300 text-slate-700 rounded-lg font-medium hover:border-slate-400 transition-colors">
              Learn More
            </a>
          </div>
        </div>

        {/* Hero Visual */}
        <div className="max-w-5xl mx-auto mt-16">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-400 to-indigo-400 rounded-2xl blur-3xl opacity-20"></div>
            <div className="relative bg-white rounded-2xl shadow-2xl border p-8">
              <div className="space-y-3">
                {[
                  { text: "Finish project proposal", done: true },
                  { text: "Review design mockups", done: true },
                  { text: "Schedule team meeting", done: false },
                  { text: "Update documentation", done: false }
                ].map((task, i) => (
                  <div key={i} className="flex items-center gap-3 p-4 bg-slate-50 rounded-lg">
                    <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${task.done ? 'bg-blue-600 border-blue-600' : 'border-slate-300'}`}>
                      {task.done && <CheckCircle2 className="w-3 h-3 text-white" />}
                    </div>
                    <span className={task.done ? 'text-slate-400 line-through' : 'text-slate-700'}>{task.text}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              Everything you need to stay organized
            </h2>
            <p className="text-lg text-slate-600">
              Simple, powerful features that help you focus on what matters.
            </p>
          </div>

          <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
            <div className="text-center space-y-4">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-blue-100 rounded-lg">
                <Users className="w-6 h-6 text-blue-600" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900">Personal Workspace</h3>
              <p className="text-slate-600">
                Your own private space to manage tasks exactly how you want.
              </p>
            </div>

            <div className="text-center space-y-4">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-indigo-100 rounded-lg">
                <Shield className="w-6 h-6 text-indigo-600" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900">Secure & Private</h3>
              <p className="text-slate-600">
                Your data is encrypted and protected with industry-standard security.
              </p>
            </div>

            <div className="text-center space-y-4">
              <div className="inline-flex items-center justify-center w-12 h-12 bg-violet-100 rounded-lg">
                <Zap className="w-6 h-6 text-violet-600" />
              </div>
              <h3 className="text-xl font-semibold text-slate-900">Lightning Fast</h3>
              <p className="text-slate-600">
                Instant updates and seamless performance across all your devices.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Auth Section */}
      <section id="auth" className="py-20 bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="container mx-auto px-4">
          <div className="text-center max-w-2xl mx-auto mb-12">
            <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-4">
              Start organizing today
            </h2>
            <p className="text-lg text-slate-600">
              Create your free account or sign in to continue.
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
            <div className="bg-white rounded-2xl border shadow-lg p-8">
              <div className="mb-6">
                <h3 className="text-2xl font-semibold text-slate-900">New User</h3>
                <p className="text-slate-600 mt-1">
                  Create your account to get started
                </p>
              </div>
              <SignupFormInline />
            </div>

            <div className="bg-white rounded-2xl border shadow-lg p-8">
              <div className="mb-6">
                <h3 className="text-2xl font-semibold text-slate-900">Existing User</h3>
                <p className="text-slate-600 mt-1">
                  Sign in to access your tasks
                </p>
              </div>
              <SigninFormInline />
            </div>
            
          </div>

          <div className="mt-8 text-center">
            <a href="/dashboard" className="text-slate-600 hover:text-slate-900 underline text-sm">
              Go to dashboard (requires authentication)
            </a>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t bg-white py-12">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center gap-2">
              <CheckCircle2 className="w-5 h-5 text-blue-600" />
              <span className="font-semibold">TaskFlow</span>
            </div>
            <p className="text-sm text-slate-600">
              © 2025 TaskFlow. Manage your personal tasks securely.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

function SignupFormInline() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const user: User = await signup({ email, password });
      setAuthUser(user);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="signup-email" className="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input
            id="signup-email"
            type="email"
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        <div>
          <label htmlFor="signup-password" className="block text-sm font-medium text-slate-700 mb-1">Password</label>
          <input
            id="signup-password"
            type="password"
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            disabled={loading}
          />
        </div>
        {error && (
          <div className="text-sm text-red-600 bg-red-100 p-2 rounded-md">
            {error}
          </div>
        )}
        <button
          type="submit"
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Creating account...' : 'Create Account'}
        </button>
      </form>
    </div>
  );
}

function SigninFormInline() {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const user: User = await signin({ email, password });
      setAuthUser(user);
      router.push('/dashboard');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="signin-email" className="block text-sm font-medium text-slate-700 mb-1">Email</label>
          <input
            id="signin-email"
            type="email"
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        <div>
          <label htmlFor="signin-password" className="block text-sm font-medium text-slate-700 mb-1">Password</label>
          <input
            id="signin-password"
            type="password"
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="••••••••"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            disabled={loading}
          />
        </div>
        {error && (
          <div className="text-sm text-red-600 bg-red-100 p-2 rounded-md">
            {error}
          </div>
        )}
        <button
          type="submit"
          className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:opacity-50"
          disabled={loading}
        >
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>
    </div>
  );
}
