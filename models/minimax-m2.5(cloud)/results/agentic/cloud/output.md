# Portfolio Risk Analysis Agent

## Section 1: Execution Plan

```markdown
## Execution Plan

### 1. Initialize Configuration
- **Tools**: None
- **Purpose**: Set up risk thresholds, portfolio list, and logging configuration
- **Data Dependencies**: None

### 2. For Each Portfolio (PORT-001, PORT-002, PORT-003):

#### Step 2a: Fetch Portfolio Holdings
- **Tool**: `get_portfolio_holdings()`
- **Input**: portfolio_id (e.g., "PORT-001")
- **Output**: Holdings dictionary with client_name, manager_email, and holdings list
- **Data Dependencies**: None (first operation for each portfolio)
- **Error Handling**: Catch ValueError for invalid portfolio_id, log error, skip to next portfolio

#### Step 2b: Extract and Validate Symbols
- **Tools**: None (data transformation)
- **Purpose**: Extract unique stock symbols from holdings
- **Data Dependencies**: Holdings from Step 2a
- **Error Handling**: Skip positions with missing symbol data

#### Step 2c: Fetch Current Stock Prices
- **Tool**: `get_stock_prices()`
- **Input**: List of symbols extracted from holdings
- **Output**: Dictionary mapping symbols to current prices
- **Data Dependencies**: Symbols from Step 2b
- **Error Handling**: Handle ValueError for empty symbols list; handle None prices for unknown symbols

#### Step 2d: Calculate Portfolio Value
- **Tool**: `calculate_portfolio_value()`
- **Input**: 
  - holdings (from Step 2a)
  - current_prices (from Step 2c)
- **Output**: Total portfolio value and position details (gain/loss)
- **Data Dependencies**: Holdings and current prices
- **Error Handling**: Handle ValueError for empty inputs; skip positions with None prices

#### Step 2e: Calculate Volatility Score
- **Tool**: `calculate_volatility_score()`
- **Input**: 
  - symbols (from Step 2b)
  - days = 30 (default)
- **Output**: Volatility score (0-100 scale)
- **Data Dependencies**: Symbols from Step 2b
- **Error Handling**: Handle ValueError for empty symbols or invalid days

#### Step 2f: Check Risk Thresholds
- **Tool**: `check_risk_threshold()`
- **Input**:
  - portfolio_value (from Step 2d)
  - volatility_score (from Step 2e)
  - risk_config (from initialization)
- **Output**: Risk assessment (is_high_risk, exceeded_thresholds, risk_level)
- **Data Dependencies**: Portfolio value and volatility score
- **Error Handling**: Handle ValueError for negative values

#### Step 2g: Log Risk Assessment
- **Tool**: `log_operation()`
- **Input**: operation="risk_check", details with portfolio_id and risk_level
- **Level**: "warning" if high risk, "info" otherwise
- **Data Dependencies**: Risk assessment from Step 2f

### 3. High-Risk Portfolio Processing (Conditional)

If `is_high_risk` is True:

#### Step 3a: Generate Report
- **Tool**: `generate_report()`
- **Input**:
  - portfolio_data (assembled from all previous steps)
  - report_format="markdown"
- **Output**: Formatted report string
- **Data Dependencies**: All portfolio analysis data
- **Error Handling**: Handle ValueError for missing fields or invalid format

#### Step 3b: Log Report Generation
- **Tool**: `log_operation()`
- **Input**: operation="report_generation", details with portfolio_id
- **Level**: "info"

#### Step 3c: Send Notification
- **Tool**: `send_notification()`
- **Input**:
  - recipient (manager_email from holdings)
  - subject (e.g., "High Risk Alert: Portfolio PORT-001")
  - message (generated report)
  - priority="high"
- **Output**: Notification result with message_id and timestamp
- **Data Dependencies**: Manager email from Step 2a, report from Step 3a
- **Error Handling**: Handle ValueError for invalid email or priority; log failure but continue

#### Step 3d: Log Notification
- **Tool**: `log_operation()`
- **Input**: operation="notification_sent", details with portfolio_id and message_id
- **Level**: "info"

### 4. Error Handling Strategy

- **Per-Portfolio Wrapping**: Each portfolio processing block wrapped in try/except
- **Failure Isolation**: One portfolio's failure doesn't stop processing of others
- **Logging**: All errors logged with appropriate level (error/warning)
- **Data Validation**: Check for None/missing values before passing to tools
- **Graceful Degradation**: Continue with next step if optional data missing

### 5. Audit Trail Maintenance

Log operations at key points:
- "analysis_started" - When beginning portfolio analysis
- "portfolio_fetched" - After getting holdings
- "prices_fetched" - After getting stock prices
- "value_calculated" - After calculating portfolio value
- "volatility_calculated" - After calculating volatility
- "risk_check" - After checking thresholds
- "report_generation" - After generating report
- "notification_sent" - After sending notification
- "analysis_completed" - After finishing all portfolios

All operations logged with portfolio_id context for traceability.
```

