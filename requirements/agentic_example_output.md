# Agentic Task Example Output

This file provides a reference implementation showing the expected format and quality for the agentic task. Use this to calibrate manual evaluation.

---

## Execution Plan

### Overview
Process three portfolios sequentially, calculate risk metrics for each, identify high-risk portfolios, generate reports, and send notifications to portfolio managers.

### Detailed Steps

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds: `{"max_volatility": 35.0, "min_value": 50000, "max_value": 2000000}`
   - Define portfolio IDs to process: `["PORT-001", "PORT-002", "PORT-003"]`

2. **For Each Portfolio (Loop through PORT-001, PORT-002, PORT-003):**

   **a. Fetch Portfolio Holdings**
   - Tool: `get_portfolio_holdings(portfolio_id)`
   - Input: Portfolio ID (e.g., "PORT-001")
   - Output: Holdings data containing client_name, manager_email, and list of holdings
   - Dependencies: None
   - Error handling: Wrap in try/except, log error and continue to next portfolio on failure

   **b. Extract Stock Symbols**
   - Tool: None (data transformation)
   - Input: Holdings list from step 2a
   - Output: List of unique stock symbols
   - Dependencies: Requires holdings from step 2a

   **c. Fetch Current Stock Prices**
   - Tool: `get_stock_prices(symbols)`
   - Input: Symbols list from step 2b
   - Output: Dictionary mapping symbols to current prices
   - Dependencies: Requires symbols from step 2b

   **d. Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value(holdings, current_prices)`
   - Input: Holdings from step 2a, prices from step 2c
   - Output: Total value and detailed position information
   - Dependencies: Requires both holdings and prices

   **e. Calculate Volatility Score**
   - Tool: `calculate_volatility_score(symbols, days=30)`
   - Input: Symbols from step 2b
   - Output: Volatility score (0-100 scale)
   - Dependencies: Requires symbols from step 2b

   **f. Check Risk Thresholds**
   - Tool: `check_risk_threshold(portfolio_value, volatility_score, risk_config)`
   - Input: Total value from step 2d, volatility from step 2e, risk config from step 1
   - Output: Risk assessment with is_high_risk flag and exceeded thresholds
   - Dependencies: Requires value and volatility calculations

   **g. Generate Report (if high risk)**
   - Tool: `generate_report(portfolio_data, report_format="markdown")`
   - Input: Consolidated portfolio data from all previous steps
   - Output: Formatted markdown report string
   - Dependencies: Only execute if is_high_risk == True
   - Portfolio data includes: portfolio_id, client_name, total_value, volatility_score, risk_level, exceeded_thresholds, positions

   **h. Send Notification (if high risk)**
   - Tool: `send_notification(recipient, subject, message, priority="high")`
   - Input: Manager email from step 2a, report from step 2g
   - Output: Notification confirmation
   - Dependencies: Only execute if is_high_risk == True

   **i. Log Operations**
   - Tool: `log_operation(operation, details, level)`
   - Called at key points:
     - Portfolio analysis start (info level)
     - Risk check result (warning level if high risk, info otherwise)
     - Report generation (info level)
     - Notification sent (warning level)
     - Portfolio analysis completion (info level)
     - Any errors encountered (error level)

3. **Error Handling Strategy**
   - Wrap each portfolio's processing in a try/except block
   - If one portfolio fails, log the error and continue to the next
   - Catch specific exceptions (ValueError for invalid portfolio IDs)
   - Log all failures at error level with details
   - Graceful degradation: system should process all accessible portfolios even if some fail

### Data Flow Summary

```
Holdings → Symbols → Prices
                      ↓
Holdings + Prices → Portfolio Value
Symbols → Volatility Score
                      ↓
Value + Volatility → Risk Check
                      ↓
All Data → Report → Notification
```

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
    """Main orchestration function for portfolio risk analysis."""

    # Step 1: Initialize configuration
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }

    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]

    log_operation(
        "portfolio_analysis_batch_start",
        {"portfolio_count": len(portfolio_ids), "risk_config": risk_config},
        level="info"
    )

    # Step 2: Process each portfolio
    for portfolio_id in portfolio_ids:
        try:
            log_operation(
                "portfolio_analysis_start",
                {"portfolio_id": portfolio_id},
                level="info"
            )

            # Step 2a: Fetch portfolio holdings
            portfolio = get_portfolio_holdings(portfolio_id)
            holdings = portfolio["holdings"]
            client_name = portfolio["client_name"]
            manager_email = portfolio["manager_email"]

            # Step 2b: Extract stock symbols
            symbols = [holding["symbol"] for holding in holdings]

            # Step 2c: Fetch current stock prices
            current_prices = get_stock_prices(symbols)

            # Step 2d: Calculate portfolio value
            value_data = calculate_portfolio_value(holdings, current_prices)
            total_value = value_data["total_value"]
            positions = value_data["positions"]

            # Step 2e: Calculate volatility score
            volatility_score = calculate_volatility_score(symbols, days=30)

            # Step 2f: Check risk thresholds
            risk_check = check_risk_threshold(total_value, volatility_score, risk_config)
            is_high_risk = risk_check["is_high_risk"]
            risk_level = risk_check["risk_level"]
            exceeded_thresholds = risk_check["exceeded_thresholds"]

            # Log risk check result
            log_operation(
                "risk_check_completed",
                {
                    "portfolio_id": portfolio_id,
                    "risk_level": risk_level,
                    "is_high_risk": is_high_risk,
                    "exceeded_thresholds": exceeded_thresholds
                },
                level="warning" if is_high_risk else "info"
            )

            # Step 2g & 2h: Generate report and send notification if high risk
            if is_high_risk:
                # Consolidate portfolio data for report
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
                    "report_generated",
                    {"portfolio_id": portfolio_id, "report_length": len(report)},
                    level="info"
                )

                # Send notification to portfolio manager
                subject = f"High Risk Alert: Portfolio {portfolio_id}"
                notification_result = send_notification(
                    recipient=manager_email,
                    subject=subject,
                    message=report,
                    priority="high"
                )

                log_operation(
                    "notification_sent",
                    {
                        "portfolio_id": portfolio_id,
                        "recipient": manager_email,
                        "message_id": notification_result["message_id"]
                    },
                    level="warning"
                )

            # Log completion
            log_operation(
                "portfolio_analysis_completed",
                {"portfolio_id": portfolio_id, "risk_level": risk_level},
                level="info"
            )

        except ValueError as e:
            # Handle specific errors (e.g., invalid portfolio ID)
            log_operation(
                "portfolio_analysis_failed",
                {"portfolio_id": portfolio_id, "error": str(e)},
                level="error"
            )
            print(f"Error processing {portfolio_id}: {e}")
            continue  # Continue to next portfolio

        except Exception as e:
            # Handle unexpected errors
            log_operation(
                "portfolio_analysis_error",
                {"portfolio_id": portfolio_id, "error_type": type(e).__name__, "error": str(e)},
                level="error"
            )
            print(f"Unexpected error processing {portfolio_id}: {e}")
            continue  # Continue to next portfolio

    log_operation(
        "portfolio_analysis_batch_completed",
        {"total_portfolios": len(portfolio_ids)},
        level="info"
    )


if __name__ == "__main__":
    analyze_portfolios()
```

