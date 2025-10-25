# VS Code Setup Guide

This project includes comprehensive VS Code configuration for an optimal Django development experience.

## 🚀 Quick Start (3 Steps)

### 1️⃣ Install Recommended Extensions

When you first open this project in VS Code, you'll see a notification:

> **This workspace has extension recommendations**
>
> [Install All] [Show Recommendations] [Ignore]

Click **"Install All"** to install all recommended extensions automatically.

**Or manually:**
1. Press `Ctrl+Shift+X` to open Extensions
2. Type `@recommended` in the search box
3. Install all workspace recommendations

### 2️⃣ Select Python Interpreter

1. Press `Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose: `./venv/bin/python`

### 3️⃣ You're Ready! 🎉

Try running a task:
- Press `Ctrl+Shift+P`
- Type: `Tasks: Run Task`
- Select: `Django: Run Server`

Your Django server should start at http://127.0.0.1:8000

---

## 📋 Common Tasks

### Quick Access

Press `Ctrl+Shift+P` then type `task` to see all tasks.

### Most Used Tasks

| What to Do | Task Name |
|------------|-----------|
| 🚀 Start Django server | `Django: Run Server` |
| 🧪 Run all tests | `Test: Run All Tests` |
| 🧪 Run tests (fast) | `Test: Run Fast Tests (No Coverage)` |
| 📊 Generate coverage report | `Test: Generate Coverage Report` |
| 🔍 Run linters | `Lint: Run All Linters` |
| ✨ Format code | `Format: All (Black + isort)` |
| 🗄️ Make migrations | `Django: Make Migrations` |
| 🗄️ Apply migrations | `Django: Migrate` |
| 👤 Create superuser | `Django: Create Superuser` |
| 🐚 Open Django shell | `Django: Shell` |
| 📚 Open Swagger docs | `Docs: Open Swagger UI` |

---

## 🐛 Debugging

### Start Debugging

1. **Set a breakpoint** - Click in the gutter next to any line number
2. **Press `F5`** - This opens the debug menu
3. **Select a configuration**:
   - `Django: Run Server` - Debug the Django server
   - `Python: Debug Tests` - Debug all tests
   - `Python: Debug Current Test File` - Debug open test file

### Debug Controls

| Key | Action |
|-----|--------|
| `F5` | Start/Continue |
| `F9` | Toggle Breakpoint |
| `F10` | Step Over |
| `F11` | Step Into |
| `Shift+F11` | Step Out |
| `Shift+F5` | Stop |

### Example: Debug a View

```python
# In api/views.py
def list(self, request, *args, **kwargs):
    breakpoint()  # Or click in gutter to set breakpoint
    return super().list(request, *args, **kwargs)
```

1. Set breakpoint in the view
2. Press `F5` → Select "Django: Run Server"
3. Make a request to the endpoint in your browser
4. VS Code pauses at your breakpoint!

---

## ⚙️ Configuration Files

All VS Code configuration is in the `.vscode/` directory:

| File | Purpose |
|------|---------|
| `settings.json` | Workspace settings (formatting, linting, Python config) |
| `tasks.json` | Runnable tasks (30+ Django/testing/linting tasks) |
| `launch.json` | Debug configurations (10+ debugging scenarios) |
| `extensions.json` | Recommended extensions list |
| `README.md` | Detailed documentation |

**Note:** The `.vscode/` folder is in `.gitignore` so each developer can customize their setup.

---

## 🎯 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Shift+P` | Command Palette (access everything) |
| `Ctrl+Shift+B` | Run Build Task |
| `F5` | Start Debugging |
| `Ctrl+` ` | Toggle Terminal |
| `Ctrl+Shift+` ` | New Terminal |
| `Shift+Alt+F` | Format Document |
| `Ctrl+K Ctrl+F` | Format Selection |
| `Shift+Alt+O` | Organize Imports |

---

## 📦 Essential Extensions

Auto-installed via workspace recommendations:

### Python Development
- **Python** - Core Python support
- **Pylance** - Fast IntelliSense
- **Black Formatter** - Code formatting
- **isort** - Import sorting
- **Flake8** - Linting
- **Mypy** - Type checking

### Django
- **Django** - Template syntax highlighting
- **Django Snippets** - Code snippets

### Testing
- **Coverage Gutters** - See coverage in editor
- **Python Test Adapter** - Visual test explorer

### API Development
- **REST Client** - Test APIs from VS Code
- **OpenAPI (Swagger)** - API schema support
- **Thunder Client** - API testing

### Git
- **GitLens** - Enhanced Git integration
- **Git Graph** - Visualize Git history

---

## 🔧 Settings Highlights

### Auto-Format on Save
Python files are automatically formatted with Black and isort when you save.

```python
# Before save
import sys
import os
import django


def my_function(  ):
    pass
```

```python
# After save (automatically formatted)
import os
import sys

import django


def my_function():
    pass
```

### Type Checking
Mypy runs automatically and shows errors inline:

```python
def add(a: int, b: int) -> int:
    return a + b

result = add("hello", "world")  # ❌ Mypy error shown inline
```

### Test Discovery
Tests are automatically discovered. Click the beaker icon in the sidebar to see all tests.

---

## 🆘 Troubleshooting

### "Python interpreter not found"
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements/development.txt

# Restart VS Code
```

### "Tasks not working"
1. Ensure venv is activated in terminal
2. Check that `./venv/bin/python` exists
3. Try: `Ctrl+Shift+P` → "Python: Select Interpreter"

### "Linters not running"
```bash
# Activate venv and install linters
source venv/bin/activate
pip install -r requirements/development.txt

# Restart VS Code
```

### "Debugger not stopping at breakpoints"
1. Ensure you've selected a debug configuration (F5)
2. Check that breakpoint is on an executable line (not comment/blank)
3. Try disabling "justMyCode" in launch configuration

---

## ✅ Verification Checklist

Run through these to verify your setup:

- [ ] Open project in VS Code
- [ ] See notification to install extensions → Click "Install All"
- [ ] Select Python interpreter: `./venv/bin/python`
- [ ] Open integrated terminal (Ctrl+`) → Should show `(venv)` prefix
- [ ] Run task: `Test: Run All Tests` → 68 tests should pass
- [ ] Run task: `Django: Run Server` → Server starts at http://127.0.0.1:8000
- [ ] Open http://127.0.0.1:8000/swagger/ → Swagger UI loads
- [ ] Set breakpoint in `api/views.py`
- [ ] Press F5 → "Django: Run Server" → Breakpoint hits
- [ ] Format a Python file (Shift+Alt+F) → Uses Black

If all checks pass: ✨ **You're all set!** ✨

---

## 📚 Additional Resources

- **Full Documentation**: See `.vscode/README.md`
- **Available Tasks**: Press `Ctrl+Shift+P` → "Tasks: Run Task"
- **Debug Configs**: Press `F5` to see all options
- **Makefile Commands**: Run `make help` in terminal

---

## 💡 Pro Tips

1. **Quick Task Access**: Type `Ctrl+Shift+P` → `task` → fuzzy search
2. **Test Explorer**: Use sidebar beaker icon for visual test running
3. **Coverage Inline**: Install Coverage Gutters extension to see coverage in editor
4. **Multiple Terminals**: Use `Ctrl+Shift+`` to create multiple terminals
5. **Workspace File**: Open `django-financial-api.code-workspace` for compound debug configs

---

**Need Help?** Check `.vscode/README.md` for comprehensive documentation.

**Happy Coding!** 🚀
