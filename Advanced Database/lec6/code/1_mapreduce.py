from functools import reduce
from typing import List, Dict, Any

def functional_patterns():
    """
    Demonstrating functional programming patterns with map and reduce.
    """
    print("\n=== FUNCTIONAL PROGRAMMING PATTERNS ===")
    
    # Pattern 1: Map-Reduce pattern (like Hadoop)
    data = ["hello world", "functional programming", "map reduce example"]
    
    # Map phase: Split into words and create (word, 1) pairs
    def mapper(text):
        words = text.lower().split()
        return [(word, 1) for word in words]
    
    mapped_data = list(map(mapper, data))
    print("Mapped data:", mapped_data)
    
    # Flatten the list of lists
    flat_data = reduce(lambda x, y: x + y, mapped_data)
    print("Flattened data:", flat_data)
    
    # Reduce phase: Sum counts by word
    def reducer(acc, item):
        word, count = item
        if word not in acc:
            acc[word] = 0
        acc[word] += count
        return acc
    
    word_counts = reduce(reducer, flat_data, {})
    print("Word counts:", word_counts)
    print()
    
    # Pattern 2: Composition of functions
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    # Compose multiple operations: filter even -> square -> sum
    pipeline_result = reduce(
        lambda x, y: x + y,
        map(
            lambda x: x ** 2,
            filter(lambda x: x % 2 == 0, numbers)
        )
    )
    
    print(f"Numbers: {numbers}")
    print(f"Sum of squares of even numbers: {pipeline_result}")

# =============================================
# MAIN EXECUTION
# =============================================

if __name__ == "__main__":
    # Run all examples
    functional_patterns()
    
    print("\n=== SUMMARY ===")
    print("map() is for transformation - applies function to each element")
    print("reduce() is for aggregation - combines elements into a single result")
    print("Together they enable powerful functional programming patterns!")