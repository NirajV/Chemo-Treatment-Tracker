# Multi-Agent Pipeline: Example Use Cases

## Quick Examples

### 1. E-Commerce REST API

```python
from multi_agent_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator(
    project_name="E-Commerce REST API",
    project_description="""
    Build a production-ready e-commerce REST API with:
    - User authentication using JWT tokens
    - Product catalog with search and filtering
    - Shopping cart functionality
    - Order management and tracking
    - Payment processing (Stripe integration)
    - Admin dashboard for inventory
    - Email notifications
    - Rate limiting and caching
    
    Technology Stack:
    - Backend: Node.js with Express or Python with FastAPI
    - Database: PostgreSQL with Redis caching
    - Authentication: JWT
    - Payment: Stripe API
    """
)

# Run completely automated - no intervention needed!
results = orchestrator.run_pipeline()
```

**Estimated Execution Time**: 15-20 minutes

**Expected Outputs**:
- Task breakdown with 8-10 components
- Complete API implementation with endpoints
- Comprehensive test suite (100+ tests)
- Deployment scripts and monitoring setup

---

### 2. Mobile App Backend

```python
orchestrator = MultiAgentOrchestrator(
    project_name="Social Media Mobile App Backend",
    project_description="""
    Build a backend for a social media mobile app with:
    - User registration and authentication
    - User profiles and profiles viewing
    - Post creation, editing, deletion
    - Like and comment functionality
    - Follow/unfollow features
    - Feed generation (personalized)
    - Real-time notifications
    - Image upload and storage
    - Analytics tracking
    
    Constraints:
    - Must support 100k concurrent users
    - API responses under 200ms
    - Zero data loss on deployment
    - Mobile clients: iOS and Android
    """
)

results = orchestrator.run_pipeline()
```

**Estimated Execution Time**: 20-25 minutes

**Key Components**:
- Authentication system
- Database schema for social features
- Real-time API design
- Scaling considerations

---

### 3. Data Processing Pipeline

```python
orchestrator = MultiAgentOrchestrator(
    project_name="Customer Data Pipeline",
    project_description="""
    Build a data pipeline for customer analytics:
    - Extract customer data from multiple sources
      (Salesforce, Google Analytics, Email)
    - Transform and normalize the data
    - Calculate customer lifetime value
    - Identify customer segments
    - Detect anomalies in behavior
    - Load into data warehouse (Snowflake)
    - Generate daily reports
    
    Requirements:
    - Handle 1GB+ daily data
    - Complete processing within 2 hours
    - 99.9% uptime SLA
    - Audit trail for compliance
    """
)

results = orchestrator.run_pipeline()
```

**Estimated Execution Time**: 18-22 minutes

**Deliverables**:
- ETL scripts
- Data validation rules
- Monitoring and alerting
- Disaster recovery plan

---

### 4. Microservices Architecture

```python
orchestrator = MultiAgentOrchestrator(
    project_name="E-Learning Platform Microservices",
    project_description="""
    Design a microservices architecture for an e-learning platform:
    
    Services:
    1. User Service - Authentication and profiles
    2. Course Service - Catalog and metadata
    3. Content Service - Video and resource delivery
    4. Learning Service - Track progress and completion
    5. Notification Service - Email and push notifications
    6. Analytics Service - User behavior tracking
    7. Payment Service - Subscription management
    
    Requirements:
    - Independent deployment of services
    - Service discovery with Consul/Eureka
    - Message queue for async communication
    - API Gateway for routing
    - Circuit breaker for resilience
    - Distributed logging (ELK Stack)
    - Kubernetes orchestration
    """
)

results = orchestrator.run_pipeline()
```

**Estimated Execution Time**: 25-30 minutes

**Architecture Includes**:
- Service boundaries and responsibilities
- API contracts between services
- Message queue schemas
- Deployment manifests

---

### 5. Machine Learning Model Deployment

