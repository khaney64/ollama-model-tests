# Portfolio Risk Analysis Agent

## Section 1: Execution Plan

```markdown
## Execution Plan

### Phase 1: Initialization
1. **Set Configuration**
   - Define portfolio list: ["PORT-001", "PORT-002", "PORT-003"]
   - Configure risk thresholds (max_volatility: 35.0, min_value: 50000, max_value: 2000000)
   - Set volatility calculation period: 30 days
   - Log initialization event

### Phase 2: Portfolio Processing Loop
For each portfolio in the portfolio list:

2. **Fetch Portfolio Holdings**
   - Tool: `get_portfolio_holdings(portfolio_id)`
   - Input: Portfolio ID string
   - Output: Holdings dictionary with client_name, manager_email, holdings array
   - Data dependency: Required for all subsequent steps

3. **Extract Symbols**
   - Extract stock symbols from holdings list
   - Input: Holdings dictionary from Step 2
   - Output: List of stock ticker symbols
   - Data dependency: Required for price fetching and volatility calculation

4. **Fetch Current Stock Prices**
   - Tool: `get_stock_prices(symbols)`
   - Input: List of symbols from Step 3
   - Output: Dictionary mapping symbols to current prices
   - Data dependency: Required for value calculation

5. **Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value(holdings, current_prices)`
   - Input: Holdings from Step 2, prices from Step 4
   - Output: Total value and position details with gains/losses
   - Data dependency: Required for risk threshold check

6. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score(symbols, days=30)`
   - Input: Symbols from Step 3
   - Output: Volatility score (0-100 scale)
   - Data dependency: Required for risk threshold check

7. **Check Risk Thresholds**
   - Tool: `check_risk_threshold(portfolio_value, volatility_score, risk_config)`
   - Input: Total value from Step 5, volatility from Step 6, risk_config
   - Output: Risk level and exceeded thresholds list
   - Data dependency: Determines if report/notifications are needed

8. **Log Analysis Start**
   - Tool: `log_operation()`
   - Input: Operation name, portfolio_id, level="info"
   - Output: Audit trail entry

9. **Generate Report (Conditional)**
   - Tool: `generate_report(portfolio_data, "markdown")`
   - Only if: `is_high_risk` is True
   - Input: Portfolio data combining all metrics
   - Output: Formatted markdown report

10. **Send Notification (Conditional)**
    - Tool: `send_notification(recipient, subject, message, priority="high")`
    - Only if: `is_high_risk` is True
    - Input: Manager email, subject, report, priority
    - Output: Notification confirmation with message_id

11. **Log Analysis Complete**
    - Tool: `log_operation()`
    - Input: Operation name, risk level, thresholds exceeded
    - Output: Audit trail entry

### Phase 3: Error Handling Strategy
- Wrap each portfolio in try-except block
- Catch ValueError for tool-specific errors
- Catch generic Exception for unexpected errors
- Log errors with level="error" and continue to next portfolio
- Track processing statistics for final summary log

### Phase 4: Final Summary
12. **Log Final Summary**
    - Tool: `log_operation()`
    - Input: Total processed, high-risk count
    - Output: Final audit entry
```

---

