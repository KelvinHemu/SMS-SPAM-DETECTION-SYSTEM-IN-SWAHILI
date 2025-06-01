import React, { useState, useEffect } from 'react';
import { Shield, AlertTriangle, Clock, Phone, TrendingUp, Activity, RefreshCw } from 'lucide-react';
import { spamDetectionAPI } from '../services/api';

const SpamDashboard = () => {
  const [stats, setStats] = useState(null);
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastRefresh, setLastRefresh] = useState(new Date());

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsData, healthData] = await Promise.all([
        spamDetectionAPI.getDeliveryStats(),
        spamDetectionAPI.getHealthStatus()
      ]);
      setStats(statsData);
      setHealth(healthData);
      setLastRefresh(new Date());
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const StatCard = ({ title, value, subtitle, icon: Icon, color = 'blue', trend }) => (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-100">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className={`text-2xl font-bold text-${color}-600`}>{value}</p>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
          {trend && (
            <div className="flex items-center mt-2">
              <TrendingUp className="w-4 h-4 text-green-500 mr-1" />
              <span className="text-xs text-green-600">{trend}</span>
            </div>
          )}
        </div>
        <div className={`p-3 bg-${color}-100 rounded-full`}>
          <Icon className={`w-6 h-6 text-${color}-600`} />
        </div>
      </div>
    </div>
  );

  const DecisionBreakdown = ({ decisions }) => (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-100">
      <h3 className="text-lg font-semibold text-gray-800 mb-4">Decision Breakdown</h3>
      <div className="space-y-3">
        {Object.entries(decisions || {}).map(([decision, count]) => {
          const getDecisionColor = (dec) => {
            switch (dec) {
              case 'clean': return 'green';
              case 'content_warning': case 'sender_warning': return 'yellow';
              case 'blocked': return 'red';
              default: return 'gray';
            }
          };
          
          const color = getDecisionColor(decision);
          const total = Object.values(decisions).reduce((sum, val) => sum + val, 0);
          const percentage = total > 0 ? (count / total * 100).toFixed(1) : 0;
          
          return (
            <div key={decision} className="flex items-center justify-between">
              <div className="flex items-center">
                <div className={`w-3 h-3 bg-${color}-500 rounded-full mr-3`}></div>
                <span className="text-sm font-medium text-gray-700 capitalize">
                  {decision.replace('_', ' ')}
                </span>
              </div>
              <div className="text-right">
                <span className="text-sm font-bold text-gray-800">{count}</span>
                <span className="text-xs text-gray-500 ml-1">({percentage}%)</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );

  const SystemHealth = ({ health }) => (
    <div className="bg-white rounded-lg shadow-md p-6 border border-gray-100">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-800">System Health</h3>
        <div className={`px-3 py-1 rounded-full text-xs font-medium ${
          health?.status === 'healthy' 
            ? 'bg-green-100 text-green-800' 
            : 'bg-red-100 text-red-800'
        }`}>
          {health?.status || 'Unknown'}
        </div>
      </div>
      
      <div className="space-y-3">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">ML Model</span>
          <span className="text-sm font-medium text-gray-800">
            {health?.ml_model?.type || 'N/A'}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Model Classes</span>
          <span className="text-sm font-medium text-gray-800">
            {health?.ml_model?.classes?.join(', ') || 'N/A'}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Vocabulary Size</span>
          <span className="text-sm font-medium text-gray-800">
            {health?.ml_model?.vocabulary_size?.toLocaleString() || 'N/A'}
          </span>
        </div>
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Phone Database</span>
          <span className="text-sm font-medium text-gray-800">
            {health?.phone_database?.total_records || 0} records
          </span>
        </div>
      </div>
    </div>
  );

  if (loading && !stats) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-4xl mx-auto">
        <div className="flex items-center justify-center h-64">
          <div className="flex items-center gap-3">
            <RefreshCw className="w-6 h-6 animate-spin text-blue-500" />
            <span className="text-gray-600">Loading dashboard...</span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-800">Spam Detection Dashboard</h1>
          <p className="text-sm text-gray-600 mt-1">
            Last updated: {lastRefresh.toLocaleTimeString()}
          </p>
        </div>
        <button
          onClick={fetchData}
          disabled={loading}
          className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
        >
          <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
          Refresh
        </button>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
        <StatCard
          title="Total Messages"
          value={stats?.delivery_performance?.total_deliveries || 0}
          subtitle="Messages processed"
          icon={Activity}
          color="blue"
        />
        <StatCard
          title="Success Rate"
          value={`${(stats?.delivery_performance?.success_rate || 0).toFixed(1)}%`}
          subtitle="Delivery success"
          icon={TrendingUp}
          color="green"
          trend="+2.3% from last hour"
        />
        <StatCard
          title="Blocked Messages"
          value={stats?.delivery_performance?.blocked_messages || 0}
          subtitle="Spam blocked"
          icon={Shield}
          color="red"
        />
        <StatCard
          title="Failed Deliveries"
          value={stats?.delivery_performance?.failed_deliveries || 0}
          subtitle="Technical failures"
          icon={AlertTriangle}
          color="yellow"
        />
      </div>

      {/* Detailed Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <DecisionBreakdown decisions={stats?.message_decisions} />
        <SystemHealth health={health} />
      </div>

      {/* Performance Metrics */}
      <div className="bg-white rounded-lg shadow-md p-6 border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">Performance Metrics</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">
              {stats?.two_party_flow?.average_processing_time_ms?.toFixed(0) || 0}ms
            </div>
            <div className="text-sm text-gray-600">Avg Processing Time</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {stats?.two_party_flow?.total_sender_receiver_pairs || 0}
            </div>
            <div className="text-sm text-gray-600">Unique Sender-Receiver Pairs</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">
              {stats?.delivery_performance?.successful_deliveries || 0}
            </div>
            <div className="text-sm text-gray-600">Successful Deliveries</div>
          </div>
        </div>
      </div>

      {/* System Status */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <div className="w-2 h-2 bg-green-500 rounded-full"></div>
            <span className="text-gray-600">System Status: </span>
            <span className="font-medium text-green-600">
              {health?.status === 'healthy' ? 'All systems operational' : 'Issues detected'}
            </span>
          </div>
          <div className="text-gray-500">
            Two-Party Messaging System v1.0
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpamDashboard; 