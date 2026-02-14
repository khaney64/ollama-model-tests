# Agentic Task: Portfolio Risk Analysis Agent

## Section 1: Execution Plan

### Step-by-Step Execution Plan

1.  **Initialize Configuration**
    *   **Tools:** None (Setup Logic)
    *   **Action:** Define the list of target portfolios ["PORT-001", "PORT-002", "PORT-003"] and the risk configuration dictionary with `max_volatility`, `min_value`, and `max_value`.

2.  **Initialize Audit Logging**
    *   **Tools:** `log_operation`
    *   **Action:** Log the start of the risk monitoring session with level "info".

3.  **Iterate Through Each Portfolio**
    *   **Tools:** `get_portfolio_holdings`, Error Handling
    *   **Action:** Loop through the portfolio list. For each ID, attempt to fetch holdings data.

4.  **Extract Symbol List**
    *   **Tools:** Data Extraction (List Comprehension)
    *   **Input:** Holdings data from Step 3
    *   **Output:** List of unique stock symbols.
    *   **Dependencies:** Required for fetching prices and calculating volatility.

5.  **Fetch Current Stock Prices**
    *   **Tools:** `get_stock_prices`
    *   **Input:** Symbol list from Step 4
    *   **Output:** Dictionary mapping symbols to current prices.
    *   **Dependencies:** Required for calculating portfolio value and individual position gains/losses.

6.  **Calculate Portfolio Value**
    *   **Tools:** `calculate_portfolio_value`
    *   **Input:** Holdings from Step 3 and Prices from Step 5
    *   **Output:** Total portfolio value and position breakdown.
    *   **Dependencies:** Required for risk threshold check and report generation.

7.  **Calculate Volatility Score**
    *   **Tools:** `calculate_volatility_score`
    *   **Input:** Symbol list from Step 4
    *   **Output:** Volatility score (0-100).
    *   **Dependencies:** Required for risk threshold check.

8.  **Check Risk Thresholds**
    *   **Tools:** `check_risk_threshold`
    *   **Input:** Total value from Step 6, Volatility from Step 7, and Risk Config from Step 1.
    *   **Output:** Risk assessment (is_high_risk, risk_level, exceeded_thresholds).

9.  **Log Analysis Results**
    *   **Tools:** `log_operation`
    *   **Action:** Log the result of the risk check for this specific portfolio (level "info" for standard, "warning" for high risk).

10. **Identify High-Risk Portfolios**
    *   **Tools:** Conditional Logic (`if` statement)
    *   **Action:** If `is_high_risk` is True, proceed to report generation and notification. If False, skip to the next portfolio.

11. **Generate Risk Report**
    *   **Tools:** `generate_report`
    *   **Input:** Consolidated analysis data (Portfolio ID, Client Name, Total Value, Volatility, Risk Level, Exceeded Thresholds, Positions) from Steps 3, 6, 7, 8.
    *   **Output:** Formatted Markdown string.

12. **Send Notification**
    *   **Tools:** `send_notification`
    *   **Input:** Manager email, Report content, High priority flag.
    *   **Output:** Delivery confirmation.

13. **Log Notification Success**
    *   **Tools:** `log_operation`
    *   **Action:** Log the notification attempt as a warning since high risk was detected.

14. **Error Handling Strategy**
    *   **Tool:** `try/except` blocks wrapped around each portfolio's processing loop.
    *   **Strategy:** Wrap the main processing loop in a `try/except` block. If a `ValueError` (or any error) occurs during a specific portfolio's processing:
        *   Log the specific error details.
        *   Continue immediately to the next portfolio in the list to ensure all other portfolios are analyzed.

---

## Section 2: Implementation

