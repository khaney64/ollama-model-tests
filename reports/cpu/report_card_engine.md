# Trading Engine Implementation Report Card

Generated: 2026-02-13 12:21:38

## Executive Summary

Evaluated **15** trading engine implementations against the requirements in `requirements/engine.md`.

**Grade Distribution:**
- A: 6 model(s)
- B: 3 model(s)
- C: 3 model(s)
- F: 3 model(s)

## Summary Rankings

| Rank | Model | Grade | Total Score | Correctness | Output Format | Worked Example | Code Quality | Edge Cases |
|------|-------|-------|-------------|-------------|---------------|----------------|--------------|------------|
| 1 | glm-4.7(cloud) | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 |
| 2 | kimi-k2.5(cloud) | A | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 | 10.0 |
| 3 | gemma3(12b-it-q4_K_M) | A | 9.9 | 10.0 | 10.0 | 10.0 | 9.5 | 10.0 |
| 4 | qwen3(8b) | A | 9.6 | 10.0 | 10.0 | 10.0 | 9.5 | 8.0 |
| 5 | phi4(14b-q4_K_M) | A | 9.2 | 10.0 | 10.0 | 10.0 | 8.5 | 6.0 |
| 6 | qwen2.5-coder(7b-instruct-q5_K_M) | A | 9.0 | 10.0 | 7.5 | 9.0 | 10.0 | 8.0 |
| 7 | glm-4.7-flash(q4_K_M) | B | 8.9 | 10.0 | 10.0 | 5.0 | 9.5 | 10.0 |
| 8 | qwen2.5-coder(14b-instruct-q4_K_M) | B | 8.4 | 10.0 | 7.5 | 6.5 | 9.5 | 8.0 |
| 9 | deepseek-coder-v2(16b) | B | 8.1 | 10.0 | 7.5 | 8.5 | 6.5 | 6.0 |
| 10 | mistral(7b-instruct-v0.3-q5_K_M) | C | 7.9 | 10.0 | 7.5 | 4.0 | 9.5 | 8.0 |
| 11 | gemma2(9b-instruct-q4_K_M) | C | 7.4 | 10.0 | 7.5 | 5.0 | 6.5 | 6.0 |
| 12 | qwen2.5-coder(7b) | C | 7.3 | 10.0 | 0.0 | 8.0 | 10.0 | 8.0 |
| 13 | llama3.1(8b) | F | 5.1 | 8.0 | 0.0 | 0.0 | 10.0 | 8.0 |
| 14 | llama3.1(8b-instruct-q4_K_M) | F | 5.0 | 9.0 | 0.0 | 0.0 | 7.0 | 8.0 |
| 15 | llama3.2(latest) | F | 4.2 | 10.0 | 0.0 | 0.0 | 0.0 | 8.0 |

## Detailed Evaluation Results

### glm-4.7(cloud)

