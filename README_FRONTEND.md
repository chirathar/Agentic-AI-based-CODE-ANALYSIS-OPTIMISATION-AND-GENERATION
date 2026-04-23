# Python Code Analyzer & Optimizer Frontend

A modern, dark-themed web interface for analyzing and optimizing Python code using local metrics and LLM-powered suggestions.

## 🚀 Quick Start

The frontend is running at **http://localhost:5000**

Start the Flask backend:
```powershell
cd c:\Users\muthu\SEPM
.\.venv\Scripts\Activate.ps1
python app.py
```

## ✨ Features

**Code Analysis**
- Lines of Code (LOC) metrics
- Logical Lines of Code (LLOC)  
- Comment analysis
- Cyclomatic Complexity per function
- Halstead metrics (Volume, Difficulty, Effort)

**Issue Detection**
- Quality issues with severity levels (High/Medium/Low)
- Performance optimization suggestions
- Code refactoring recommendations

**LLM-Powered Optimization**
- AI-powered code optimization using Ollama
- Automated improvement suggestions
- Full optimized code generation

**Results Display**
- Tabbed interface (Quality, Performance, Refactoring, Optimized Code)
- Detailed issue cards with actionable suggestions
- Code metrics summary dashboard
- Export analysis as JSON

## 📋 Usage

### 1. Input Code
- **Paste Code**: Enter Python code directly in the editor
- **Upload File**: Drag & drop or select a `.py` file

### 2. Analyze
Click "Analyze Code" button to:
1. Calculate code metrics
2. Analyze cyclomatic complexity
3. Get LLM optimization suggestions

### 3. Review Results
- **Quality Issues**: Cyclomatic complexity per function
- **Performance**: Optimization opportunities
- **Refactoring**: Code improvement suggestions
- **Optimized Code**: Full refactored code from LLM

### 4. Export
- **Export**: Save analysis as JSON
- **Copy**: Copy optimized code to clipboard

## 🔧 Requirements

### For Metrics Analysis (Always works)
- radon - Code metrics calculation
- Flask - Web server

### For Optimization Features (Optional but recommended)
Ollama must be running locally:

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run the model
ollama run phi3
```

## 📁 Project Structure

```
Frontend/
├── index.html          # HTML template
└── static/
    ├── app.js          # Frontend logic
    └── style.css       # Dark theme

app.py                  # Flask server
code_analyzer.py        # Metrics engine
llm_optimizer.py        # LLM integration
```

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Serve frontend |
| `/api/analyze` | POST | Analyze code & metrics |
| `/api/optimize` | POST | Get LLM optimization |
| `/api/health` | GET | Server health check |

## ⚙️ Setup

1. **Install dependencies:**
   ```bash
   pip install -r env/requirements.txt
   ```

2. **Start Flask server:**
   ```bash
   python app.py
   ```

3. **(Optional) Setup Ollama for optimization:**
   - Install Ollama from https://ollama.ai
   - Run: `ollama serve` in one terminal
   - Run: `ollama run phi3` in another terminal

## 🐛 Troubleshooting

**Frontend won't load?**
- Ensure Flask is running on port 5000
- Check: http://localhost:5000
- Look for errors in the terminal

**Optimization not working?**
- Ollama may not be running on localhost:11434
- Start Ollama: `ollama serve`
- Ensure phi3 model is available: `ollama run phi3`
- Metrics will still work even if Ollama fails

**Code analysis fails?**
- Check for valid Python syntax
- View browser console for details (F12)
- Ensure code doesn't have syntax errors

## 📝 Notes

- Analysis is performed locally on your machine
- LLM optimization requires Ollama (local, not cloud)
- Exported results are in JSON format
- Works with Python files of any size

   ```

## Running the Application

1. **Start the Flask server:**
   ```bash
   python app.py
   ```

2. **Open in browser:**
   Navigate to `http://localhost:5000`

3. **Analyze code:**
   - Paste Python code directly or upload a `.py` file
   - Click "Analyze Code" button
   - View results in different tabs

## Project Structure

```
SEPM/
├── app.py                    # Flask web server
├── code_analyzer.py          # Code analysis engine
├── llm_optimizer.py          # LLM-based optimization
├── main.py                   # CLI interface
├── Frontend/
│   ├── index.html           # Main page
│   └── static/
│       ├── style.css        # Styling
│       └── app.js           # JavaScript logic
└── env/
    └── requirements.txt     # Python dependencies
```

## Usage

### Input Methods
- **Paste Code**: Copy and paste Python code directly
- **Upload File**: Upload a `.py` file from your computer

### Analysis Results
The analysis displays results in four tabs:

1. **Quality Issues**: Code quality and best practice violations
2. **Performance**: Performance optimization suggestions
3. **Refactoring**: Code refactoring recommendations
4. **Optimized Code**: Full optimized version of your code

### Actions
- **Copy Code**: Copy the optimized code to clipboard
- **Export**: Download analysis results as JSON

## API Endpoints

### POST `/api/analyze`
Analyzes code and returns metrics and suggestions.

**Request:**
```json
{
  "code": "# Your Python code here"
}
```

**Response:**
```json
{
  "success": true,
  "metrics": {
    "raw": {...},
    "cyclomatic": {...},
    "halstead": {...}
  },
  "suggestions": "..."
}
```

## Troubleshooting

### Port Already in Use
If port 5000 is busy, modify `app.py`:
```python
app.run(debug=True, port=5001)  # Use different port
```

### FileNotFoundError for Templates
Ensure the file structure matches:
- `Frontend/index.html`
- `Frontend/static/style.css`
- `Frontend/static/app.js`

### CORS Errors
CORS is already enabled. If issues persist, check browser console for more details.

## Development

### Modifying Styles
Edit `Frontend/static/style.css` to customize the appearance.

### Extending JavaScript
Modify `Frontend/static/app.js` to add new features.

### Adding Backend Logic
Update `app.py` to add new API endpoints or modify existing ones.

## License

This project is part of SEPM coursework.

## Support

For issues or questions, please contact the development team.