```python
"""
Portfolio Risk Analysis Agent
Orchestrates analysis of multiple portfolios, calculates risk metrics,
and sends notifications for high-risk portfolios.
"""

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
    Main orchestration function for portfolio risk analysis.
    Processes multiple portfolios and handles high-risk notifications.
    """
    # Configuration
    PORTFOLIO_IDS = ["PORT-001", "PORT-002", "PORT-003"]
    
    RISK_CONFIG = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    # Log session start
    log_operation(
        "system_start",
        {"total_portfolios": len(PORTFOLIO_IDS)},
        level="info"
    )

    for portfolio_id in PORTFOLIO_IDS:
        try:
            # Step 1: Fetch Holdings
            holdings_data = get_portfolio_holdings(portfolio_id)
            
            # Step 2: Extract Symbols for further tools
            symbols = [holding["symbol"] for holding in holdings_data["holdings"]]
            
            log_operation(
                "portfolio_analysis_start",
                {"portfolio_id": portfolio_id, "symbols_count": len(symbols)},
                level="info"
            )
            
            # Step 3: Fetch Current Stock Prices
            prices = get_stock_prices(symbols)
            
            # Step 4: Calculate Portfolio Value
            value_data = calculate_portfolio_value(holdings_data["holdings"], prices)
            
            # Step 5: Calculate Volatility Score
            volatility = calculate_volatility_score(symbols, days=30)
            
            # Step 6: Check Risk Thresholds
            risk_check = check_risk_threshold(
                value_data["total_value"], 
                volatility, 
                RISK_CONFIG
            )
            
            # Step 7: Log the risk assessment
            log_operation(
                "risk_check",
                {
                    "portfolio_id": portfolio_id,
                    "total_value": value_data["total_value"],
                    "volatility": volatility,
                    "risk_level": risk_check["risk_level"],
                    "exceeded": risk_check["exceeded_thresholds"]
                },
                level="info"
            )
            
            # Step 8: High Risk Response
            if risk_check["is_high_risk"]:
                # Prepare report data
                report_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": holdings_data["client_name"],
                    "total_value": value_data["total_value"],
                    "volatility_score": volatility,
                    "risk_level": risk_check["risk_level"],
                    "exceeded_thresholds": risk_check["exceeded_thresholds"],
                    "positions": value_data["positions"]
                }
                
                # Generate Report
                report_text = generate_report(report_data, report_format="markdown")
                
                log_operation(
                    "report_generation",
                    {"portfolio_id": portfolio_id},
                    level="warning"
                )
                
                # Send Notification
                notification_result = send_notification(
                    holder_email := holdings_data["manager_email"],
                    f"URGENT: High Risk Alert - Portfolio {portfolio_id}",
                    report_text,
                    priority="high"
                )
                
                log_operation(
                    "notification_sent",
                    {
                        "portfolio_id": portfolio_id,
                        "recipient": holder_email,
                        "message_id": notification_result["message_id"]
                    },
                    level="warning"
                )
            
        except ValueError as e:
            # Handle specific API errors gracefully
            log_operation(
                "processing_error",
                {"portfolio_id": portfolio_id, "error_type": "ValueError", "message": str(e)},
                level="error"
            )
            continue
            
        except Exception as e:
            # Handle any unexpected errors gracefully
            log_operation(
                "unexpected_error",
                {"portfolio_id": portfolio_id, "error_message": str(e)},
                level="error"
            )
            continue

    # Log session completion
    log_operation(
        "system_complete",
        {"status": "completed"},
        level="info"
    )

if __name__ == "__main__":
    analyze_portfolios()
```

---

## Section 3: Design Justification

### Tool Orchestration Sequence
I chose a strictly sequential orchestration model where the output of one tool becomes the input of the next. This is dictated by the data dependencies:
1.  **Data Ingress**: We must start with `get_portfolio_holdings` to get the raw data.
2.  **Parallel Preparation**: We need the `symbols` list immediately, so after fetching holdings, we extract symbols.
3.  **Data Processing**: The `calculate_portfolio_value` and `calculate_volatility_score` tools require different inputs. One requires `holdings` + `prices`, the other just `symbols`. This necessitates fetching prices *after* extracting symbols.
4.  **Analysis**: Once `total_value`, `volatility`, and `holdings` are ready, `check_risk_threshold` can be called.
5.  **Action**: Finally, if a high risk is detected, `generate_report` and `send_notification` are triggered. This sequential flow ensures that no data is lost between steps and operations only proceed if the prerequisites (like valid prices) are met.

### Data Flow Strategy
The data flow is designed to minimize redundant calls. For example, the `symbols` list is used twice: once for fetching prices and once for calculating volatility. I extract this once during the loop to ensure consistency. The portfolio details (ID, Client Name, Manager Email) are carried forward from the initial `holdings_data` dictionary to ensure the report and notification contain the correct client context.

### Error Handling Strategy Rationale
The `try-except` block is the core of the agent's resilience.
*   **Granularity**: I wrapped the specific portfolio processing loop in a `try-except`. This ensures that if `PORT-001` fails due to a network error or invalid ID, the script logs the error and immediately moves to `PORT-002` and `PORT-003`. Without this, a single failure would terminate the entire analysis for all clients.
*   **Specific Exceptions**: The `ValueError` is caught specifically because the tools are specified to raise this type of error (e.g., "Raises ValueError if portfolio_id is invalid"). Catching this allows the script to handle the "expected" errors defined in the tool specs gracefully rather than crashing with a raw exception.
*   **Logging**: Every step is paired with a `log_operation` call. This satisfies the requirement to maintain an audit trail, ensuring that every portfolio analyzed and every error encountered is recorded for future review.

### Trade-offs Considered
*   **Parallel vs. Sequential**: I chose sequential processing over parallel. While fetching prices for multiple portfolios *could* happen in parallel, the tools provided in this scenario are function calls (simulating synchronous API calls). Orchestrating true parallelism would require more complex concurrency logic (like `concurrent.futures`) and could complicate the audit trail ordering. Sequential is clearer for a monitoring script where one portfolio's delay shouldn't necessarily block others indefinitely, and it's easier to read/maintain.
*   **Default vs. Custom**: I used the default `days=30` for volatility calculation as specified in the requirements, as no specific time period was requested for this metric, and 30 days is a standard industry benchmark.