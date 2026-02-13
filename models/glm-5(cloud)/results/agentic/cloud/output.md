# Portfolio Risk Analysis Agent Solution

## Section 1: Execution Plan

### Execution Plan

#### 1. **Initialize Configuration**
- **Tools:** `log_operation()`
- **Actions:**
  - Define risk thresholds configuration
  - Define portfolio list to analyze ["PORT-001", "PORT-002", "PORT-003"]
  - Log system initialization
- **Output:** Configuration ready for processing

#### 2. **For Each Portfolio (Sequential Processing):**

   **a. Log Portfolio Analysis Start**
   - **Tool:** `log_operation()`
   - **Input:** portfolio_id, operation="portfolio_analysis_start"
   - **Purpose:** Audit trail for compliance

   **b. Fetch Portfolio Holdings**
   - **Tool:** `get_portfolio_holdings()`
   - **Input:** portfolio_id
   - **Output:** holdings data including client_name, manager_email, holdings list
   - **Error Handling:** Catch ValueError for invalid portfolio_id, log error, skip to next portfolio
   - **Data Dependency:** Required for steps c, d, e, f

   **c. Extract Stock Symbols**
   - **Tool:** None (internal data transformation)
   - **Input:** holdings list from step b
   - **Output:** list of unique stock symbols
   - **Data Dependency:** Feeds into steps d and f

   **d. Fetch Current Stock Prices**
   - **Tool:** `get_stock_prices()`
   - **Input:** symbols list from step c
   - **Output:** dictionary mapping symbols to current prices
   - **Error Handling:** Handle None prices gracefully (calculate_portfolio_value handles this)
   - **Data Dependency:** Required for step e

   **e. Calculate Portfolio Value**
   - **Tool:** `calculate_portfolio_value()`
   - **Input:** holdings (from step b), current_prices (from step d)
   - **Output:** total_value, positions with gain/loss data
   - **Error Handling:** Catch ValueError for empty inputs
   - **Data Dependency:** Required for step g

   **f. Calculate Volatility Score**
   - **Tool:** `calculate_volatility_score()`
   - **Input:** symbols list (from step c), days=30
   - **Output:** volatility score (0-100 scale)
   - **Error Handling:** Catch ValueError for invalid inputs
   - **Data Dependency:** Required for step g

   **g. Check Risk Threshold**
   - **Tool:** `check_risk_threshold()`
   - **Input:** portfolio_value (from step e), volatility_score (from step f), risk_config
   - **Output:** is_high_risk, exceeded_thresholds, risk_level
   - **Data Dependency:** Determines if steps h, i, j are executed
   - **Logging:** Log risk check result with appropriate level

   **h. Generate Report (If High Risk)**
   - **Tool:** `generate_report()`
   - **Input:** portfolio_data (aggregated from steps b, e, f, g), report_format="markdown"
   - **Output:** formatted report string
   - **Condition:** Only if is_high_risk == True
   - **Error Handling:** Catch ValueError for missing required fields

   **i. Send Notification (If High Risk)**
   - **Tool:** `send_notification()`
   - **Input:** recipient (manager_email from step b), subject, message (report from step h), priority="high"
   - **Output:** sent status, message_id, timestamp
   - **Condition:** Only if is_high_risk == True
   - **Error Handling:** Catch ValueError for invalid email, log failure

   **j. Log Completion for Portfolio**
   - **Tool:** `log_operation()`
   - **Input:** operation, details (portfolio_id, risk_level, notification_sent)
   - **Level:** "info" for normal, "warning" for high risk

#### 3. **Log System Completion**
- **Tool:** `log_operation()`
- **Actions:** Log summary of all processed portfolios, count of high-risk portfolios

#### 4. **Error Handling Strategy**

