## Execution Plan (Markdown)

### Step 1: Initialize Configuration
- **Tool**: None
- **Set up risk thresholds and portfolio list**
- **Error Handling Strategy**: Not applicable for configuration setup

### Step 2: For Each Portfolio:
#### a. Fetch Holdings
- **Tool**: `get_portfolio_holdings()`
- **Input**: portfolio_id (e.g., "PORT-001")
- **Output**: holdings data (needed for steps b, c, e)

#### b. Get Stock Prices
- **Tool**: `get_stock_prices()`
- **Input**: symbols extracted from holdings
- **Output**: current prices (needed for step c)

#### c. Calculate Portfolio Value and Positions
- **Tool**: `calculate_portfolio_value()`
- **Inputs**: holdings data, current prices
- **Output**: portfolio value, position details

#### d. Calculate Volatility Score
- **Tool**: `calculate_volatility_score()`
- **Input**: symbols extracted from holdings (30-day period)
- **Output**: volatility score

#### e. Check Risk Thresholds
- **Tool**: `check_risk_threshold()`
- **Inputs**: portfolio value, volatility score, risk configuration
- **Output**: is_high_risk, exceeded thresholds, risk level

#### f. Generate Report
- **Tool**: `generate_report()`
- **Input**: all calculated data (portfolio analysis data)
- **Output**: formatted report string

#### g. Send Notification
- **Tool**: `send_notification()`
- **Inputs**: manager_email from portfolio data, generated report, priority="high"
- **Output**: notification result

#### h. Log Operation
- **Tool**: `log_operation()`
- **Inputs**: operation name (e.g., "portfolio_analysis"), operation details
- **Output**: None (logs to system)

### Step 3: Error Handling Strategy
- Wrap each portfolio processing block in a try/except block
- Log errors using the `log_operation` tool with level="error"
- Continue processing remaining portfolios if one fails

## Implementation (Python)

```python
from tools_reference import (
    get_stock_prices,
    get_portfolio_holdings,
    calculate_portfolio_value,
    calculate_volatility_score,
    check_risk_threshold,
    generate_report,
    send_notification,
    log_operation
)

def analyze_portfolios():
    """Main orchestration function."""
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }

    log_operation("portfolio_analysis_start", {"portfolios": portfolios})

    for portfolio_id in portfolios:
        try:
            # Step a: Fetch Holdings
            portfolio = get_portfolio_holdings(portfolio_id)
            holdings = portfolio["holdings"]
            manager_email = portfolio["manager_email"]

            # Step b: Get Stock Prices
            symbols = [h["symbol"] for h in holdings]
            current_prices = get_stock_prices(symbols)

            # Step c: Calculate Portfolio Value and Positions
            value_data = calculate_portfolio_value(holdings, current_prices)

            # Step d: Calculate Volatility Score
            volatility = calculate_volatility_score(symbols, days=30)

            # Step e: Check Risk Thresholds
            risk_check = check_risk_threshold(
                value_data["total_value"], volatility, risk_config
            )

            # Log risk check result
            log_operation("risk_check", {
                "portfolio_id": portfolio_id,
                "risk_level": risk_check["risk_level"],
                "exceeded_thresholds": risk_check["exceeded_thresholds"]
            })

            if risk_check["is_high_risk"]:
                # Step f: Generate Report
                report_text = generate_report(
                    {**portfolio, **value_data, "volatility_score": volatility},
                    report_format="markdown"
                )

                # Step g: Send Notification
                result = send_notification(
                    recipient=manager_email,
                    subject="High Risk Alert: Portfolio {}".format(portfolio_id),
                    message=report_text,
                    priority="high"
                )

                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "sent": result["sent"],
                    "message_id": result["message_id"]
                })

        except ValueError as e:
            log_operation("error", {"operation": "portfolio_analysis", "details": str(e)})
        except Exception as e:  # Catch all other exceptions
            log_operation("error", {"operation": "portfolio_analysis", "details": str(e)})

    log_operation("portfolio_analysis_end", {"portfolios": portfolios})

if __name__ == "__main__":
    analyze_portfolios()
```

## Design Justification (Markdown)

### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because it simplifies dependency management and error handling. Each portfolio's data is processed independently, making it easier to diagnose issues and continue processing subsequent portfolios.

### Data Flow Strategy
Holdings data feeds into three downstream operations: price fetching, value calculation, and volatility scoring. This modular approach ensures that each step operates on the necessary input data and produces the correct output for further steps.

### Error Handling Strategy
Wrapping each portfolio's processing in a try/except block allows for graceful degradation. Errors are logged using `log_operation` with an appropriate log level to maintain an audit trail. By continuing to process other portfolios even if one fails, we ensure that no single error prevents the entire analysis from running.

### Trade-offs Considered
- **Sequential Processing**: Simplicity and easier debugging but may be slower for large numbers of portfolios.
- **Parallel Processing**: Potential for faster execution but adds complexity in managing dependencies and error handling.
- **Logging**: Comprehensive logging helps with debugging and maintaining an audit trail, adding overhead compared to bare-minimum logging.