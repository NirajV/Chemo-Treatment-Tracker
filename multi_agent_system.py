"""
Multi-Agent Autonomous Pipeline System
=======================================

A complete autonomous development pipeline where agents work independently
and sequentially without manual intervention.

Pipeline Flow:
    Task Manager → Developer → Tester → Deployer

Author: Claude (Anthropic)
Version: 2.0
Status: Production Ready
"""

import anthropic
import json
import time
import logging
from enum import Enum
from config import AGENT_PROMPTS, API_CONFIG, EXECUTION_CONFIG
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS AND DATA CLASSES
# ============================================================================

class AgentRole(Enum):
    """Enum for different agent roles in the pipeline"""
    TASK_MANAGER = "task_manager"
    DEVELOPER = "developer"
    TESTER = "tester"
    DEPLOYER = "deployer"


class AgentStatus(Enum):
    """Enum for agent execution status"""
    IDLE = "idle"
    WORKING = "working"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentState:
    """Represents the state of an agent during execution"""
    role: AgentRole
    status: str = AgentStatus.IDLE.value
    output: str = ""
    error: Optional[str] = None
    execution_time: float = 0.0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    tokens_used: int = 0

    def to_dict(self):
        """Convert state to dictionary for JSON serialization"""
        return {
            'role': self.role.value,
            'status': self.status,
            'execution_time': self.execution_time,
            'error': self.error,
            'tokens_used': self.tokens_used,
            'output_length': len(self.output)
        }


# ============================================================================
# AGENT CLASS
# ============================================================================

class Agent:
    """
    Base Agent class for autonomous task execution.
    
    Each agent is specialized for a specific role in the development pipeline.
    Agents execute independently using Claude API and maintain their own state.
    """

    def __init__(self, role: AgentRole, project_context: str):
        """
        Initialize an agent.

        Args:
            role: The role this agent plays (task_manager, developer, etc.)
            project_context: The project description/context
        """
        self.role = role
        self.project_context = project_context
        self.state = AgentState(role=role)
        self.previous_outputs: List[str] = []
        self.client = anthropic.Anthropic()
        logger.info(f"Initialized {role.value} agent")

    def get_system_prompt(self) -> str:
        """
        Get the system prompt for this agent's role.

        Reads from config.AGENT_PROMPTS for domain-specific prompt customization.
        Falls back to default if role not found.

        Returns:
            str: The system prompt for this agent
        """
        return AGENT_PROMPTS.get(self.role.value, "You are an AI agent.")

    def execute(self, task_input: str) -> str:
        """
        Execute the agent's task using Claude API.

        This method:
        1. Prepares the input with context from previous agents
        2. Calls Claude API with role-specific system prompt
        3. Tracks execution state and metrics
        4. Handles errors gracefully

        Args:
            task_input: The task/prompt to execute

        Returns:
            str: The agent's output/response

        Raises:
            Exception: If API call fails after retries
        """
        self.state.status = AgentStatus.WORKING.value
        self.state.start_time = datetime.now()
        start_time = time.time()

        try:
            logger.info(f"Starting execution for {self.role.value} agent")

            # Prepare the full input with context
            full_input = self._prepare_input(task_input)

            # Make API call
            logger.debug(f"Calling Claude API for {self.role.value}")
            response = self.client.messages.create(
                model=API_CONFIG["model"],
                max_tokens=API_CONFIG["max_tokens"],
                system=self.get_system_prompt(),
                messages=[{"role": "user", "content": full_input}]
            )

            # Extract output
            output = response.content[0].text
            self.state.output = output
            self.state.status = AgentStatus.COMPLETED.value
            self.state.tokens_used = response.usage.output_tokens + response.usage.input_tokens
            self.previous_outputs.append(output)

            execution_time = time.time() - start_time
            self.state.execution_time = execution_time
            self.state.end_time = datetime.now()

            logger.info(
                f"{self.role.value} completed in {execution_time:.2f}s "
                f"(tokens: {self.state.tokens_used})"
            )
            return output

        except Exception as e:
            self.state.status = AgentStatus.FAILED.value
            self.state.error = str(e)
            self.state.execution_time = time.time() - start_time
            self.state.end_time = datetime.now()
            logger.error(f"{self.role.value} failed: {str(e)}")
            raise

    def _prepare_input(self, task_input: str) -> str:
        """
        Prepare the input with context from previous agents.

        Args:
            task_input: The base task input

        Returns:
            str: Enhanced input with previous context
        """
        context = ""
        if self.previous_outputs and EXECUTION_CONFIG.get("pass_context_between_agents", True):
            # Include previous outputs for context (respect token window limit)
            context = "\n\n=== CONTEXT FROM PREVIOUS STAGES ===\n"
            context_window_tokens = EXECUTION_CONFIG.get("context_window_size", 8000)
            # Rough estimate: ~4 characters per token, include full outputs if they fit
            max_chars = context_window_tokens * 4
            included_count = 0
            for i, output in enumerate(self.previous_outputs, 1):
                if len(context) + len(output) < max_chars:
                    context += f"\nStage {i} Output:\n{output}\n"
                    included_count += 1
                else:
                    # If full output doesn't fit, include a preview
                    preview = output[:500] + "..." if len(output) > 500 else output
                    context += f"\nStage {i} Output Preview (truncated):\n{preview}\n"
                    break
            if not included_count and self.previous_outputs:
                # Include at least one output preview
                context = "\n\n=== CONTEXT FROM PREVIOUS STAGES ===\n"
                preview = self.previous_outputs[-1][:1000] + "..." if len(self.previous_outputs[-1]) > 1000 else self.previous_outputs[-1]
                context += f"\nStage {len(self.previous_outputs)} Output Preview:\n{preview}\n"

        return task_input + context


