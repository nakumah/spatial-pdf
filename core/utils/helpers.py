import numpy as np

def get_factors(n: int) -> np.ndarray:
    """
    Returns all factors of a positive integer `n`.
    """
    if n <= 0:
        raise ValueError("Only positive integers are allowed.")
    factors = [i for i in range(1, n + 1) if n % i == 0]
    return np.array(factors)


def closest_common_factors(n: int) -> tuple[int, int]:
    """
    Returns the two closest factors (a, b) of n such that a * b == n.
    """
    if n <= 0:
        raise ValueError("Only positive integers are allowed.")

    factors = get_factors(n)
    min_diff = float("inf")
    closest_pair = (1, n)

    for f in factors:
        other = n // f
        if f * other == n:
            diff = abs(f - other)
            if diff < min_diff:
                min_diff = diff
                closest_pair = (min(f, other), max(f, other))

    return closest_pair
