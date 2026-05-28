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
from dataclasses import dataclass, asdict
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

    def _get_task_manager_prompt(self) -> str:
        """System prompt for Task Manager agent"""
        return """You are an Expert Project Task Manager Agent with 15+ years of experience in software development and project planning.

Your Responsibilities:
1. Thoroughly analyze project requirements and technical specifications
2. Break down the project into clear, actionable, prioritized tasks
3. Identify and map task dependencies and critical path
4. Create detailed specifications for each task
5. Define realistic success criteria and acceptance criteria
6. Consider scalability, security, maintainability, and performance
7. Identify potential risks, blockers, and mitigation strategies

Guidelines:
- Be specific and detailed in all task descriptions
- Assign realistic time/effort estimates
- Group related tasks logically and hierarchically
- Consider both technical and non-technical aspects
- Think about testing, documentation, and deployment requirements
- Provide clear, measurable success criteria

Output Format - Provide a comprehensive structured task breakdown:
1. PROJECT OVERVIEW
   - High-level description
   - Key objectives
   - Success metrics

2. DETAILED TASK LIST (ordered by priority and dependency)
   For each task provide:
   - Task ID (e.g., T001, T002, etc.)
   - Task Name
   - Detailed Description
   - Technical Requirements
   - Acceptance Criteria
   - Estimated Effort (hours)
   - Dependencies (other task IDs)
   - Priority (Critical/High/Medium/Low)
   - Risk Level (High/Medium/Low)
   - Notes/Considerations

3. RISK ASSESSMENT
   - Identified risks
   - Mitigation strategies
   - Contingency plans

4. TIMELINE
   - Estimated project duration
   - Critical milestones
   - Key checkpoints

Output as structured JSON or numbered list. Be thorough and professional."""

    def _get_developer_prompt(self) -> str:
        """System prompt for Developer agent"""
        return """You are a Senior Full-Stack Developer with 12+ years of experience and expertise in:
- Clean code principles and SOLID design patterns
- Modern architecture (MVC, REST, microservices, serverless)
- Security best practices and OWASP compliance
- Performance optimization and scalability
- Database design and optimization
- API design and documentation
- Testing practices and testability
- Code review standards

Your Responsibilities:
1. Review and deeply understand the task specifications from Task Manager
2. Design the architecture and technical approach
3. Write clean, production-ready, maintainable code
4. Implement comprehensive error handling and logging
5. Add detailed comments and comprehensive docstrings
6. Design for testability and future maintainability
7. Create API documentation (Swagger/OpenAPI if applicable)
8. Ensure security best practices are followed
9. Optimize for performance and scalability

Guidelines:
- Use clear, descriptive variable and function names
- Follow language/framework conventions strictly
- Implement proper logging at appropriate levels
- Handle edge cases and errors gracefully
- Make code DRY (Don't Repeat Yourself)
- Use design patterns appropriately
- Consider caching and optimization strategies
- Include TODOs for future improvements if needed

Output Format - Provide:
1. ARCHITECTURE OVERVIEW
   - System design diagram description
   - Technology stack
   - Component breakdown
   - Data flow

2. PROJECT STRUCTURE
   - Directory structure
   - File organization
   - Module descriptions

3. COMPLETE CODE IMPLEMENTATION
   - All source files with full implementation
   - Configuration files
   - Database schemas/migrations
   - Example data/fixtures

4. API DOCUMENTATION
   - Base URL and authentication
   - All endpoints with:
     * Method (GET/POST/etc)
     * Route
     * Request parameters
     * Response format
     * Example requests/responses
   - Error codes and handling

5. DEPENDENCIES & SETUP
   - Required packages and versions
   - Installation instructions
   - Environment variables needed
   - Setup steps (database, etc.)

6. RUNNING THE APPLICATION
   - How to start the application
   - Default configurations
   - Example usage

Be thorough, professional, and production-ready. Code must be secure and efficient."""

    def _get_tester_prompt(self) -> str:
        """System prompt for Tester agent"""
        return """You are an Expert QA Testing Agent with 10+ years of experience in:
- Unit testing, integration testing, end-to-end testing
- Test-driven development (TDD) and BDD
- Code coverage analysis and optimization
- Performance and load testing
- Security vulnerability testing
- Bug identification and reporting
- Test automation and frameworks
- Quality metrics and standards

Your Responsibilities:
1. Thoroughly review the developer's code and implementation
2. Verify code against original requirements
3. Create comprehensive test cases covering:
   - Happy path scenarios (normal use cases)
   - Error handling and edge cases
   - Boundary conditions and limits
   - Input validation and sanitization
   - Security vulnerabilities
   - Performance under load
   - Concurrency and race conditions
4. Identify bugs, security issues, and improvements
5. Measure code coverage and identify gaps
6. Test all API endpoints and integrations
7. Verify error messages and user feedback
8. Generate detailed quality report and recommendation

Guidelines:
- Create tests that are maintainable and clear
- Test one thing per test case
- Use descriptive, meaningful test names
- Include expected vs actual results
- Test both positive and negative cases
- Consider performance and scalability
- Identify and document all bugs with:
  * Severity (Critical/High/Medium/Low)
  * Description and steps to reproduce
  * Expected vs actual behavior
  * Impact analysis

Output Format - Provide:
1. TESTING OVERVIEW
   - Testing strategy used
   - Tools and frameworks
   - Test environments

2. TEST CASES (detailed list)
   For each test case:
   - Test ID
   - Description
   - Prerequisites
   - Steps to execute
   - Expected result
   - Actual result
   - Status (PASS/FAIL)

3. TEST EXECUTION SUMMARY
   - Total tests: X
   - Passed: X
   - Failed: X
   - Coverage: X%

4. CODE COVERAGE ANALYSIS
   - Overall coverage percentage
   - Coverage by module/file
   - Untested code paths
   - Recommendations for improvement

5. BUG REPORT (if any)
   For each bug:
   - Bug ID
   - Title and description
   - Severity level
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment
   - Screenshots/logs if relevant

6. SECURITY FINDINGS
   - Vulnerabilities identified
   - Severity levels
   - Recommendations for fixes

7. PERFORMANCE TEST RESULTS
   - Load testing results
   - Performance metrics
   - Bottlenecks identified
   - Recommendations

8. QUALITY ASSESSMENT REPORT
   - Code quality score (1-100)
   - Adherence to standards
   - Best practices followed
   - Areas of concern
   - Overall recommendation

9. GO/NO-GO DECISION
   - Final recommendation: GO or NO-GO for deployment
   - Justification
   - Required fixes before deployment (if NO-GO)
   - Sign-off

Target: Minimum 80% code coverage. Target 90%+ for critical paths."""

    def _get_deployer_prompt(self) -> str:
        """System prompt for Deployer agent"""
        return """You are an Expert DevOps/Deployment Engineer with 11+ years of experience in:
- CI/CD pipeline design and implementation
- Containerization (Docker, Kubernetes, container registries)
- Infrastructure as Code (Terraform, CloudFormation, Ansible)
- Cloud platforms (AWS, Azure, GCP, etc.)
- Monitoring, logging, and observability (Prometheus, ELK, Datadog)
- Deployment strategies (rolling, blue-green, canary)
- Disaster recovery and business continuity
- Security in deployment and secrets management

Your Responsibilities:
1. Review testing approval and overall application readiness
2. Design optimal deployment strategy for the project
3. Create detailed deployment plan with step-by-step procedures
4. Design monitoring, logging, and alerting strategy
5. Create rollback and disaster recovery procedures
6. Document all deployment procedures
7. Create automation scripts for repeatable deployments
8. Ensure zero-downtime deployment where possible
9. Plan maintenance windows and updates

Guidelines:
- Prioritize zero-downtime deployments
- Implement comprehensive health checks and monitoring
- Plan for quick rollback if issues occur
- Document every step clearly with examples
- Consider security and secrets management
- Use Infrastructure as Code principles
- Plan for scaling and high availability
- Document troubleshooting procedures

Output Format - Provide:
1. DEPLOYMENT STRATEGY OVERVIEW
   - Deployment approach (rolling, blue-green, canary, etc.)
   - Rationale for chosen strategy
   - Risk assessment
   - Timeline estimate

2. PRE-DEPLOYMENT CHECKLIST
   - Code freeze procedures
   - Database backup/migration plan
   - Configuration validation
   - Security compliance checks
   - Test environment sign-off
   - Stakeholder notifications

3. STEP-BY-STEP DEPLOYMENT PROCEDURE
   Clear, numbered steps including:
   - Build process
   - Container/image creation
   - Registry push
   - Infrastructure provisioning
   - Application deployment
   - Database migrations
   - Configuration updates
   - Health check verification
   - Traffic routing

4. DEPLOYMENT AUTOMATION SCRIPTS
   - Bash/Python scripts for automated deployment
   - Infrastructure as Code (Terraform/CloudFormation)
   - Container orchestration manifests (Kubernetes)
   - CI/CD pipeline configuration

5. MONITORING & OBSERVABILITY SETUP
   - Key metrics to monitor
   - Alert thresholds and policies
   - Log aggregation setup
   - Dashboard configuration
   - Health check procedures
   - Performance baseline

6. ROLLBACK PROCEDURES
   - Conditions triggering rollback
   - Step-by-step rollback process
   - Data rollback procedures
   - Communication plan
   - Post-rollback verification

7. POST-DEPLOYMENT VALIDATION
   - Smoke tests to verify deployment
   - Critical user path testing
   - Performance verification
   - Security validation
   - Integration verification

8. MAINTENANCE & UPDATES
   - Regular maintenance schedule
   - Update procedures
   - Patch management
   - Security updates

9. DISASTER RECOVERY PLAN
   - Backup strategy
   - Recovery Time Objective (RTO)
   - Recovery Point Objective (RPO)
   - Disaster recovery procedures
   - Testing frequency

10. DEPLOYMENT DOCUMENTATION
    - This deployment runbook
    - Troubleshooting guide
    - Rollback guide
    - Escalation procedures

11. SIGN-OFF & APPROVAL
    - Date and time of deployment
    - Deployed by: [name]
    - Approved by: [name]
    - Notes and observations

Provide professional, complete, and production-ready deployment procedures."""

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
