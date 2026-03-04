 Here is a breakdown of the steps required to build the Portfolio Risk Analysis Agent:

## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds, portfolio list, and format for generated reports

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: portfolio_id
   - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: symbols extracted from holdings
   - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value and Risk Metrics**
   - Tools: `calculate_portfolio_value()`, `calculate_volatility_score()`
   - Inputs: holdings, current prices
   - Output: portfolio value, volatility score (needed for step 4)

3. **Error Handling Strategy**
   - Wrap each portfolio in a try/except block to handle errors from the tools
   - Log errors and continue to next portfolio if possible

## Implementation (Python)

```python
from typing import Dict, List
import re
import logging
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

# Global constants
RISK_THRESHOLDS = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000,
}
PORTFOLIOS = ["PORT-001", "PORT-002", "PORT-003"]
REPORT_FORMAT = "markdown"
LOGGING_FORMAT = "%(levelname)s: %(message)s"

def fetch_holdings_and_prices(portfolio_id):
    holdings = get_portfolio_holdings(portfolio_id)
    symbols = [holding["symbol"] for holding in holdings]
    prices = get_stock_prices(symbols)
    return holdings, prices

def analyze_portfolio(portfolio_data):
    holdings, prices = fetch_holdings_and_prices(portfolio_data["portfolio_id"])
    portfolio_value, positions = calculate_portfolio_value(holdings, prices)
    volatility_score = calculate_volatility_score([position["symbol"] for position in positions], 30)
    risk_check_result = check_risk_threshold(
        portfolio_value["total_value"], volatility_score, RISK_THRESHOLDS
    )
    return (
        portfolio_data,
        {"volatility_score": volatility_score, "risk_check_result": risk_check_result},
    )

def process_portfolios():
    for portfolio in PORTFOLIOS:
        try:
            portfolio_data = get_portfolio_holdings(portfolio)
            analyzed_data, metrics = analyze_portfolio(portfolio_data)
            log_operation(f"AnalyzePortfolio_{portfolio}", {"portfolio": portfolio}, "info")

            # Identify high-risk portfolios and generate reports/notifications
            if metrics["risk_check_result"]["is_high_risk"]:
                report = generate_report(analyzed_data, REPORT_FORMAT)
                log_operation(f"GenerateReport_{portfolio}", {"report": report}, "info")

                recipients = [analyzed_data["manager_email"]]
                subject = f"High Risk Alert: Portfolio {portfolio}"
                message = f"{report}\nExceeded Thresholds: {metrics['risk_check_result']['exceeded_thresholds']}"
                send_notification(recipients[0], subject, message, "high")
                log_operation(f"SendNotification_{portfolio}", {"message": message}, "info")
        except Exception as e:
            logging.error(f"Error processing portfolio {portfolio}: {str(e)}")
    log_operation("PortfolioAnalysisCompletion", {}, "info")

if __name__ == "__main__":
    logging.basicConfig(format=LOGGING_FORMAT)
    process_portfolios()
```

## Design Justification

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because it simplifies error handling by isolating issues to individual portfolios. This approach also allows for more efficient resource usage, as we only fetch stock prices once for each portfolio.

### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because the holdings are required to fetch current prices and perform portfolio analysis calculations. The risk threshold check depends on both portfolio value and volatility score, so they need to be calculated beforehand.

### Error Handling Strategy
Wrapping each portfolio in a try/except block allows for more efficient error handling by isolating issues to individual portfolios. This approach also ensures that the system continues processing remaining portfolios if one fails. The logging function is used throughout the script to maintain an audit trail of all major operations.