---

## Section 2: Implementation (Python)

```python
#!/usr/bin/env python3
"""
Portfolio Risk Analysis Agent

This script orchestrates multiple tools to analyze investment portfolios,
calculate risk metrics, identify high-risk portfolios, generate reports,
and send notifications to portfolio managers.
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


# Configuration
PORTFOLIO_IDS = ["PORT-001", "PORT-002", "PORT-003"]

RISK_CONFIG = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000
}


def analyze_portfolio(portfolio_id: str) -> dict:
    """
    Analyze a single portfolio and return analysis results.
    
    Args:
        portfolio_id: The portfolio identifier to analyze
        
    Returns:
        Dictionary with analysis results or error information
    """
    result = {
        "portfolio_id": portfolio_id,
        "success": False,
        "is_high_risk": False,
        "error": None
    }
    
    # Step 1: Fetch portfolio holdings
    log_operation(
        "portfolio_analysis_started",
        {"portfolio_id": portfolio_id},
        "info"
    )
    
    try:
        portfolio_data = get_portfolio_holdings(portfolio_id)
    except ValueError as e:
        log_operation(
            "portfolio_fetch_error",
            {"portfolio_id": portfolio_id, "error": str(e)},
            "error"
        )
        result["error"] = f"Failed to fetch holdings: {str(e)}"
        return result
    
    log_operation(
        "portfolio_fetched",
        {"portfolio_id": portfolio_id, "client_name": portfolio_data.get("client_name")},
        "info"
    )
    
    # Step 2: Extract symbols from holdings
    symbols = []
    for holding in portfolio_data.get("holdings", []):
        if holding.get("symbol"):
            symbols.append(holding["symbol"])
    
    if not symbols:
        log_operation(
            "no_symbols",
            {"portfolio_id": portfolio_id},
            "warning"
        )
        result["error"] = "No valid symbols found in holdings"
        return result
    
    # Step 3: Fetch current stock prices
    try:
        current_prices = get_stock_prices(symbols)
    except ValueError as e:
        log_operation(
            "price_fetch_error",
            {"portfolio_id": portfolio_id, "error": str(e)},
            "error"
        )
        result["error"] = f"Failed to fetch prices: {str(e)}"
        return result
    
    # Filter out None prices (unknown symbols)
    valid_prices = {sym: price for sym, price in current_prices.items() if price is not None}
    missing_prices = set(symbols) - set(valid_prices.keys())
    
    if missing_prices:
        log_operation(
            "missing_prices",
            {"portfolio_id": portfolio_id, "missing_symbols": list(missing_prices)},
            "warning"
        )
    
    log_operation(
        "prices_fetched",
        {"portfolio_id": portfolio_id, "symbols_count": len(valid_prices)},
        "info"
    )
    
    # Step 4: Calculate portfolio value
    try:
        value_data = calculate_portfolio_value(
            portfolio_data.get("holdings", []),
            valid_prices
        )
    except ValueError as e:
        log_operation(
            "value_calculation_error",
            {"portfolio_id": portfolio_id, "error": str(e)},
            "error"
        )
        result["error"] = f"Failed to calculate value: {str(e)}"
        return result
    
    total_value = value_data.get("total_value", 0)
    
    log_operation(
        "value_calculated",
        {"portfolio_id": portfolio_id, "total_value": total_value},
        "info"
    )
    
    # Step 5: Calculate volatility score
    try:
        volatility_score = calculate_volatility_score(symbols, days=30)
    except ValueError as e:
        log_operation(
            "volatility_calculation_error",
            {"portfolio_id": portfolio_id, "error": str(e)},
            "error"
        )
        result["error"] = f"Failed to calculate volatility: {str(e)}"
        return result
    
    log_operation(
        "volatility_calculated",
        {"portfolio_id": portfolio_id, "volatility_score": volatility_score},
        "info"
    )
    
    # Step 6: Check risk thresholds
    try:
        risk_check = check_risk_threshold(
            total_value,
            volatility_score,
            RISK_CONFIG
        )
    except ValueError as e:
        log_operation(
            "risk_check_error",
            {"portfolio_id": portfolio_id, "error": str(e)},
            "error"
        )
        result["error"] = f"Failed to check risk: {str(e)}"
        return result
    
    is_high_risk = risk_check.get("is_high_risk", False)
    risk_level = risk_check.get("risk_level", "UNKNOWN")
    exceeded_thresholds = risk_check.get("exceeded_thresholds", [])
    
    # Log risk assessment
    log_operation(
        "risk_check",
        {
            "portfolio_id": portfolio_id,
            "risk_level": risk_level,
            "is_high_risk": is_high_risk,
            "exceeded_thresholds": exceeded_thresholds
        },
        "warning" if is_high_risk else "info"
    )
    
    # Update result
    result["success"] = True
    result["is_high_risk"] = is_high_risk
    result["client_name"] = portfolio_data.get("client_name")
    result["manager_email"] = portfolio_data.get("manager_email")
    result["total_value"] = total_value
    result["volatility_score"] = volatility_score
    result["risk_level"] = risk_level
    result["exceeded_thresholds"] = exceeded_thresholds
    result["positions"] = value_data.get("positions", [])
    
    # Step 7: Generate report and send notification for high-risk portfolios
    if is_high_risk:
        # Assemble portfolio data for report
        report_data = {
            "portfolio_id": portfolio_id,
            "client_name": portfolio_data.get("client_name"),
            "total_value": total_value,
            "volatility_score": volatility_score,
            "risk_level": risk_level,
            "exceeded_thresholds": exceeded_thresholds,
            "positions": value_data.get("positions", [])
        }
        
        # Generate report
        try:
            report = generate_report(report_data, report_format="markdown")
        except ValueError as e:
            log_operation(
                "report_generation_error",
                {"portfolio_id": portfolio_id, "error": str(e)},
                "error"
            )
            result["error"] = f"Failed to generate report: {str(e)}"
            return result
        
        log_operation(
            "report_generated",
            {"portfolio_id": portfolio_id},
            "info"
        )
        
        # Send notification
        manager_email = portfolio_data.get("manager_email")
        subject = f"High Risk Alert: Portfolio {portfolio_id}"
        
        try:
            notification_result = send_notification(
                recipient=manager_email,
                subject=subject,
                message=report,
                priority="high"
            )
            
            if notification_result.get("sent"):
                log_operation(
                    "notification_sent",
                    {
                        "portfolio_id": portfolio_id,
                        "recipient": manager_email,
                        "message_id": notification_result.get("message_id")
                    },
                    "info"
                )
                result["notification_sent"] = True
                result["message_id"] = notification_result.get("message_id")
            else:
                log_operation(
                    "notification_failed",
                    {"portfolio_id": portfolio_id, "recipient": manager_email},
                    "error"
                )
                result["notification_sent"] = False
                
        except ValueError as e:
            log_operation(
                "notification_error",
                {"portfolio_id": portfolio_id, "error": str(e)},
                "error"
            )
            result["notification_sent"] = False
            result["error"] = f"Failed to send notification: {str(e)}"
    
    log_operation(
        "portfolio_analysis_completed",
        {"portfolio_id": portfolio_id},
        "info"
    )
    
    return result


def analyze_portfolios():
    """
    Main orchestration function to analyze all portfolios.
    
    Processes multiple portfolios sequentially, calculates risk metrics,
    identifies high-risk portfolios, generates reports, and sends notifications.
    """
    print("=" * 60)
    print("PORTFOLIO RISK ANALYSIS AGENT")
    print("=" * 60)
    
    # Log start of analysis
    log_operation(
        "analysis_batch_started",
        {"portfolios": PORTFOLIO_IDS},
        "info"
    )
    
    results = []
    high_risk_count = 0
    success_count = 0
    error_count = 0
    
    # Process each portfolio
    for portfolio_id in PORTFOLIO_IDS:
        print(f"\n{'=' * 40}")
        print(f"Analyzing Portfolio: {portfolio_id}")
        print(f"{'=' * 40}")
        
        try:
            result = analyze_portfolio(portfolio_id)
            results.append(result)
            
            if result["success"]:
                success_count += 1
                if result["is_high_risk"]:
                    high_risk_count += 1
                    print(f"\n⚠️  HIGH RISK ALERT: {portfolio_id}")
                    print(f"   Client: {result.get('client_name', 'N/A')}")
                    print(f"   Risk Level: {result.get('risk_level', 'N/A')}")
                    print(f"   Exceeded: {result.get('exceeded_thresholds', [])}")
                    print(f"   Notification: {'Sent' if result.get('notification_sent') else 'Failed'}")
                else:
                    print(f"\n✅ Portfolio {portfolio_id} - Risk Level: {result.get('risk_level', 'N/A')}")
            else:
                error_count += 1
                print(f"\n❌ Error analyzing {portfolio_id}: {result.get('error', 'Unknown error')}")
                
        except Exception as e:
            # Catch any unexpected errors
            error_count += 1
            log_operation(
                "unexpected_error",
                {"portfolio_id": portfolio_id, "error": str(e)},
                "error"
            )
            print(f"\n❌ Unexpected error for {portfolio_id}: {str(e)}")
            results.append({
                "portfolio_id": portfolio_id,
                "success": False,
                "error": str(e)
            })
    
    # Log completion of analysis
    log_operation(
        "analysis_batch_completed",
        {
            "total_portfolios": len(PORTFOLIO_IDS),
            "success_count": success_count,
            "high_risk_count": high_risk_count,
            "error_count": error_count
        },
        "info"
    )
    
    # Print summary
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)
    print(f"Total Portfolios Processed: {len(PORTFOLIO_IDS)}")
    print(f"Successful: {success_count}")
    print(f"High Risk Identified: {high_risk_count}")
    print(f"Errors: {error_count}")
    print("=" * 60)
    
    return results


if __name__ == "__main__":
    # Run the portfolio analysis
    results = analyze_portfolios()
```

