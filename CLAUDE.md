# Chemo Treatment Tracker - Multi-Agent Autonomous Pipeline System

## Project Overview

**Chemo Treatment Tracker** is a sophisticated multi-agent autonomous development pipeline system that uses Claude API (Anthropic) to automatically generate complete software projects. The system orchestrates four specialized AI agents that work sequentially to transform project descriptions into production-ready systems with code, tests, and deployment plans.

### What It Does
- Takes a project description as input
- Automatically generates complete systems in 15-30 minutes
- No manual intervention required
- Produces: Task breakdown + Production code + Tests + Deployment plan

### Key Value Proposition
- **Fully Autonomous**: No human intervention once started
- **Sequential Execution**: Task Manager → Developer → Tester → Deployer
- **Production Quality**: Follows industry best practices
- **Cost Effective**: $0.30-$1.50 per pipeline run
- **Time Saving**: 15-30 minutes automated vs 40+ hours manual work

---

## Architecture & System Design

### High-Level Pipeline Flow

```
User Input (Project Description)
           ↓
      STAGE 1: Task Manager Agent
      • Analyzes requirements
      • Creates task breakdown
      • Maps dependencies
           ↓
      STAGE 2: Developer Agent
      • Writes production code
      • Documents APIs
      • Follows best practices
           ↓
      STAGE 3: Tester Agent
      • Creates test suite
      • Validates quality
      • Reports coverage
           ↓
      STAGE 4: Deployer Agent
      • Creates deployment plan
      • Sets up monitoring
      • Plans rollback
           ↓
      Final Output (JSON)
      • All agent outputs
      • Execution metrics
      • Complete system ready
```

### System Layers

1. **User Interface Layer**
   - `quickstart.py`: CLI interface for interactive use
   - `multi_agent_dashboard.jsx`: React dashboard for real-time monitoring (optional)

2. **Orchestration Layer**
   - `MultiAgentOrchestrator` class: Manages pipeline execution
   - Handles agent initialization, sequencing, and result collection
   - Tracks pipeline status and error handling

3. **Agent Layer**
   - `Agent` base class: Handles API communication with Claude
   - Four specialized agent roles: Task Manager, Developer, Tester, Deployer
   - Each agent maintains its own state and execution context

4. **AI Service Layer**
   - Claude API (Anthropic)
   - Model: claude-opus-4-20250805 (configurable)
   - 4096 token limit per request (configurable)

---

## Core Files

### Python Implementation Files

#### `multi_agent_system.py` (400+ lines)
**Purpose**: Core backend implementation of agents and orchestration

**Key Classes**:
- `AgentRole` (Enum): Defines agent roles (TASK_MANAGER, DEVELOPER, TESTER, DEPLOYER)
- `AgentStatus` (Enum): Tracks agent states (IDLE, WORKING, COMPLETED, FAILED)
- `AgentState` (Dataclass): Stores agent execution state and metrics
- `Agent`: Base agent class with methods to execute tasks and manage state
- `MultiAgentOrchestrator`: Main orchestrator that manages pipeline execution

**Key Methods**:
- `Agent.get_system_prompt()`: Returns role-specific instructions
- `Agent.execute()`: Sends task to Claude API and processes response
- `MultiAgentOrchestrator.run_pipeline()`: Executes complete pipeline
- `MultiAgentOrchestrator.get_summary()`: Returns execution summary

**Dependencies**:
- `anthropic`: Claude API client
- `logging`: Standard Python logging

#### `config.py` (600+ lines)
**Purpose**: Centralized configuration for all system parameters

**Key Sections**:
- `API_CONFIG`: Model settings (model, max_tokens, temperature, timeout)
- `AGENT_PROMPTS`: System prompts for each agent role
- `QUALITY_STANDARDS`: Code coverage, bug limits, performance requirements
- `EXECUTION_CONFIG`: Pipeline execution settings (retries, timeouts)
- `PIPELINE_WORKFLOW`: Definition of the 4-stage pipeline
- `PROJECT_TEMPLATES`: Pre-built project templates
- `VALIDATION_RULES`: Output validation criteria
- `INTEGRATIONS`: Advanced integrations (Slack, GitHub, Jira)

**Customization**: All values fully customizable for different use cases

#### `quickstart.py` (300+ lines)
**Purpose**: User-friendly CLI entry point

**Features**:
- Interactive project input (name and description)
- Progress tracking and status display
- Error handling with helpful messages
- Results saved to `pipeline_results.json`
- Summary output with metrics

