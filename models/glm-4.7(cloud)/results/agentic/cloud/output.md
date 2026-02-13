## Execution Plan

1. **Initialize Configuration**
   - Set the list of portfolio IDs to analyze: `["PORT-001", "PORT-002", "PORT-003"]`.
   - Define the risk configuration dictionary with thresholds:
     ```python
     {
         "max_volatility": 35.0,
         "min_value": 50000,
         "max_value": 2000000
     }
     ```

2. **Iterate over each portfolio ID**

   a. **Log start of analysis**  
      - Tool: `log_operation`  
      - Log level: `info`  
      - Details: portfolio_id

   b. **Fetch portfolio holdings**  
      - Tool: `get_portfolio_holdings`  
      - Input: portfolio_id  
      - Output: holdings dictionary (contains client_name, manager_email, holdings list)  

   c. **Extract stock symbols**  
      - No tool; process holdings list to get list of symbols.  
      - If holdings list is empty, raise a ValueError to trigger error handling.

   d. **Retrieve current stock prices**  
      - Tool: `get_stock_prices`  
      - Input: list of symbols  
      - Output: dictionary mapping symbols to prices (some may be `None`)  

   e. **Calculate portfolio value**  
      - Tool: `calculate_portfolio_value`  
      - Input: holdings list and current prices dictionary  
      - Output: total_value and detailed positions  

   f. **Calculate volatility score**  
      - Tool: `calculate_volatility_score`  
      - Input: symbols list, `days=30`  
      - Output: volatility score (0-100)  

   g. **Check risk thresholds**  
      - Tool: `check_risk_threshold`  
      - Input: total_value, volatility_score, risk_config  
      - Output: dict with `is_high_risk`, `exceeded_thresholds`, `risk_level`  

   h. **Log risk check result**  
      - Tool: `log_operation`  
      - Level: `warning` if high risk, else `info`  
      - Details: include portfolio_id, total_value, volatility, risk_level, is_high_risk  

   i. **If portfolio is high-risk:**

      1. **Assemble data for report**  
         - Combine: portfolio_id, client_name, total_value, volatility_score, risk_level, exceeded_thresholds, positions (from value calculation)

      2. **Generate markdown report**  
         - Tool: `generate_report`  
         - Input: assembled data, `report_format="markdown"`  
         - Output: formatted report string  

      3. **Log report generation**  
         - Tool: `log_operation`  
         - Level: `info`  

      4. **Send notification**  
         - Tool: `send_notification`  
         - Input: recipient = manager_email, subject = "High Risk Alert: Portfolio {portfolio_id}", message = report, `priority="high"`  
         - Output: dict with sent status and message_id  

      5. **Log notification**  
         - Tool: `log_operation`  
         - Level: `info`  
         - Details: recipient, message_id, sent status  

   j. **If portfolio is not high-risk:**
      - Log completion with status "safe" (info level).

3. **Error Handling Strategy**
   - Each portfolio processing block is wrapped in a `try...except` to catch errors.
   - Specific `ValueError` exceptions are caught because all tools raise `ValueError` for invalid inputs or missing data (e.g., invalid portfolio_id, empty symbols, negative values, etc.).
   - A generic `Exception` catch handles any unexpected errors.
   - On error, details are logged with level `error` and the loop continues to the next portfolio (graceful degradation).
   - Missing stock price data: if `get_stock_prices` returns an empty dictionary or all prices are `None`, `calculate_portfolio_value` will raise a `ValueError`, which is caught and logged.
   - Failed notifications: if `send_notification` raises an error (e.g., invalid email), it is caught and logged; the script proceeds without retrying.

4. **Final Step**
   - After all portfolios are processed, the script ends.

---

