# System Requirements & Setup Guide

## 📋 Requirements

### Minimum System Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **Python**: 3.8 or higher
- **RAM**: 512 MB (minimum), 2GB (recommended)
- **Disk Space**: 500 MB for dependencies
- **Internet**: Good connection for API calls

### Network Requirements
- **API Access**: Can reach api.anthropic.com
- **No Proxy**: No corporate proxy blocking API calls (can be configured if needed)
- **Bandwidth**: 1 MB/s sufficient for API communication

### API Requirements
- **Anthropic API Key**: Required for Claude access
- **API Quota**: Sufficient tokens available
- **Rate Limits**: Default limits are sufficient for typical use

---

## 🚀 Installation

### Step 1: Install Python

**macOS:**
```bash
brew install python3
python3 --version  # Verify installation
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version  # Verify installation
```

**Windows (with WSL2):**
```bash
wsl --install
# Inside WSL2:
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```

### Step 2: Install Dependencies

```bash
# Create a virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install anthropic package
pip install anthropic
pip install anthropic --upgrade  # For latest version
```

### Step 3: Get Anthropic API Key

1. Visit https://console.anthropic.com
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (keep it secret!)

### Step 4: Set Environment Variable

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Permanent Setup (macOS/Linux):**
```bash
# Add to ~/.bashrc or ~/.zshrc
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

**Windows (Permanent):**
```powershell
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY","sk-ant-...","User")
```

### Step 5: Verify Installation

```bash
python3 -c "import anthropic; print('✓ Anthropic SDK installed')"
echo $ANTHROPIC_API_KEY  # Should show your API key (or part of it)
```

---

## 📂 File Structure

```
multi-agent-system/
├── README.md                      # Quick start guide
├── ARCHITECTURE.txt               # System architecture diagram
├── MULTI_AGENT_GUIDE.md          # Detailed documentation
├── EXAMPLES.md                    # Example projects and use cases
├── multi_agent_system.py         # Core Python backend
├── config.py                      # Configuration settings
├── quickstart.py                  # Quick-start CLI script
├── multi_agent_dashboard.jsx     # React dashboard (optional)
├── SYSTEM_SETUP.md               # This file
└── pipeline_results.json         # Generated output (after first run)
```

---

## 🏃 Quick Start

### Option 1: Using CLI (Recommended for beginners)

```bash
# Run the quick-start script
python3 quickstart.py

# Follow the prompts:
# Enter project name: My Project
# Enter description: Your project description
# Watch it execute!
```

### Option 2: Using Python Script

```python
# Create my_project.py
from multi_agent_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator(
    project_name="My Project",
    project_description="Your project description"
)

results = orchestrator.run_pipeline()
print(orchestrator.get_summary())
```

```bash
python3 my_project.py
```

### Option 3: Using React Dashboard

```jsx
// Import in your React app
import MultiAgentDashboard from './multi_agent_dashboard'

export default function App() {
  return <MultiAgentDashboard />
}
```

---

## ⚙️ Configuration

### Default Configuration
The system comes with sensible defaults. For basic use, no configuration needed!

### Customizing Agents

Edit `config.py`:

```python
# Change the developer's instructions
AGENT_PROMPTS["developer"] = """
You are a Developer with these specific requirements:
- Use TypeScript only
- 100% test coverage required
- Follow strict linting rules
..."""

# Change quality standards
QUALITY_STANDARDS = {
    "code_coverage_minimum": 95,  # 95% instead of 80%
    "max_code_issues_allowed": 0,  # Zero issues allowed
}

# Change execution settings
EXECUTION_CONFIG = {
    "max_retries": 5,  # More retries
    "agent_timeout_seconds": 180,  # Longer timeout
}
```

### API Configuration

```python
# In config.py
API_CONFIG = {
    "model": "claude-opus-4-20250805",  # Latest model
    "max_tokens": 4096,  # Tokens per request
    "temperature": 0.7,  # Creativity level (0-1)
    "timeout_seconds": 120  # Max wait time
}
```

---

## 🧪 Testing the Installation

### Test 1: API Key Works

```python
import anthropic
import os

