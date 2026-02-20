#!/usr/bin/env python3
"""
Analyze marker distribution across test suite
"""
import ast
from pathlib import Path
from collections import defaultdict
from typing import Dict, Set


def extract_markers_from_file(filepath: Path) -> Dict[str, Set[str]]:
    """Parse Python file and extract pytest markers"""
    markers_by_test = {}

    try:
        with open(filepath, 'r') as f:
            tree = ast.parse(f.read())

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if node.name.startswith('test_'):
                    markers = set()
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Attribute):
                            # @pytest.mark.smoke
                            if (isinstance(decorator.value, ast.Attribute) and
                                decorator.value.attr == 'mark'):
                                markers.add(decorator.attr)

                    if markers:
                        markers_by_test[node.name] = markers

    except Exception as e:
        print(f"Error parsing {filepath}: {e}")

    return markers_by_test


def main():
    """Generate marker statistics"""
    tests_dir = Path(__file__).parent / "tests"

    all_markers = defaultdict(int)
    test_count = 0
    marker_combinations = defaultdict(int)

    print("\n" + "="*60)
    print("📊 MARKER DISTRIBUTION ANALYSIS")
    print("="*60)

    for test_file in tests_dir.glob("test_*.py"):
        print(f"\n📄 Analyzing: {test_file.name}")
        markers_by_test = extract_markers_from_file(test_file)

        for test_name, markers in markers_by_test.items():
            test_count += 1
            marker_combo = ", ".join(sorted(markers))
            marker_combinations[marker_combo] += 1

            print(f"  • {test_name}: {marker_combo}")

            for marker in markers:
                all_markers[marker] += 1

    # Summary statistics
    print(f"\n{'='*60}")
    print("SUMMARY STATISTICS")
    print(f"{'='*60}")
    print(f"Total tests: {test_count}")
    print(f"\nMarker usage:")

    for marker, count in sorted(all_markers.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / test_count) * 100
        print(f"  • {marker:15} : {count:2} tests ({percentage:.1f}%)")

    print(f"\nCommon combinations:")
    for combo, count in sorted(marker_combinations.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"  • [{combo}] : {count} tests")


if __name__ == "__main__":
    main()