**Usage**: `python3 quickstart.py`

**For**: Non-programmers, quick testing, learning

#### `multi_agent_dashboard.jsx` (800+ lines)
**Purpose**: Real-time interactive monitoring dashboard (React)

**Features**:
- Live progress visualization (0-100%)
- Individual agent status tracking
- Execution time per stage
- Output preview panels
- Control buttons (Start/Reset)
- Responsive design with Tailwind CSS

**Framework**: React 18+
**For**: Visual monitoring and real-time feedback

### Documentation Files

#### Main Guides
- `README.md`: Quick start guide and system overview
- `ARCHITECTURE.txt`: Visual system design with ASCII diagrams
- `MULTI_AGENT_GUIDE.md`: Complete technical documentation
- `EXAMPLES.md`: Real-world example projects
- `SYSTEM_SETUP.md`: Installation and configuration guide

#### Navigation Guides
- `START_HERE.txt`: Welcome and orientation
- `INDEX.md`: Complete navigation guide
- `FILE_MANIFEST.txt`: Detailed file directory with metadata
- `DELIVERABLES.md`: Summary of all deliverables

#### Configuration
- `requirements.txt`: Python dependencies
- `.gitignore`: Excluded files (if present)

---

## How to Run the System

### Quick Start (5 minutes)

1. **Install Dependencies**
   ```bash
   pip install anthropic
   ```

2. **Set API Key**
   ```bash
   # macOS/Linux
   export ANTHROPIC_API_KEY="sk-ant-..."
   
   # Windows PowerShell
   $env:ANTHROPIC_API_KEY="sk-ant-..."
   ```

3. **Run Pipeline**
   ```bash
   python3 quickstart.py
   ```

4. **Enter Project Details**
   - Project Name: Your project name
   - Description: Detailed requirements

5. **Wait 15-30 minutes** for automatic execution

### Using in Python Code

```python
from multi_agent_system import MultiAgentOrchestrator
import json

# Create orchestrator
orchestrator = MultiAgentOrchestrator(
    project_name="E-Commerce API",
    project_description="""
    Build REST API with:
    - User authentication (JWT)
    - Product catalog with search
    - Shopping cart
    - Order processing
    Using Node.js and PostgreSQL
    """
)

# Run pipeline
results = orchestrator.run_pipeline()

# View summary
summary = orchestrator.get_summary()
print(f"Status: {summary['pipeline_status']}")
print(f"Agents: {summary['agents_status']}")

# Save results
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
```

---

## Configuration & Customization

### Agent Prompts

Edit `config.py` to customize how agents behave:

```python
# Custom developer instructions
AGENT_PROMPTS["developer"] = """
You are a Senior Full-Stack Developer with specific requirements:
- Use TypeScript exclusively
- Implement 100% test coverage
- Follow strict error handling patterns
- Add comprehensive logging
"""
```

### Quality Standards

Adjust code quality requirements:

```python
QUALITY_STANDARDS = {
    "code_coverage_minimum": 95,      # 95% coverage
    "max_code_issues_allowed": 0,     # Zero issues
    "performance_timeout_ms": 5000    # 5 second timeout
}
```

### API Configuration

Change model, tokens, or temperature:

```python
API_CONFIG = {
    "model": "claude-opus-4-20250805",  # Latest model
    "max_tokens": 4096,                 # Max response length
    "temperature": 0.7,                 # Creativity (0-1)
    "timeout_seconds": 120              # API timeout
}
```

### Execution Settings

Control pipeline behavior:

```python
EXECUTION_CONFIG = {
    "sequential_execution": True,  # Always sequential
    "max_retries": 3,              # Retry failed calls
    "agent_timeout_seconds": 120   # Per-agent timeout
}
```

---

## Agent Roles & Responsibilities

### 1. Task Manager Agent
**Role**: Project Manager / Requirements Analyst

**Input**: Project description
**Output**: Structured task breakdown

**Responsibilities**:
- Analyze project requirements
- Break down into clear, actionable tasks
- Identify task dependencies
- Define priorities and success criteria
- Assess risks and mitigation strategies

**Output Format**:
- Task ID, name, detailed description
- Technical requirements and acceptance criteria
- Estimated effort, dependencies, priority
- Risk assessment and notes

### 2. Developer Agent
**Role**: Senior Full-Stack Engineer

**Input**: Task list from Task Manager
**Output**: Production-ready code

**Responsibilities**:
- Design architecture
- Write clean, maintainable code
- Implement error handling and logging
- Add comprehensive documentation
- Ensure security best practices
- Create API documentation if applicable