**Overall Grade: A (10.0/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 10.0/10.0
- **Worked Example Match (20%):** 10.0/10.0
- **Code Quality (15%):** 10.0/10.0
- **Edge Cases (15%):** 10.0/10.0

#### Code Analysis

- Lines of code: 126
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### kimi-k2.5(cloud)

**Overall Grade: A (10.0/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 10.0/10.0
- **Worked Example Match (20%):** 10.0/10.0
- **Code Quality (15%):** 10.0/10.0
- **Edge Cases (15%):** 10.0/10.0

#### Code Analysis

- Lines of code: 86
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### gemma3(12b-it-q4_K_M)

**Overall Grade: A (9.9/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 10.0/10.0
- **Worked Example Match (20%):** 10.0/10.0
- **Code Quality (15%):** 9.5/10.0
- **Edge Cases (15%):** 10.0/10.0

#### Issues Found

- Many hardcoded values - should use constants

#### Code Analysis

- Lines of code: 77
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### qwen3(8b)

**Overall Grade: A (9.6/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 10.0/10.0
- **Worked Example Match (20%):** 10.0/10.0
- **Code Quality (15%):** 9.5/10.0
- **Edge Cases (15%):** 8.0/10.0

#### Issues Found

- Many hardcoded values - should use constants
- No error handling for file operations

#### Code Analysis

- Lines of code: 87
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### phi4(14b-q4_K_M)

**Overall Grade: A (9.2/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 10.0/10.0
- **Worked Example Match (20%):** 10.0/10.0
- **Code Quality (15%):** 8.5/10.0
- **Edge Cases (15%):** 6.0/10.0

#### Issues Found

- No main guard (__name__ == '__main__')
- Many hardcoded values - should use constants
- No error handling for file operations
- No explicit handling of trade_price == ClosePrice case

#### Code Analysis

- Lines of code: 71
- Uses functions: Yes
- Has main guard: No
- Has comments: Yes

### qwen2.5-coder(7b-instruct-q5_K_M)

**Overall Grade: A (9.0/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 7.5/10.0
- **Worked Example Match (20%):** 9.0/10.0
- **Code Quality (15%):** 10.0/10.0
- **Edge Cases (15%):** 8.0/10.0

#### Issues Found

- Decimal formatting issues (not 2 places): Cost
- Worked example mismatches (2 total):
-   • Row 2 Shares: expected 0.0, got 100000.0
-   • Row 4 Shares: expected 0.0, got -100000.0
- No error handling for file operations

#### Code Analysis

- Lines of code: 82
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### glm-4.7-flash(q4_K_M)

**Overall Grade: B (8.9/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 10.0/10.0
- **Worked Example Match (20%):** 5.0/10.0
- **Code Quality (15%):** 9.5/10.0
- **Edge Cases (15%):** 10.0/10.0

#### Issues Found

- Many hardcoded values - should use constants
- Worked example mismatches (10 total):
-   • Row 2 Shares: expected 0.0, got 100000.0
-   • Row 2 Cost: expected 0.0, got -14231500.0
-   • Row 2 ReceivablePayable: expected -13675500.0, got -27907000.0
-   • Row 3 Shares: expected -100000.0, got 0.0
-   • Row 3 Cost: expected 14998805.0, got 0.0
-   • Row 3 ReceivablePayable: expected 1323305.0, got -27907000.0
-   • Row 3 Profit: expected 1323305.0, got 0.0
-   • Row 3 TotalProfit: expected 1323305.0, got 0.0
-   • Row 4 ReceivablePayable: expected 1323305.0, got -27907000.0
-   • Row 4 TotalProfit: expected 1323305.0, got 0.0

#### Code Analysis

- Lines of code: 99
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### qwen2.5-coder(14b-instruct-q4_K_M)

**Overall Grade: B (8.4/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 7.5/10.0
- **Worked Example Match (20%):** 6.5/10.0
- **Code Quality (15%):** 9.5/10.0
- **Edge Cases (15%):** 8.0/10.0

#### Issues Found

- Many hardcoded values - should use constants
- Decimal formatting issues (not 2 places): Cost
- Worked example mismatches (7 total):
-   • Row 1 Cost: expected -13675500.0, got -0.0
-   • Row 1 ReceivablePayable: expected -13675500.0, got 0.0
-   • Row 2 Shares: expected 0.0, got 100000.0
-   • Row 2 ReceivablePayable: expected -13675500.0, got 0.0
-   • Row 3 ReceivablePayable: expected 1323305.0, got 14998804.999999998
-   • Row 4 Shares: expected 0.0, got -100000.0
-   • Row 4 ReceivablePayable: expected 1323305.0, got 14998804.999999998
- No error handling for file operations

#### Code Analysis

- Lines of code: 90
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### deepseek-coder-v2(16b)

**Overall Grade: B (8.1/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 7.5/10.0
- **Worked Example Match (20%):** 8.5/10.0
- **Code Quality (15%):** 6.5/10.0
- **Edge Cases (15%):** 6.0/10.0

#### Issues Found

- No functions defined - should use functions for better structure
- No main guard (__name__ == '__main__')
- Many hardcoded values - should use constants
- Decimal formatting issues (not 2 places): Cost, ReceivablePayable
- Worked example mismatches (3 total):
-   • Row 1 Shares: expected 100000.0, got -100000.0
-   • Row 2 Shares: expected 0.0, got -100000.0
-   • Row 3 Shares: expected -100000.0, got 0.0
- No error handling for file operations
- No explicit handling of trade_price == ClosePrice case

#### Code Analysis

- Lines of code: 64
- Uses functions: No
- Has main guard: No
- Has comments: Yes

### mistral(7b-instruct-v0.3-q5_K_M)

**Overall Grade: C (7.9/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 7.5/10.0
- **Worked Example Match (20%):** 4.0/10.0
- **Code Quality (15%):** 9.5/10.0
- **Edge Cases (15%):** 8.0/10.0

#### Issues Found

- Large code with no comments
- Decimal formatting issues (not 2 places): Cost
- Worked example mismatches (12 total):
-   • Row 1 Cost: expected -13675500.0, got 0.0
-   • Row 1 ReceivablePayable: expected -13675500.0, got 0.0
-   • Row 2 Shares: expected 0.0, got 100000.0
-   • Row 2 ReceivablePayable: expected -13675500.0, got 0.0
-   • Row 3 Shares: expected -100000.0, got 100000.0
-   • Row 3 Cost: expected 14998805.0, got 0.0
-   • Row 3 ReceivablePayable: expected 1323305.0, got 0.0
-   • Row 3 Profit: expected 1323305.0, got 0.0
-   • Row 3 TotalProfit: expected 1323305.0, got 0.0
-   • Row 4 Shares: expected 0.0, got 100000.0
-   • ... and 2 more
- No error handling for file operations

#### Code Analysis

- Lines of code: 60
- Uses functions: Yes
- Has main guard: Yes
- Has comments: No

### gemma2(9b-instruct-q4_K_M)

**Overall Grade: C (7.4/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 7.5/10.0
- **Worked Example Match (20%):** 5.0/10.0
- **Code Quality (15%):** 6.5/10.0
- **Edge Cases (15%):** 6.0/10.0

#### Issues Found

- No functions defined - should use functions for better structure
- No main guard (__name__ == '__main__')
- Many hardcoded values - should use constants
- Decimal formatting issues (not 2 places): Cost
- Worked example mismatches (10 total):
-   • Row 2 Shares: expected 0.0, got 100000.0
-   • Row 2 Cost: expected 0.0, got -14231500.0
-   • Row 2 ReceivablePayable: expected -13675500.0, got -27907000.0
-   • Row 3 Shares: expected -100000.0, got 0.0
-   • Row 3 Cost: expected 14998805.0, got 0.0
-   • Row 3 ReceivablePayable: expected 1323305.0, got -27907000.0
-   • Row 3 Profit: expected 1323305.0, got 0.0
-   • Row 3 TotalProfit: expected 1323305.0, got 0.0
-   • Row 4 ReceivablePayable: expected 1323305.0, got -27907000.0
-   • Row 4 TotalProfit: expected 1323305.0, got 0.0
- No error handling for file operations
- No explicit handling of trade_price == ClosePrice case

#### Code Analysis

- Lines of code: 49
- Uses functions: No
- Has main guard: No
- Has comments: Yes

### qwen2.5-coder(7b)

**Overall Grade: C (7.3/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 0.0/10.0
- **Worked Example Match (20%):** 8.0/10.0
- **Code Quality (15%):** 10.0/10.0
- **Edge Cases (15%):** 8.0/10.0

#### Issues Found

- Row 1: Cost contains non-numeric value
- Row 1: ReceivablePayable contains non-numeric value
- Row 1: Profit contains non-numeric value
- Row 1: TotalProfit contains non-numeric value
- Row 1: TradePrice contains non-numeric value
- Row 2: Cost contains non-numeric value
- Row 2: ReceivablePayable contains non-numeric value
- Row 2: Profit contains non-numeric value
- Row 2: TotalProfit contains non-numeric value
- Row 2: TradePrice contains non-numeric value
- Row 3: Cost contains non-numeric value
- Row 3: ReceivablePayable contains non-numeric value
- Row 3: Profit contains non-numeric value
- Row 3: TotalProfit contains non-numeric value
- Row 3: TradePrice contains non-numeric value
- Row 4: Cost contains non-numeric value
- Row 4: ReceivablePayable contains non-numeric value
- Row 4: Profit contains non-numeric value
- Row 4: TotalProfit contains non-numeric value
- Row 4: TradePrice contains non-numeric value
- Row 5: Cost contains non-numeric value
- Row 5: ReceivablePayable contains non-numeric value
- Row 5: Profit contains non-numeric value
- Row 5: TotalProfit contains non-numeric value
- Row 5: TradePrice contains non-numeric value
- Non-numeric values in worked example rows: Row 1 Shares, Row 2 Shares, Row 3 Shares, Row 4 Shares
- No error handling for file operations

#### Code Analysis

- Lines of code: 68
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### llama3.1(8b)

**Overall Grade: F (5.1/10.0)**

#### Score Breakdown

- **Correctness (30%):** 8.0/10.0
- **Output Format (20%):** 0.0/10.0
- **Worked Example Match (20%):** 0.0/10.0
- **Code Quality (15%):** 10.0/10.0
- **Edge Cases (15%):** 8.0/10.0

#### Issues Found

- No output.csv file generated
- No output.csv to compare with worked example
- Missing logic component: buy_condition
- Missing logic component: sell_condition
- No error handling for file operations

#### Code Analysis

- Lines of code: 80
- Uses functions: Yes
- Has main guard: Yes
- Has comments: Yes

### llama3.1(8b-instruct-q4_K_M)

**Overall Grade: F (5.0/10.0)**

#### Score Breakdown

- **Correctness (30%):** 9.0/10.0
- **Output Format (20%):** 0.0/10.0
- **Worked Example Match (20%):** 0.0/10.0
- **Code Quality (15%):** 7.0/10.0
- **Edge Cases (15%):** 8.0/10.0

#### Issues Found

- No functions defined - should use functions for better structure
- No main guard (__name__ == '__main__')
- Script execution failed: AttributeError: '_csv.writer' object has no attribute 'line_num'
- Output has fewer than 4 rows for worked example comparison
- Wrong number of output rows: 0 vs expected 275
- No error handling for file operations

#### Code Analysis

- Lines of code: 60
- Uses functions: No
- Has main guard: No
- Has comments: Yes

### llama3.2(latest)

**Overall Grade: F (4.2/10.0)**

#### Score Breakdown

- **Correctness (30%):** 10.0/10.0
- **Output Format (20%):** 0.0/10.0
- **Worked Example Match (20%):** 0.0/10.0
- **Code Quality (15%):** 0.0/10.0
- **Edge Cases (15%):** 8.0/10.0

#### Issues Found

- Syntax error: invalid syntax (<unknown>, line 61)
- Script execution failed: SyntaxError: invalid syntax
- No output.csv to compare with worked example
- No error handling for file operations

## Evaluation Criteria

### Correctness (30%)
- Buy/sell/hold logic matches the requirements exactly
- Proper trade_price calculation: (HighPrice + LowPrice) / 2
- Correct buy condition: trade_price < ClosePrice AND shares with client
- Correct sell condition: trade_price > ClosePrice AND shares with trust
- Accurate cost and profit calculations

### Output Format (20%)
- CSV has correct column headers in right order
- All monetary values formatted to 2 decimal places
- Output file is created successfully
- Header row is present

### Worked Example Match (20%)
- First 4 days of output match the provided worked example
- Values are within acceptable tolerance (±0.01)
- Share transfers happen on correct days

### Code Quality (15%)
- Clean, readable, well-structured Python code
- Appropriate use of functions
- Proper main guard (if __name__ == '__main__':)
- Reasonable code length and organization

### Edge Cases (15%)
- Handles UTF-8 BOM in input file (encoding='utf-8-sig')
- Proper file I/O error handling
- Handles trade_price == ClosePrice case (hold)
- Uses only standard library (no pandas, numpy, etc.)

---

*Report generated by evaluate_engine_code.py*