```python
orchestrator = MultiAgentOrchestrator(
    project_name="ML Model API Service",
    project_description="""
    Build an API service for ML model predictions:
    - Deploy pre-trained recommendation model
    - Accept user input and features
    - Run model inference in real-time
    - Return top-N recommendations
    - Log predictions for retraining
    - A/B test different models
    - Monitor model performance metrics
    - Handle model versioning
    
    Model Details:
    - Type: Collaborative Filtering
    - Framework: TensorFlow
    - Size: 500MB
    - Latency requirement: <100ms
    - Expected load: 1000 requests/minute
    """
)

results = orchestrator.run_pipeline()
```

**Estimated Execution Time**: 20-25 minutes

---

## Running Examples

### Setup Environment

```bash
# 1. Install dependencies
pip install anthropic

# 2. Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Create a project file
touch my_project.py
```

### Run an Example

```python
# my_project.py
from multi_agent_system import MultiAgentOrchestrator

def run_example():
    orchestrator = MultiAgentOrchestrator(
        project_name="My Project",
        project_description="Project description here..."
    )
    
    # Execute the pipeline (fully automated!)
    results = orchestrator.run_pipeline()
    
    # Get summary
    summary = orchestrator.get_summary()
    print(f"Pipeline Status: {summary['status']}")
    
    return results

if __name__ == "__main__":
    results = run_example()
```

```bash
python my_project.py
```

---

## Real-World Scenarios

### Scenario 1: Startup MVP

**Situation**: New startup needs MVP in 1 week

**Pipeline Used**:
- Run the pipeline with detailed requirements
- Agents create tasks, code, tests, deployment in 20 minutes
- Developer gets complete working system
- Can focus on customization and integrations
- Deploy within days instead of weeks

**Time Saved**: 30-40 developer hours

---

### Scenario 2: Rapid Prototyping

**Situation**: Need to validate business idea quickly

**Pipeline Used**:
- Describe the feature/product concept
- Pipeline generates working prototype
- Get feedback from stakeholders
- Iterate quickly with updated requirements

**Time Saved**: 50% reduction in prototyping time

---

### Scenario 3: Team Onboarding

**Situation**: New developer joining team

**Pipeline Used**:
- Generate comprehensive documentation
- New dev reviews generated code
- Understand architecture and design patterns
- Faster onboarding with complete system

**Time Saved**: 1-2 weeks of learning curve

---

### Scenario 4: Legacy System Modernization

**Situation**: Need to migrate old system to microservices

**Pipeline Used**:
```python
description = """
Modernize legacy monolith to microservices:
- Existing system: Monolithic Django app
- Target: Microservices with Kubernetes
- Features to extract:
  1. User management
  2. Billing system
  3. Reporting
  4. Notifications
- Timeline: 3 months
- Team size: 3 developers
"""

orchestrator = MultiAgentOrchestrator(
    project_name="Legacy Modernization",
    project_description=description
)

results = orchestrator.run_pipeline()
```

---

## Advanced Customization

### Custom Quality Gates

```python
from config import QUALITY_STANDARDS

# Modify quality requirements
QUALITY_STANDARDS["code_coverage_minimum"] = 95  # Stricter requirement
QUALITY_STANDARDS["max_code_issues_allowed"] = 0  # Zero issues
```

### Custom Agent Prompts

```python
# Modify prompts in config.py for your specific needs

AGENT_PROMPTS["developer"] = """Custom developer instructions:
- Use TypeScript exclusively
- Follow strict coding standards
- Generate 100% test coverage
- Use async/await patterns
- Add comprehensive error handling
..."""
```

### Adding Validation

```python
from config import validate_output

# Validate agent outputs
is_valid, errors = validate_output("developer", code_output)
if not is_valid:
    print(f"Validation errors: {errors}")
```

---

## Common Patterns

### Pattern 1: Minimal Project

Use for quick testing:

```python
orchestrator = MultiAgentOrchestrator(
    project_name="Simple API",
    project_description="Create a REST API for a todo list with CRUD operations"
)
```

### Pattern 2: Detailed Project

Use for production systems:

