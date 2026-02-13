 # Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list (hardcoded for simplicity)

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: get_portfolio_holdings()
   - Input: portfolio_id
   - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
   - Tool: get_stock_prices()
   - Input: symbols extracted from holdings
   - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value and Position Details**
   - Tools: calculate_portfolio_value(), get_stock_prices()
   - Input: holdings, current_prices
   - Output: portfolio value, position details

   d. **Calculate Volatility Score**
   - Tool: calculate_volatility_score()
   - Input: symbols from holdings
   - Output: volatility score

   e. **Check Risk Thresholds**
   - Tool: check_risk_threshold()
   - Input: portfolio value, volatility score, risk configuration
   - Output: whether the portfolio is high-risk and which thresholds were exceeded

3. **Error Handling Strategy**
   - Wrap each portfolio in try/except blocks to handle API errors
   - If a portfolio encounters an error, continue with the next one and log the issue

# Implementation

```python
from tools_reference import (
    get_portfolio_holdings,
    get_stock_prices,
    calculate_portfolio_value,
    calculate_volatility_score,
    check_risk_threshold,
    generate_report,
    send_notification,
    log_operation
)

RISK_CONFIG = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000
}

PORTFOLIOS = ["PORT-001", "PORT-002", "PORT-003"]

def analyze_portfolio(portfolio_id):
    try:
        holdings = get_portfolio_holdings(portfolio_id)
    except ValueError as e:
        log_operation(f"Portfolio Analysis - Error ({portfolio_id})", {"error": str(e)}, level="error")
        return None

    try:
        stock_prices = get_stock_prices([holding["symbol"] for holding in holdings])
    except ValueError as e:
        log_operation(f"Portfolio Analysis - Error ({portfolio_id})", {"error": str(e)}, level="error")
        return None

    try:
        portfolio_value_data = calculate_portfolio_value(holdings, stock_prices)
    except ValueError as e:
        log_operation(f"Portfolio Analysis - Error ({portfolio_id})", {"error": str(e)}, level="error")
        return None

    try:
        volatility = calculate_volatility_score([holding["symbol"] for holding in holdings])
    except ValueError as e:
        log_operation(f"Portfolio Analysis - Error ({portfolio_id})", {"error": str(e)}, level="error")
        return None

    risk_check = check_risk_threshold(
        portfolio_value_data["total_value"], volatility, RISK_CONFIG)

    if risk_check["is_high_risk"]:
        log_operation("Risk Check", risk_check, level="warning")
        report = generate_report(
            {
                "portfolio_id": portfolio_id,
                **portfolio_value_data.dict(),
                "risk_level": "HIGH",
                "exceeded_thresholds": risk_check["exceeded_thresholds"]
            }, report_format="markdown"
        )

        try:
            send_notification(holdings[0]["manager_email"], f"High Risk Alert: Portfolio {portfolio_id}", report, priority="high")
        except ValueError as e:
            log_operation("Notification Send - Error ({portfolio_id})", {"error": str(e)}, level="warning")

    return risk_check

if __name__ == "__main__":
    for portfolio in PORTFOLIOS:
        result = analyze_portfolio(portfolio)
        if result is not None:
            log_operation("Portfolio Analysis", {"portfolio_id": portfolio}, level="info")
```

# Design Justification

### Tool Orchestration Sequence
I chose to process each portfolio sequentially since it simplifies the implementation and allows for individual error handling. If performance is a concern, parallel processing could be implemented later as an optimization.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because they require information from the holdings to perform their tasks correctly. The calculated portfolio value and volatility score are used in the risk threshold check and report generation, respectively.

### Error Handling Strategy
Each portfolio is wrapped in a try/except block to handle API errors. If a portfolio encounters an error during analysis, it will be logged and skipped, allowing the next portfolio to be analyzed without interruption. This approach ensures that all portfolios are processed as much as possible before failing due to an error.