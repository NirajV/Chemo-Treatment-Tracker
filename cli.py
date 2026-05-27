#!/usr/bin/env python3
"""
Multi-Agent Pipeline CLI Interface
===================================

User-friendly command-line interface for running the multi-agent pipeline.

Features:
- Interactive project input
- Project templates selection
- Real-time progress display
- Results management
- Result analysis
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

from multi_agent_system import MultiAgentOrchestrator
from agent_utils import (
    InputValidator,
    OutputFormatter,
    ResultAnalyzer,
    ProjectTemplate,
    TEMPLATES,
)


# ============================================================================
# CLI COLORS AND FORMATTING
# ============================================================================

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    @staticmethod
    def disable():
        """Disable colors (for non-terminal output)"""
        Colors.HEADER = ''
        Colors.BLUE = ''
        Colors.CYAN = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.RED = ''
        Colors.ENDC = ''
        Colors.BOLD = ''
        Colors.UNDERLINE = ''


def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(80)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*80}{Colors.ENDC}\n")


def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.ENDC}")


def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}❌ {text}{Colors.ENDC}")


def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ️  {text}{Colors.ENDC}")


def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")


# ============================================================================
# INTERACTIVE INPUT FUNCTIONS
# ============================================================================

def check_api_key() -> bool:
    """
    Check if API key is configured.

    Returns:
        bool: True if API key is set, False otherwise
    """
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        print_error("ANTHROPIC_API_KEY environment variable not set!")
        print_info("Get your API key from: https://console.anthropic.com")
        print_info("Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        return False
    return True


def select_template() -> str:
    """
    Let user select a project template.

    Returns:
        str: Selected template or custom if user provides own description
    """
    print_info("Available project templates:")
    print()

    templates_list = list(TEMPLATES.items())
    for idx, (template_key, template) in enumerate(templates_list, 1):
        print(f"{Colors.CYAN}{idx}. {template['name']}{Colors.ENDC}")
        print(f"   {template['description'].split(chr(10))[0]}")
        print(f"   Time: {template['description'].split('Estimated time: ')[1].split(chr(10))[0]}")
        print()

    print(f"{Colors.CYAN}0. Use custom description{Colors.ENDC}")
    print()

    while True:
        try:
            choice = int(input(f"{Colors.BOLD}Select template (0-{len(templates_list)}): {Colors.ENDC}"))
            if 0 <= choice <= len(templates_list):
                if choice == 0:
                    return "custom"
                return templates_list[choice - 1][0].value
            else:
                print_error(f"Please select a number between 0 and {len(templates_list)}")
        except ValueError:
            print_error("Invalid input. Please enter a number.")


def get_project_input() -> tuple[str, str]:
    """
    Get project name and description from user.

    Returns:
        tuple[str, str]: (project_name, project_description)
    """
    print_header("PROJECT SETUP")

    # Get project name
    while True:
        project_name = input(f"{Colors.BOLD}Project Name: {Colors.ENDC}").strip()
        is_valid, error = InputValidator.validate_project_name(project_name)
        if is_valid:
            break
        print_error(error)

    # Select template or custom
    template_choice = select_template()

    # Get description
    print_info("Enter detailed project description:")
    print_info("(You can paste multiple lines. Type 'END' on a new line when done)")
    print()

    lines = []
    if template_choice != "custom":
        template = TEMPLATES[ProjectTemplate[template_choice.upper()]]
        print(f"Template: {template['name']}")
        print(f"Description preview:\n{template['description'][:200]}...")
        print()
        use_template = input(f"{Colors.BOLD}Use this template? (y/n): {Colors.ENDC}").lower()
        if use_template == 'y':
            project_description = template['description']
        else:
            lines = []
    else:
        lines = []

    if not lines:
        while True:
            line = input()
            if line.upper() == 'END':
                break
            lines.append(line)

        project_description = '\n'.join(lines)

    # Validate description
    is_valid, error = InputValidator.validate_project_description(project_description)
    if not is_valid:
        print_error(error)
        return get_project_input()  # Recursively ask again

    return project_name, project_description


def confirm_execution(project_name: str, description: str) -> bool:
    """
    Confirm pipeline execution before starting.

    Returns:
        bool: True if user confirms, False otherwise
    """
    print_header("EXECUTION CONFIRMATION")

    print(f"Project Name: {Colors.CYAN}{project_name}{Colors.ENDC}")
    print(f"\nDescription:")
    print(f"{description[:500]}{'...' if len(description) > 500 else ''}\n")

    print_warning("This will execute the following stages:")
    print("  1. Task Manager     (Analyze & create task breakdown)")
    print("  2. Developer        (Implement code)")
    print("  3. Tester           (Create tests & validate)")
    print("  4. Deployer         (Create deployment plan)")

    print_info("Estimated execution time: 15-30 minutes")
    print_info("Estimated cost: $0.30-$1.50 (API tokens)")

    while True:
        confirm = input(f"\n{Colors.BOLD}Continue with execution? (yes/no): {Colors.ENDC}").lower()
        if confirm in ['yes', 'y']:
            return True
        elif confirm in ['no', 'n']:
            return False
        else:
            print_error("Please enter 'yes' or 'no'")


# ============================================================================
# PIPELINE EXECUTION
# ============================================================================

def run_pipeline(project_name: str, project_description: str, output_file: str) -> bool:
    """
    Run the multi-agent pipeline.

    Args:
        project_name: Name of the project
        project_description: Project description
        output_file: File to save results

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Create orchestrator
        orchestrator = MultiAgentOrchestrator(
            project_name=project_name,
            project_description=project_description
        )

        # Run pipeline
        results = orchestrator.run_pipeline()

        # Save results
        orchestrator.save_results(output_file)
        print_success(f"Results saved to: {output_file}")

        # Analyze results
        summary = orchestrator.get_summary()
        analyze_results(summary, results)

        return True

    except KeyboardInterrupt:
        print_warning("\nPipeline interrupted by user")
        return False
    except Exception as e:
        print_error(f"Pipeline execution failed: {str(e)}")
        return False