## Section 2: Implementation

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
    Orchestrates the analysis of multiple investment portfolios.
    
    Analyzes each portfolio for risk metrics, identifies high-risk portfolios,
    generates reports, and sends notifications.
    """
    
    # ============== Configuration ==============
    portfolios_to_analyze = ["PORT-001", "PORT-002", "PORT-003"]
    
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    days_for_volatility = 30
    
    # ============== Processing Statistics ==============
    total_portfolios = len(portfolios_to_analyze)
    processed_count = 0
    high_risk_count = 0
    
    # ============== Initialization ==============
    log_operation(
        "portfolio_analysis_start",
        {
            "portfolios": portfolios_to_analyze,
            "risk_config": risk_config
        },
        level="info"
    )
    
    # ============== Portfolio Processing Loop ==============
    for portfolio_id in portfolios_to_analyze:
        processed_count += 1
        
        log_operation(
            "portfolio_analysis_start",
            {
                "portfolio_id": portfolio_id,
                "progress": f"{processed_count}/{total_portfolios}"
            },
            level="info"
        )
        
        try:
            # ============== Step 1: Fetch Holdings ==============
            holdings = get_portfolio_holdings(portfolio_id)
            client_name = holdings.get("client_name", "Unknown")
            manager_email = holdings.get("manager_email", "")
            
            # Extract stock symbols from holdings
            symbols = [h["symbol"] for h in holdings.get("holdings", [])]
            
            # ============== Step 2: Get Stock Prices ==============
            prices = get_stock_prices(symbols)
            
            # ============== Step 3: Calculate Portfolio Value ==============
            value_data = calculate_portfolio_value(holdings["holdings"], prices)
            total_value = value_data["total_value"]
            
            # ============== Step 4: Calculate Volatility Score ==============
            volatility = calculate_volatility_score(symbols, days=days_for_volatility)
            
            # ============== Step 5: Check Risk Thresholds ==============
            risk_check = check_risk_threshold(total_value, volatility, risk_config)
            risk_level = risk_check["risk_level"]
            exceeded_thresholds = risk_check["exceeded_thresholds"]
            is_high_risk = risk_check["is_high_risk"]
            
            # ============== Step 6: Log Analysis Start ==============
            log_operation(
                "portfolio_analysis_start",
                {
                    "portfolio_id": portfolio_id,
                    "client_name": client_name,
                    "total_value": total_value,
                    "volatility_score": volatility,
                    "risk_level": risk_level
                },
                level="info"
            )
            
            # ============== Step 7: Generate Report (Conditional) ==============
            if is_high_risk:
                high_risk_count += 1
                
                # Combine all data for report generation
                portfolio_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": client_name,
                    "total_value": total_value,
                    "volatility_score": volatility,
                    "risk_level": risk_level,
                    "exceeded_thresholds": exceeded_thresholds,
                    "positions": value_data["positions"]
                }
                
                # Generate markdown report
                report = generate_report(portfolio_data, report_format="markdown")
                
                # ============== Step 8: Send Notification (Conditional) ==============
                subject = f"High Risk Alert: Portfolio {portfolio_id}"
                notification_result = send_notification(
                    recipient=manager_email,
                    subject=subject,
                    message=report,
                    priority="high"
                )
                
                # Log high-risk notification
                log_operation(
                    "high_risk_notification",
                    {
                        "portfolio_id": portfolio_id,
                        "client_name": client_name,
                        "risk_level": risk_level,
                        "exceeded_thresholds": exceeded_thresholds,
                        "message_id": notification_result["message_id"]
                    },
                    level="warning"
                )
                
            else:
                # Log normal analysis completion
                log_operation(
                    "portfolio_analysis_complete",
                    {
                        "portfolio_id": portfolio_id,
                        "client_name": client_name,
                        "risk_level": risk_level,
                        "exceeded_thresholds": exceeded_thresholds
                    },
                    level="info"
                )
            
            # ============== Step 9: Log Analysis Complete ==============
            log_operation(
                "portfolio_analysis_complete",
                {
                    "portfolio_id": portfolio_id,
                    "client_name": client_name,
                    "risk_level": risk_level,
                    "exceeded_thresholds": exceeded_thresholds
                },
                level="info"
            )
            
        except ValueError as e:
            # Handle tool-specific validation errors
            log_operation(
                "portfolio_error",
                {
                    "portfolio_id": portfolio_id,
                    "error_type": "ValueError",
                    "details": str(e)
                },
                level="error"
            )
            continue
            
        except Exception as e:
            # Handle unexpected errors
            log_operation(
                "portfolio_error",
                {
                    "portfolio_id": portfolio_id,
                    "error_type": "Exception",
                    "details": str(e)
                },
                level="error"
            )
            continue
    
    # ============== Final Summary ==============
    log_operation(
        "portfolio_analysis_complete",
        {
            "total_portfolios": total_portfolios,
            "processed": processed_count,
            "high_risk_count": high_risk_count
        },
        level="info"
    )


if __name__ == "__main__":
    analyze_portfolios()
```

---

## Section 3: Design Justification

### Tool Orchestration Sequence

I chose a **sequential processing approach** rather than parallel execution because each portfolio's analysis depends entirely on the previous steps within that portfolio. Specifically:
- `get_portfolio_holdings()` is required before any other operations
- `get_stock_prices()` requires symbols extracted from holdings
- `calculate_portfolio_value()` needs both holdings and prices
- `calculate_volatility_score()` only needs symbols
- `check_risk_threshold()` needs value and volatility results

Sequential processing ensures data integrity and avoids race conditions. The outer loop iterates over portfolios while the inner pipeline processes each portfolio's data flow independently.

### Data Flow Strategy

The data flow is **linear and unidirectional**:
1. Holdings → Symbols (extraction step)
2. Holdings + Prices → Portfolio Value (requires both)
3. Symbols → Volatility (independent of holdings)
4. Value + Volatility → Risk Check (combined result)

This design ensures:
- No data is lost between steps
- Each intermediate result is used by downstream operations
- Conditional operations (report/notification) only execute when needed

### Error Handling Strategy

I implemented **layered error handling**:
- **Try-except wrapper** around each portfolio to prevent a single failure from stopping the entire process
- **Specific exception catching** for `ValueError` (expected tool errors) vs generic `Exception` (unexpected issues)
- **Comprehensive logging** at each error point with error type and details
- **Continue on error** ensures processing continues for remaining portfolios

This approach ensures **resilience** - if one portfolio has invalid data or API issues, the system can still analyze and report on the others.

### Trade-offs Considered

1. **Conditional Operations**: Report generation and notifications are only created for high-risk portfolios, conserving resources for portfolios that need attention.

2. **Logging Granularity**: Multiple log operations are placed at strategic points (start, error, completion, high-risk notification) to provide a complete audit trail without excessive verbosity.

3. **Error Severity Levels**: Using different log levels ("info" for routine operations, "warning" for high-risk findings, "error" for failures) helps in filtering and alerting.

4. **Default Values**: Using `.get()` with defaults for optional fields (client_name, manager_email) prevents crashes if data is incomplete.

### Code Quality

- **Type hints** are implicitly handled through Python's dynamic nature
- **Docstrings** explain each function's purpose
- **Comments** indicate each major section of the orchestration logic
- **Clear variable names** improve readability
- **Logical structure** groups related operations together