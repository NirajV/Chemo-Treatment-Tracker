"""
Multi-Agent Pipeline Configuration
Customize agent behavior, prompts, and pipeline settings
"""

# ============================================================================
# MODEL AND API SETTINGS
# ============================================================================

API_CONFIG = {
    "model": "claude-opus-4-20250805",  # Latest Claude model
    "max_tokens": 4096,
    "temperature": 0.7,
    "top_p": 1.0,
    "timeout_seconds": 120
}

# ============================================================================
# AGENT SYSTEM PROMPTS
# ============================================================================

AGENT_PROMPTS = {
    "task_manager": """You are an Expert Project Task Manager Agent with 10+ years of experience.
Your responsibilities:
1. Analyze and understand the project requirements thoroughly
2. Break down the project into clear, actionable, prioritized tasks
3. Identify task dependencies and critical path
4. Create a detailed specification for each task
5. Define success criteria and acceptance criteria
6. Consider scalability, security, and maintainability

Guidelines:
- Be specific and detailed in task descriptions
- Assign realistic complexity estimates (hours)
- Group related tasks logically
- Identify potential risks and blockers
- Consider edge cases and error handling

Output Format: Provide a comprehensive task breakdown with:
- Task ID (unique identifier)
- Task Description (clear and detailed)
- Requirements (specific requirements for this task)
- Priority (Critical, High, Medium, Low)
- Estimated Hours (realistic estimate)
- Dependencies (other tasks this depends on)
- Success Criteria (how to verify completion)
- Risk Assessment (potential issues)

Structure your output as a numbered list or JSON for clarity.""",

    "developer": """You are a Senior Full-Stack Developer with expertise in:
- Clean code and SOLID principles
- Modern architecture patterns (MVC, REST, microservices)
- Security best practices
- Performance optimization
- Testing and documentation

Your responsibilities:
1. Review and understand the task specifications from Task Manager
2. Write clean, production-ready code
3. Follow established best practices and design patterns
4. Implement comprehensive error handling
5. Add detailed comments and docstrings
6. Design for testability and maintainability
7. Create API documentation if applicable

Guidelines:
- Use clear variable and function names
- Implement logging for debugging
- Handle edge cases and errors gracefully
- Consider performance implications
- Make code DRY (Don't Repeat Yourself)
- Follow language-specific conventions

Output Format: Provide:
- Code files with full implementation
- Architecture overview (diagram or description)
- API endpoints and their contracts (if REST API)
- Database schema (if applicable)
- Environment configuration needed
- Installation and setup instructions
- Dependencies and versions
- Code walkthrough highlights""",

    "tester": """You are an Expert QA Testing Agent with deep expertise in:
- Unit testing, integration testing, end-to-end testing
- Test-driven development (TDD)
- Code coverage analysis
- Performance testing
- Security testing basics
- Bug report writing

Your responsibilities:
1. Review the developer's code thoroughly
2. Create comprehensive test cases covering:
   - Happy path scenarios
   - Error handling and edge cases
   - Boundary conditions
   - Input validation
   - Performance under load
3. Identify bugs, vulnerabilities, and improvements
4. Verify code against original requirements
5. Generate detailed test report
6. Provide Go/No-Go recommendation

Guidelines:
- Create tests that are maintainable and clear
- Test one thing per test case
- Use descriptive test names
- Include expected vs actual results
- Consider both positive and negative cases
- Test error messages and user feedback
- Verify performance meets requirements

Output Format: Provide:
- Test cases (unit, integration, E2E)
- Test execution results (pass/fail)
- Code coverage metrics (target: 80%+)
- Bug reports (severity, description, steps to reproduce)
- Performance test results
- Security findings (if any)
- Quality score (1-100)
- Go/No-Go decision with justification""",

    "deployer": """You are an Expert DevOps/Deployment Engineer with expertise in:
- CI/CD pipelines (GitHub Actions, GitLab CI, Jenkins)
- Containerization (Docker, Kubernetes)
- Infrastructure as Code (Terraform, CloudFormation)
- Monitoring and logging (Prometheus, ELK Stack)
- Rollback and disaster recovery strategies
- Security in deployment

Your responsibilities:
1. Review test approval and application readiness
2. Design deployment strategy (rolling, canary, blue-green)
3. Create automated deployment scripts
4. Set up monitoring and alerting
5. Document rollback procedures
6. Plan maintenance and updates
7. Configure logging and observability

Guidelines:
- Ensure zero-downtime deployment where possible
- Implement comprehensive health checks
- Set up proper monitoring and alerting
- Document all steps clearly
- Plan for quick rollback if issues occur
- Consider database migrations carefully
- Test deployment in staging first
- Set up proper environment management

Output Format: Provide:
- Deployment strategy overview
- Pre-deployment checklist
- Step-by-step deployment procedure
- Deployment automation scripts (Bash, Python)
- Health check and verification steps
- Monitoring and alerting setup
- Rollback procedures and triggers
- Post-deployment validation
- Maintenance schedule
- Disaster recovery plan"""
}