api_key = os.getenv("ANTHROPIC_API_KEY")
if api_key:
    print("✓ API key found")
    client = anthropic.Anthropic(api_key=api_key)
    print("✓ Client initialized")
else:
    print("✗ API key not found")
```

### Test 2: Simple API Call

```python
import anthropic

client = anthropic.Anthropic()
response = client.messages.create(
    model="claude-opus-4-20250805",
    max_tokens=100,
    messages=[{"role": "user", "content": "Hello!"}]
)
print("✓ API call successful")
print(response.content[0].text)
```

### Test 3: Run Sample Pipeline

```bash
python3 quickstart.py
# Enter simple project:
# Name: "Hello World API"
# Description: "Simple REST API that returns 'Hello World'"
# Watch it complete!
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'anthropic'"

**Solution:**
```bash
# Install the package
pip install anthropic

# Or upgrade
pip install --upgrade anthropic

# Verify
python3 -c "import anthropic; print('OK')"
```

---

### Issue: "ANTHROPIC_API_KEY not found"

**Solution:**
```bash
# Check if variable is set
echo $ANTHROPIC_API_KEY

# If empty, set it
export ANTHROPIC_API_KEY="sk-ant-..."

# Verify
python3 -c "import os; print(os.getenv('ANTHROPIC_API_KEY'))"
```

---

### Issue: "Invalid API Key"

**Solution:**
1. Check your API key is correct
2. Make sure it's not expired
3. Verify on https://console.anthropic.com
4. Create a new key if needed

---

### Issue: "Rate limit exceeded"

**Solution:**
- Wait a few minutes before retrying
- Check API usage on console.anthropic.com
- Upgrade to higher tier if needed

---

### Issue: "Timeout - API call took too long"

**Solution:**
```python
# In config.py, increase timeout
EXECUTION_CONFIG = {
    "agent_timeout_seconds": 180  # Increase from 120
}

# Or reduce project scope
# (use simpler project description)
```

---

### Issue: "Pipeline produces poor output"

**Solution:**

1. **Be more specific in description:**
   ```python
   # Bad description
   "Build an API"
   
   # Good description
   "Build a REST API for e-commerce with:
   - User authentication with JWT
   - Product catalog with search
   - Shopping cart functionality
   - Order processing
   Using Node.js and PostgreSQL"
   ```

2. **Modify agent prompts:**
   ```python
   # In config.py
   AGENT_PROMPTS["developer"] += """
   Important requirements:
   - Use TypeScript exclusively
   - Follow strict error handling
   - Add comprehensive logging
   """
   ```

3. **Increase quality standards:**
   ```python
   QUALITY_STANDARDS = {
       "code_coverage_minimum": 95,
       "max_code_issues_allowed": 0,
   }
   ```

---

## 📊 Performance Optimization

### For Better Performance

1. **Use shorter descriptions**
   ```python
   # Instead of 1000 words, use 200-300 words
   # Focus on key requirements only
   ```

2. **Reduce scope**
   ```python
   # Instead of: "Build complete e-commerce platform"
   # Use: "Build product catalog REST API"
   ```

3. **Set tighter constraints**
   ```python
   description = """
   Build API with constraints:
   - Max response time: 200ms
   - Max endpoints: 10
   - Stack: Node.js + PostgreSQL
   """
   ```

### For Cost Optimization

1. **Use Sonnet model** (faster, cheaper)
   ```python
   API_CONFIG["model"] = "claude-sonnet-4-20250514"
   ```

2. **Reduce max_tokens**
   ```python
   API_CONFIG["max_tokens"] = 2048  # Reduce from 4096
   ```

3. **Reuse outputs** (avoid re-running)
   ```python
   # Save results and reuse for multiple projects
   with open("cached_output.json") as f:
       cached_results = json.load(f)
   ```

---

## 🔐 Security Best Practices

### API Key Security

