# Advent of Code 2024

This repository contains solutions for [Advent of Code 2024](https://adventofcode.com/2024) challenges.

## Project Structure

The project is organized by days (1-25), where each day contains:

- `solution.py` - Python script containing solutions for:
  - Part 1 of the day's challenge
  - Part 2 of the day's challenge
- `input.txt` - Input data provided by Advent of Code

```
aoc-2024/
├── day_01/
│   ├── solution.py  # Contains part1() and part2() solutions
│   └── input.txt
├── day_02/
│   ├── solution.py  # Contains part1() and part2() solutions
│   └── input.txt
...
└── day_25/
    ├── solution.py  # Contains part1() and part2() solutions
    └── input.txt
```

## Workflow

1. Each day's challenge consists of two parts
2. The input data is unique for each user and should be saved in `input.txt`
3. Both parts of the solution are implemented in `solution.py` as separate functions
4. Each solution part prints its result to the console

## Running Solutions

To run a specific day's solution:

```bash
cd day_XX && python solution.py
```