```python
detailed_description = """
Build [system] with following requirements:

FUNCTIONAL REQUIREMENTS:
1. User Management
   - Signup and login
   - Password reset
   - Profile management

2. Core Features
   - [Feature 1]
   - [Feature 2]
   - [Feature 3]

TECHNICAL REQUIREMENTS:
- Scalability: 100k concurrent users
- Performance: API response < 200ms
- Availability: 99.99% uptime
- Security: OWASP Top 10 compliance

CONSTRAINTS:
- Stack: [specific tech]
- Timeline: [duration]
- Budget: [if relevant]
"""

orchestrator = MultiAgentOrchestrator(
    project_name="Production System",
    project_description=detailed_description
)
```

### Pattern 3: Integration Testing

```python
# First pipeline
result1 = orchestrator1.run_pipeline()

# Second pipeline using first results
orchestrator2 = MultiAgentOrchestrator(
    project_name="Integration Layer",
    project_description=f"""
    Build integration layer for:
    - System 1 (from previous pipeline): {result1['task_manager']}
    - System 2: [description]
    """
)
result2 = orchestrator2.run_pipeline()
```

---

## Performance Benchmarks

Based on typical runs:

| Project Type | Size | Est. Time | Tokens Used |
|---|---|---|---|
| Simple API | Small | 8-12 min | 3,000-5,000 |
| Web App | Medium | 15-20 min | 8,000-12,000 |
| Microservices | Large | 20-30 min | 12,000-18,000 |
| Full Platform | XL | 30-45 min | 18,000-25,000 |

---

## Troubleshooting Examples

### Issue: Agent produces incomplete output

```python
# Solution: Modify the prompt to be more specific
AGENT_PROMPTS["developer"] += """

IMPORTANT: You MUST provide:
1. Complete code files
2. Configuration needed
3. Setup instructions
4. Dependencies list
5. Example API calls

Do not omit any of these sections."""
```

### Issue: Pipeline takes too long

```python
# Solution: Reduce scope or use faster model
API_CONFIG["model"] = "claude-sonnet-4-20250514"  # Faster model
# or split into smaller projects
```

### Issue: Low code coverage

```python
# Solution: Strengthen testing requirements
AGENT_PROMPTS["tester"] += """

You MUST achieve:
- Minimum 90% code coverage
- Test all edge cases
- Test all error paths
- Test all validation rules"""
```

---

## Integration Ideas

### With CI/CD Pipeline

```bash
# Run Multi-Agent Pipeline in GitHub Actions
name: Generate Architecture
on: [workflow_dispatch]
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Pipeline
        run: python quickstart.py
      - name: Commit Results
        run: git add . && git commit -m "Auto-generated architecture"
```

### With Slack

```python
# Notify team on completion
import requests

def notify_slack(message):
    requests.post(
        "YOUR_SLACK_WEBHOOK",
        json={"text": message}
    )

# After pipeline completes
notify_slack(f"✅ Pipeline completed: {summary['project_name']}")
```

### With GitHub

```python
# Create PR with generated code
from github import Github

g = Github("github_token")
repo = g.get_user().get_repo("my-repo")
repo.create_file("generated_code.py", "Auto-generated", code_content)
```

---

## Best Practices

1. **Start Simple**: Begin with small projects to understand the system
2. **Review Outputs**: Always review generated code before using in production
3. **Iterate**: Use feedback to refine prompts and requirements
4. **Version Control**: Keep all pipeline outputs in git
5. **Document**: Add comments explaining why changes were made
6. **Test**: Validate generated code with your own test suite
7. **Monitor**: Track pipeline execution times and token usage

---

## Next Steps

1. ✅ Install dependencies: `pip install anthropic`
2. ✅ Set API key: `export ANTHROPIC_API_KEY="..."`
3. ✅ Run first pipeline: `python quickstart.py`
4. ✅ Review outputs and customize config
5. ✅ Use in your projects!

---

**Ready to automate your development? Pick an example above and try it now!**
