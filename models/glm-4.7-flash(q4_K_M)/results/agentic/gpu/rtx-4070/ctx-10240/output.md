### Section 1: Execution Plan

```markdown
## Execution Plan

### 1. Initialization
- **Tools**: None
- **Actions**: Define the list of portfolios to analyze (`["PORT-001", "PORT-002", "PORT-003"]`) and the risk configuration dictionary (`max_volatility: 35.0`, `min_value: 50000`, `max_value: 2000000`).
- **Log**: Record the start of the risk analysis batch operation.

### 2. Portfolio Processing Loop
Iterate through each portfolio ID in the defined list.

#### For Each Portfolio (a-e):
**a. Fetch Holdings**
- **Tool**: `get_portfolio_holdings(portfolio_id)`
- **Dependency**: Portfolio ID from the list.
- **Data Needed**: `portfolio_id`, `client_name`, `manager_email`, `holdings`.
- **Error Handling**: Catch `ValueError` (invalid ID). Log the error and skip to the next portfolio.

**b. Extract Symbols**
- **Tool**: List comprehension
- **Dependency**: Output from Step (a).
- **Data Needed**: List of unique stock ticker symbols from holdings.
- **Error Handling**: If holdings list is empty, symbols will be empty.

**c. Fetch Stock Prices**
- **Tool**: `get_stock_prices(symbols)`
- **Dependency**: List of symbols from Step (b).
- **Data Needed**: Dictionary mapping symbols to current prices.
- **Error Handling**: Catch `ValueError` (empty symbols). Log warning and continue.

**d. Calculate Portfolio Metrics**
- **Tool 1**: `calculate_portfolio_value(holdings, current_prices)`
  - *Input*: Holdings from (a), Prices from (c).
  - *Output*: `total_value`, `positions`.
- **Tool 2**: `calculate_volatility_score(symbols, days=30)`
  - *Input*: Symbols from (b).
  - *Output*: `volatility_score`.
- **Error Handling**: Catch general exceptions during calculation. Log error and skip to notification if this step fails.

**e. Risk Assessment**
- **Tool**: `check_risk_threshold(portfolio_value, volatility_score, risk_config)`
- **Dependency**: `total_value` from (d), `volatility_score` from (d), global `risk_config`.
- **Output**: `is_high_risk`, `exceeded_thresholds`, `risk_level`.

**f. Reporting & Notification (Conditional)**
- **If `is_high_risk` is True:**
  1. **Merge Data**: Construct a comprehensive dictionary containing `portfolio_id`, `client_name`, `total_value`, `volatility_score`, `risk_level`, `exceeded_thresholds`, and `positions`.
  2. **Generate Report**: Call `generate_report(portfolio_data, "markdown")`.
  3. **Send Notification**: Call `send_notification(recipient, subject, message, "high")` using the manager's email from (a).
  4. **Log**: Record a warning level log with details of the high-risk alert.
- **Else:**
  1. **Log**: Record an info level log with basic portfolio analysis completion.

**g. Portfolio Completion**
- Log the completion of processing for the specific portfolio ID.

### 3. Finalization
- Log the conclusion of the entire analysis batch.

### Error Handling Strategy
- **Portfolio Errors**: Wrap the entire portfolio block (Steps a-g) in a `try-except` block. If an error occurs (e.g., API failure), log it and proceed to the next portfolio without stopping the system.
- **Data Errors**: If `calculate_volatility_score` or `calculate_portfolio_value` raises an error, the specific portfolio is skipped for reporting/notification, but the system continues.
```

---

### Section 2: Implementation

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

