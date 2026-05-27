# Multi-Agent Pipeline System - Python Scripts Usage Guide

## 📚 Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Detailed Usage](#detailed-usage)
4. [Script Reference](#script-reference)
5. [Examples](#examples)
6. [Troubleshooting](#troubleshooting)

---

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Anthropic API key

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `anthropic` - Claude API client library (required)
- `python-dotenv` - Environment variable management (optional)
- `requests` - HTTP library (optional)

### Step 2: Set Anthropic API Key

```bash
# On macOS/Linux
export ANTHROPIC_API_KEY="sk-ant-..."

# On Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-..."

# Or create .env file in project directory
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env
```

### Step 3: Verify Installation

```bash
python3 -c "import anthropic; print('✓ Installation successful')"
```

---

## Quick Start

### Option 1: Interactive CLI (Easiest)

```bash
python3 cli.py
```

This launches an interactive interface where you:
1. Enter project name
2. Select from templates or provide custom description
3. Confirm execution
4. Watch pipeline run
5. Review results automatically

### Option 2: Simple Runner

```bash
python3 run.py
```

Similar to CLI but simpler interface - just provide project name and description.

### Option 3: Direct Python Script

```bash
python3 -c "
from multi_agent_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator(
    project_name='My API',
    project_description='Build a REST API with authentication'
)

orchestrator.run_pipeline()
orchestrator.save_results()
"
```

---

## Detailed Usage

### Using the CLI (cli.py)

#### Interactive Mode (Default)
```bash
python3 cli.py
```

Features:
- Project template selection
- Interactive input validation
- Execution confirmation
- Real-time progress display
- Automatic result analysis
- Color-coded output

#### View Results
```bash
python3 cli.py --view
```

#### List All Results
```bash
python3 cli.py --list
```

#### Non-Interactive Mode
```bash
python3 cli.py \
  --project "E-Commerce API" \
  --description "Build REST API with authentication and products" \
  --output results.json
```

#### Disable Colors
```bash
python3 cli.py --no-color
```

---

### Using Python Code Directly

#### Basic Usage

```python
from multi_agent_system import MultiAgentOrchestrator

# Create orchestrator
orchestrator = MultiAgentOrchestrator(
    project_name="My Project",
    project_description="Detailed project description..."
)

# Run pipeline (fully automated)
results = orchestrator.run_pipeline()

# Save results
orchestrator.save_results('my_results.json')

# Get summary
summary = orchestrator.get_summary()
print(summary)
```

#### Advanced Usage with Utilities

```python
from multi_agent_system import MultiAgentOrchestrator
from agent_utils import (
    InputValidator,
    ResultAnalyzer,
    OutputFormatter,
    ConfigBuilder,
)

# Validate input
is_valid, error = InputValidator.validate_project(
    "My Project",
    "Complete project description..."
)

if not is_valid:
    print(f"Validation error: {error}")
    exit(1)

# Create orchestrator
orchestrator = MultiAgentOrchestrator(
    project_name="My Project",
    project_description="..."
)

# Run pipeline
results = orchestrator.run_pipeline()

# Analyze results
summary = orchestrator.get_summary()
time_analysis = ResultAnalyzer.analyze_execution_time(summary)
token_analysis = ResultAnalyzer.analyze_token_usage(summary)

print(f"Total time: {time_analysis['total_time']:.2f}s")
print(f"Total tokens: {token_analysis['total_tokens']}")
print(f"Estimated cost: ${token_analysis['estimated_cost']}")

# Format output
formatted = OutputFormatter.format_json_output(summary)
print(formatted)
```

---

## Script Reference

### multi_agent_system.py

Main module containing core classes.

#### Classes

**AgentRole (Enum)**
- `TASK_MANAGER` - Analyzes requirements, creates tasks
- `DEVELOPER` - Implements code
- `TESTER` - Tests and validates
- `DEPLOYER` - Creates deployment plan

**AgentStatus (Enum)**
- `IDLE` - Agent is idle
- `WORKING` - Agent is executing
- `COMPLETED` - Agent completed successfully
- `FAILED` - Agent failed

**AgentState (Dataclass)**
- `role` - Agent's role
- `status` - Current status
- `output` - Agent's output
- `error` - Error message if failed
- `execution_time` - Time taken to execute
- `tokens_used` - Tokens used by API

**Agent**
```python
agent = Agent(AgentRole.DEVELOPER, project_description)
output = agent.execute(task_input)
```

Methods:
- `execute(task_input)` - Execute agent's task
- `get_system_prompt()` - Get role-specific prompt
- `_prepare_input()` - Prepare input with context

**MultiAgentOrchestrator**
```python
orchestrator = MultiAgentOrchestrator(
    project_name="Project Name",
    project_description="Description..."
)
results = orchestrator.run_pipeline()
```

Methods:
- `run_pipeline()` - Execute complete pipeline
- `get_summary()` - Get execution summary
- `save_results(filename)` - Save results to JSON
- `_print_summary()` - Print summary to console

---

### agent_utils.py

Utility functions and helpers.

#### Classes

**InputValidator**
```python
is_valid, error = InputValidator.validate_project(name, description)
```

Methods:
- `validate_project_name()` - Validate project name
- `validate_project_description()` - Validate description
- `validate_project()` - Validate complete project

**OutputFormatter**
```python
text = OutputFormatter.truncate_text(long_text, 500)
json_obj = OutputFormatter.extract_json_from_text(text)
```

Methods:
- `truncate_text()` - Truncate text with ellipsis
- `extract_json_from_text()` - Extract JSON from text
- `extract_task_list()` - Extract task list from text
- `format_json_output()` - Format as pretty JSON

**ResultAnalyzer**
```python
time_analysis = ResultAnalyzer.analyze_execution_time(summary)
token_analysis = ResultAnalyzer.analyze_token_usage(summary)
completion = ResultAnalyzer.check_completion_status(summary)
```

Methods:
- `analyze_execution_time()` - Analyze time metrics
- `analyze_token_usage()` - Analyze token usage
- `check_completion_status()` - Check completion status

**ConfigBuilder**
```python
config = ConfigBuilder()
config.set_max_tokens(2048)
config.set_quality_standards(code_coverage_minimum=90)
final_config = config.build()
```

Methods:
- `set_model()` - Set Claude model
- `set_max_tokens()` - Set max tokens
- `set_agent_config()` - Set agent-specific config
- `set_quality_standards()` - Set quality standards
- `build()` - Build final configuration

**ReportGenerator**
```python
text_report = ReportGenerator.generate_text_report(name, summary, results)
json_report = ReportGenerator.generate_json_report(name, summary, results)
```

Methods:
- `generate_text_report()` - Generate text report
- `generate_json_report()` - Generate JSON report

---

### cli.py

Command-line interface.

#### Functions

**check_api_key()** - Verify API key is set

**select_template()** - Let user select project template

**get_project_input()** - Get project name and description interactively

**confirm_execution()** - Confirm before running pipeline

**run_pipeline()** - Execute the pipeline

**analyze_results()** - Analyze and display results

**view_results()** - View saved results

**list_results()** - List all saved results

**main()** - Main CLI entry point

#### Usage Examples

```bash
# Interactive mode
python3 cli.py

# View latest results
python3 cli.py --view

# List all results
python3 cli.py --list

# Non-interactive with options
python3 cli.py --project "API" --description "REST API" --output api_results.json

# Disable colors
python3 cli.py --no-color
```

---

### run.py

Simple quick-start runner.

```bash
python3 run.py
```

Prompts for:
1. Project name
2. Project description
3. Confirmation
4. Runs pipeline
5. Saves results

---

## Examples

### Example 1: Simple API Project

```python
from multi_agent_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator(
    project_name="Todo List API",
    project_description="""
    Build a simple REST API for a todo list application with:
    - User authentication using JWT
    - Create, read, update, delete todos
    - Database persistence with PostgreSQL
    - Error handling and validation
    - API documentation
    """
)

orchestrator.run_pipeline()
orchestrator.save_results('todo_api_results.json')
```

### Example 2: Web Application

```python
from multi_agent_system import MultiAgentOrchestrator

project = {
    "name": "Blog Platform",
    "description": """
    Build a complete blog platform with:
    - User authentication and profiles
    - Blog post creation and management
    - Comments system
    - Search functionality
    - Admin dashboard
    - Frontend and backend
    """
}

orchestrator = MultiAgentOrchestrator(
    project_name=project["name"],
    project_description=project["description"]
)

results = orchestrator.run_pipeline()
orchestrator.save_results()
```

### Example 3: With Analysis

```python
from multi_agent_system import MultiAgentOrchestrator
from agent_utils import ResultAnalyzer

orchestrator = MultiAgentOrchestrator(
    project_name="E-Commerce API",
    project_description="REST API for e-commerce platform..."
)

results = orchestrator.run_pipeline()
summary = orchestrator.get_summary()

# Analyze
time_analysis = ResultAnalyzer.analyze_execution_time(summary)
token_analysis = ResultAnalyzer.analyze_token_usage(summary)
completion = ResultAnalyzer.check_completion_status(summary)

print(f"Execution Time: {time_analysis['total_time']:.2f}s")
print(f"Tokens Used: {token_analysis['total_tokens']}")
print(f"Completion: {completion['completion_rate']}%")
print(f"Success: {completion['success']}")

orchestrator.save_results()
```

### Example 4: Non-Interactive

```bash
python3 cli.py \
  --project "Data Pipeline" \
  --description "ETL pipeline for data warehouse" \
  --output data_pipeline.json
```

---

## Troubleshooting

### Issue: API Key Not Found

**Error:**
```
❌ ERROR: ANTHROPIC_API_KEY environment variable not set!
```

**Solution:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
# Verify it's set
echo $ANTHROPIC_API_KEY
```

### Issue: Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'anthropic'
```

**Solution:**
```bash
pip install anthropic
# Or install all requirements
pip install -r requirements.txt
```

### Issue: Timeout or Slow Response

**Problem:** Pipeline takes longer than expected

**Solutions:**
1. Check internet connection
2. Check if API is responding (curl https://api.anthropic.com)
3. Try simpler project description
4. Increase timeout in code

```python
# Modify max_tokens in multi_agent_system.py
# model="claude-opus-4-20250805",
# max_tokens=2048,  # Reduce from 4096
```

### Issue: API Errors

**Error:**
```
API Error: rate_limit_exceeded
```

**Solution:**
- Wait before retrying
- Check API quota on console.anthropic.com
- Upgrade to higher tier if needed

### Issue: Results Not Saved

**Error:**
```
Error saving results: Permission denied
```

**Solution:**
```bash
# Check permissions
ls -la pipeline_results.json

# Or specify different location
python3 cli.py --output /tmp/results.json
```

---

## File Structure

```
project/
├── multi_agent_system.py    # Core system (400+ lines)
├── agent_utils.py            # Utilities (300+ lines)
├── cli.py                    # CLI interface (400+ lines)
├── run.py                    # Simple runner (50+ lines)
├── requirements.txt          # Dependencies
└── pipeline_results.json     # Generated results (output)
```

---

## Performance Tips

1. **Reduce project description length**
   - Shorter descriptions run faster
   - Focus on key requirements

2. **Use templates**
   - Pre-built templates are optimized
   - Faster execution than custom

3. **Monitor token usage**
   - Check results for token count
   - Optimize prompts if too high

4. **Batch multiple projects**
   - Run several in sequence
   - Costs less than parallel

---

## Security Notes

- **Never commit API key to git**
- **Use environment variables**
- **Keep .env files in .gitignore**
- **Rotate keys periodically**
- **Don't share results with sensitive data**

---

## Getting Help

1. Check this guide (you're reading it!)
2. Review example usage
3. Check error messages carefully
4. Look at saved results file
5. Read inline code comments

---

## Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Set API key: `export ANTHROPIC_API_KEY="sk-ant-..."`
3. Run first pipeline: `python3 cli.py`
4. Review results: `python3 cli.py --view`
5. Customize and explore!

---

**Happy automating!** 🚀