# ============================================================================
# QUALITY STANDARDS AND REQUIREMENTS
# ============================================================================

QUALITY_STANDARDS = {
    "code_coverage_minimum": 80,  # Minimum percentage
    "max_code_issues_allowed": 5,  # Maximum bugs allowed
    "performance_timeout_ms": 5000,  # Maximum response time
    "security_issues_critical": 0,  # No critical security issues allowed
    "documentation_required": True,
    "test_case_ratio": 2  # At least 2 tests per feature
}

# ============================================================================
# AGENT EXECUTION SETTINGS
# ============================================================================

EXECUTION_CONFIG = {
    "max_retries": 3,
    "retry_delay_seconds": 2,
    "agent_timeout_seconds": 120,
    "sequential_execution": True,  # Always True - agents must run one after another
    "pass_context_between_agents": True,
    "context_window_size": 8000,  # tokens to include from previous agent
    "save_intermediate_outputs": True,
    "output_directory": "./pipeline_outputs"
}

# ============================================================================
# PIPELINE WORKFLOW
# ============================================================================

PIPELINE_WORKFLOW = [
    {
        "stage": 1,
        "agent": "task_manager",
        "name": "Task Manager",
        "icon": "📋",
        "timeout": 120,
        "description": "Analyze requirements and create task breakdown"
    },
    {
        "stage": 2,
        "agent": "developer",
        "name": "Developer",
        "icon": "💻",
        "timeout": 180,
        "description": "Implement code based on tasks"
    },
    {
        "stage": 3,
        "agent": "tester",
        "name": "QA Tester",
        "icon": "🧪",
        "timeout": 150,
        "description": "Test code and verify quality"
    },
    {
        "stage": 4,
        "agent": "deployer",
        "name": "DevOps Deployer",
        "icon": "🚀",
        "timeout": 120,
        "description": "Create deployment plan and procedures"
    }
]

# ============================================================================
# ERROR HANDLING AND RECOVERY
# ============================================================================

ERROR_HANDLING = {
    "continue_on_warning": True,  # Continue to next stage even with warnings
    "continue_on_minor_error": False,  # Stop if critical error
    "collect_partial_outputs": True,  # Save outputs even if agent fails
    "send_notifications": False,  # Email/Slack on completion
    "log_all_outputs": True,
    "backup_outputs": True
}

# ============================================================================
# MONITORING AND METRICS
# ============================================================================

MONITORING = {
    "track_execution_time": True,
    "track_token_usage": True,
    "track_api_costs": False,
    "log_level": "INFO",  # DEBUG, INFO, WARNING, ERROR
    "metrics_file": "metrics.json",
    "verbose_output": True
}

# ============================================================================
# PROJECT TEMPLATES
# ============================================================================

PROJECT_TEMPLATES = {
    "web_api": {
        "name": "RESTful Web API",
        "description": """Create a production-ready REST API with:
- User authentication and authorization (JWT)
- Database models and relationships
- RESTful endpoints for CRUD operations
- Input validation and error handling
- Rate limiting and caching
- API documentation (Swagger/OpenAPI)
- Comprehensive test coverage
- Docker containerization
- CI/CD pipeline setup""",
        "estimated_time_minutes": 20
    },
    
    "web_application": {
        "name": "Full-Stack Web Application",
        "description": """Build a complete web application with:
- Frontend (React/Vue/Angular) with responsive design
- Backend API (Node.js/Python/Go)
- Database design and setup
- User authentication and sessions
- Admin dashboard
- Real-time features (WebSocket)
- Mobile responsive design
- Performance optimization
- Security hardening
- Deployment configuration""",
        "estimated_time_minutes": 30
    },
    
    "microservices": {
        "name": "Microservices Architecture",
        "description": """Design and implement microservices with:
- Multiple independent services
- API Gateway pattern
- Service-to-service communication
- Message queuing (RabbitMQ/Kafka)
- Database per service
- Container orchestration (Kubernetes)
- Service discovery
- Monitoring and tracing
- Load balancing
- Fault tolerance and resilience""",
        "estimated_time_minutes": 40
    },
    
    "data_pipeline": {
        "name": "Data Processing Pipeline",
        "description": """Build a data pipeline with:
- Data extraction from multiple sources
- Data transformation and cleaning
- Data validation and quality checks
- Data loading to warehouse
- Error handling and retry logic
- Data versioning
- Metadata management
- Monitoring and alerting
- Documentation and lineage
- Scalability for large datasets""",
        "estimated_time_minutes": 25
    },
    
    "mobile_app": {
        "name": "Mobile Application",
        "description": """Develop a mobile application with:
- Cross-platform development (React Native/Flutter)
- Native features (camera, location, etc.)
- Offline functionality
- Local storage and database
- API integration
- Push notifications
- Performance optimization
- Security best practices
- App store deployment
- Analytics and crash reporting""",
        "estimated_time_minutes": 35
    }
}

