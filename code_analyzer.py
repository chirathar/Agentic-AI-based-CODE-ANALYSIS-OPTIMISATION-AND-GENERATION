import ast
from radon.complexity import cc_visit
from radon.metrics import h_visit
from radon.raw import analyze


class CodeAnalyzer:
    def __init__(self, code: str):
        self.code = code
        self.tree = ast.parse(code)

    def get_cyclomatic_complexity(self):
        """Calculate cyclomatic complexity of functions/methods."""
        results = {}
        try:
            blocks = cc_visit(self.code)

            for block in blocks:
                results[block.name] = {
                    'complexity': block.complexity,
                    'line': block.lineno
                }

        except Exception as e:
            print(f"Error calculating complexity: {e}")

        return results

    def get_halstead_metrics(self):
        """Calculate Halstead metrics."""
        try:
            halstead = h_visit(self.code)

            return {
                'vocabulary': halstead.total.vocabulary,
                'length': halstead.total.length,
                'volume': round(halstead.total.volume, 2),
                'difficulty': round(halstead.total.difficulty, 2),
                'effort': round(halstead.total.effort, 2)
            }

        except Exception as e:
            print(f"Error in Halstead metrics: {e}")
            return {}

    def get_raw_metrics(self):
        """Get basic code metrics."""
        try:
            raw = analyze(self.code)
            return {
                'loc': raw.loc,
                'lloc': raw.lloc,
                'comments': raw.comments
            }
        except Exception as e:
            print(f"Error in raw metrics: {e}")
            return {}

    def get_all_metrics(self):
        """Get all metrics in one call."""
        return {
            'cyclomatic': self.get_cyclomatic_complexity(),
            'halstead': self.get_halstead_metrics(),
            'raw': self.get_raw_metrics()
        }


def main():
    # Example usage
    sample_code = """
def calculate_sum(numbers):
    total = 0
    for num in numbers:
        total += num
    return total
"""
    
    analyzer = CodeAnalyzer(sample_code)
    metrics = analyzer.get_all_metrics()
    
    print("Code Analysis Results:")
    print(f"Cyclomatic Complexity: {metrics['cyclomatic']}")
    print(f"Halstead Metrics: {metrics['halstead']}")
    print(f"Raw Metrics: {metrics['raw']}")


if __name__ == '__main__':
    main()