| Error Type | Handling Approach |
|------------|-------------------|
| Invalid portfolio_id | Log error with "error" level, continue to next portfolio |
| Empty holdings | Log warning, skip portfolio |
| Missing stock prices | calculate_portfolio_value handles None prices by skipping positions |
| Failed notification | Log error, mark notification as failed, continue processing |
| Invalid risk config | Caught at threshold check, log error, skip portfolio |
| General exceptions | Catch-all handler, log full error details, continue |

**Key Principles:**
- Each portfolio processed in isolated try/except block
- Errors logged immediately with relevant context
- Processing continues for remaining portfolios
- Partial results preserved when possible

---

## Section 2: Implementation

```python
"""
Portfolio Risk Analysis Agent

This script orchestrates multiple tools to analyze investment portfolios,
calculate risk metrics, identify high-risk portfolios, generate reports,
and send notifications to portfolio managers.
"""

from typing import Any

# Import tools from the reference module
# In production, these would be actual API calls to backend systems
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


def analyze_portfolios() -> dict:
    """
    Main orchestration function for portfolio risk analysis.
    
    Processes multiple portfolios, calculates risk metrics, identifies
    high-risk portfolios, generates reports, and sends notifications.
    
    Returns:
        dict: Summary of analysis results including processed portfolios
              and high-risk count
    """
    # Initialize configuration
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    # Track results
    results = {
        "processed": [],
        "high_risk": [],
        "failed": [],
        "notifications_sent": 0
    }
    
    # Log system initialization
    log_operation(
        operation="system_initialization",
        details={
            "portfolios_to_analyze": portfolio_ids,
            "risk_config": risk_config
        },
        level="info"
    )
    
    print("=" * 60)
    print("PORTFOLIO RISK ANALYSIS SYSTEM")
    print("=" * 60)
    print(f"Analyzing {len(portfolio_ids)} portfolios...")
    print(f"Risk thresholds - Max Volatility: {risk_config['max_volatility']}, "
          f"Min Value: ${risk_config['min_value']:,}, Max Value: ${risk_config['max_value']:,}")
    print()
    
    # Process each portfolio
    for portfolio_id in portfolio_ids:
        portfolio_result = process_single_portfolio(
            portfolio_id=portfolio_id,
            risk_config=risk_config
        )
        
        if portfolio_result["status"] == "success":
            results["processed"].append(portfolio_id)
            if portfolio_result.get("is_high_risk"):
                results["high_risk"].append(portfolio_id)
            if portfolio_result.get("notification_sent"):
                results["notifications_sent"] += 1
        else:
            results["failed"].append(portfolio_id)
    
    # Log system completion
    log_operation(
        operation="system_completion",
        details={
            "total_portfolios": len(portfolio_ids),
            "processed": len(results["processed"]),
            "high_risk_count": len(results["high_risk"]),
            "failed": len(results["failed"]),
            "notifications_sent": results["notifications_sent"]
        },
        level="info"
    )
    
    # Print summary
    print()
    print("=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"Processed: {len(results['processed'])} portfolios")
    print(f"High Risk: {len(results['high_risk'])} portfolios")
    print(f"Failed: {len(results['failed'])} portfolios")
    print(f"Notifications Sent: {results['notifications_sent']}")
    
    if results["high_risk"]:
        print(f"\nHigh-Risk Portfolios: {', '.join(results['high_risk'])}")
    
    return results


def process_single_portfolio(portfolio_id: str, risk_config: dict) -> dict:
    """
    Process a single portfolio through the complete analysis pipeline.
    
    Args:
        portfolio_id: Portfolio identifier to analyze
        risk_config: Risk threshold configuration
        
    Returns:
        dict: Result status and analysis details
    """
    result = {
        "status": "success",
        "portfolio_id": portfolio_id,
        "is_high_risk": False,
        "notification_sent": False
    }
    
    try:
        # Step 1: Log analysis start
        log_operation(
            operation="portfolio_analysis_start",
            details={"portfolio_id": portfolio_id},
            level="info"
        )
        print(f"\n--- Analyzing {portfolio_id} ---")
        
        # Step 2: Fetch portfolio holdings
        holdings_data = get_portfolio_holdings(portfolio_id)
        
        client_name = holdings_data.get("client_name", "Unknown")
        manager_email = holdings_data.get("manager_email", "")
        holdings = holdings_data.get("holdings", [])
        
        print(f"  Client: {client_name}")
        print(f"  Holdings count: {len(holdings)}")
        
        if not holdings:
            raise ValueError(f"No holdings found for portfolio {portfolio_id}")
        
        # Step 3: Extract stock symbols
        symbols = list(set(holding["symbol"] for holding in holdings))
        print(f"  Symbols: {', '.join(symbols)}")
        
        # Step 4: Fetch current stock prices
        current_prices = get_stock_prices(symbols)
        
        # Check for missing prices
        missing_prices = [s for s in symbols if current_prices.get(s) is None]
        if missing_prices:
            log_operation(
                operation="price_data_warning",
                details={
                    "portfolio_id": portfolio_id,
                    "missing_symbols": missing_prices
                },
                level="warning"
            )
            print(f"  WARNING: Missing prices for: {', '.join(missing_prices)}")
        
        # Step 5: Calculate portfolio value
        value_data = calculate_portfolio_value(holdings, current_prices)
        total_value = value_data.get("total_value", 0)
        positions = value_data.get("positions", [])
        
        print(f"  Total Value: ${total_value:,.2f}")
        
        # Step 6: Calculate volatility score (30-day period)
        volatility_score = calculate_volatility_score(symbols, days=30)
        print(f"  Volatility Score: {volatility_score:.2f}")
        
        # Step 7: Check risk threshold
        risk_check = check_risk_threshold(total_value, volatility_score, risk_config)
        is_high_risk = risk_check.get("is_high_risk", False)
        risk_level = risk_check.get("risk_level", "UNKNOWN")
        exceeded_thresholds = risk_check.get("exceeded_thresholds", [])
        
        result["is_high_risk"] = is_high_risk
        result["risk_level"] = risk_level
        result["total_value"] = total_value
        result["volatility_score"] = volatility_score
        
        print(f"  Risk Level: {risk_level}")
        
        if exceeded_thresholds:
            print(f"  Exceeded Thresholds: {', '.join(exceeded_thresholds)}")
        
        # Log risk check result
        log_level = "warning" if is_high_risk else "info"
        log_operation(
            operation="risk_check",
            details={
                "portfolio_id": portfolio_id,
                "total_value": total_value,
                "volatility_score": volatility_score,
                "risk_level": risk_level,
                "exceeded_thresholds": exceeded_thresholds,
                "is_high_risk": is_high_risk
            },
            level=log_level
        )
        
        # Steps 8-10: Handle high-risk portfolios
        if is_high_risk:
            handle_high_risk_portfolio(
                portfolio_id=portfolio_id,
                client_name=client_name,
                manager_email=manager_email,
                total_value=total_value,
                volatility_score=volatility_score,
                risk_level=risk_level,
                exceeded_thresholds=exceeded_thresholds,
                positions=positions
            )
            result["notification_sent"] = True
        
        # Log portfolio analysis completion
        log_operation(
            operation="portfolio_analysis_complete",
            details={
                "portfolio_id": portfolio_id,
                "risk_level": risk_level,
                "notification_sent": result["notification_sent"]
            },
            level="info"
        )
        
        print(f"  Status: Analysis complete - {risk_level} risk")
        
    except ValueError as ve:
        # Handle expected errors (invalid portfolio, empty data, etc.)
        error_msg = str(ve)
        result["status"] = "failed"
        result["error"] = error_msg
        
        log_operation(
            operation="portfolio_analysis_error",
            details={
                "portfolio_id": portfolio_id,
                "error_type": "ValueError",
                "error_message": error_msg
            },
            level="error"
        )
        print(f"  ERROR: {error_msg}")
        
    except Exception as e:
        # Handle unexpected errors
        error_msg = str(e)
        result["status"] = "failed"
        result["error"] = error_msg
        
        log_operation(
            operation="portfolio_analysis_error",
            details={
                "portfolio_id": portfolio_id,
                "error_type": type(e).__name__,
                "error_message": error_msg
            },
            level="error"
        )
        print(f"  UNEXPECTED ERROR: {error_msg}")
    
    return result


def handle_high_risk_portfolio(
    portfolio_id: str,
    client_name: str,
    manager_email: str,
    total_value: float,
    volatility_score: float,
    risk_level: str,
    exceeded_thresholds: list,
    positions: list
) -> bool:
    """
    Generate report and send notification for a high-risk portfolio.
    
    Args:
        portfolio_id: Portfolio identifier
        client_name: Name of the client
        manager_email: Email of portfolio manager
        total_value: Total portfolio value
        volatility_score: Calculated volatility score
        risk_level: Risk level classification
        exceeded_thresholds: List of exceeded threshold names
        positions: List of position details
        
    Returns:
        bool: True if notification sent successfully
    """
    notification_sent = False
    
    try:
        # Prepare portfolio data for report generation
        portfolio_data = {
            "portfolio_id": portfolio_id,
            "client_name": client_name,
            "total_value": total_value,
            "volatility_score": volatility_score,
            "risk_level": risk_level,
            "exceeded_thresholds": exceeded_thresholds,
            "positions": positions
        }
        
        # Generate markdown report
        report = generate_report(portfolio_data, report_format="markdown")
        
        log_operation(
            operation="report_generated",
            details={
                "portfolio_id": portfolio_id,
                "report_format": "markdown",
                "report_length": len(report)
            },
            level="info"
        )
        
        print(f"  Report generated for {portfolio_id}")
        
        # Send notification to portfolio manager
        subject = f"HIGH RISK ALERT: Portfolio {portfolio_id} - {risk_level} Risk"
        
        notification_result = send_notification(
            recipient=manager_email,
            subject=subject,
            message=report,
            priority="high"
        )
        
        if notification_result.get("sent", False):
            notification_sent = True
            log_operation(
                operation="notification_sent",
                details={
                    "portfolio_id": portfolio_id,
                    "recipient": manager_email,
                    "message_id": notification_result.get("message_id"),
                    "priority": "high"
                },
                level="info"
            )
            print(f"  Notification sent to {manager_email}")
        else:
            log_operation(
                operation="notification_failed",
                details={
                    "portfolio_id": portfolio_id,
                    "recipient": manager_email,
                    "reason": "send_notification returned sent=False"
                },
                level="error"
            )
            print(f"  WARNING: Notification failed to send")
            
    except ValueError as ve:
        log_operation(
            operation="notification_error",
            details={
                "portfolio_id": portfolio_id,
                "error_type": "ValueError",
                "error_message": str(ve)
            },
            level="error"
        )
        print(f"  ERROR sending notification: {ve}")
        
    except Exception as e:
        log_operation(
            operation="notification_error",
            details={
                "portfolio_id": portfolio_id,
                "error_type": type(e).__name__,
                "error_message": str(e)
            },
            level="error"
        )
        print(f"  UNEXPECTED ERROR sending notification: {e}")
    
    return notification_sent


if __name__ == "__main__":
    analyze_portfolios()
```