**Output Format**:
- Complete code files with implementation
- Architecture overview
- API contracts and documentation
- Database schema
- Setup and installation instructions

### 3. Tester Agent
**Role**: QA/Testing Engineer

**Input**: Code from Developer
**Output**: Test suite and quality report

**Responsibilities**:
- Create comprehensive test cases
- Test happy paths and edge cases
- Generate code coverage metrics
- Identify bugs and vulnerabilities
- Provide quality score
- Make Go/No-Go recommendation

**Output Format**:
- Unit, integration, and E2E tests
- Code coverage percentage (target: 80%+)
- Bug reports with severity levels
- Performance test results
- Quality score and go/no-go decision

### 4. Deployer Agent
**Role**: DevOps/Infrastructure Engineer

**Input**: Approved code and test results
**Output**: Deployment procedures

**Responsibilities**:
- Design deployment strategy
- Create automated deployment scripts
- Set up monitoring and alerting
- Plan rollback procedures
- Document maintenance procedures
- Configure logging and observability

**Output Format**:
- Step-by-step deployment guide
- Automation scripts (Docker, Kubernetes, etc.)
- Monitoring and alerting setup
- Rollback procedures
- Health check configurations

---

## Data Structures

### AgentState
Represents the execution state of an agent:
```python
@dataclass
class AgentState:
    role: AgentRole              # Agent's role
    status: str                  # idle, working, completed, failed
    output: str                  # Agent's output
    error: Optional[str]         # Error message if failed
    execution_time: float        # Time taken in seconds
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    tokens_used: int            # API tokens consumed
```

### Pipeline Results
Saved to `pipeline_results.json`:
```json
{
  "timestamp": "2026-05-27T...",
  "project": {
    "name": "Project Name",
    "description": "Project Description"
  },
  "pipeline_status": "completed",
  "agents": {
    "task_manager": {
      "status": "completed",
      "execution_time": 7.2,
      "output_length": 2450
    },
    // ... other agents
  },
  "detailed_outputs": {
    "task_manager": "...",
    "developer": "...",
    "tester": "...",
    "deployer": "..."
  }
}
```

---

## Common Tasks & Workflows

### Running a Simple Project

1. **Prepare requirements** (detailed description, 200-300 words)
2. **Run**: `python3 quickstart.py`
3. **Input**: Project name and description
4. **Wait**: 15-30 minutes (fully automated)
5. **Review**: Check `pipeline_results.json`

### Customizing Agent Behavior

1. Open `config.py`
2. Modify relevant `AGENT_PROMPTS` section
3. Adjust `QUALITY_STANDARDS` if needed
4. Run `python3 quickstart.py` with custom config

### Using in a Python Project

1. Copy `multi_agent_system.py` to your project
2. Copy `config.py` to your project
3. Import and use:
   ```python
   from multi_agent_system import MultiAgentOrchestrator
   orchestrator = MultiAgentOrchestrator(...)
   results = orchestrator.run_pipeline()
   ```

### Integrating with External Systems

1. Modify `INTEGRATIONS` in `config.py`
2. Add Slack, GitHub, or Jira hooks
3. Extend `MultiAgentOrchestrator` class as needed
4. Implement custom notification logic

---

## Troubleshooting

### Common Issues

**Issue**: "ANTHROPIC_API_KEY not found"
- **Solution**: Set environment variable with valid API key
- **Reference**: `SYSTEM_SETUP.md` - Step 4

**Issue**: "ModuleNotFoundError: No module named 'anthropic'"
- **Solution**: Install with `pip install anthropic`
- **Reference**: `SYSTEM_SETUP.md` - Step 2

**Issue**: Poor code quality or irrelevant output
- **Solution**: Be more specific in project description
- **Reference**: `config.py` - Customize agent prompts

**Issue**: Pipeline timeout or stalls
- **Solution**: Reduce project scope or increase timeout
- **Reference**: `EXECUTION_CONFIG` in `config.py`

### Debugging

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check `pipeline_results.json` for full outputs and timing information.

---

## Performance & Costs

### Execution Times
- **Simple API**: 8-12 minutes
- **Web App**: 15-20 minutes
- **Microservices**: 25-30 minutes
- **Full Platform**: 30-45 minutes

### Token Usage
- **Per Pipeline**: 5,000-25,000 tokens
- **Cost**: ~$0.30-$1.50 per pipeline run

