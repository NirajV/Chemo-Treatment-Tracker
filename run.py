#!/usr/bin/env python3
"""
Quick Start Runner Script
=========================

Simple script to run the multi-agent pipeline without configuration.
"""

import os
import sys
from multi_agent_system import MultiAgentOrchestrator


def main():
    """Main runner function"""
    print("\n" + "=" * 80)
    print("🚀 MULTI-AGENT PIPELINE - QUICK START".center(80))
    print("=" * 80)

    # Check API key
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print("\n❌ ERROR: ANTHROPIC_API_KEY environment variable not set!")
        print("\nSet it with:")
        print("  export ANTHROPIC_API_KEY='sk-ant-...'")
        print("\nGet your API key from: https://console.anthropic.com")
        sys.exit(1)

    print("\n✅ API key found")

    # Get project details
    print("\n" + "-" * 80)
    print("PROJECT INFORMATION")
    print("-" * 80)

    project_name = input("\n📝 Project Name: ").strip()
    if not project_name:
        project_name = "My Project"

    print("\n📝 Project Description:")
    print("(Enter your description. Type 'END' when done)")
    lines = []
    while True:
        line = input()
        if line.upper() == 'END':
            break
        lines.append(line)

    project_description = '\n'.join(lines)
    if not project_description:
        project_description = "Build a REST API with authentication, database, and testing"

    # Confirm
    print("\n" + "-" * 80)
    print("CONFIRMATION")
    print("-" * 80)
    print(f"\nProject: {project_name}")
    print(f"Description: {project_description[:100]}...")
    confirm = input("\nProceed with execution? (yes/no): ").lower()

    if confirm not in ['yes', 'y']:
        print("\n❌ Execution cancelled")
        sys.exit(0)

    # Run pipeline
    print("\n" + "=" * 80)
    orchestrator = MultiAgentOrchestrator(
        project_name=project_name,
        project_description=project_description
    )

    try:
        results = orchestrator.run_pipeline()
        orchestrator.save_results()
        print("\n✅ Pipeline completed successfully!")
        print(f"📁 Results saved to: pipeline_results.json")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