def analyze_results(summary: dict, results: dict):
    """
    Analyze and display pipeline results.

    Args:
        summary: Pipeline summary
        results: Pipeline results
    """
    print_header("RESULTS ANALYSIS")

    # Execution time analysis
    time_analysis = ResultAnalyzer.analyze_execution_time(summary)
    print(f"Total Execution Time: {Colors.CYAN}{time_analysis['total_time']:.2f}s{Colors.ENDC}")
    print(f"Fastest Agent: {Colors.GREEN}{time_analysis['fastest_agent']} ({time_analysis['agent_times'].get(time_analysis['fastest_agent'], 0):.2f}s){Colors.ENDC}")
    print(f"Slowest Agent: {Colors.YELLOW}{time_analysis['slowest_agent']} ({time_analysis['agent_times'].get(time_analysis['slowest_agent'], 0):.2f}s){Colors.ENDC}")

    # Token usage analysis
    print()
    token_analysis = ResultAnalyzer.analyze_token_usage(summary)
    print(f"Total Tokens Used: {Colors.CYAN}{token_analysis['total_tokens']:,}{Colors.ENDC}")
    print(f"Estimated Cost: {Colors.CYAN}${token_analysis['estimated_cost']}{Colors.ENDC}")

    # Completion status
    print()
    completion = ResultAnalyzer.check_completion_status(summary)
    print(f"Completion Rate: {Colors.GREEN}{completion['completion_rate']}%{Colors.ENDC}")
    print(f"Completed Agents: {completion['completed']}/{completion['total_agents']}")
    if completion['failed'] > 0:
        print_warning(f"Failed Agents: {completion['failed']}")

    # Show detailed agent status
    print("\n" + "-" * 80)
    print("Agent Status Details:")
    print("-" * 80)
    for agent_name, status in summary['agents_status'].items():
        status_icon = "✅" if status['status'] == 'completed' else "❌"
        print(
            f"{status_icon} {agent_name:20} | "
            f"Status: {status['status']:10} | "
            f"Time: {status['execution_time']:6.2f}s | "
            f"Tokens: {status['tokens_used']:6}"
        )