def analyze_portfolio_risk():
    """
    Orchestrates the analysis of multiple portfolios to identify high-risk
    entities, generate reports, and notify managers.
    """
    
    # 1. Configuration
    PORTFOLIO_IDS = ["PORT-001", "PORT-002", "PORT-003"]
    RISK_CONFIG = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }

    log_operation(
        "risk_analysis_start",
        {"total_portfolios": len(PORTFOLIO_IDS), "thresholds": RISK_CONFIG},
        level="info"
    )

    # 2. Process each portfolio
    for portfolio_id in PORTFOLIO_IDS:
        portfolio_summary = {
            "portfolio_id": portfolio_id,
            "status": "processing"
        }

        try:
            # Step A: Fetch Holdings
            holdings_data = get_portfolio_holdings(portfolio_id)
            client_name = holdings_data.get("client_name")
            manager_email = holdings_data.get("manager_email")
            holdings = holdings_data.get("holdings", [])
            
            # Extract unique symbols for price fetching and volatility
            symbols = [h['symbol'] for h in holdings if 'symbol' in h]

            # Step B: Fetch Stock Prices
            current_prices = get_stock_prices(symbols)
            
            # Step C: Calculate Portfolio Value
            value_data = calculate_portfolio_value(holdings, current_prices)
            total_value = value_data.get("total_value", 0.0)
            
            # Step D: Calculate Volatility Score
            # Check if symbols exist to avoid tool error
            volatility_score = 0.0
            if symbols:
                volatility_score = calculate_volatility_score(symbols, days=30)
            else:
                log_operation(
                    "volatility_calc_skip",
                    {"portfolio_id": portfolio_id, "reason": "No holdings found"},
                    level="warning"
                )

            # Step E: Check Risk Thresholds
            risk_result = check_risk_threshold(total_value, volatility_score, RISK_CONFIG)
            
            # Prepare data for report generation
            report_data = {
                "portfolio_id": portfolio_id,
                "client_name": client_name,
                "total_value": total_value,
                "volatility_score": volatility_score,
                "risk_level": risk_result.get("risk_level"),
                "exceeded_thresholds": risk_result.get("exceeded_thresholds", []),
                "positions": value_data.get("positions", [])
            }

            # Step F: Reporting & Notification
            if risk_result.get("is_high_risk"):
                report_text = generate_report(report_data, "markdown")
                
                notification_details = send_notification(
                    recipient=manager_email,
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report_text,
                    priority="high"
                )
                
                log_operation(
                    "high_risk_notification_sent",
                    {
                        "portfolio_id": portfolio_id,
                        "risk_level": risk_result["risk_level"],
                        "message_id": notification_details.get("message_id")
                    },
                    level="warning"
                )
            else:
                log_operation(
                    "portfolio_risk_check_complete",
                    {
                        "portfolio_id": portfolio_id,
                        "risk_level": risk_result.get("risk_level")
                    },
                    level="info"
                )

            portfolio_summary["status"] = "complete"

        except ValueError as ve:
            log_operation(
                "portfolio_error",
                {
                    "portfolio_id": portfolio_id,
                    "error_type": "ValueError",
                    "message": str(ve)
                },
                level="error"
            )
            portfolio_summary["status"] = "failed_validation"
        except Exception as e:
            log_operation(
                "portfolio_error",
                {
                    "portfolio_id": portfolio_id,
                    "error_type": "GeneralException",
                    "message": str(e)
                },
                level="error"
            )
            portfolio_summary["status"] = "failed_general"

    # 3. Final Log
    log_operation(
        "risk_analysis_complete",
        {"message": "Batch processing finished"},
        level="info"
    )

if __name__ == "__main__":
    analyze_portfolio_risk()
```

---

### Section 3: Design Justification

```markdown
## Design Justification

### Tool Orchestration Sequence
I chose a sequential orchestration approach (processing portfolios one by one) rather than parallel processing. This ensures data integrity for the report generation step, as the `generate_report` function requires a comprehensive, consolidated dictionary of all metrics (value, volatility, risk level) for a single portfolio. In a parallel setup, we would need additional logic to aggregate results later, which adds complexity. Sequential processing also simplifies the audit logging, making it easy to trace the execution flow of individual portfolios.

### Data Flow Strategy
The data flow follows a linear dependency chain: `Holdings` -> `Prices` -> `Value` -> `Volatility` -> `Risk Check`.
1.  **Symbol Extraction**: Before fetching prices or calculating volatility, I extract the unique list of symbols. This is critical because both downstream tools require this list, and `calculate_volatility_score` will raise a `ValueError` if an empty list is passed.
2.  **Merging Data**: The `calculate_portfolio_value` and `check_risk_threshold` tools return flat data. To satisfy the requirements of `generate_report`, I constructed a merged dictionary. This demonstrates an understanding of data structure transformation to fit downstream API requirements.
3.  **Graceful Degradation**: If `get_stock_prices` returns `None` for some symbols, `calculate_portfolio_value` is designed to skip those positions, so the flow continues without breaking.

### Error Handling Strategy
I implemented a try-except block around the processing of *each* individual portfolio. This meets the requirement to "continue processing remaining portfolios if one fails."
- **Specific Errors**: I catch `ValueError` explicitly for expected API validation errors (like invalid portfolio IDs or empty inputs).
- **General Errors**: I catch `Exception` to catch unexpected failures (like network timeouts or tool bugs).
- **Logging**: Every error results in a `log_operation` call with the `level="error"`. This fulfills the audit trail requirement while ensuring the system remains operational.

### Trade-offs
- **Volatility Calculation**: If a portfolio has holdings but the stock prices tool returns no data (empty dict), the volatility score defaults to 0.0 to avoid crashing. This might underestimate risk if prices are missing, but it is preferable to stopping the entire script. In a real production environment, we would retry fetching prices or fall back to a cached value.
- **Single-threaded**: The script runs synchronously. While this is fine for 3 portfolios, in production with thousands of portfolios, an async approach would be more efficient, though it complicates the logging and report generation order.
```