---

## Design Justification

### Tool Orchestration Sequence

I chose to process portfolios **sequentially** rather than in parallel for several reasons:

1. **Simplicity and Reliability**: Sequential processing is straightforward to implement and reason about. Error handling is simpler since we process one portfolio at a time.

2. **Resource Management**: The mock tools simulate API calls that might have rate limits in production. Sequential processing naturally throttles requests.

3. **Audit Trail Clarity**: Log entries appear in chronological order, making it easier to trace the analysis flow for each portfolio.

While parallel processing could improve performance, the added complexity (thread safety, concurrent logging, error aggregation) isn't justified for analyzing just 3 portfolios.

### Data Flow Strategy

The orchestration follows a **fan-out, then fan-in** pattern for each portfolio:

1. **Fan-out**: Holdings data feeds into three independent operations:
   - Symbol extraction → price fetching
   - Symbol extraction → volatility calculation
   - Holdings storage for value calculation

2. **Fan-in**: Results converge for risk assessment:
   - Value + Volatility → Risk check
   - All data → Report generation

This pattern minimizes redundant API calls (fetch prices once, use for both value calculation and as context for volatility) while maximizing parallelizable steps (price fetching and volatility calculation could run concurrently in an optimized implementation).

### Error Handling Rationale

I implemented **graceful degradation** at the portfolio level:

- Each portfolio is wrapped in a try/except block
- If one portfolio fails (invalid ID, missing data, API error), the system continues processing remaining portfolios
- All failures are logged at error level with full context
- The system doesn't fail-fast because partial results are valuable (processing 2 of 3 portfolios is better than 0)

I differentiated between:
- **Expected errors** (ValueError for invalid portfolio IDs): Caught specifically and logged with clear messages
- **Unexpected errors** (Exception): Caught broadly, logged with error type, and continued

### High-Risk Filtering Decision

Only high-risk portfolios trigger report generation and notifications to reduce noise:

- If every portfolio generated a report, portfolio managers would be overwhelmed
- The task explicitly asks to "identify high-risk portfolios" and send notifications for them
- Low/medium risk portfolios are still logged for audit purposes but don't trigger alerts

### Logging Strategy

I included 5+ log operations to create a comprehensive audit trail:

1. **Batch start/end**: Track when analysis runs began and completed
2. **Per-portfolio start/completion**: Track processing of each portfolio
3. **Risk checks**: Log risk level and exceeded thresholds (warning level for high risk)
4. **Report generation**: Track when reports are created
5. **Notifications**: Track when alerts are sent (warning level)
6. **Errors**: Log all failures with full context (error level)

This provides full traceability for compliance and debugging.

### Trade-offs Considered

**Sequential vs. Parallel Processing**:
- Chose sequential for simplicity
- Trade-off: ~3x slower for 3 portfolios, but easier to implement correctly
- In production with 100+ portfolios, would reconsider with async/await or threading

**Error Handling Granularity**:
- Chose portfolio-level try/except
- Trade-off: Could wrap each tool call individually for finer-grained error handling, but adds complexity
- Current approach balances robustness with code clarity

**Report Format**:
- Chose markdown as specified
- Trade-off: HTML would render better in email clients, but markdown is more readable in logs and easier to generate
- Markdown is also version-control friendly for audit purposes

### Why This Approach Works

This design demonstrates **autonomous goal decomposition** and **tool orchestration**:

1. **Clear decomposition**: 8 distinct steps per portfolio, each with a specific purpose
2. **Correct dependencies**: Data flows logically (can't calculate value before fetching prices)
3. **Defensive programming**: Errors don't cascade; system continues processing
4. **Production-ready**: Comprehensive logging, error handling, and audit trail
5. **Efficient**: Minimizes redundant API calls while maintaining clarity

The implementation would work correctly in production with real APIs by simply swapping the mock tools for real ones.