### Resource Requirements
- **CPU**: Minimal (mostly API calls)
- **Memory**: <500MB
- **Disk Space**: 1GB recommended
- **Network**: Good internet connection required

---

## Security Considerations

### API Key Management
- Never commit API keys to version control
- Use environment variables, never hardcode
- Rotate keys monthly
- Monitor usage in console.anthropic.com

### Generated Code
- Review all generated code before production use
- Run security scanners (e.g., Snyk, OWASP ZAP)
- Check dependencies for vulnerabilities
- Sanitize and validate inputs

### Output Security
- Don't commit sensitive outputs to public repos
- Use .gitignore for `pipeline_results.json`
- Encrypt sensitive data in outputs
- Audit before deployment

---

## Project Structure

```
Chemo-Treatment-Tracker/
├── multi_agent_system.py          # Core backend (400+ lines)
├── config.py                      # Configuration (600+ lines)
├── quickstart.py                  # CLI entry point (300+ lines)
├── multi_agent_dashboard.jsx      # React dashboard (800+ lines)
├── requirements.txt               # Python dependencies
│
├── README.md                      # Quick start guide
├── ARCHITECTURE.txt               # System design diagrams
├── MULTI_AGENT_GUIDE.md          # Technical documentation
├── EXAMPLES.md                    # Example projects
├── SYSTEM_SETUP.md               # Installation guide
├── DELIVERABLES.md               # Summary of deliverables
│
├── START_HERE.txt                # Welcome guide
├── INDEX.md                       # Navigation guide
├── FILE_MANIFEST.txt             # File directory
│
├── pipeline_results.json         # Generated results (after run)
└── .git/                         # Git repository
```

---

## Development & Extension

### Key Entry Points

1. **For customization**: Edit `config.py`
2. **For agent logic**: Modify `Agent` class in `multi_agent_system.py`
3. **For orchestration**: Modify `MultiAgentOrchestrator` class
4. **For UI**: Modify `multi_agent_dashboard.jsx`

### Adding Custom Agents

1. Define new agent role in `PIPELINE_WORKFLOW` in `config.py`
2. Add system prompt in `AGENT_PROMPTS`
3. Add stage to workflow in `config.py`
4. Extend `MultiAgentOrchestrator` to handle new stage

### Integration Patterns

- **Slack Notifications**: Modify execution callbacks
- **GitHub Integration**: Add commit/PR creation logic
- **Jira Integration**: Create tickets from task list
- **Database Logging**: Store results in your database

---

## API Reference

### MultiAgentOrchestrator

```python
class MultiAgentOrchestrator:
    def __init__(
        self,
        project_name: str,
        project_description: str
    )
    
    def run_pipeline() -> Dict[str, str]
        # Execute full pipeline, return all agent outputs
    
    def get_summary() -> Dict
        # Return execution summary with status and metrics
    
    def get_pipeline_status() -> str
        # Return current pipeline status
```

### Agent

```python
class Agent:
    def __init__(
        self,
        role: AgentRole,
        project_context: str
    )
    
    def execute(
        self,
        task_input: str
    ) -> str
        # Execute task, return output
    
    def get_system_prompt() -> str
        # Return system prompt for this agent
```

---

## Resources & Documentation

### Primary Documentation
- **README.md**: Quick start and feature overview
- **ARCHITECTURE.txt**: Visual system design
- **MULTI_AGENT_GUIDE.md**: Complete technical guide

### Setup & Installation
- **SYSTEM_SETUP.md**: Step-by-step installation guide
- **requirements.txt**: Python dependencies

### Examples & Reference
- **EXAMPLES.md**: Real-world project examples
- **INDEX.md**: Complete navigation guide
- **FILE_MANIFEST.txt**: Detailed file reference

### External Resources
- [Anthropic Claude API Docs](https://docs.anthropic.com)
- [Python anthropic SDK](https://github.com/anthropics/anthropic-sdk-python)

---

## Version Information

- **System Version**: 2.0
- **Status**: Production Ready
- **Claude Model**: claude-opus-4-20250805
- **Python**: 3.8+
- **Last Updated**: 2026-05-27

---

## License & Attribution

This system demonstrates multi-agent orchestration using Claude API by Anthropic.

---

## Quick Commands

```bash
# Install
pip install anthropic

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run pipeline
python3 quickstart.py

# Check installation
python3 -c "import anthropic; print('✓ OK')"

# View results
cat pipeline_results.json
```

---

**Ready to generate a complete project in 15-30 minutes? Run `python3 quickstart.py` now!**
