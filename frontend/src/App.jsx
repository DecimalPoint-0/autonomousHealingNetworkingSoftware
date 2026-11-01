import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area 
} from 'recharts';
import { 
  Activity, Shield, ShieldAlert, Zap, AlertTriangle, RefreshCw, Cpu, HardDrive, Network 
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = "http://localhost:8000";

function App() {
  const [metrics, setMetrics] = useState(null);
  const [history, setHistory] = useState([]);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get(`${API_BASE}/metrics`);
        setMetrics(res.data.current);
        setHistory(res.data.history);
        setLogs(res.data.healing_logs);
        setLoading(false);
      } catch (err) {
        console.error("API Error:", err);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 2000);
    return () => clearInterval(interval);
  }, []);

  const injectFault = async (type) => {
    try {
      await axios.post(`${API_BASE}/inject-fault/${type}`);
    } catch (err) {
      console.error("Error injecting fault:", err);
    }
  };

  const clearFaults = async () => {
    try {
      await axios.post(`${API_BASE}/clear-faults`);
    } catch (err) {
      console.error("Error clearing faults:", err);
    }
  };

  if (loading) return <div className="loading">Initializing Neural Link...</div>;

  const isAnomaly = metrics?.is_anomaly;

  return (
    <div className="dashboard-container">
      <header className="header">
        <div style={{ display: 'flex', alignItems: 'center', gap: '15px' }}>
          <Shield size={32} color="var(--accent-primary)" />
          <h1>AutoHeal AI <span style={{fontSize: '0.8rem', opacity: 0.6}}>v1.0.4</span></h1>
        </div>
        <div className={`status-badge ${isAnomaly ? 'status-anomaly' : 'status-healthy'}`}>
          {isAnomaly ? <ShieldAlert size={18} /> : <Shield size={18} />}
          {isAnomaly ? 'Anomaly Detected' : 'System Healthy'}
        </div>
      </header>

      <div className="grid-layout">
        {/* Real-time Metrics */}
        <div className="card metrics-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
            <h3 className="metric-label">Network Latency & Throughput</h3>
            <Activity size={20} color="var(--accent-primary)" />
          </div>
          <div style={{ height: '300px' }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={history}>
                <defs>
                  <linearGradient id="colorLat" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="var(--accent-primary)" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="var(--accent-primary)" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" />
                <XAxis dataKey="timestamp" hide />
                <YAxis stroke="rgba(0,0,0,0.3)" fontSize={12} />
                <Tooltip 
                  contentStyle={{ background: '#ffffff', border: '1px solid #e2e8f0', borderRadius: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                />
                <Area 
                  type="monotone" 
                  dataKey="latency" 
                  stroke="var(--accent-primary)" 
                  fillOpacity={1} 
                  fill="url(#colorLat)" 
                  strokeWidth={3}
                />
                <Area 
                  type="monotone" 
                  dataKey="packet_loss" 
                  stroke="var(--accent-danger)" 
                  fillOpacity={0.1} 
                  strokeWidth={2}
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px', marginTop: '20px' }}>
            <div className="mini-metric">
              <div className="metric-label">Latency</div>
              <div className="metric-value" style={{ color: metrics.latency > 100 ? 'var(--accent-danger)' : 'var(--accent-primary)' }}>
                {metrics.latency.toFixed(1)} <span style={{fontSize: '1rem'}}>ms</span>
              </div>
            </div>
            <div className="mini-metric">
              <div className="metric-label">Throughput</div>
              <div className="metric-value" style={{ color: metrics.throughput < 500 ? 'var(--accent-warning)' : 'var(--accent-secondary)' }}>
                {metrics.throughput.toFixed(0)} <span style={{fontSize: '1rem'}}>Mbps</span>
              </div>
            </div>
            <div className="mini-metric">
              <div className="metric-label">CPU Load</div>
              <div className="metric-value">
                {metrics.cpu_usage.toFixed(1)} <span style={{fontSize: '1rem'}}>%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Fault Injection Controls */}
        <div className="card controls-card">
          <h3 className="metric-label" style={{ marginBottom: '1.5rem' }}>Simulation Control</h3>
          <button className="fault-btn" onClick={() => injectFault('congestion')}>
            <Network size={18} /> Sim. Link Congestion
          </button>
          <button className="fault-btn" onClick={() => injectFault('ddos')}>
            <Zap size={18} /> Sim. DDoS Attack
          </button>
          <button className="fault-btn" onClick={() => injectFault('hardware_failure')}>
            <HardDrive size={18} /> Sim. Hardware Failure
          </button>
          <button className="fault-btn" onClick={() => injectFault('latency_spike')}>
            <Activity size={18} /> Sim. Latency Spike
          </button>
          <button 
            className="fault-btn" 
            onClick={clearFaults}
            style={{ marginTop: '1rem', background: 'rgba(0, 255, 65, 0.05)', borderColor: 'rgba(0, 255, 65, 0.2)' }}
          >
            <RefreshCw size={18} /> Clear All Faults
          </button>
        </div>

        {/* Healing Logs */}
        <div className="card logs-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <h3 className="metric-label">Autonomous Healing Activity Log</h3>
            <span className="action-badge">AI ACTIVE</span>
          </div>
          <div className="logs-container">
            <AnimatePresence>
              {logs.length === 0 && <div style={{color: 'var(--text-secondary)', padding: '20px', textAlign: 'center'}}>Monitoring for neural events...</div>}
              {logs.map((log, i) => (
                <motion.div 
                  key={log.timestamp}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  className="log-entry"
                >
                  <div>
                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                      {new Date(log.timestamp).toLocaleTimeString()}
                    </div>
                    <div style={{ fontWeight: 600, marginTop: '4px' }}>{log.action}</div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div className="status-badge status-healthy" style={{ fontSize: '0.7rem' }}>
                      RESOLVED
                    </div>
                    <div style={{ fontSize: '0.75rem', marginTop: '4px', opacity: 0.7 }}>
                      Trigger: {log.reason}
                    </div>
                  </div>
                </motion.div>
              )).reverse()}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