---

## Section 3: Design Justification

### Design Justification

#### Tool Orchestration Sequence

I chose to process portfolios **sequentially** rather than in parallel for several reasons:

1. **Error Isolation**: Sequential processing ensures that a failure in one portfolio analysis doesn't affect others. Each portfolio is wrapped in its own try/except block, allowing the system to continue processing remaining portfolios.

2. **Simplified State Management**: Sequential execution avoids race conditions and simplifies logging, making audit trails clearer and easier to trace.

3. **Rate Limiting Considerations**: In production environments, API calls often have rate limits. Sequential processing naturally throttles requests, reducing the risk of hitting rate limits.

4. **Clear Data Flow**: Sequential processing makes the dependency chain explicit - holdings → symbols → prices → value and volatility → risk check → report/notification.

#### Data Flow Strategy

The data flow was designed with clear dependencies:

```
get_portfolio_holdings() 
    │
    ├──→ Extract symbols (internal transformation)
    │        │
    │        ├──→ get_stock_prices()
    │        │        │
    │        │        └──→ calculate_portfolio_value()
    │        │
    │        └──→ calculate_volatility_score()
    │
    └──→ (combined with above results) → check_risk_threshold()
                                              │
                                              └──→ [if high_risk] generate_report()
                                                          │
                                                          └──→ send_notification()
```