# ============================================================================
# ORCHESTRATOR CLASS
# ============================================================================

class MultiAgentOrchestrator:
    """
    Orchestrates multiple agents working sequentially.

    This class manages:
    - Agent initialization and execution
    - Sequential pipeline flow
    - State management and tracking
    - Result collection and reporting
    - Error handling and recovery
    """

    def __init__(self, project_name: str, project_description: str):
        """
        Initialize the orchestrator.

        Args:
            project_name: Name of the project
            project_description: Detailed project description
        """
        self.project_name = project_name
        self.project_description = project_description
        self.start_time = None
        self.end_time = None

        # Initialize agents
        self.agents = {
            AgentRole.TASK_MANAGER: Agent(AgentRole.TASK_MANAGER, project_description),
            AgentRole.DEVELOPER: Agent(AgentRole.DEVELOPER, project_description),
            AgentRole.TESTER: Agent(AgentRole.TESTER, project_description),
            AgentRole.DEPLOYER: Agent(AgentRole.DEPLOYER, project_description),
        }

        # Define execution order (sequential, no parallelization)
        self.execution_order = [
            AgentRole.TASK_MANAGER,
            AgentRole.DEVELOPER,
            AgentRole.TESTER,
            AgentRole.DEPLOYER
        ]

        self.pipeline_status = "idle"
        self.results = {}
        logger.info(f"Initialized orchestrator for project: {project_name}")

    def run_pipeline(self) -> Dict[str, str]:
        """
        Execute the complete pipeline without manual intervention.

        Pipeline Flow:
        1. Task Manager - Analyzes requirements, creates task breakdown
        2. Developer - Receives tasks, implements code
        3. Tester - Receives code, creates tests and validates
        4. Deployer - Receives approval, creates deployment plan

        Returns:
            Dict[str, str]: Dictionary with all agent outputs

        Raises:
            Exception: If any agent fails
        """
        self.pipeline_status = "running"
        self.start_time = datetime.now()

        print("\n" + "=" * 80)
        print(f"🚀 MULTI-AGENT PIPELINE EXECUTION: {self.project_name}")
        print("=" * 80)
        print(f"📝 Description: {self.project_description[:100]}...")
        print("=" * 80 + "\n")

        try:
            for idx, role in enumerate(self.execution_order, 1):
                agent = self.agents[role]
                print(f"\n[STAGE {idx}/{len(self.execution_order)}] {role.value.upper()}")
                print("-" * 80)

                # Prepare input for this agent
                if role == AgentRole.TASK_MANAGER:
                    task_input = self._prepare_task_manager_input()
                else:
                    # Pass previous agent's output
                    prev_role = self.execution_order[idx - 2]
                    prev_output = self.agents[prev_role].state.output
                    task_input = self._prepare_next_agent_input(role, prev_output)

                # Execute agent
                try:
                    logger.info(f"Executing {role.value} agent")
                    output = agent.execute(task_input)
                    self.results[role.value] = output

                    # Print summary
                    print(f"✅ Status: {agent.state.status}")
                    print(f"⏱️  Execution Time: {agent.state.execution_time:.2f}s")
                    print(f"📊 Tokens Used: {agent.state.tokens_used}")
                    print(f"\n📄 Output Preview (first 500 characters):")
                    print("-" * 80)
                    preview = output[:500] + "..." if len(output) > 500 else output
                    print(preview)
                    print("-" * 80)

                except Exception as e:
                    print(f"❌ Agent failed: {str(e)}")
                    logger.error(f"{role.value} agent failed: {str(e)}")
                    self.pipeline_status = "failed"
                    return self.results

                # Brief pause between agents
                if idx < len(self.execution_order):
                    print("\n⏳ Moving to next stage...")
                    time.sleep(1)

            self.pipeline_status = "completed"
            self.end_time = datetime.now()

            print("\n" + "=" * 80)
            print("✅ PIPELINE EXECUTION COMPLETED SUCCESSFULLY!")
            print("=" * 80)
            self._print_summary()

            return self.results

        except Exception as e:
            self.pipeline_status = "failed"
            self.end_time = datetime.now()
            logger.error(f"Pipeline execution failed: {str(e)}")
            print(f"\n❌ Pipeline failed: {str(e)}")
            return self.results

    def _prepare_task_manager_input(self) -> str:
        """Prepare input for Task Manager agent"""
        return f"""Analyze and create a comprehensive task breakdown for this project:

PROJECT NAME: {self.project_name}

PROJECT DESCRIPTION:
{self.project_description}

Please provide:
1. Detailed task list with all components
2. Task priorities and dependencies
3. Technical requirements and specifications
4. Realistic effort estimates
5. Risk assessment
6. Success criteria and metrics

Be thorough and professional. Structure your response clearly."""

    def _prepare_next_agent_input(self, role: AgentRole, prev_output: str) -> str:
        """Prepare input for Developer, Tester, or Deployer agents"""
        role_instructions = {
            AgentRole.DEVELOPER: (
                "You are now the Developer. Based on the task breakdown from the Task Manager:\n\n"
                f"{prev_output[:2000]}...\n\n"
                "Please implement the complete solution with:\n"
                "1. Full code implementation\n"
                "2. Architecture overview\n"
                "3. Setup and installation instructions\n"
                "4. API documentation\n"
                "5. All dependencies"
            ),
            AgentRole.TESTER: (
                "You are now the Tester. Based on the code implementation from the Developer:\n\n"
                "Please create comprehensive tests and validate the code:\n"
                "1. Test cases (unit, integration, end-to-end)\n"
                "2. Code coverage analysis\n"
                "3. Bug report (if any)\n"
                "4. Performance assessment\n"
                "5. Go/No-Go recommendation for deployment"
            ),
            AgentRole.DEPLOYER: (
                "You are now the Deployer. Based on the test approval:\n\n"
                "Please create the deployment plan:\n"
                "1. Deployment strategy\n"
                "2. Step-by-step procedures\n"
                "3. Automation scripts\n"
                "4. Monitoring and logging setup\n"
                "5. Rollback procedures"
            ),
        }
        return role_instructions.get(role, "")

    def _print_summary(self):
        """Print execution summary"""
        summary = self.get_summary()
        print("\n📊 PIPELINE SUMMARY:")
        print("-" * 80)
        print(f"Project: {summary['project_name']}")
        print(f"Status: {summary['status'].upper()}")
        print(f"Total Duration: {summary['total_duration_seconds']:.2f}s")
        print(f"Results Collected: {summary['total_results']}/{len(self.execution_order)}")
        print("\n🔍 AGENT STATUS:")
        for agent_name, status in summary['agents_status'].items():
            status_icon = "✅" if status['status'] == 'completed' else "❌"
            print(
                f"{status_icon} {agent_name:20} | "
                f"Status: {status['status']:10} | "
                f"Time: {status['execution_time']:6.2f}s | "
                f"Tokens: {status['tokens_used']}"
            )

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all agent executions.

        Returns:
            Dict: Summary with all metrics and statuses
        """
        total_duration = 0
        if self.start_time and self.end_time:
            total_duration = (self.end_time - self.start_time).total_seconds()

        return {
            "project_name": self.project_name,
            "status": self.pipeline_status,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "total_duration_seconds": total_duration,
            "agents_status": {
                role.value: {
                    "status": self.agents[role].state.status,
                    "execution_time": self.agents[role].state.execution_time,
                    "tokens_used": self.agents[role].state.tokens_used,
                    "error": self.agents[role].state.error
                }
                for role in self.execution_order
            },
            "total_results": len(self.results),
            "results_keys": list(self.results.keys())
        }

    def save_results(self, filename: str = "pipeline_results.json") -> str:
        """
        Save all results to a JSON file.

        Args:
            filename: Output filename

        Returns:
            str: Path to saved file
        """
        output = {
            "metadata": {
                "project_name": self.project_name,
                "execution_time": self.get_summary()['total_duration_seconds'],
                "status": self.pipeline_status,
                "timestamp": datetime.now().isoformat()
            },
            "summary": self.get_summary(),
            "detailed_results": self.results
        }

        with open(filename, 'w') as f:
            json.dump(output, f, indent=2)

        logger.info(f"Results saved to {filename}")
        return filename


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example project definition
    project = {
        "name": "E-Commerce Platform API",
        "description": """
