# Advent of Code 2024

This repository contains solutions for [Advent of Code 2024](https://adventofcode.com/2024) challenges, solved by different AI models.

## Project Structure

The project is organized by days (1-25), where each day contains:

- `solutions/` directory with different AI model solutions:
  - `o1-preview.py` - OpenAI GPT-4 Preview solution
  - `gpt-4o-mini.py` - GPT-4 Mini solution
  - `claude-3.5-haiku.py` - Claude 3.5 Haiku solution
  - `claude-3.5-sonnet.py` - Claude 3.5 Sonnet solution
  - `o1-mini.py` - OpenAI Mini solution
  - `gpt-4o.py` - GPT-4 solution
- `input.txt` - Input data provided by Advent of Code
- `results.md` - Results tracking for each model's performance
- `solution.py` - The main solution file

```
aoc-2024/
├── day_01/
│   ├── solutions/
│   │   ├── o1-preview.py
│   │   ├── gpt-4o-mini.py
│   │   ├── claude-3.5-haiku.py
│   │   ├── claude-3.5-sonnet.py
│   │   ├── o1-mini.py
│   │   └── gpt-4o.py
│   ├── input.txt
│   ├── solution.py
│   └── results.md
├── day_02/
│   ├── solutions/
│   │   └── [model solutions]
│   ├── input.txt
│   ├── solution.py
│   └── results.md
...
└── day_25/
    ├── solutions/
    │   └── [model solutions]
    ├── input.txt
    ├── solution.py
    └── results.md
```

## Results Tracking

Each day contains a `results.md` file that tracks the success/failure of each model's solution for both parts of the challenge.

## Running Solutions

To run a specific model's solution for a day:

```bash
cd day_XX/solutions && python model-name.py
```

For example:

```bash
cd day_10/solutions && python o1-preview.py
```
