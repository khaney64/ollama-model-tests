# Agentic Task: Portfolio Risk Analysis Agent

## Objective

Build a Python script that autonomously orchestrates multiple tools to analyze investment portfolios, calculate risk metrics, identify high-risk portfolios, generate reports, and send notifications to portfolio managers.

This task evaluates your ability to:
- Decompose a complex goal into sequential steps
- Select and orchestrate appropriate tools from a toolkit
- Manage data flow between operations
- Handle errors gracefully
- Create executable, production-ready code

## Scenario

You are building an automated risk monitoring system for a financial advisory firm. The system needs to:
1. Monitor multiple client portfolios
2. Calculate current portfolio values and risk metrics
3. Identify portfolios that exceed risk thresholds
4. Generate detailed reports for high-risk portfolios
5. Send notifications to portfolio managers
6. Maintain audit logs of all operations

The firm has provided you with a toolkit of 8 API functions that simulate their backend systems. Your task is to create a Python script that orchestrates these tools to accomplish the goal.

## Available Tools

You have access to the following 8 tools (simulated APIs):

### 1. `get_stock_prices(symbols: list[str]) -> dict[str, float]`

Fetches current market prices for given stock symbols.

**Parameters:**
- `symbols`: List of stock ticker symbols (e.g., ["AAPL", "GOOGL"])

**Returns:**
- Dictionary mapping symbols to current prices in USD

**Example:**
```python
prices = get_stock_prices(["AAPL", "MSFT"])
# Returns: {"AAPL": 178.50, "MSFT": 380.25}
```

**Error Cases:**
- Raises `ValueError` if symbols list is empty
- Unknown symbols return `None` as their price value

---

### 2. `get_portfolio_holdings(portfolio_id: str) -> dict`

Retrieves holdings information for a specific portfolio.

**Parameters:**
- `portfolio_id`: Portfolio identifier (e.g., "PORT-001")

**Returns:**
- Dictionary with structure:
  ```python
  {
      "portfolio_id": str,
      "client_name": str,
      "manager_email": str,
      "holdings": [
          {"symbol": str, "shares": int, "purchase_price": float},
          ...
      ]
  }
  ```

**Example:**
```python
portfolio = get_portfolio_holdings("PORT-001")
# Returns holdings data for portfolio PORT-001
```

**Error Cases:**
- Raises `ValueError` if portfolio_id is invalid or not found

---

### 3. `calculate_portfolio_value(holdings: list[dict], current_prices: dict[str, float]) -> dict`

Calculates total portfolio value and individual position values.

**Parameters:**
- `holdings`: List of holdings from `get_portfolio_holdings`
- `current_prices`: Price dictionary from `get_stock_prices`

**Returns:**
- Dictionary with structure:
  ```python
  {
      "total_value": float,
      "positions": [
          {
              "symbol": str,
              "shares": int,
              "current_price": float,
              "position_value": float,
              "gain_loss": float,
              "gain_loss_percent": float
          },
          ...
      ]
  }
  ```

**Example:**
```python
value_data = calculate_portfolio_value(holdings, prices)
# Returns calculated values and gains/losses
```

**Error Cases:**
- Raises `ValueError` if holdings or current_prices are empty
- Skips positions where current_price is None

---

### 4. `calculate_volatility_score(symbols: list[str], days: int = 30) -> float`

Calculates aggregate volatility score for a set of stocks.

**Parameters:**
- `symbols`: List of stock symbols in the portfolio
- `days`: Historical period for volatility calculation (default: 30)

**Returns:**
- Float representing volatility score (0-100 scale, higher = more volatile)

**Example:**
```python
volatility = calculate_volatility_score(["AAPL", "GOOGL", "MSFT"], days=30)
# Returns: 24.5 (indicating moderate volatility)
```

**Error Cases:**
- Raises `ValueError` if symbols list is empty
- Raises `ValueError` if days < 1

---

### 5. `check_risk_threshold(portfolio_value: float, volatility_score: float, risk_config: dict) -> dict`

Checks if portfolio exceeds configured risk thresholds.

**Parameters:**
- `portfolio_value`: Total portfolio value in USD
- `volatility_score`: Volatility score from `calculate_volatility_score`
- `risk_config`: Configuration with structure:
  ```python
  {
      "max_volatility": float,  # Maximum acceptable volatility score
      "min_value": float,       # Minimum portfolio value for monitoring
      "max_value": float        # Maximum portfolio value for monitoring
  }
  ```

**Returns:**
- Dictionary with structure:
  ```python
  {
      "is_high_risk": bool,
      "exceeded_thresholds": list[str],  # Which thresholds were exceeded
      "risk_level": str  # "LOW", "MEDIUM", or "HIGH"
  }
  ```

**Example:**
```python
risk_config = {"max_volatility": 30.0, "min_value": 10000, "max_value": 1000000}
risk_check = check_risk_threshold(250000, 35.5, risk_config)
# Returns: {"is_high_risk": True, "exceeded_thresholds": ["volatility"], "risk_level": "HIGH"}
```

**Error Cases:**
- Raises `ValueError` if portfolio_value is negative
- Raises `ValueError` if volatility_score is negative

---

### 6. `generate_report(portfolio_data: dict, report_format: str = "markdown") -> str`

Generates a formatted risk analysis report.

**Parameters:**
- `portfolio_data`: Dictionary containing all portfolio analysis data with structure:
  ```python
  {
      "portfolio_id": str,
      "client_name": str,
      "total_value": float,
      "volatility_score": float,
      "risk_level": str,
      "exceeded_thresholds": list[str],
      "positions": list[dict]  # From calculate_portfolio_value
  }
  ```
- `report_format`: Output format ("markdown", "html", or "text")

