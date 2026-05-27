# Multi-Agent Autonomous System Guide

## Overview
This system implements a fully autonomous multi-agent pipeline where agents work independently and sequentially without any manual intervention. Once started, the pipeline automatically flows through each stage:

**Task Manager → Developer → Tester → Deployer**

## Architecture

### Agents & Roles

#### 1. **Task Manager Agent** 📋
- **Responsibility**: Analyze project requirements and create a detailed task breakdown
- **Output**: Structured task list with priorities and dependencies
- **Next Stage Input**: Task list serves as specification for Developer

#### 2. **Developer Agent** 💻
- **Responsibility**: Write production-ready code based on tasks
- **Output**: Complete code implementation with documentation
- **Next Stage Input**: Code and implementation details for Tester

#### 3. **Tester Agent** 🧪
- **Responsibility**: Create test cases and verify code quality
- **Output**: Test results, bug reports, and Go/No-Go decision
- **Next Stage Input**: Test approval and findings for Deployer

#### 4. **Deployer Agent** 🚀
- **Responsibility**: Create deployment plan and procedures
- **Output**: Deployment scripts, monitoring setup, and rollback plans
- **Next Stage Input**: (Final stage - no downstream dependencies)

## System Components

### 1. Python Backend (`multi_agent_system.py`)

#### Key Classes

**AgentRole Enum**
```python
class AgentRole(Enum):
    TASK_MANAGER = "task_manager"
    DEVELOPER = "developer"
    TESTER = "tester"
    DEPLOYER = "deployer"
```

**AgentState**
```python
@dataclass
class AgentState:
    role: AgentRole
    status: str  # idle, working, completed, failed
    output: str
    error: Optional[str]
    execution_time: float
```

**Agent Class**
- Handles independent task execution
- Maintains execution state and output
- Uses Claude API for AI-powered work
- Context-aware prompting based on role

**MultiAgentOrchestrator Class**
- Orchestrates sequential agent execution
- Passes outputs between stages
- Handles pipeline status and results
- No manual intervention required

### 2. React Dashboard (`multi_agent_dashboard.jsx`)

Real-time visualization of:
- Pipeline progress (0-100%)
- Individual agent status
- Execution duration
- Output preview
- Control buttons (Start/Reset)

## How It Works

### Execution Flow

```
1. START PIPELINE
   ↓
2. TASK MANAGER EXECUTES
   - Analyzes project description
   - Creates detailed task breakdown
   - Output: Task list
   ↓
3. DEVELOPER EXECUTES
   - Receives task list from Task Manager
   - Writes code based on specifications
   - Output: Code implementation
   ↓
4. TESTER EXECUTES
   - Receives code from Developer
   - Creates and runs test cases
   - Output: Test results + Go/No-Go
   ↓
5. DEPLOYER EXECUTES
   - Receives approval from Tester
   - Creates deployment plan
   - Output: Deployment procedures
   ↓
6. PIPELINE COMPLETE
   - All results collected
   - Summary generated
```

### Context Passing

Each agent receives:
1. **System Prompt**: Role-specific instructions
2. **Current Task**: Input for this stage
3. **Previous Outputs**: Last 2 agent outputs for context

This ensures smooth handoff and continuity.

## Usage

### Setup

```bash
# Install dependencies
pip install anthropic

# Set environment variable
export ANTHROPIC_API_KEY='your-api-key-here'
```

### Running the Pipeline

```python
from multi_agent_system import MultiAgentOrchestrator

# Define your project
orchestrator = MultiAgentOrchestrator(
    project_name="Your Project Name",
    project_description="Your project description"
)

# Run completely automated pipeline
results = orchestrator.run_pipeline()

# Get summary
summary = orchestrator.get_summary()
```

### Using the Dashboard

1. Open the React component in your browser
2. Enter Project Name and Description
3. Click "Start Pipeline"
4. Watch agents execute sequentially
5. Monitor progress in real-time
6. View output for each agent

## Key Features

### ✅ Fully Autonomous
- No manual intervention needed
- Agents execute sequentially
- Each agent completes before next starts
- Automatic context passing

### ✅ Intelligent Handoffs
- Previous outputs inform next stage
- Agents understand project context
- Progressive refinement of work
- Error handling and recovery

### ✅ Real-Time Monitoring
- Live dashboard updates
- Progress tracking
- Execution timing
- Output preview

### ✅ Production Quality
- Each agent uses best practices
- Code follows standards
- Comprehensive testing
- Deployment-ready output

## Customization

### Adding New Agents

```python
# 1. Add to AgentRole enum
class AgentRole(Enum):
    # ... existing roles ...
    SECURITY = "security"

# 2. Create agent instance
orchestrator.agents[AgentRole.SECURITY] = Agent(
    AgentRole.SECURITY,
    project_description
)

# 3. Add to execution order
orchestrator.execution_order.insert(3, AgentRole.SECURITY)

# 4. Add system prompt in Agent.get_system_prompt()
```

### Modifying Agent Behavior

Edit system prompts in `Agent.get_system_prompt()`:

```python
def get_system_prompt(self) -> str:
    return """You are a Developer Agent with specific instructions:
    - Use TypeScript exclusively
    - Follow SOLID principles
    - Generate 100% test coverage
    - etc."""
```

### Adjusting Prompts

Each agent's instructions can be customized:
- Change output format
- Add specific requirements
- Modify validation rules
- Adjust scope and depth

## Output Structure

### Task Manager Output
```json
{
  "tasks": [
    {
      "task_id": "1",
      "description": "Setup API framework",
      "requirements": [...],
      "priority": "high",
      "dependencies": []
    },
    ...
  ]
}
```

### Developer Output
```
Code Files:
- /src/main.ts
- /src/utils/helpers.ts
- /src/api/routes.ts

Architecture: MVC pattern
Dependencies: Express, TypeScript
API Endpoints: /api/v1/...
```

### Tester Output
```
Test Coverage: 92%
Test Results: 87/87 passed
Bug Reports: 2 minor issues
Go/No-Go: GO FOR DEPLOYMENT
```

### Deployer Output
```
Deployment Plan:
1. Build Docker image
2. Push to registry
3. Deploy to staging
4. Run smoke tests
5. Deploy to production

Monitoring: Active
Rollback Ready: Yes
```

## Error Handling

### Agent Failure
- Pipeline catches exceptions
- Sets agent status to "failed"
- Logs error message
- Stops pipeline gracefully
- Returns partial results

### Timeout Handling
- Set max_tokens in API call
- Implement timeout logic
- Capture partial outputs
- Continue to next agent (optional)

### Retry Logic

```python
def execute_with_retry(self, task_input: str, retries: int = 3):
    for attempt in range(retries):
        try:
            return self.execute(task_input)
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

## Performance Optimization

### Parallel Execution (Advanced)
For independent stages, use async:

```python
import asyncio

async def run_parallel():
    # Only possible if stages don't depend on each other
    tasks = [agent.execute_async(input) for agent in agents]
    results = await asyncio.gather(*tasks)
```

### Token Optimization
- Summarize long outputs
- Focus on key information
- Cache repeated data
- Use streaming for large outputs

## Monitoring & Logging

### Pipeline Status

```python
status = orchestrator.get_summary()
# Returns:
# {
#   "project_name": "...",
#   "status": "completed",
#   "agents_status": {...},
#   "total_results": 4
# }
```

### Agent State

```python
agent = orchestrator.agents[AgentRole.DEVELOPER]
print(agent.state.status)           # "completed"
print(agent.state.execution_time)   # 12.34
print(agent.state.output)           # Full output
```

### Logging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In execution loop
logger.info(f"Starting {role.value}...")
logger.info(f"Completed in {execution_time}s")
```

## Best Practices

### 1. Clear Project Description
- Be specific about requirements
- Define success criteria
- Include constraints and limitations
- Provide examples if helpful

### 2. Monitor Output
- Check agent outputs between stages
- Verify task completion
- Validate code quality
- Review test results

### 3. Adjust Prompts
- Refine based on results
- Add missing requirements
- Clarify ambiguities
- Set quality standards

### 4. Handle Edge Cases
- Test with various project types
- Consider error scenarios
- Plan for large projects
- Set reasonable timeouts

## Troubleshooting

### Agent Produces Poor Output
- Refine system prompt
- Add examples to instructions
- Break down task smaller
- Adjust max_tokens

### Pipeline Stalls
- Check API connectivity
- Verify API key is valid
- Monitor token usage
- Check rate limits

### Context Loss Between Stages
- Increase context window
- Summarize key points
- Maintain thread continuity
- Use explicit handoff format

## Future Enhancements

1. **Feedback Loop**: Allow human review between stages
2. **Parallel Execution**: Run independent agents simultaneously
3. **Custom Metrics**: Track quality scores per agent
4. **Learning**: Improve prompts based on results
5. **Multi-Project**: Handle multiple projects in pipeline
6. **Rollback**: Automatically rollback if tests fail

## API Integration

This system uses **Claude API** with:
- Model: `claude-opus-4-20250805`
- Max Tokens: 4096 per request
- Temperature: Default (0.7)
- Top P: Default (1.0)

### Rate Limits
- Ensure you have adequate API quota
- Monitor token usage
- Implement rate limiting if needed
- Budget: ~5000-8000 tokens per pipeline run

## Support & Contributing

For issues or improvements:
1. Check the error logs
2. Review agent prompts
3. Verify API connectivity
4. Test with simpler projects first

## Example Projects

### E-Commerce Platform
```
Name: E-Commerce API
Description: REST API with auth, products, cart, orders, payments
Estimated Time: 10-15 minutes
```

### Blog System
```
Name: Blog Platform
Description: Multi-user blog with posts, comments, admin panel
Estimated Time: 8-12 minutes
```

### Data Pipeline
```
Name: ETL System
Description: Data extraction, transformation, loading automation
Estimated Time: 12-18 minutes
```

## License & Attribution

This system demonstrates multi-agent orchestration using Claude API by Anthropic.

---

**Ready to automate your development pipeline? Start with a clear project description and let the agents handle the rest!**
