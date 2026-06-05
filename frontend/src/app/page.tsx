import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Activity, Users, FileText, CheckCircle } from 'lucide-react';

export default function Home() {
  return (
    <div className="flex min-h-screen bg-gray-950 text-white font-sans">
      <div className="flex-1 p-8 space-y-8">
        
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-emerald-400">
              AgentSphere
            </h1>
            <p className="text-gray-400 mt-2 text-lg">Autonomous Multi-Agent Social Media Management</p>
          </div>
          <div className="flex items-center space-x-4">
            <button className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded-full shadow-lg transition-all transform hover:scale-105 font-medium">
              + New Campaign
            </button>
            <div className="w-12 h-12 rounded-full bg-gradient-to-tr from-purple-500 to-pink-500 border-2 border-gray-800 shadow-md"></div>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard title="Active Campaigns" value="12" icon={<Activity className="text-blue-400" />} />
          <StatCard title="Posts Scheduled" value="84" icon={<FileText className="text-emerald-400" />} />
          <StatCard title="Pending Approvals" value="5" icon={<CheckCircle className="text-amber-400" />} />
          <StatCard title="Audience Reach" value="2.4M" icon={<Users className="text-purple-400" />} />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-6">
            <h2 className="text-2xl font-bold text-gray-100">Live Agent Activity</h2>
            <div className="bg-gray-900 rounded-xl p-6 shadow-xl border border-gray-800 space-y-4">
              <AgentLog agent="Trend Analyst" action="Discovered rising hashtag #AIAutomation" status="success" />
              <AgentLog agent="Content Creator" action="Generated 5 variations for LinkedIn post" status="success" />
              <AgentLog agent="Brand Guardian" action="Reviewing tone consistency..." status="pending" />
            </div>
          </div>
          
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-gray-100">Quick Actions</h2>
            <div className="bg-gray-900 rounded-xl p-6 shadow-xl border border-gray-800 flex flex-col space-y-4">
              <button className="w-full text-left bg-gray-800 hover:bg-gray-700 px-4 py-3 rounded-lg transition-colors border border-gray-700 hover:border-blue-500">
                🔍 Run Trend Analysis
              </button>
              <button className="w-full text-left bg-gray-800 hover:bg-gray-700 px-4 py-3 rounded-lg transition-colors border border-gray-700 hover:border-emerald-500">
                ✍️ Draft Single Post
              </button>
              <button className="w-full text-left bg-gray-800 hover:bg-gray-700 px-4 py-3 rounded-lg transition-colors border border-gray-700 hover:border-purple-500">
                📊 View Analytics Report
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}

function StatCard({ title, value, icon }: { title: string, value: string, icon: React.ReactNode }) {
  return (
    <div className="bg-gray-900 rounded-xl p-6 border border-gray-800 shadow-lg hover:border-gray-700 transition-colors">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-gray-400 font-medium">{title}</h3>
        {icon}
      </div>
      <p className="text-3xl font-bold text-white">{value}</p>
    </div>
  );
}

function AgentLog({ agent, action, status }: { agent: string, action: string, status: 'success' | 'pending' | 'error' }) {
  const statusColors = {
    success: 'bg-emerald-500',
    pending: 'bg-amber-500 animate-pulse',
    error: 'bg-red-500'
  };

  return (
    <div className="flex items-start space-x-4 p-4 rounded-lg bg-gray-800/50">
      <div className={`mt-1.5 w-3 h-3 rounded-full ${statusColors[status]}`}></div>
      <div>
        <h4 className="font-semibold text-gray-200">{agent}</h4>
        <p className="text-gray-400 text-sm">{action}</p>
      </div>
    </div>
  );
}
