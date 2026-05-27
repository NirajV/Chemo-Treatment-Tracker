#!/usr/bin/env python3
"""
Quick Start Script for Multi-Agent Pipeline
Run your first automated project pipeline in seconds!
"""

import os
import sys
import json
from datetime import datetime

# Try to import required modules
try:
    import anthropic
except ImportError:
    print("❌ anthropic module not found")
    print("Install with: pip install anthropic")
    sys.exit(1)

from multi_agent_system import MultiAgentOrchestrator

def print_banner():
    """Print welcome banner"""
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                   MULTI-AGENT PIPELINE SYSTEM                      ║
║                  Autonomous Development Pipeline                    ║
║           Task Manager → Developer → Tester → Deployer              ║
╚════════════════════════════════════════════════════════════════════╝
    """)

def get_user_input():
    """Get project details from user"""
    print("\n📋 PROJECT SETUP")
    print("─" * 60)
    
    print("\nEnter your project details:")
    project_name = input("🏷️  Project Name: ").strip() or "Sample Project"
    project_desc = input("📝 Project Description: ").strip() or "A sample project"
    
    return project_name, project_desc

def save_results(orchestrator, output_file):
    """Save pipeline results to file"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "project": {
            "name": orchestrator.project_name,
            "description": orchestrator.project_description
        },
        "pipeline_status": orchestrator.pipeline_status,
        "agents": {}
    }
    
    for role, agent in orchestrator.agents.items():
        results["agents"][role.value] = {
            "status": agent.state.status,
            "execution_time": agent.state.execution_time,
            "error": agent.state.error,
            "output_length": len(agent.state.output)
        }
    
    results["detailed_outputs"] = orchestrator.results
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return output_file

def print_summary(orchestrator):
    """Print pipeline execution summary"""
    print("\n" + "=" * 70)
    print("PIPELINE EXECUTION SUMMARY")
    print("=" * 70)
    
    summary = orchestrator.get_summary()
    
    print(f"\n📊 OVERVIEW")
    print(f"Project: {summary['project_name']}")
    print(f"Status: {summary['pipeline_status'].upper()}")
    print(f"Results Collected: {summary['total_results']}/4")
    
    print(f"\n🔍 AGENT STATUS BREAKDOWN")
    for agent_name, status in summary['agents_status'].items():
        status_emoji = "✅" if status['status'] == 'completed' else "❌" if status['status'] == 'failed' else "⭕"
        print(f"{status_emoji} {agent_name.replace('_', ' ').title():20} | Status: {status['status']:10} | Time: {status['execution_time']:.2f}s")
    
    print("\n" + "=" * 70)

def main():
    """Main execution"""
    print_banner()
    
    # Check API key
    if not os.getenv('ANTHROPIC_API_KEY'):
        print("⚠️  WARNING: ANTHROPIC_API_KEY not set")
        print("Set it with: export ANTHROPIC_API_KEY='your-key-here'")
        print("\nYou can continue, but the pipeline will fail without a valid API key.\n")
        response = input("Continue? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
    
    # Get project details
    project_name, project_desc = get_user_input()
    
    # Create orchestrator
    print("\n🚀 STARTING PIPELINE...")
    print("─" * 60)
    
    orchestrator = MultiAgentOrchestrator(
        project_name=project_name,
        project_description=project_desc
    )
    
    try:
        # Run pipeline
        results = orchestrator.run_pipeline()
        
        # Print summary
        print_summary(orchestrator)
        
        # Save results
        output_file = "pipeline_results.json"
        save_results(orchestrator, output_file)
        print(f"\n📁 Results saved to: {output_file}")
        
        # Offer to display outputs
        print("\n" + "=" * 70)
        print("DETAILED OUTPUTS AVAILABLE")
        print("=" * 70)
        
        for agent_name, output in results.items():
            preview = output[:150] + "..." if len(output) > 150 else output
            print(f"\n📋 {agent_name.upper()}")
            print("─" * 60)
            print(preview)
            print()
        
        print("\n✅ Pipeline completed successfully!")
        print("Check 'pipeline_results.json' for full details.")
        
    except Exception as e:
        print(f"\n❌ Pipeline failed with error:")
        print(f"{str(e)}")
        print("\nTroubleshooting:")
        print("1. Check your ANTHROPIC_API_KEY is set correctly")
        print("2. Verify you have API quota available")
        print("3. Check your internet connection")
        print("4. Try with a simpler project description")
        sys.exit(1)

if __name__ == "__main__":
    main()
