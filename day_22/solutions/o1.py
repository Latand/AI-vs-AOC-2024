#!/usr/bin/env python3

"""
Advent of Code 2024 - Day 22: Monkey Market

We have two parts:

Part 1:
--------
Given a list of initial secret numbers (one per line in ../input.txt), each "buyer"
produces a sequence of secret numbers via a pseudorandom process:
    1) Multiply n by 64 => mix via XOR => prune mod 16777216
    2) Floor-divide n by 32 => mix via XOR => prune mod 16777216
    3) Multiply n by 2048 => mix via XOR => prune mod 16777216

Repeat that process to get the "next" secret number.

For each buyer, we start with the initial secret number as "secret_0". Then we generate
2000 new secret numbers (secret_1 ... secret_2000). We need the sum of all buyers'
secret_2000. Print this sum.

Part 2:
--------
Prices offered by each buyer are the ones digit (last decimal digit) of each secret number.

So for buyer i, we have a price sequence p_0, p_1, ..., p_2000, where p_0 is the last digit
of the initial secret number, and p_k is the last digit of secret_k for k=1..2000.

We look at the consecutive changes (price differences):
  change_k = p_{k+1} - p_k   (for k=0..1999)
There are 2000 changes for each buyer.

We can only pick ONE 4-change pattern (d1, d2, d3, d4) for *all* buyers. For each buyer,
we find the earliest occurrence of that 4-change pattern in their first 2000 changes.
- If it occurs at index i (meaning change_i = d1, change_{i+1} = d2, change_{i+2} = d3,
  change_{i+3} = d4), we "sell" at price_{i+4}.
- If the pattern never occurs, we get 0 bananas from that buyer.

We want to find the pattern (d1, d2, d3, d4) that maximizes the SUM of all buyers' sales
(i.e. sum of the first-occurrence selling price for each buyer). Print that maximum sum.

Implementation Outline
----------------------
1) Read input from ../input.txt (each line is one initial secret number).
2) For each buyer:
   - Generate the sequence of 2001 secret numbers (the initial plus 2000 new).
   - Convert them to prices (last digit of each secret number).
   - Compute the 2000 changes in the prices.
3) Part 1: Sum up each buyer's secret_2000 and print.
4) Part 2: We build, for each buyer, a dictionary of (d1,d2,d3,d4) -> price_at_earliest_occurrence.
   Then we combine (sum) across buyers for each pattern and take the max.

   Why not brute force 19^4 = 130321 patterns? Because for many buyers, and 2000 changes each,
   that might be too slow (130k * (#buyers) * 2000). Instead, we invert the problem:
   - For each buyer, we iterate over its 2000-3 = 1997 possible 4-change sequences
     and record the earliest index => the price at i+4.
   - Then we combine across buyers: sum up those prices for each unique 4-change pattern.
   - The pattern with the highest sum is the answer.

   This is O(#buyers * 2000) to build all buyer dictionaries, plus O(sum_of_dictionary_sizes)
   to combine them. This is typically feasible in Python for a normal AoC-sized input.

5) Print both results.

NOTE: The puzzle example data is given in the problem statement. You should provide your
own input.txt with the actual puzzle input for Day 22 (not publicly provided here).
"""


def next_secret(n: int) -> int:
    """
    Given the current secret number n, produce the next secret number via:
      1) multiply n by 64 => XOR into n => n % 16777216
      2) floor-divide n by 32 => XOR into n => n % 16777216
      3) multiply n by 2048 => XOR into n => n % 16777216
    """
    # Step 1
    n1 = n * 64
    n = (n ^ n1) % 16777216

    # Step 2
    n2 = n // 32
    n = (n ^ n2) % 16777216

    # Step 3
    n3 = n * 2048
    n = (n ^ n3) % 16777216

    return n


def part1(initial_secrets):
    """
    Part 1:
    For each buyer, generate 2000 new secret numbers from the initial secret number
    and return the sum of those 2000th secret numbers.
    """
    total = 0
    for init in initial_secrets:
        n = init
        for _ in range(2000):
            n = next_secret(n)
        total += n
    return total


def part2(initial_secrets):
    """
    Part 2:
    We only care about the last decimal digit (prices).
    For each buyer, we'll generate an array of length 2001 (price_0..price_2000).
    Then we create 2000 changes, each = price_{k+1} - price_k.

    We'll store in a dictionary for each buyer:
       dict_4changes[ (d1,d2,d3,d4) ] = earliest price_{i+4} for that 4-change pattern

    Then we combine across all buyers in a global dict, summing prices for each pattern.

    Finally, we take the maximum sum among all patterns and return that value.
    """
    from collections import defaultdict

    # We'll store one dictionary per buyer: 4-change pattern -> price at earliest occurrence
    buyers_dicts = []
    for init in initial_secrets:
        # Generate the secret number sequence for this buyer
        secrets = [init]
        n = init
        for _ in range(2000):
            n = next_secret(n)
            secrets.append(n)

        # Convert to prices (last decimal digit)
        prices = [s % 10 for s in secrets]

        # Compute changes
        changes = []
        for i in range(len(prices) - 1):
            changes.append(prices[i + 1] - prices[i])

        # Build the dictionary of earliest 4-change pattern -> price (i+4)
        dict_4changes = {}
        for i in range(len(changes) - 3):  # up to i+3 < len(changes)
            pattern = (changes[i], changes[i + 1], changes[i + 2], changes[i + 3])
            if pattern not in dict_4changes:
                dict_4changes[pattern] = prices[i + 4]
        buyers_dicts.append(dict_4changes)

    # Now combine them. For each buyer, we have dict_4changes. We want to sum
    # the values across buyers for the same pattern.
    global_sums = defaultdict(int)
    for dict_4changes in buyers_dicts:
        for pattern, price_at_sale in dict_4changes.items():
            global_sums[pattern] += price_at_sale

    # The answer is the maximum sum among all patterns
    if not global_sums:
        # No patterns at all (which is unlikely unless there's no input)
        return 0

    best_sum = max(global_sums.values())
    return best_sum


def read_input():
    """
    Reads the puzzle input from ../input.txt
    Returns a list of integers, each representing an initial secret number for a buyer.
    """
    with open("../input.txt") as f:
        lines = f.read().strip().split()
    return list(map(int, lines))


def main():
    data = read_input()

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