# ============================================================================
# CUSTOM VALIDATION RULES
# ============================================================================

VALIDATION_RULES = {
    "task_manager_output": {
        "must_have_tasks": True,
        "min_tasks": 3,
        "must_have_priorities": True,
        "must_have_dependencies": True,
        "valid_priorities": ["Critical", "High", "Medium", "Low"]
    },
    
    "developer_output": {
        "must_have_code": True,
        "must_have_documentation": True,
        "must_have_setup_instructions": True,
        "required_sections": ["Code", "Architecture", "Dependencies", "Setup"]
    },
    
    "tester_output": {
        "must_have_test_cases": True,
        "min_test_cases": 5,
        "must_have_coverage": True,
        "min_coverage_percent": 70,
        "must_have_decision": True,
        "valid_decisions": ["GO", "NO-GO"]
    },
    
    "deployer_output": {
        "must_have_checklist": True,
        "must_have_scripts": True,
        "must_have_rollback_plan": True,
        "must_have_monitoring": True,
        "required_sections": ["Strategy", "Checklist", "Scripts", "Rollback", "Monitoring"]
    }
}

# ============================================================================
# INTEGRATIONS (Advanced)
# ============================================================================

INTEGRATIONS = {
    "slack": {
        "enabled": False,
        "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
        "notify_on_completion": True,
        "notify_on_failure": True,
        "channel": "#deployments"
    },
    
    "github": {
        "enabled": False,
        "repo": "owner/repo",
        "create_branch": False,
        "create_pull_request": False,
        "commit_message": "Auto-generated by Multi-Agent Pipeline"
    },
    
    "jira": {
        "enabled": False,
        "instance": "your-instance.atlassian.net",
        "project_key": "PROJECT",
        "create_tickets": False,
        "update_tickets": False
    },
    
    "database": {
        "enabled": False,
        "type": "postgresql",  # postgresql, mysql, mongodb
        "host": "localhost",
        "port": 5432,
        "database": "pipeline_logs",
        "save_results": False
    }
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_template(template_name: str) -> dict:
    """Get a project template by name"""
    return PROJECT_TEMPLATES.get(template_name, {})

def get_agent_prompt(agent_role: str) -> str:
    """Get system prompt for an agent"""
    return AGENT_PROMPTS.get(agent_role, "")

def validate_output(agent_role: str, output: str) -> tuple[bool, list]:
    """Validate agent output against rules
    
    Returns: (is_valid, error_messages)
    """
    errors = []
    rules = VALIDATION_RULES.get(agent_role + "_output", {})
    
    # Add validation logic here
    # This is a placeholder implementation
    
    return len(errors) == 0, errors

# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Print current configuration
    print("Multi-Agent Pipeline Configuration Loaded")
    print("=" * 60)
    print(f"Model: {API_CONFIG['model']}")
    print(f"Max Tokens: {API_CONFIG['max_tokens']}")
    print(f"Pipeline Stages: {len(PIPELINE_WORKFLOW)}")
    print(f"Available Templates: {len(PROJECT_TEMPLATES)}")
    print("\nPipeline Stages:")
    for stage in PIPELINE_WORKFLOW:
        print(f"  {stage['stage']}. {stage['name']} ({stage['agent']})")
    
    # Get a template
    print("\nAvailable Templates:")
    for name, template in PROJECT_TEMPLATES.items():
        print(f"  - {name}: {template['name']}")
