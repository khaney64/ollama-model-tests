## Section 1: Execution Plan (Markdown)

### Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list.

2. **For Each Portfolio:**

   a. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: portfolio_id
   - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: symbols extracted from holdings
   - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value()`
   - Input: holdings data and current prices
   - Output: portfolio value and position details

   d. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: symbols from holdings
   - Output: volatility score

   e. **Check Risk Thresholds**
   - Tool: `check_risk_threshold()`
   - Input: portfolio value, volatility score, and risk configuration
   - Output: risk level and exceeded thresholds

   f. **Generate Report (if high-risk)**
   - Tool: `generate_report()`
   - Input: portfolio data (including risk level and exceeded thresholds)
   - Output: formatted report string

   g. **Send Notification (if high-risk)**
   - Tool: `send_notification()`
   - Input: recipient email, subject line, message, and priority
   - Output: notification result

3. **Log Operations**
   - Tools: `log_operation()`
   - Log portfolio analysis start/completion, risk threshold checks, report generation, and notification sending.

4. **Error Handling Strategy**
   - Wrap each major operation in try/except blocks.
   - Log errors with appropriate log levels.
   - Continue processing remaining portfolios if one fails.

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

    for portfolio_id in portfolios:
        log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id})
        
        try:
            # Step a: Fetch Holdings
            holdings_data = get_portfolio_holdings(portfolio_id)
            symbols = [holding["symbol"] for holding in holdings_data.get("holdings", [])]

            # Step b: Get Stock Prices
            current_prices = get_stock_prices(symbols)

            # Step c: Calculate Portfolio Value
            portfolio_value_data = calculate_portfolio_value(holdings_data["holdings"], current_prices)
            
            # Step d: Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols, days=30)

            # Step e: Check Risk Thresholds
            risk_check_result = check_risk_threshold(
                portfolio_value_data["total_value"],
                volatility_score,
                risk_config
            )

            # Prepare data for report generation
            portfolio_data = {
                "portfolio_id": holdings_data["portfolio_id"],
                "client_name": holdings_data["client_name"],
                "total_value": portfolio_value_data["total_value"],
                "volatility_score": volatility_score,
                "risk_level": risk_check_result["risk_level"],
                "exceeded_thresholds": risk_check_result["exceeded_thresholds"],
                "positions": portfolio_value_data["positions"]
            }

            if risk_check_result["is_high_risk"]:
                # Step f: Generate Report
                report_text = generate_report(portfolio_data, report_format="markdown")

                # Step g: Send Notification
                notification_result = send_notification(
                    holdings_data["manager_email"],
                    "High Risk Alert",
                    report_text,
                    priority="high"
                )
                
                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "recipient": holdings_data["manager_email"],
                    "sent": notification_result.get("sent", False)
                })

        except Exception as e:
            # Log any errors encountered during processing
            log_operation("error_occurred", {
                "portfolio_id": portfolio_id,
                "error_message": str(e)
            })
        
        finally:
            log_operation("portfolio_analysis_end", {"portfolio_id": portfolio_id})

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification (Markdown)

### Design Justification

#### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because it simplifies error handling and ensures that all operations for a single portfolio are completed before moving on to the next. This approach also allows us to maintain a clear audit trail with logs for each portfolio, making troubleshooting easier.

#### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
1. Holdings provide the list of stock symbols needed to fetch current prices.
2. Both holdings and current prices are required to calculate the portfolio's total value and position details.
3. Symbols from holdings are used to compute the volatility score.

This sequential flow ensures that data dependencies are met at each step, preventing errors due to missing or incomplete information.

#### Error Handling Strategy
Error handling is crucial to ensure the robustness of the system:
- Each major operation is wrapped in a try/except block to catch and log any exceptions.
- Errors during portfolio processing do not halt the entire script; instead, the script logs the error and continues with the next portfolio.
- Specific error messages are logged for better traceability.

#### Trade-offs Considered
1. **Sequential vs. Parallel Processing**: While parallel processing could speed up execution for large numbers of portfolios, it increases complexity in terms of error handling and data synchronization. Given that we only have three portfolios to process, the simplicity of sequential processing is preferred.
2. **Logging Verbosity**: Logging every operation provides a detailed audit trail but may generate a large volume of logs. The balance between verbosity and performance has been considered by focusing on critical operations.

This design ensures that all requirements are met while maintaining a robust, scalable, and maintainable system.