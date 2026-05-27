"""
Multi-Agent System Utilities
=============================

Helper functions, validators, and utilities for the multi-agent pipeline system.

Includes:
- Project template definitions
- Input validation functions
- Output formatting utilities
- Result analysis tools
- Configuration helpers
"""

import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum


# ============================================================================
# PROJECT TEMPLATES
# ============================================================================

class ProjectTemplate(Enum):
    """Pre-built project templates for quick start"""
    SIMPLE_API = "simple_api"
    WEB_APP = "web_app"
    MICROSERVICES = "microservices"
    DATA_PIPELINE = "data_pipeline"
    MOBILE_BACKEND = "mobile_backend"


TEMPLATES = {
    ProjectTemplate.SIMPLE_API: {
        "name": "Simple REST API",
        "description": """Build a REST API with:
- User authentication (JWT)
- CRUD operations for main resource
- Error handling and validation
- Database integration
- API documentation

Perfect for: Getting started, learning, MVPs
Estimated time: 8-12 minutes
Complexity: Low""",
    },
    ProjectTemplate.WEB_APP: {
        "name": "Full-Stack Web Application",
        "description": """Build a complete web application with:
- Frontend (React/Vue/HTML)
- Backend API (Node.js/Python)
- Database design
- User authentication
- Real-time features
- Responsive design

Perfect for: Complete applications, SaaS products
Estimated time: 15-20 minutes
Complexity: Medium""",
    },
    ProjectTemplate.MICROSERVICES: {
        "name": "Microservices Architecture",
        "description": """Design and implement microservices with:
- Multiple independent services
- API Gateway pattern
- Service-to-service communication
- Message queues
- Service discovery
- Kubernetes orchestration

Perfect for: Scalable systems, enterprise applications
Estimated time: 25-30 minutes
Complexity: High""",
    },
    ProjectTemplate.DATA_PIPELINE: {
        "name": "Data Processing Pipeline",
        "description": """Build a data pipeline with:
- Data extraction from sources
- Transformation and cleaning
- Data validation and quality checks
- Loading to warehouse
- Monitoring and alerting
- Error handling

Perfect for: Analytics, data engineering, ETL
Estimated time: 15-20 minutes
Complexity: Medium""",
    },
    ProjectTemplate.MOBILE_BACKEND: {
        "name": "Mobile App Backend",
        "description": """Build a backend for mobile apps with:
- REST or GraphQL API
- Real-time features (WebSocket)
- Push notifications
- File upload handling
- Offline support
- Analytics integration

Perfect for: Mobile applications, real-time apps
Estimated time: 18-25 minutes
Complexity: Medium-High""",
    },
}


# ============================================================================
# VALIDATION AND FORMATTING
# ============================================================================

