## Section 1: Execution Plan

1. **Initialize Configuration**:
   - Tools: None
   - Define risk thresholds dictionary (`risk_config`)
   - List of portfolios to analyze (`portfolios = ["PORT-001", "PORT-002", "PORT-003"]`).

2. **Iterate through Portfolios**: 
   For each portfolio in `portfolios`:

    a. **Fetch Portfolio Holdings**:
       - Tool: `get_portfolio_holdings()`
       - Input: current portfolio ID (`portfolio_id`)
       - Output: Portfolio holdings data (stored as `portfolio_data`).
    b. **Get Stock Prices**:
       - Tool: `get_stock_prices()`
       - Input: List of symbols from `portfolio_data`
       - Output: Dictionary of current stock prices (`current_prices`).

    c. **Calculate Portfolio Value and Position Details**:
       - Tool: `calculate_portfolio_value()`
       - Input: `portfolio_data`, `current_prices`
       - Output: Dictionary containing portfolio total value, position details, and other relevant metrics (`portfolio_value_data`).

    d. **Calculate Volatility Score**:
       - Tool: `calculate_volatility_score()`
       - Input: List of symbols from `portfolio_data` (all holdings)
       - Output: Aggregate volatility score for the portfolio (`volatility_score`).

    e. **Check Risk Thresholds**:
       - Tool: `check_risk_threshold()`
       - Input: `portfolio_value_data['total_value']`, `volatility_score`, `risk_config`
       - Output: Dictionary containing risk assessment results including `is_high_risk`, `exceeded_thresholds`, and `risk_level`.

    f. **Generate Report (if high risk)**:
       - Tool: `generate_report()`
       - Input: `portfolio_data`, `portfolio_value_data`, `risk_config`, report format ("markdown") 
       - Output: Markdown formatted risk analysis report (`report_text`).

    g. **Send Notification (if high risk)**:
       - Tool: `send_notification()`
       - Input: Portfolio manager email, subject line ("High Risk Alert"), report text (`report_text`), "high" priority
       - Output: Dictionary containing notification details (sent status, message ID, timestamp).

3. **Log Operations**: 
   - After each major step, use `log_operation()` to record the operation name and relevant details (e.g., portfolio ID, risk level, success/failure status). Use "info" for normal operations, "warning" for thresholds exceeded, and "error" for failures.

4. **Error Handling Strategy**:
   - Wrap each portfolio processing step in a `try...except` block to catch potential exceptions (e.g., invalid portfolio ID, missing stock prices, API errors).
   - Log the error details using `log_operation()` with an "error" level message.
   - Continue processing remaining portfolios if one encounters an error.


## Section 2: Implementation (Python)

```python
from tools_reference import (
    get_stock_prices,
    get_portfolio_holdings,
    calculate_portfolio_value,
    calculate_volatility_score,
    check_risk_threshold,
    generate_report,
    send_notification,
    log_operation,
)

risk_config = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000,
}

portfolios = ["PORT-001", "PORT-002", "PORT-003"]

def analyze_portfolio(portfolio_id):
    try:
        portfolio_data = get_portfolio_holdings(portfolio_id)
        symbols = [holding["symbol"] for holding in portfolio_data["holdings"]]
        current_prices = get_stock_prices(symbols)
        portfolio_value_data = calculate_portfolio_value(portfolio_data["holdings"], current_prices)
        volatility_score = calculate_volatility_score(symbols, days=30)
        risk_check = check_risk_threshold(
            portfolio_value_data["total_value"], volatility_score, risk_config
        )

        if risk_check["is_high_risk"]:
            report_text = generate_report(
                {**portfolio_data, **portfolio_value_data, "risk_level": risk_check["risk_level"]},
                report_format="markdown",
            )
            send_notification(
                "manager@firm.com",
                f"High Risk Alert: Portfolio {portfolio_id}",
                report_text,
                priority="high",
            )

        log_operation(
            "portfolio_analysis",
            {"portfolio_id": portfolio_id, "risk_level": risk_check["risk_level"]},
            level="info" if not risk_check["is_high_risk"] else "warning",
        )
    except Exception as e:
        log_operation(
            "portfolio_analysis_error",
            {"portfolio_id": portfolio_id, "error": str(e)},
            level="error",
        )

if __name__ == "__main__":
    for portfolio in portfolios:
        analyze_portfolio(portfolio)



```




## Section 3: Design Justification

### Tool Orchestration Sequence
The sequential processing of each portfolio was chosen for simplicity and clarity. This approach allows us to clearly define the data flow between steps, making it easier to understand and debug. While parallel processing could potentially speed up the overall execution, the added complexity in handling dependencies and potential race conditions might outweigh the benefit for this task.

### Data Flow Strategy
Holdings data is essential for several subsequent operations. Therefore, fetching holdings first ensures that all downstream processes have access to this crucial information before calculating portfolio values, volatility scores, and risk assessments. This sequential approach avoids unnecessary recalculations and simplifies data management.

### Error Handling Strategy Rationale
The `try...except` blocks are placed around each step of the portfolio analysis process to gracefully handle potential errors without crashing the entire script. 


Logging errors with detailed information allows for efficient troubleshooting and identification of recurring issues. By continuing processing remaining portfolios after encountering an error, the system minimizes downtime and ensures that as many portfolios as possible are analyzed successfully.

---