---

## Section 3: Design Justification

### Tool Orchestration Sequence

I chose to process portfolios **sequentially** rather than in parallel for several reasons:

1. **Data Dependencies**: Each portfolio analysis has internal sequential dependencies (holdings → prices → value → volatility → risk check). Parallelizing across portfolios would require more complex concurrency handling without significant performance gains since we're I/O-bound on API calls.

2. **Error Isolation**: Sequential processing ensures that if one portfolio fails (invalid ID, missing data), we can gracefully continue with the next without complex error recovery mechanisms.

3. **API Rate Limiting**: In production, sequential processing reduces the risk of hitting API rate limits from the backend systems.

4. **Audit Trail Clarity**: Logging operations in sequence provides a clear, chronological audit trail that's easier to trace for compliance purposes.

### Data Flow Strategy

The data flow follows a **pipeline pattern** where each step produces outputs consumed by subsequent steps:

```
Portfolio Holdings → Symbols → Stock Prices → Portfolio Value
                                   ↓
                            Volatility Score
                                   ↓
                             Risk Threshold Check
                                   ↓
                        (Conditional) → Report → Notification
```

**Key Design Decisions:**

1. **Symbol Extraction Early**: We extract symbols from holdings immediately after fetching to enable parallel fetching of prices and volatility calculation (though we process sequentially for simplicity).

