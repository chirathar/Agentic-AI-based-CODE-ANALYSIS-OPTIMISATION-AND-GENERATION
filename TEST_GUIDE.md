# Testing Guide - Optimization Output & Progress Tracking

## What Was Fixed

✅ **Streaming Response** - Progress bar updates in real-time (0%, 10%, 20%... 100%)
✅ **Better Parsing** - Quality, Performance, and Refactoring issues now extracted properly
✅ **Auto Display** - Results displayed automatically as they arrive
✅ **Enhanced UI** - Professional progress bar with percentage and status
✅ **Error Handling** - Better error messages and recovery

## How to Test

### 1. Open the Frontend
```
http://localhost:5000
```

### 2. Test with Sample Code
Copy and paste this Python code into the analyzer:

```python
def calculate_fibonacci(n):
    if n <= 1:
        return n
    else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)

def process_data(input_list):
    result = []
    for item in input_list:
        if item > 0:
            if item % 2 == 0:
                if item < 100:
                    result.append(item)
    return result

class DataProcessor:
    def __init__(self):
        self.data = []
    
    def add(self, value):
        self.data.append(value)
    
    def process(self):
        processed = []
        for d in self.data:
            processed.append(d * 2)
        return processed
```

### 3. Click "Analyze Code" Button
You should see:
- ✅ Metrics appear instantly (LOC, LLOC, Comments, Complexity)
- ✅ Progress bar appears below results
- ✅ Progress goes: 0% → 10% → 20% → 30%... → 100%
- ✅ Status messages: "Building prompt..." → "Connecting to Ollama..." → etc.

### 4. View Results Tabs
Once optimization completes (100%):

**Quality Issues Tab** ✅
- Shows cyclomatic complexity for each function
- `calculate_fibonacci()` - Complexity: likely high (recursive)
- `process_data()` - Complexity: 3+ (nested conditions)
- `DataProcessor.process()` - Complexity: 1 (simple)

**Performance Tab** ✅  
- Should show suggestions like:
  - "Use memoization for recursive fibonacci"
  - "Replace nested loops with list comprehension"
  - "Consider algorithmic optimization"

**Refactoring Tab** ✅
- Should show suggestions like:
  - "Extract nested condition into separate function"
  - "Use more descriptive variable names"
  - "Add type hints to functions"

**Optimized Code Tab** ✅
- Complete refactored code with all improvements

### 5. Test Export
- Click "Export" button → Downloads `analysis_*.json`
- Click "Copy" button → Copies optimized code to clipboard

## What Each Component Does

### Progress Bar
```
LLM Processing [==================>    ] 45%
Parsing response...
```

**Progress Stages:**
- 10% - Building optimization prompt
- 20% - Connecting to Ollama  
- 30% - Sending request to LLM
- 60% - Response received, parsing
- 80% - Processing quality issues
- 85% - Processing performance improvements
- 90% - Processing refactoring suggestions
- 100% - Complete

### API Response Format
The `/api/optimize` endpoint returns Server-Sent Events (SSE):

```javascript
data: {"progress": 10, "status": "processing", "section": "Building prompt..."}
data: {"progress": 20, "status": "processing", "section": "Connecting to Ollama..."}
...
data: {"progress": 100, "status": "complete", "section": "Optimization complete!", "content": "==== QUALITY ISSUES ====\n..."}
```

## Troubleshooting

### Progress Bar Not Showing?
1. Check browser console (F12)
2. Look for JavaScript errors
3. Ensure `/api/optimize` returns 200 OK

**Fix:** Refresh the page (Ctrl+R) and try again

### No Quality/Performance/Refactoring Issues?
1. Check if Ollama is running
   ```bash
   ollama serve
   ollama run phi3
   ```

2. Look at browser console for parsing errors
3. Check LLM response format

**Fix:** Ensure Ollama is responding properly

### Optimization Takes Too Long?
- Ollama processing depends on model and hardware
- Typical time: 5-30 seconds
- Check terminal for Ollama errors

### Code Output is Empty?
1. Ensure Ollama is running
2. Check model is available: `ollama list`
3. Try simpler code first

**Fix:** Restart Ollama:
```bash
ollama serve
ollama run phi3
```

## Debug Mode

To see detailed logs:

### Browser Console (F12)
Opens developer tools - shows:
- Network requests to `/api/optimize`
- Progress update logs
- JavaScript errors
- Parsed issues count

### Flask Terminal
Shows:
- HTTP request logs
- Python errors
- Connection status

## Performance Notes

**Fast (Metrics Only):** ~100ms
- Lines of Code: Instant
- Complexity Analysis: Instant
- Halstead Metrics: Instant

**Slow (with LLM):** 5-30 seconds
- LLM Processing: 5-20 seconds (depends on hardware)
- Response Parsing: ~100ms
- UI Updates: Real-time with progress

## Expected Output Example

### Quality Issues (from cyclomatic complexity)
```
calculate_fibonacci() - Complexity: 2
  Line 1: Recursive function with simple condition
  Recommendation: Good complexity level - maintainable code.

process_data() - Complexity: 3  
  Line 6: Nested conditions increase complexity
  Recommendation: Consider refactoring to reduce complexity.
```

### Performance Improvements (from LLM)
```
⚠️ Inefficient Recursion
  Recursive fibonacci has exponential time complexity O(2^n)
  Suggestion: Use memoization or dynamic programming

⚠️ Nested Conditions
  Triple nested if statements reduce readability
  Suggestion: Use list comprehension for filtering
```

### Refactoring Suggestions (from LLM)
```
ℹ️ Missing Type Hints
  Functions lack type annotations
  Suggestion: Add type hints for better IDE support

ℹ️ Unclear Variable Names
  Variable names could be more descriptive  
  Suggestion: Use meaningful names like 'result_list'
```

## Files Changed

- **app.py** - Streaming endpoint with progress tracking
- **app.js** - SSE handling, parsing improvements, progress display
- **style.css** - Progress bar styling

## Testing Checklist

- [ ] Server starts without errors
- [ ] Frontend loads at http://localhost:5000
- [ ] Can paste code
- [ ] Can upload .py files
- [ ] Metrics display after analyze
- [ ] Progress bar shows (0%-100%)
- [ ] Quality Issues tab shows functions
- [ ] Performance tab shows suggestions
- [ ] Refactoring tab shows suggestions  
- [ ] Optimized Code tab shows code
- [ ] Export works (JSON download)
- [ ] Copy works (code clipboard)
- [ ] Status messages appear

## Next Steps

1. **Test with your own code files** - Upload different Python files
2. **Note timing** - How long does optimization take on your system?
3. **Check coverage** - Are all issues being detected?
4. **Verify accuracy** - Do suggestions make sense?

## Support

If something isn't working:
1. Check terminal for Flask errors
2. Open F12 browser console for JavaScript errors
3. Verify Ollama is running
4. Check network tab (F12) for API responses
5. Look at the output format in "Network" tab