# ============================================================================
# RESULTS MANAGEMENT
# ============================================================================

def view_results(output_file: str):
    """
    View saved pipeline results.

    Args:
        output_file: Path to results file
    """
    if not os.path.exists(output_file):
        print_error(f"Results file not found: {output_file}")
        return

    with open(output_file, 'r') as f:
        data = json.load(f)

    print_header("PIPELINE RESULTS")

    metadata = data.get('metadata', {})
    print(f"Project: {Colors.CYAN}{metadata.get('project_name')}{Colors.ENDC}")
    print(f"Status: {Colors.GREEN}{metadata.get('status')}{Colors.ENDC}")
    print(f"Timestamp: {metadata.get('timestamp')}")
    print(f"Duration: {metadata.get('execution_time'):.2f}s")

    print("\n" + "=" * 80)
    results = data.get('detailed_results', {})
    for agent_name, output in results.items():
        print(f"\n--- {Colors.BOLD}{agent_name.upper()}{Colors.ENDC} ---")
        print(output[:1000] + "..." if len(output) > 1000 else output)
        print("-" * 80)


def list_results():
    """List available result files"""
    print_header("AVAILABLE RESULTS")

    json_files = list(Path('.').glob('pipeline_results*.json'))
    if not json_files:
        print_info("No results files found")
        return

    for idx, file in enumerate(sorted(json_files), 1):
        stat = file.stat()
        timestamp = datetime.fromtimestamp(stat.st_mtime)
        print(f"{idx}. {file.name} ({stat.st_size:,} bytes) - {timestamp}")


# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Multi-Agent Autonomous Pipeline System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 cli.py                     # Interactive mode
  python3 cli.py --view              # View latest results
  python3 cli.py --list              # List all results
        """
    )

    parser.add_argument(
        '--view',
        action='store_true',
        help='View latest pipeline results'
    )
    parser.add_argument(
        '--list',
        action='store_true',
        help='List all available results'
    )
    parser.add_argument(
        '--project',
        type=str,
        help='Project name (for non-interactive mode)'
    )
    parser.add_argument(
        '--description',
        type=str,
        help='Project description (for non-interactive mode)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='pipeline_results.json',
        help='Output file for results (default: pipeline_results.json)'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='Disable colored output'
    )

    args = parser.parse_args()

    # Disable colors if requested
    if args.no_color:
        Colors.disable()

    # Print welcome banner
    print_header("MULTI-AGENT PIPELINE SYSTEM")
    print_info("Autonomous development pipeline: Task Manager → Developer → Tester → Deployer")

    # Check API key
    if not check_api_key():
        sys.exit(1)

    # Handle different modes
    if args.view:
        view_results(args.output)
    elif args.list:
        list_results()
    elif args.project and args.description:
        # Non-interactive mode
        print_info("Running in non-interactive mode")
        if run_pipeline(args.project, args.description, args.output):
            print_success("Pipeline execution completed successfully!")
        else:
            sys.exit(1)
    else:
        # Interactive mode
        try:
            project_name, project_description = get_project_input()

            if not confirm_execution(project_name, project_description):
                print_info("Pipeline execution cancelled")
                sys.exit(0)

            if run_pipeline(project_name, project_description, args.output):
                print_success("Pipeline execution completed successfully!")
                print_info(f"Results saved to: {args.output}")
            else:
                sys.exit(1)

        except KeyboardInterrupt:
            print_warning("\nApplication interrupted by user")
            sys.exit(0)
        except Exception as e:
            print_error(f"Application error: {str(e)}")
            sys.exit(1)


if __name__ == "__main__":
    main()