2. **Price Filtering**: We filter out `None` prices (unknown symbols) but log which symbols are missing. This prevents calculation errors while maintaining transparency.

3. **Data Assembly for Reports**: We assemble the complete `report_data` dictionary before calling `generate_report()` to ensure all required fields are available and validated.

### Error Handling Strategy

I implemented a **defensive error handling** approach with multiple layers:

1. **Per-Portfolio Try/Except**: Each portfolio is wrapped in its own try/except block, ensuring one portfolio's failure doesn't crash the entire batch.

2. **Tool-Level Error Handling**: Each tool call is wrapped individually to:
   - Log the specific error with context
   - Return early with an error result
   - Allow the next step to proceed if possible

3. **Validation Before Tool Calls**: We validate data (e.g., checking for empty symbols list) before calling tools to provide meaningful error messages.

4. **Graceful Degradation**: 
   - If price fetching fails, we can't calculate value → skip portfolio
   - If value calculation fails, we can't check risk → skip portfolio
   - If notification fails for a high-risk portfolio, we log the error but mark the portfolio as analyzed

5. **Logging at Every Step**: Every major operation is logged, ensuring we have a complete audit trail even when errors occur.

### Trade-offs Considered

1. **Sequential vs Parallel**: Chose sequential for simplicity and error isolation. In a real production system with many portfolios, we'd consider async processing with proper concurrency controls.

2. **Fail-Fast vs Continue**: We continue processing remaining portfolios when one fails rather than failing completely. This design choice prioritizes overall system availability over atomicity.

3. **Notification Timing**: We send notifications immediately after identifying a high-risk portfolio rather than batching them. This ensures portfolio managers receive alerts promptly, which is critical for risk management.

4. **Report Format**: We chose Markdown as the default format because:
   - It's human-readable for quick review
   - It can be easily converted to HTML or PDF for formal reports
   - It's the specified default in the tool definition

### Completeness Check

The implementation satisfies all requirements:
- ✅ Analyzes 3 portfolios (PORT-001, PORT-002, PORT-003)
- ✅ Calculates all risk metrics (value, volatility, threshold checks)
- ✅ Uses specified risk configuration
- ✅ Identifies high-risk portfolios
- ✅ Generates markdown reports for high-risk portfolios
- ✅ Sends high-priority notifications to managers
- ✅ Maintains comprehensive audit logs
- ✅ Handles errors gracefully with try/except blocks