**Key Design Decisions:**

1. **Symbol Extraction**: Symbols are extracted once and reused for both price fetching and volatility calculation, avoiding redundant data retrieval.

2. **Aggregated Portfolio Data**: The `portfolio_data` dictionary passed to `generate_report()` aggregates data from multiple sources (holdings, value calculation, volatility, risk check), ensuring all required fields are available.

3. **Progressive Logging**: Each major operation is logged immediately after completion, creating a complete audit trail even if subsequent steps fail.

#### Error Handling Strategy Rationale

| Error Type | Strategy | Rationale |
|------------|----------|-----------|
| Invalid portfolio ID | Skip portfolio, log error, continue | Invalid IDs are data errors that can't be recovered; logging provides visibility |
| Missing stock prices | Log warning, continue with available prices | `calculate_portfolio_value` handles None prices by skipping positions, allowing partial analysis |
| Empty holdings | Raise ValueError, skip portfolio | Can't calculate metrics without holdings; logged for investigation |
| Notification failure | Log error, mark as failed, continue | Notification failures shouldn't block other portfolios; can be retried separately |
| General exceptions | Catch-all handler, log details, continue | Prevents system crash; ensures all portfolios get a chance to be processed |

**Why this approach:**

1. **Graceful Degradation**: The system continues processing even when individual portfolios fail, maximizing throughput.