1. **Never commit API key to git:**
   ```bash
   # Add to .gitignore
   echo "ANTHROPIC_API_KEY" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variable (not hardcoded):**
   ```python
   # Bad:
   api_key = "sk-ant-..."
   
   # Good:
   import os
   api_key = os.getenv("ANTHROPIC_API_KEY")
   ```

3. **Never share API key in:**
   - Slack messages
   - GitHub issues
   - Public repositories
   - Email

4. **Rotate keys regularly:**
   - Generate new key monthly
   - Revoke old keys
   - Monitor usage

### Output Security

1. **Sanitize generated code before use:**
   - Review for security issues
   - Check for hardcoded secrets
   - Verify dependencies

2. **Store results securely:**
   - Don't commit to public repos
   - Use .gitignore for sensitive output
   - Encrypt if storing sensitive data

3. **Audit generated code:**
   - Run security scanners
   - Check for vulnerabilities
   - Review dependencies

---

## 📈 Monitoring & Logging

### View Logs

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Now logs will show detailed info
```

### Track Execution

```python
results = orchestrator.run_pipeline()
summary = orchestrator.get_summary()

print(f"Status: {summary['status']}")
print(f"Total Results: {summary['total_results']}")

for agent_name, status in summary['agents_status'].items():
    print(f"{agent_name}: {status['status']} ({status['execution_time']:.2f}s)")
```

### Save Results

```python
import json

results = orchestrator.run_pipeline()

# Save to file
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)

# Load later
with open("results.json") as f:
    results = json.load(f)
```

---

## 🔄 Updating

### Update Anthropic SDK

```bash
pip install --upgrade anthropic
```

### Check Version

```bash
pip show anthropic
# Shows: Version: X.Y.Z
```

### Breaking Changes

Check release notes before updating:
https://github.com/anthropics/anthropic-sdk-python/releases

---

## 🆘 Support

### Getting Help

1. **Documentation**: Read MULTI_AGENT_GUIDE.md
2. **Examples**: Check EXAMPLES.md
3. **Config**: Review comments in config.py
4. **Errors**: Read error messages carefully
5. **Anthropic Docs**: https://docs.anthropic.com

### Common Issues Reference

| Issue | Solution | Docs |
|-------|----------|------|
| API key not found | Set ANTHROPIC_API_KEY env var | [Setup Guide](#step-4-set-environment-variable) |
| Module not found | pip install anthropic | [Installation](#step-2-install-dependencies) |
| Rate limited | Wait or check quota | [API Requirements](#api-requirements) |
| Poor output | Be more specific | [Optimization](#performance-optimization) |
| High cost | Use Sonnet model | [Cost Optimization](#for-cost-optimization) |

---

## ✅ Verification Checklist

Before running your first pipeline, verify:

- [ ] Python 3.8+ installed (`python3 --version`)
- [ ] anthropic package installed (`pip show anthropic`)
- [ ] API key available (`echo $ANTHROPIC_API_KEY`)
- [ ] API key has quota (check console.anthropic.com)
- [ ] Internet connection working
- [ ] Files in correct location (README.md, config.py, etc.)
- [ ] config.py can be opened without errors (`python3 -c "import config"`)
- [ ] Test API call works (run test script above)

---

## 🎓 Learning Resources

### Understanding the System
1. Start with README.md for overview
2. Read ARCHITECTURE.txt for system design
3. Review MULTI_AGENT_GUIDE.md for details
4. Check EXAMPLES.md for real projects

### Using the System
1. Run `python3 quickstart.py` with simple project
2. Review generated results
3. Try with your own project
4. Customize config.py as needed

### Advanced Usage
1. Chain multiple pipelines
2. Integrate with external systems
3. Add custom validation
4. Build custom UI

---

## 📝 Next Steps

1. **Install**: Complete installation steps above
2. **Test**: Run the verification tests
3. **Explore**: Try the quick-start guide
4. **Create**: Run your first pipeline
5. **Customize**: Modify config for your needs
6. **Integrate**: Use in your projects

---

## 🎉 Ready?

```bash
# Everything set up? Run your first pipeline!
python3 quickstart.py

# or

python3 -c "
from multi_agent_system import MultiAgentOrchestrator

orchestrator = MultiAgentOrchestrator(
    project_name='My First Project',
    project_description='Build a simple REST API for a todo list'
)

orchestrator.run_pipeline()
print('✅ Pipeline complete!')
"
```

---

**You're all set! Happy automating! 🚀**
