from code_analyzer import CodeAnalyzer
from llm_optimizer import LLMOptimizer

def read_code_from_file(file_path: str) -> str:
    """Read code from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return ""

def main():
    # Get code from file or user input
    file_path = input("Enter the path to your Python file: ")
    code = read_code_from_file(file_path)
    
    if not code:
        print("No code to analyze. Exiting...")
        return
    
    # Analyze code
    print("\nAnalyzing code...")
    analyzer = CodeAnalyzer(code)
    metrics = analyzer.get_all_metrics()
    
    # Display metrics
    print("\n=== Code Analysis Results ===")
    print(f"Lines of Code: {metrics['raw'].get('loc', 'N/A')}")
    print(f"Logical Lines of Code: {metrics['raw'].get('lloc', 'N/A')}")
    print(f"Comments: {metrics['raw'].get('comments', 'N/A')}")
    
    print("\nCyclomatic Complexity:")
    for func, data in metrics['cyclomatic'].items():
        print(f"  {func}(): {data.get('complexity', 'N/A')} (line {data.get('line', 'N/A')})")
    
    # Get optimization suggestions
        print("\nGenerating optimized code...")
        optimizer = LLMOptimizer()
        suggestions = optimizer.get_optimization_suggestions(code, metrics)
        print("\n=== Optimized Code ===\n")
        print(suggestions)
        
        # Save optimized code to file
        save = input("\nWould you like to save the optimized code? (y/n): ").lower()
        if save == 'y':
            output_file = input("Enter output file name (default: optimized_code.py): ").strip()
            if not output_file:
                output_file = "optimized_code.py"
            
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(suggestions)
                print(f"\nOptimized code saved to: {output_file}")
            except Exception as e:
                print(f"Error saving file: {e}")

if __name__ == "__main__":
    main()