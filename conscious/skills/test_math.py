def factorial(n: int) -> int:
    """Calculate factorial of a non-negative integer n."""
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def run() -> None:
    """Main execution function."""
    n = 5
    print(factorial(n))

if __name__ == "__main__":
    run()