class InputValidator:
    """Validates user inputs and project specifications"""

    @staticmethod
    def validate_project_name(name: str) -> Tuple[bool, str]:
        """
        Validate project name.

        Args:
            name: Project name to validate

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not name or len(name) < 3:
            return False, "Project name must be at least 3 characters"
        if len(name) > 100:
            return False, "Project name must not exceed 100 characters"
        if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
            return False, "Project name can only contain letters, numbers, spaces, hyphens, and underscores"
        return True, ""

    @staticmethod
    def validate_project_description(description: str) -> Tuple[bool, str]:
        """
        Validate project description.

        Args:
            description: Project description to validate

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not description or len(description) < 20:
            return False, "Description must be at least 20 characters"
        if len(description) > 5000:
            return False, "Description must not exceed 5000 characters"
        return True, ""

    @staticmethod
    def validate_project(name: str, description: str) -> Tuple[bool, str]:
        """
        Validate complete project specification.

        Args:
            name: Project name
            description: Project description

        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        is_valid, error = InputValidator.validate_project_name(name)
        if not is_valid:
            return False, error

        is_valid, error = InputValidator.validate_project_description(description)
        if not is_valid:
            return False, error

        return True, ""


class OutputFormatter:
    """Formats and structures output from agents"""

    @staticmethod
    def truncate_text(text: str, max_length: int = 500) -> str:
        """
        Truncate text to specified length.

        Args:
            text: Text to truncate
            max_length: Maximum length

        Returns:
            str: Truncated text with ellipsis if needed
        """
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."

    @staticmethod
    def extract_json_from_text(text: str) -> Optional[Dict]:
        """
        Extract JSON object from text.

        Args:
            text: Text potentially containing JSON

        Returns:
            Optional[Dict]: Extracted JSON object or None
        """
        try:
            # Try to find JSON object in text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except (json.JSONDecodeError, AttributeError):
            pass
        return None

    @staticmethod
    def extract_task_list(text: str) -> List[Dict[str, str]]:
        """
        Extract task list from Task Manager output.

        Args:
            text: Task Manager output text

        Returns:
            List[Dict]: List of extracted tasks
        """
        tasks = []
        # This is a simple extraction; in production, use more sophisticated parsing
        lines = text.split('\n')
        for line in lines:
            if line.strip() and re.match(r'^[T\-]?\d+\.?\s+', line):
                tasks.append({'description': line.strip()})
        return tasks

    @staticmethod
    def format_json_output(data: Any, indent: int = 2) -> str:
        """
        Format data as pretty JSON.

        Args:
            data: Data to format
            indent: Indentation level

        Returns:
            str: Formatted JSON string
        """
        return json.dumps(data, indent=indent, ensure_ascii=False)


# ============================================================================
# RESULT ANALYSIS
# ============================================================================

class ResultAnalyzer:
    """Analyzes pipeline results and provides insights"""

    @staticmethod
    def analyze_execution_time(summary: Dict) -> Dict[str, Any]:
        """
        Analyze execution time metrics.

        Args:
            summary: Pipeline summary

        Returns:
            Dict: Execution time analysis
        """
        agent_times = {}
        total_time = 0

        for agent_name, status in summary['agents_status'].items():
            exec_time = status['execution_time']
            agent_times[agent_name] = exec_time
            total_time += exec_time

        return {
            'total_time': total_time,
            'agent_times': agent_times,
            'average_time': total_time / len(agent_times) if agent_times else 0,
            'slowest_agent': max(agent_times, key=agent_times.get) if agent_times else None,
            'fastest_agent': min(agent_times, key=agent_times.get) if agent_times else None,
        }

    @staticmethod
    def analyze_token_usage(summary: Dict) -> Dict[str, Any]:
        """
        Analyze token usage across agents.

        Args:
            summary: Pipeline summary

        Returns:
            Dict: Token usage analysis
        """
        token_usage = {}
        total_tokens = 0

        for agent_name, status in summary['agents_status'].items():
            tokens = status.get('tokens_used', 0)
            token_usage[agent_name] = tokens
            total_tokens += tokens

        return {
            'total_tokens': total_tokens,
            'agent_tokens': token_usage,
            'average_tokens': total_tokens / len(token_usage) if token_usage else 0,
            'estimated_cost': round((total_tokens / 1000) * 0.003, 2),  # Rough estimate
        }

    @staticmethod
    def check_completion_status(summary: Dict) -> Dict[str, Any]:
        """
        Check pipeline completion status.

        Args:
            summary: Pipeline summary

        Returns:
            Dict: Completion status analysis
        """
        total_agents = len(summary['agents_status'])
        completed = sum(
            1 for status in summary['agents_status'].values()
            if status['status'] == 'completed'
        )
        failed = sum(
            1 for status in summary['agents_status'].values()
            if status['status'] == 'failed'
        )

        return {
            'total_agents': total_agents,
            'completed': completed,
            'failed': failed,
            'completion_rate': round((completed / total_agents) * 100, 1),
            'success': summary['status'] == 'completed' and failed == 0,
        }


# ============================================================================
# CONFIGURATION HELPERS
# ============================================================================

@dataclass
class AgentConfig:
    """Configuration for agent customization"""
    role: str
    temperature: float = 0.7
    max_tokens: int = 4096
    model: str = "claude-opus-4-20250805"
    custom_prompt: Optional[str] = None
    custom_instructions: Optional[str] = None


class ConfigBuilder:
    """Builder for creating agent configurations"""

    def __init__(self):
        self.config = {
            "api": {
                "model": "claude-opus-4-20250805",
                "max_tokens": 4096,
                "temperature": 0.7,
                "timeout": 120,
            },
            "agents": {
                "task_manager": {},
                "developer": {},
                "tester": {},
                "deployer": {},
            },
            "quality": {
                "code_coverage_minimum": 80,
                "max_issues_allowed": 5,
                "performance_timeout_ms": 5000,
            },
            "execution": {
                "sequential": True,
                "max_retries": 3,
                "retry_delay": 2,
            },
        }

    def set_model(self, model: str) -> 'ConfigBuilder':
        """Set the model to use"""
        self.config["api"]["model"] = model
        return self

    def set_max_tokens(self, tokens: int) -> 'ConfigBuilder':
        """Set maximum tokens per request"""
        self.config["api"]["max_tokens"] = tokens
        return self

    def set_agent_config(self, agent: str, **kwargs) -> 'ConfigBuilder':
        """Set configuration for a specific agent"""
        if agent in self.config["agents"]:
            self.config["agents"][agent].update(kwargs)
        return self

    def set_quality_standards(self, **kwargs) -> 'ConfigBuilder':
        """Set quality standards"""
        self.config["quality"].update(kwargs)
        return self

    def build(self) -> Dict:
        """Build the configuration"""
        return self.config


# ============================================================================
# REPORTING UTILITIES
# ============================================================================

class ReportGenerator:
    """Generates formatted reports from pipeline results"""

    @staticmethod
    def generate_text_report(project_name: str, summary: Dict, results: Dict) -> str:
        """
        Generate a text report of pipeline execution.

        Args:
            project_name: Name of the project
            summary: Pipeline summary
            results: Pipeline results

        Returns:
            str: Formatted text report
        """
        report = []
        report.append("=" * 80)
        report.append(f"MULTI-AGENT PIPELINE EXECUTION REPORT")
        report.append("=" * 80)
        report.append(f"\nProject: {project_name}")
        report.append(f"Status: {summary['status'].upper()}")
        report.append(f"Total Duration: {summary['total_duration_seconds']:.2f} seconds")
        report.append(f"\nAgent Execution Summary:")
        report.append("-" * 80)

        for agent_name, status in summary['agents_status'].items():
            report.append(
                f"{agent_name:20} | Status: {status['status']:10} | "
                f"Time: {status['execution_time']:6.2f}s | "
                f"Tokens: {status['tokens_used']:6}"
            )

        report.append("\n" + "=" * 80)
        report.append("Generated Reports:")
        report.append("=" * 80)

        for agent_name, output in results.items():
            report.append(f"\n\n--- {agent_name.upper()} OUTPUT ---")
            report.append(output[:1000] + "..." if len(output) > 1000 else output)

        return "\n".join(report)

    @staticmethod
    def generate_json_report(project_name: str, summary: Dict, results: Dict) -> str:
        """
        Generate a JSON report of pipeline execution.

        Args:
            project_name: Name of the project
            summary: Pipeline summary
            results: Pipeline results

        Returns:
            str: Formatted JSON report
        """
        report = {
            "project": project_name,
            "summary": summary,
            "results": results,
        }
        return json.dumps(report, indent=2)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: Validate project
    is_valid, error = InputValidator.validate_project(
        "E-Commerce API",
        "Build a REST API for e-commerce with authentication, products, orders, and payments"
    )
    print(f"Validation Result: {is_valid}")
    if error:
        print(f"Error: {error}")

    # Example: Get template
    template = TEMPLATES[ProjectTemplate.SIMPLE_API]
    print(f"\nTemplate: {template['name']}")
    print(f"Description: {template['description']}")

    # Example: Build configuration
    config = ConfigBuilder()
    config.set_max_tokens(2048)
    config.set_quality_standards(code_coverage_minimum=90)
    final_config = config.build()
    print(f"\nConfiguration: {json.dumps(final_config, indent=2)}")

    # Example: Extract and format
    sample_text = "Task 1: Setup database\nTask 2: Create API endpoints"
    tasks = OutputFormatter.extract_task_list(sample_text)
    print(f"\nExtracted Tasks: {tasks}")