2. **Comprehensive Logging**: Every error is logged with context (portfolio_id, error type, message), enabling post-hoc debugging and audit compliance.

3. **Partial Results Preservation**: When possible (e.g., missing prices), the system continues with available data rather than failing completely.

#### Trade-offs Considered

1. **Sequential vs. Parallel Processing**
   - **Chosen**: Sequential
   - **Trade-off**: Slower execution time vs. simpler error handling and clearer audit trails
   - **Justification**: In a risk monitoring system, reliability and auditability are more critical than speed

2. **Early vs. Late Validation**
   - **Chosen**: Progressive validation (validate at each step)
   - **Trade-off**: More validation code vs. catching errors earlier
   - **Justification**: Each tool has its own validation; catching errors at the source provides clearer error messages

3. **Single vs. Multiple Report Formats**
   - **Chosen**: Markdown only for notifications
   - **Trade-off**: Less flexibility vs. simpler implementation
   - **Justification**: Markdown is well-suited for email and can be easily converted to other formats if needed

4. **Notification on All vs. High-Risk Only**
   - **Chosen**: High-risk only
   - **Trade-off**: Less notification volume vs. less visibility on normal portfolios
   - **Justification**: Managers don't need alerts for healthy portfolios; this reduces notification fatigue

5. **In-Memory vs. Persistent Results**
   - **Chosen**: In-memory with logging for persistence
   - **Trade-off**: Results lost on crash vs. simpler implementation
   - **Justification**: The audit log provides persistent record; results can be reconstructed if needed

#### Compliance and Audit Considerations

The design prioritizes audit compliance:

1. **Operation Logging**: Every significant operation is logged with operation name, details, and appropriate level.

2. **Log Levels Used Appropriately**:
   - `info`: Normal operations (initialization, completion, successful checks)
   - `warning`: High-risk detections, missing data warnings
   - `error`: Failures, exceptions, invalid data

3. **Complete Audit Trail**: The combination of operation logs and printed output provides both machine-readable and human-readable records of all activities.