## Implementation

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
    """
    Main orchestration function to analyze multiple portfolios,
    calculate risk metrics, and notify managers for high-risk portfolios.
    """
    # Configuration
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }

    for portfolio_id in portfolio_ids:
        try:
            # 1. Start analysis
            log_operation(
                "portfolio_analysis_start",
                {"portfolio_id": portfolio_id},
                level="info"
            )

            # 2. Retrieve holdings
            holdings_data = get_portfolio_holdings(portfolio_id)
            holdings_list = holdings_data["holdings"]
            log_operation(
                "portfolio_holdings_retrieved",
                {"portfolio_id": portfolio_id, "holdings_count": len(holdings_list)},
                level="info"
            )

            if not holdings_list:
                raise ValueError(f"Portfolio {portfolio_id} has no holdings")

            # 3. Extract symbols
            symbols = [h["symbol"] for h in holdings_list]

            # 4. Fetch current prices
            prices = get_stock_prices(symbols)
            log_operation(
                "stock_prices_fetched",
                {"portfolio_id": portfolio_id, "symbols": symbols},
                level="info"
            )

            # 5. Calculate portfolio value
            value_data = calculate_portfolio_value(holdings_list, prices)
            total_value = value_data["total_value"]
            positions = value_data["positions"]

            # 6. Calculate volatility
            volatility = calculate_volatility_score(symbols, days=30)

            # 7. Check risk thresholds
            risk_result = check_risk_threshold(total_value, volatility, risk_config)
            is_high_risk = risk_result["is_high_risk"]
            risk_level = risk_result["risk_level"]
            exceeded_thresholds = risk_result["exceeded_thresholds"]

            log_operation(
                "risk_check",
                {
                    "portfolio_id": portfolio_id,
                    "total_value": total_value,
                    "volatility": volatility,
                    "risk_level": risk_level,
                    "is_high_risk": is_high_risk
                },
                level="warning" if is_high_risk else "info"
            )

            if is_high_risk:
                # 8. Prepare data for report
                portfolio_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings_data["client_name"],
                    "total_value": total_value,
                    "volatility_score": volatility,
                    "risk_level": risk_level,
                    "exceeded_thresholds": exceeded_thresholds,
                    "positions": positions
                }

                # 9. Generate markdown report
                report = generate_report(portfolio_data, report_format="markdown")
                log_operation(
                    "report_generated",
                    {"portfolio_id": portfolio_id, "format": "markdown"},
                    level="info"
                )

                # 10. Send notification
                recipient = holdings_data["manager_email"]
                subject = f"High Risk Alert: Portfolio {portfolio_id}"
                notification_result = send_notification(
                    recipient,
                    subject,
                    report,
                    priority="high"
                )
                log_operation(
                    "notification_sent",
                    {
                        "portfolio_id": portfolio_id,
                        "recipient": recipient,
                        "message_id": notification_result["message_id"],
                        "sent": notification_result["sent"]
                    },
                    level="info"
                )
            else:
                # Safe portfolio
                log_operation(
                    "portfolio_analysis_complete",
                    {"portfolio_id": portfolio_id, "status": "safe"},
                    level="info"
                )

        except ValueError as e:
            # Expected errors from tools (invalid inputs, missing data)
            log_operation(
                "error",
                {"portfolio_id": portfolio_id, "error": str(e)},
                level="error"
            )
            continue
        except Exception as e:
            # Unexpected errors
            log_operation(
                "error",
                {"portfolio_id": portfolio_id, "error": f"Unexpected error: {str(e)}"},
                level="error"
            )
            continue


if __name__ == "__main__":
    analyze_portfolios()
```

---

## Design Justification

### Tool Orchestration Sequence

The script processes portfolios sequentially rather than in parallel. This approach simplifies error handling and ensures that each portfolio's analysis is independent. Sequential processing is appropriate for this task because the number of portfolios is small (three) and there is no requirement for parallel execution. It also makes logging and debugging straightforward, as each portfolio's operations are performed in a well-defined order.

### Data Flow Strategy

Data flows in a clear, linear pipeline for each portfolio:

- `get_portfolio_holdings` provides the foundational holdings data.
- The list of symbols extracted from holdings is used as input to `get_stock_prices` and `calculate_volatility_score`.
- The holdings list and the prices dictionary feed into `calculate_portfolio_value` to obtain total value and position details.
- Total value and volatility score are passed to `check_risk_threshold`.
- If the portfolio is high-risk, all collected data (portfolio_id, client_name, total_value, volatility, risk_level, exceeded_thresholds, positions) is assembled into a single dictionary for `generate_report`.
- Finally, the manager's email from holdings and the generated report are used to send a notification.

This pipeline ensures that each tool receives the exact inputs it expects and that no data is lost or incorrectly transformed. The intermediate results are stored in variables to be reused, avoiding redundant calls.

### Error Handling Strategy

The script employs a multi-layered error handling approach:

- **Try-except around each portfolio**: Any error during processing of a single portfolio is caught, logged, and then the loop continues to the next portfolio. This meets the requirement to "continue processing remaining portfolios if one fails."
- **Specific catches for `ValueError`**: All provided tools raise `ValueError` for invalid inputs (e.g., empty symbols, negative values, invalid portfolio IDs). Catching `ValueError` allows us to distinguish expected errors from unexpected ones.
- **Generic `Exception` catch**: As a safety net, any other exception is also caught and logged, preventing the script from crashing.
- **Logging at appropriate levels**: Operations are logged as `info`, warnings as `warning` (for high-risk detection), and errors as `error`. This creates a clear audit trail.

### Completeness and Tool Usage

All eight tools are utilized, fulfilling the requirement to orchestrate them. The script meets all functional requirements: analyzing three portfolios, calculating value and volatility, applying the given risk configuration, identifying high-risk portfolios, generating markdown reports, sending high-priority notifications, and maintaining an audit log.

### Trade-offs

One trade-off is that the script does not implement retries for failed notifications or missing price data. While retries could improve reliability, the requirement only asks to "handle errors gracefully" and continue; adding retries would increase complexity without explicit instruction. Additionally, the script does not aggregate statistics across portfolios (e.g., summary report), as the task focuses on individual portfolio monitoring and alerts.

Overall, the design prioritizes clarity, correctness, and robustness, making it suitable for production use in a simulated environment.