**Returns:**
- Formatted report string

**Example:**
```python
report = generate_report(portfolio_data, report_format="markdown")
# Returns formatted markdown report
```

**Error Cases:**
- Raises `ValueError` if required fields missing from portfolio_data
- Raises `ValueError` if report_format not in ["markdown", "html", "text"]

---

### 7. `send_notification(recipient: str, subject: str, message: str, priority: str = "normal") -> dict`

Sends notification email to portfolio manager.

**Parameters:**
- `recipient`: Email address
- `subject`: Email subject line
- `message`: Email body (can be formatted text)
- `priority`: "low", "normal", or "high"

**Returns:**
- Dictionary with structure:
  ```python
  {
      "sent": bool,
      "message_id": str,
      "timestamp": str
  }
  ```

**Example:**
```python
result = send_notification(
    "manager@firm.com",
    "High Risk Alert: Portfolio PORT-001",
    report_text,
    priority="high"
)
# Returns: {"sent": True, "message_id": "msg-12345", "timestamp": "2026-02-09T10:30:00Z"}
```

**Error Cases:**
- Raises `ValueError` if recipient is empty or invalid email format
- Raises `ValueError` if priority not in ["low", "normal", "high"]

---

### 8. `log_operation(operation: str, details: dict, level: str = "info") -> None`

Logs operations to audit trail.

**Parameters:**
- `operation`: Operation name (e.g., "portfolio_analysis", "risk_check")
- `details`: Dictionary with operation-specific details
- `level`: Log level ("info", "warning", "error")

**Returns:**
- None (logs to system)

**Example:**
```python
log_operation(
    "risk_check",
    {"portfolio_id": "PORT-001", "risk_level": "HIGH"},
    level="warning"
)
```

**Error Cases:**
- Raises `ValueError` if level not in ["info", "warning", "error"]

## Requirements

Your script must accomplish the following:

1. **Analyze Multiple Portfolios**: Process portfolios "PORT-001", "PORT-002", and "PORT-003"

2. **Calculate Risk Metrics**: For each portfolio:
   - Get current holdings
   - Fetch current stock prices for all holdings
   - Calculate total portfolio value and position details
   - Calculate volatility score using 30-day period

3. **Apply Risk Configuration**: Use the following risk thresholds:
   ```python
   {
       "max_volatility": 35.0,
       "min_value": 50000,
       "max_value": 2000000
   }
   ```

4. **Identify High-Risk Portfolios**: Determine which portfolios exceed the risk thresholds

5. **Generate and Send Reports**: For each high-risk portfolio:
   - Generate a markdown-formatted report
   - Send notification to portfolio manager with "high" priority
   - Include portfolio details, risk metrics, and exceeded thresholds in the report

6. **Maintain Audit Trail**: Log all major operations:
   - Portfolio analysis start/completion
   - Risk threshold checks
   - Report generation
   - Notification sending

7. **Handle Errors Gracefully**: Include error handling for:
   - Invalid portfolio IDs
   - Missing stock price data
   - Failed notifications
   - Continue processing remaining portfolios if one fails

## Expected Output Format

Your response must include three sections:

### Section 1: Execution Plan (Markdown)

Provide a step-by-step execution plan with:
- Clear numbered steps
- Tool(s) used in each step
- Data dependencies between steps
- Error handling strategy

**Example Structure:**
```markdown
## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: get_portfolio_holdings()
   - Input: portfolio_id
   - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
   - Tool: get_stock_prices()
   - Input: symbols extracted from holdings
   - Output: current prices (needed for step c)

   [Continue for all steps...]

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except
   - Log errors and continue to next portfolio
   - [etc...]
```

### Section 2: Implementation (Python)

Provide complete, executable Python code that:
- Imports the tools from `tools_reference` module
- Orchestrates the tools according to your plan
- Includes comprehensive error handling
- Includes logging for audit trail
- Is well-commented and follows best practices

**Example Structure:**
```python
from tools_reference import (
    get_stock_prices,
    get_portfolio_holdings,
    # ... other imports
)

def analyze_portfolios():
    """Main orchestration function."""
    # Implementation here
    pass

if __name__ == "__main__":
    analyze_portfolios()
```

### Section 3: Design Justification (Markdown)

Explain your design decisions:
- Why you chose this tool orchestration sequence
- How you handled data flow between steps
- Error handling strategy rationale
- Trade-offs considered

**Example Structure:**
```markdown
## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because...

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because...

[Continue with reasoning...]
```

## Evaluation Criteria

Your submission will be scored on the following weighted criteria:

| Criterion | Weight | Description |
|-----------|--------|-------------|
| **Planning Quality** | 25% | Clear decomposition of goal into logical steps with correct dependencies |
| **Tool Selection** | 20% | Appropriate tools chosen for each operation; no missing or unnecessary tools |
| **Data Flow Correctness** | 20% | Outputs correctly passed as inputs; no data loss or incorrect transformations |
| **Error Handling** | 15% | Comprehensive try/except blocks; graceful degradation; proper logging |
| **Completeness** | 15% | All requirements met; all 3 portfolios processed; audit trail maintained |
| **Code Quality** | 5% | Well-structured, readable, commented code following Python best practices |

**Automated Checks:**
- At least 6 of 8 tools used appropriately
- Code executes without errors against mock tools
- All 3 portfolios processed
- At least 5 log operations recorded
- Error handling present (try/except blocks)

**Manual Review:**
- Execution plan logic and clarity
- Tool orchestration strategy effectiveness
- Design justification reasoning quality

**Passing Score:** 7.0/10.0

---

**Note:** The tools are simulated for this task. In production, these would be real API calls to backend systems. Your implementation should assume the tools work as specified and focus on orchestration logic.
