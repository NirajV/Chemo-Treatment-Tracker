import React, { useState, useEffect } from 'react';
import { Play, Pause, RotateCcw, Zap, CheckCircle, AlertCircle, Clock } from 'lucide-react';

export default function MultiAgentDashboard() {
  const [pipelineRunning, setPipelineRunning] = useState(false);
  const [projectName, setProjectName] = useState('E-Commerce Platform API');
  const [projectDesc, setProjectDesc] = useState('Build a REST API with user auth, product catalog, shopping cart, orders, payments, and admin dashboard');
  
  const [agents, setAgents] = useState({
    task_manager: {
      name: 'Task Manager',
      status: 'idle',
      progress: 0,
      duration: 0,
      icon: '📋',
      output: '',
      startTime: null
    },
    developer: {
      name: 'Developer',
      status: 'idle',
      progress: 0,
      duration: 0,
      icon: '💻',
      output: '',
      startTime: null
    },
    tester: {
      name: 'QA Tester',
      status: 'idle',
      progress: 0,
      duration: 0,
      icon: '🧪',
      output: '',
      startTime: null
    },
    deployer: {
      name: 'Deployer',
      status: 'idle',
      progress: 0,
      duration: 0,
      icon: '🚀',
      output: '',
      startTime: null
    }
  });

  const agentSequence = ['task_manager', 'developer', 'tester', 'deployer'];

  const simulateAgentExecution = async (agentKey) => {
    const agentData = agents[agentKey];
    const agent = { ...agentData };
    
    // Start execution
    agent.status = 'working';
    agent.progress = 0;
    agent.startTime = Date.now();
    
    setAgents(prev => ({ ...prev, [agentKey]: agent }));

    // Simulate work
    const duration = 4000 + Math.random() * 3000; // 4-7 seconds
    const startTime = Date.now();

    const simulateProgress = setInterval(() => {
      const elapsed = Date.now() - startTime;
      const progress = Math.min((elapsed / duration) * 100, 99);
      
      setAgents(prev => ({
        ...prev,
        [agentKey]: {
          ...prev[agentKey],
          progress: Math.round(progress)
        }
      }));

      if (elapsed >= duration) {
        clearInterval(simulateProgress);
      }
    }, 100);

    // Wait for "execution" to complete
    await new Promise(resolve => setTimeout(resolve, duration));

    // Complete
    const outputs = {
      task_manager: `✓ Task breakdown created\n✓ 8 main tasks identified\n✓ Dependencies mapped\n✓ Priority levels assigned\n\nKey Tasks:\n1. API Setup & Architecture\n2. User Authentication\n3. Product Management\n4. Cart System\n5. Order Processing\n6. Payment Integration\n7. Admin Dashboard\n8. Testing & Deployment`,
      developer: `✓ Code implementation complete\n✓ 1,240 lines of code\n✓ 8 modules created\n✓ All APIs documented\n✓ Error handling implemented\n\nDeliverables:\n- /src/auth/jwt-handler.ts\n- /src/products/catalog.ts\n- /src/cart/cart-manager.ts\n- /src/orders/processor.ts\n- /src/payments/stripe.ts\n- /src/admin/dashboard.ts\n- /src/utils/database.ts\n- /src/middleware/auth.ts`,
      tester: `✓ Test suite created\n✓ 87 test cases passed\n✓ 3 bugs identified\n✓ 92% code coverage\n✓ Performance: PASS\n\nTest Results:\n- Unit Tests: 45/45 ✓\n- Integration Tests: 28/28 ✓\n- Edge Cases: 14/14 ✓\n\nMinor Issues Found:\n1. Cart discount calculation edge case\n2. Payment timeout handling\n3. Admin role validation\n\nGO/NO-GO: ✓ GO FOR DEPLOYMENT`,
      deployer: `✓ Deployment plan ready\n✓ Infrastructure prepared\n✓ Rollback procedures set\n✓ Monitoring configured\n✓ Documentation complete\n\nDeployment Steps:\n1. Build Docker image\n2. Push to registry\n3. Update Kubernetes manifests\n4. Deploy to staging\n5. Run smoke tests\n6. Deploy to production\n7. Enable canary traffic\n8. Monitor for 24 hours\n\nEstimated Deployment Time: 45 minutes\nMonitoring: Active\nRollback Ready: Yes`
    };

    const finalAgent = {
      ...agent,
      status: 'completed',
      progress: 100,
      duration: (Date.now() - startTime) / 1000,
      output: outputs[agentKey] || ''
    };

    setAgents(prev => ({ ...prev, [agentKey]: finalAgent }));
  };

  const startPipeline = async () => {
    setPipelineRunning(true);
    
    // Execute agents sequentially
    for (const agentKey of agentSequence) {
      await simulateAgentExecution(agentKey);
      // Small delay between agents
      await new Promise(resolve => setTimeout(resolve, 500));
    }
    
    setPipelineRunning(false);
  };

  const resetPipeline = () => {
    setAgents(prev => 
      Object.keys(prev).reduce((acc, key) => ({
        ...acc,
        [key]: {
          ...prev[key],
          status: 'idle',
          progress: 0,
          duration: 0,
          output: ''
        }
      }), {})
    );
    setPipelineRunning(false);
  };

  const getStatusIcon = (status) => {
    switch(status) {
      case 'idle': return '⭕';
      case 'working': return '🔄';
      case 'completed': return '✅';
      case 'failed': return '❌';
      default: return '⭕';
    }
  };

  const getStatusColor = (status) => {
    switch(status) {
      case 'idle': return 'from-gray-400 to-gray-500';
      case 'working': return 'from-blue-400 to-cyan-500';
      case 'completed': return 'from-emerald-400 to-green-500';
      case 'failed': return 'from-red-400 to-rose-500';
      default: return 'from-gray-400 to-gray-500';
    }
  };

  const completedCount = Object.values(agents).filter(a => a.status === 'completed').length;
  const totalAgents = Object.keys(agents).length;
  const pipelineProgress = (completedCount / totalAgents) * 100;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 p-6 font-sans">
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Outfit:wght@300;400;600;700&display=swap');
        
        .terminal-font { font-family: 'Space Mono', monospace; }
        .display-font { font-family: 'Outfit', sans-serif; }
        
        @keyframes pulse-ring {
          0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.7); }
          70% { box-shadow: 0 0 0 10px rgba(59, 130, 246, 0); }
          100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
        }
        
        .pulse-ring { animation: pulse-ring 2s infinite; }
        
        @keyframes slide-up {
          from { opacity: 0; transform: translateY(20px); }
          to { opacity: 1; transform: translateY(0); }
        }
        
        .slide-up { animation: slide-up 0.6s ease-out; }
        
        @keyframes flow {
          0%, 100% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
        }
        
        .gradient-flow { animation: flow 3s ease infinite; background-size: 200% 200%; }
      `}</style>

      {/* Header */}
      <div className="max-w-7xl mx-auto mb-8">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h1 className="display-font text-4xl font-bold text-white mb-2">Multi-Agent Pipeline</h1>
            <p className="text-slate-400">Autonomous task execution: Manager → Developer → Tester → Deployer</p>
          </div>
          <div className="text-right">
            <div className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-500">
              {completedCount}/{totalAgents}
            </div>
            <p className="text-slate-400 text-sm">Stages Completed</p>
          </div>
        </div>

        {/* Project Input */}
        <div className="bg-slate-800/40 backdrop-blur border border-slate-700 rounded-lg p-4 mb-6">
          <div className="grid grid-cols-2 gap-4 mb-4">
            <input
              type="text"
              placeholder="Project Name"
              value={projectName}
              onChange={(e) => setProjectName(e.target.value)}
              disabled={pipelineRunning}
              className="terminal-font bg-slate-900 border border-slate-600 text-white px-3 py-2 rounded text-sm"
            />
            <input
              type="text"
              placeholder="Project Description"
              value={projectDesc}
              onChange={(e) => setProjectDesc(e.target.value)}
              disabled={pipelineRunning}
              className="terminal-font bg-slate-900 border border-slate-600 text-white px-3 py-2 rounded text-sm col-span-2"
            />
          </div>

          {/* Control Buttons */}
          <div className="flex gap-3">
            <button
              onClick={startPipeline}
              disabled={pipelineRunning}
              className="display-font flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-500 to-blue-500 hover:from-cyan-600 hover:to-blue-600 disabled:opacity-50 text-white rounded font-semibold transition-all"
            >
              <Zap size={18} /> Start Pipeline
            </button>
            <button
              onClick={resetPipeline}
              disabled={pipelineRunning}
              className="display-font flex items-center gap-2 px-4 py-2 bg-slate-700 hover:bg-slate-600 disabled:opacity-50 text-white rounded font-semibold transition-all"
            >
              <RotateCcw size={18} /> Reset
            </button>
          </div>
        </div>

        {/* Overall Progress */}
        <div className="bg-slate-800/40 backdrop-blur border border-slate-700 rounded-lg p-4">
          <div className="flex items-center justify-between mb-2">
            <span className="display-font text-sm font-semibold text-slate-300">Pipeline Progress</span>
            <span className="terminal-font text-sm text-cyan-400">{Math.round(pipelineProgress)}%</span>
          </div>
          <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-cyan-400 via-blue-400 to-purple-500 gradient-flow transition-all duration-300"
              style={{ width: `${pipelineProgress}%` }}
            />
          </div>
        </div>
      </div>

      {/* Agent Cards Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-6">
        {agentSequence.map((agentKey, idx) => {
          const agent = agents[agentKey];
          return (
            <div
              key={agentKey}
              className="slide-up group"
              style={{ animationDelay: `${idx * 100}ms` }}
            >
              {/* Card */}
              <div className="relative h-full">
                {/* Glowing background */}
                {agent.status === 'working' && (
                  <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-blue-500/20 rounded-lg blur-lg group-hover:blur-xl transition-all" />
                )}

                {/* Main card */}
                <div className={`relative bg-slate-800/60 backdrop-blur border rounded-lg p-6 transition-all ${
                  agent.status === 'completed' ? 'border-emerald-500/50' :
                  agent.status === 'working' ? 'border-cyan-500/50' :
                  'border-slate-600'
                }`}>
                  {/* Header */}
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <div className="text-4xl">{agent.icon}</div>
                      <div>
                        <h3 className="display-font text-lg font-bold text-white">{agent.name}</h3>
                        <p className="terminal-font text-xs text-slate-400">Stage {idx + 1}/4</p>
                      </div>
                    </div>
                    <div className="text-2xl">{getStatusIcon(agent.status)}</div>
                  </div>

                  {/* Status & Progress */}
                  <div className="space-y-3 mb-4">
                    <div className="flex items-center justify-between">
                      <span className="display-font text-sm text-slate-300">Status</span>
                      <span className={`terminal-font text-sm font-semibold uppercase tracking-wide ${
                        agent.status === 'idle' ? 'text-slate-400' :
                        agent.status === 'working' ? 'text-cyan-400' :
                        agent.status === 'completed' ? 'text-emerald-400' :
                        'text-red-400'
                      }`}>
                        {agent.status}
                      </span>
                    </div>

                    {(agent.status === 'working' || agent.status === 'completed') && (
                      <>
                        <div className="space-y-1">
                          <div className="flex items-center justify-between">
                            <span className="display-font text-xs text-slate-400">Progress</span>
                            <span className="terminal-font text-xs text-cyan-400">{agent.progress}%</span>
                          </div>
                          <div className="w-full h-1.5 bg-slate-700 rounded-full overflow-hidden">
                            <div
                              className={`h-full bg-gradient-to-r ${getStatusColor(agent.status)} transition-all duration-200`}
                              style={{ width: `${agent.progress}%` }}
                            />
                          </div>
                        </div>

                        <div className="flex items-center gap-2 text-slate-400">
                          <Clock size={14} />
                          <span className="terminal-font text-xs">{agent.duration.toFixed(2)}s</span>
                        </div>
                      </>
                    )}
                  </div>

                  {/* Output Panel */}
                  {agent.output && (
                    <div className="bg-slate-900/80 border border-slate-700 rounded p-3 max-h-48 overflow-y-auto">
                      <p className="terminal-font text-xs text-slate-300 whitespace-pre-wrap break-words">
                        {agent.output}
                      </p>
                    </div>
                  )}

                  {/* Arrow to next agent */}
                  {idx < agentSequence.length - 1 && (
                    <div className="absolute -right-3 top-1/2 -translate-y-1/2 hidden md:block">
                      <div className="text-2xl text-slate-600">→</div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Status Legend */}
      <div className="max-w-7xl mx-auto mt-8 p-4 bg-slate-800/40 backdrop-blur border border-slate-700 rounded-lg">
        <p className="display-font text-xs font-semibold text-slate-400 mb-3">STATUS LEGEND</p>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="flex items-center gap-2">
            <span className="text-lg">⭕</span>
            <span className="terminal-font text-xs text-slate-400">Idle - Waiting</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg">🔄</span>
            <span className="terminal-font text-xs text-cyan-400">Working - In Progress</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg">✅</span>
            <span className="terminal-font text-xs text-emerald-400">Completed - Done</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-lg">❌</span>
            <span className="terminal-font text-xs text-red-400">Failed - Error</span>
          </div>
        </div>
      </div>
    </div>
  );
}