Build a production-ready REST API for an e-commerce platform with the following features:

CORE FEATURES:
1. User Management
   - User registration and authentication (JWT tokens)
   - Password hashing and reset functionality
   - User profile management
   - Role-based access control (RBAC)

2. Product Catalog
   - Product management (CRUD operations)
   - Product categories and tags
   - Search and filtering capabilities
   - Product images and descriptions

3. Shopping Cart
   - Add/remove items
   - Quantity management
   - Cart persistence
   - Cart total calculation

4. Order Processing
   - Order creation from cart
   - Order history and tracking
   - Order status management
   - Order notifications

5. Payment Integration
   - Stripe API integration
   - Payment processing
   - Payment history
   - Refund handling

6. Admin Dashboard
   - Product management
   - Order management
   - User management
   - Analytics and reporting

7. API Documentation
   - Swagger/OpenAPI documentation
   - Endpoint documentation
   - Example requests and responses

TECHNICAL REQUIREMENTS:
- Technology: Node.js + Express OR Python + FastAPI
- Database: PostgreSQL with Redis caching
- Authentication: JWT tokens
- API Style: RESTful with proper status codes
- Error Handling: Comprehensive error responses
- Logging: Structured logging with different levels
- Testing: Unit tests, integration tests
- Security: OWASP Top 10 compliance
- Performance: Sub-200ms API response times
- Scalability: Design for 100k+ users

CONSTRAINTS:
- Timeline: 2 weeks for MVP
- Team: 3 developers
- Budget: Standard
"""
    }

    # Create orchestrator
    orchestrator = MultiAgentOrchestrator(
        project_name=project["name"],
        project_description=project["description"]
    )

    # Run the pipeline (fully automated!)
    results = orchestrator.run_pipeline()

    # Save results
    output_file = orchestrator.save_results()
    print(f"\n💾 Results saved to: {output_file}")

    # Print full summary
    print("\n" + "=" * 80)
    print("📋 FINAL SUMMARY")
    print("=" * 80)
    summary = orchestrator.get_summary()
    print(json.dumps(summary, indent=2))
