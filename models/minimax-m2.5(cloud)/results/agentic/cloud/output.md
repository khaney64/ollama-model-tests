# Portfolio Risk Analysis Agent

## Section 1: Execution Plan

```markdown
## Execution Plan

### 1. Initialize Configuration
- **Tools**: None (local configuration)
- **Inputs**: None
- **Outputs**: Risk configuration dictionary and portfolio list
- **Description**: Set up the risk thresholds and define which portfolios to analyze

### 2. Log Analysis Start
- **Tool**: `log_operation()`
- **Inputs**: Operation name "portfolio_analysis_start", list of portfolio IDs
- **Outputs**: Audit log entry
- **Purpose**: Begin audit trail for the analysis session

### 3. For Each Portfolio (Sequential Processing):

#### 3a. Log Portfolio Analysis Start
- **Tool**: `log_operation()`
- **Inputs**: portfolio_id, status "started"
- **Outputs**: Audit log entry

#### 3b. Fetch Portfolio Holdings
- **Tool**: `get_portfolio_holdings(portfolio_id)`
- **Inputs**: portfolio_id (e.g., "PORT-001")
- **Outputs**: Holdings dictionary with client_name, manager_email, holdings list
- **Data Dependencies**: None (first step for each portfolio)
- **Error Handling**: Catch ValueError for invalid portfolio_id, log error, skip to next portfolio

#### 3c. Extract Stock Symbols
- **Tool**: None (data transformation)
- **Inputs**: holdings list from step 3b
- **Outputs**: List of stock symbols
- **Description**: Parse holdings to extract unique symbols for price lookup

#### 3d. Fetch Current Stock Prices
- **Tool**: `get_stock_prices(symbols)`
- **Inputs**: List of stock symbols from step 3c
- **Outputs**: Dictionary mapping symbols to current prices
- **Data Dependencies**: Symbols from holdings
- **Error Handling**: Skip positions with None prices, continue with available data

#### 3e. Calculate Portfolio Value
- **Tool**: `calculate_portfolio_value(holdings, current_prices)`
- **Inputs**: Holdings from step 3b, prices from step 3d
- **Outputs**: Dictionary with total_value and positions (including gain/loss)
- **Data Dependencies**: Holdings and current prices
- **Error Handling**: Skip positions with missing prices, log warning

#### 3f. Calculate Volatility Score
- **Tool**: `calculate_volatility_score(symbols, days=30)`
- **Inputs**: Symbols list, days=30
- **Outputs**: Volatility score (float 0-100)
- **Data Dependencies**: Symbols from step 3c
- **Error Handling**: Catch ValueError for empty symbols, assign default high volatility

#### 3g. Check Risk Thresholds
- **Tool**: `check_risk_threshold(portfolio_value, volatility_score, risk_config)`
- **Inputs**: Total value from step 3e, volatility from step 3f, risk config
- **Outputs**: Risk check result (is_high_risk, exceeded_thresholds, risk_level)
- **Data Dependencies**: Portfolio value and volatility score
- **Error Handling**: Catch ValueError for negative values

#### 3h. Conditional: Generate Report (if high-risk)
- **Tool**: `generate_report(portfolio_data, report_format="markdown")`
- **Inputs**: Combined portfolio data dictionary
- **Outputs**: Formatted markdown report string
- **Data Dependencies**: All previous results combined
- **Error Handling**: Catch ValueError for missing fields

#### 3i. Conditional: Send Notification (if high-risk)
- **Tool**: `send_notification(recipient, subject, message, priority="high")`
- **Inputs**: manager_email from holdings, subject, report text, priority
- **Outputs**: Notification result dictionary
- **Data Dependencies**: Report from step 3h, manager_email from step 3b
- **Error Handling**: Catch ValueError for invalid email/priority, log failure

#### 3j. Log Portfolio Analysis Completion
- **Tool**: `log_operation()`
- **Inputs**: portfolio_id, risk_level, status "completed"
- **Outputs**: Audit log entry

### 4. Log Analysis Session Completion
- **Tool**: `log_operation()`
- **Inputs**: Summary statistics (portfolios processed, high-risk count)
- **Outputs**: Audit log entry

### Error Handling Strategy
1. **Per-portfolio try/except**: Each portfolio processed in isolated try/except block
2. **Specific exception handling**: Catch ValueError, TypeError, KeyError separately
3. **Graceful degradation**: Continue processing remaining portfolios if one fails
4. **Detailed error logging**: Log error details including exception type and message
5. **Default values**: Assign safe defaults (e.g., high volatility) when calculations fail
6. **Notification failures**: Log but don't fail entire process if notification sending fails
```

## Section 2: Implementation

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


# =============================================================================
# CONFIGURATION
# =============================================================================

# Portfolio IDs to analyze
PORTFOLIO_IDS = ["PORT-001", "PORT-002", "PORT-003"]

# Risk configuration thresholds
RISK_CONFIG = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000
}

# Volatility calculation period
VOLATILITY_DAYS = 30


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def extract_symbols(holdings: list[dict]) -> list[str]:
    """Extract unique stock symbols from holdings list.
    
    Args:
        holdings: List of holding dictionaries with 'symbol' key
        
    Returns:
        List of unique stock symbols
    """
    symbols = set()
    for holding in holdings:
        if "symbol" in holding:
            symbols.add(holding["symbol"])
    return list(symbols)


def prepare_portfolio_data(
    portfolio_id: str,
    holdings_data: dict,
    value_data: dict,
    volatility_score: float,
    risk_check: dict
) -> dict:
    """Prepare comprehensive portfolio data dictionary for reporting.
    
    Args:
        portfolio_id: Portfolio identifier
        holdings_data: Raw holdings from API
        value_data: Calculated portfolio value
        volatility_score: Volatility score
        risk_check: Risk threshold check result
        
    Returns:
        Dictionary formatted for report generation
    """
    return {
        "portfolio_id": portfolio_id,
        "client_name": holdings_data.get("client_name", "Unknown"),
        "total_value": value_data.get("total_value", 0.0),
        "volatility_score": volatility_score,
        "risk_level": risk_check.get("risk_level", "UNKNOWN"),
        "exceeded_thresholds": risk_check.get("exceeded_thresholds", []),
        "positions": value_data.get("positions", [])
    }


# =============================================================================
# MAIN ANALYSIS FUNCTION
# =============================================================================

def analyze_portfolios():
    """Main orchestration function for portfolio risk analysis.
    
    This function coordinates the entire risk analysis workflow:
    1. Fetches portfolio holdings
    2. Gets current stock prices
    3. Calculates portfolio values and position metrics
    4. Computes volatility scores
    5. Checks risk thresholds
    6. Generates reports for high-risk portfolios
    7. Sends notifications to portfolio managers
    """
    
    # Initialize tracking variables
    processed_count = 0
    high_risk_count = 0
    error_count = 0
    
    # Log the start of analysis session
    log_operation(
        operation="portfolio_analysis_start",
        details={
            "portfolios": PORTFOLIO_IDS,
            "risk_config": RISK_CONFIG,
            "volatility_days": VOLATILITY_DAYS
        },
        level="info"
    )
    
    print("=" * 60)
    print("PORTFOLIO RISK ANALYSIS AGENT")
    print("=" * 60)
    print(f"\nAnalyzing {len(PORTFOLIO_IDS)} portfolios...")
    print(f"Risk Config: Max Volatility={RISK_CONFIG['max_volatility']}, "
          f"Min Value=${RISK_CONFIG['min_value']:,}, "
          f"Max Value=${RISK_CONFIG['max_value']:,}\n")
    
    # Process each portfolio
    for portfolio_id in PORTFOLIO_IDS:
        print(f"\n{'─' * 50}")
        print(f"Processing: {portfolio_id}")
        print(f"{'─' * 50}")
        
        try:
            # =================================================================
            # Step 1: Fetch Portfolio Holdings
            # =================================================================
            log_operation(
                operation="fetch_holdings",
                details={"portfolio_id": portfolio_id},
                level="info"
            )
            
            print(f"  [1] Fetching holdings...")
            holdings_data = get_portfolio_holdings(portfolio_id)
            
            client_name = holdings_data.get("client_name", "Unknown")
            manager_email = holdings_data.get("manager_email", "")
            holdings = holdings_data.get("holdings", [])
            
            print(f"      Client: {client_name}")
            print(f"      Holdings: {len(holdings)} positions")
            
            # =================================================================
            # Step 2: Extract Symbols and Get Stock Prices
            # =================================================================
            symbols = extract_symbols(holdings)
            print(f"  [2] Fetching stock prices for {len(symbols)} symbols: {symbols}")
            
            log_operation(
                operation="fetch_prices",
                details={"portfolio_id": portfolio_id, "symbols": symbols},
                level="info"
            )
            
            current_prices = get_stock_prices(symbols)
            print(f"      Prices retrieved: {len(current_prices)} symbols")
            
            # =================================================================
            # Step 3: Calculate Portfolio Value
            # =================================================================
            print(f"  [3] Calculating portfolio value...")
            
            log_operation(
                operation="calculate_value",
                details={"portfolio_id": portfolio_id},
                level="info"
            )
            
            value_data = calculate_portfolio_value(holdings, current_prices)
            total_value = value_data.get("total_value", 0.0)
            
            print(f"      Total Value: ${total_value:,.2f}")
            
            # Log position details
            for position in value_data.get("positions", []):
                gl_pct = position.get("gain_loss_percent", 0)
                gl_indicator = "▲" if gl_pct >= 0 else "▼"
                print(f"      {position['symbol']}: {position['shares']} shares @ "
                      f"${position['current_price']:.2f} ({gl_indicator} {abs(gl_pct):.2f}%)")
            
            # =================================================================
            # Step 4: Calculate Volatility Score
            # =================================================================
            print(f"  [4] Calculating volatility score ({VOLATILITY_DAYS}-day)...")
            
            log_operation(
                operation="calculate_volatility",
                details={"portfolio_id": portfolio_id, "symbols": symbols},
                level="info"
            )
            
            # Handle case where we have no valid symbols
            if not symbols:
                volatility_score = 0.0
                print(f"      No valid symbols for volatility calculation")
            else:
                volatility_score = calculate_volatility_score(symbols, days=VOLATILITY_DAYS)
                print(f"      Volatility Score: {volatility_score:.2f}/100")
            
            # =================================================================
            # Step 5: Check Risk Thresholds
            # =================================================================
            print(f"  [5] Checking risk thresholds...")
            
            log_operation(
                operation="risk_check",
                details={
                    "portfolio_id": portfolio_id,
                    "total_value": total_value,
                    "volatility_score": volatility_score
                },
                level="info"
            )
            
            risk_check = check_risk_threshold(
                total_value,
                volatility_score,
                RISK_CONFIG
            )
            
            is_high_risk = risk_check.get("is_high_risk", False)
            risk_level = risk_check.get("risk_level", "UNKNOWN")
            exceeded = risk_check.get("exceeded_thresholds", [])
            
            print(f"      Risk Level: {risk_level}")
            if exceeded:
                print(f"      Exceeded: {', '.join(exceeded)}")
            
            # =================================================================
            # Step 6: Handle High-Risk Portfolios
            # =================================================================
            if is_high_risk:
                high_risk_count += 1
                print(f"\n  ⚠️  HIGH RISK PORTFOLIO DETECTED!")
                print(f"  [6] Generating report...")
                
                log_operation(
                    operation="high_risk_detected",
                    details={
                        "portfolio_id": portfolio_id,
                        "risk_level": risk_level,
                        "exceeded_thresholds": exceeded
                    },
                    level="warning"
                )
                
                # Prepare portfolio data for report
                portfolio_data = prepare_portfolio_data(
                    portfolio_id,
                    holdings_data,
                    value_data,
                    volatility_score,
                    risk_check
                )
                
                # Generate markdown report
                try:
                    report = generate_report(portfolio_data, report_format="markdown")
                    print(f"      Report generated ({len(report)} characters)")
                except ValueError as e:
                    log_operation(
                        operation="report_generation_error",
                        details={"portfolio_id": portfolio_id, "error": str(e)},
                        level="error"
                    )
                    report = f"Error generating report: {str(e)}"
                
                # Send notification to portfolio manager
                print(f"  [7] Sending notification to manager...")
                
                log_operation(
                    operation="send_notification",
                    details={"portfolio_id": portfolio_id, "recipient": manager_email},
                    level="info"
                )
                
                try:
                    notification_result = send_notification(
                        recipient=manager_email,
                        subject=f"High Risk Alert: Portfolio {portfolio_id}",
                        message=report,
                        priority="high"
                    )
                    
                    if notification_result.get("sent"):
                        print(f"      ✓ Notification sent successfully!")
                        print(f"        Message ID: {notification_result.get('message_id')}")
                        
                        log_operation(
                            operation="notification_sent",
                            details={
                                "portfolio_id": portfolio_id,
                                "message_id": notification_result.get("message_id"),
                                "timestamp": notification_result.get("timestamp")
                            },
                            level="info"
                        )
                    else:
                        print(f"      ✗ Notification failed to send")
                        
                except ValueError as e:
                    print(f"      ✗ Notification error: {str(e)}")
                    log_operation(
                        operation="notification_error",
                        details={"portfolio_id": portfolio_id, "error": str(e)},
                        level="error"
                    )
            else:
                print(f"\n  ✓ Portfolio within acceptable risk parameters")
                log_operation(
                    operation="risk_acceptable",
                    details={"portfolio_id": portfolio_id, "risk_level": risk_level},
                    level="info"
                )
            
            processed_count += 1
            print(f"\n  ✓ Completed processing {portfolio_id}")
            
        except ValueError as e:
            # Handle invalid portfolio ID or other ValueError
            error_count += 1
            print(f"\n  ✗ Error processing {portfolio_id}: {str(e)}")
            log_operation(
                operation="portfolio_error",
                details={"portfolio_id": portfolio_id, "error": str(e), "type": "ValueError"},
                level="error"
            )
            
        except KeyError as e:
            # Handle missing data keys
            error_count += 1
            print(f"\n  ✗ Data error for {portfolio_id}: Missing key {str(e)}")
            log_operation(
                operation="portfolio_error",
                details={"portfolio_id": portfolio_id, "error": str(e), "type": "KeyError"},
                level="error"
            )
            
        except Exception as e:
            # Catch any unexpected errors
            error_count += 1
            print(f"\n  ✗ Unexpected error for {portfolio_id}: {str(e)}")
            log_operation(
                operation="portfolio_error",
                details={"portfolio_id": portfolio_id, "error": str(e), "type": "Exception"},
                level="error"
            )
    
    # =================================================================
    # Log Session Completion
    # =================================================================
    print(f"\n{'=' * 60}")
    print("ANALYSIS COMPLETE")
    print(f"{'=' * 60}")
    print(f"  Portfolios Processed: {processed_count}")
    print(f"  High-Risk Portfolios: {high_risk_count}")
    print(f"  Errors: {error_count}")
    print(f"{'=' * 60}\n")
    
    log_operation(
        operation="portfolio_analysis_complete",
        details={
            "portfolios_processed": processed_count,
            "high_risk_count": high_risk_count,
            "error_count": error_count
        },
        level="info"
    )
    
    return {
        "processed": processed_count,
        "high_risk": high_risk_count,
        "errors": error_count
    }


# =============================================================================
# ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    results = analyze_portfolios()
```

## Section 3: Design Justification

```markdown
## Design Justification

### Tool Orchestration Sequence

I chose a sequential processing approach for the following reasons:

1. **Data Dependencies**: Each portfolio requires a strict dependency chain:
   - Holdings → Symbols → Prices → Value Calculation → Volatility → Risk Check
   
   This sequential flow ensures each step has the required data from the previous step.

2. **API Rate Limiting**: In production, financial APIs often have rate limits. Sequential 
   processing prevents overwhelming the backend systems with parallel requests.

3. **Error Isolation**: By processing one portfolio completely before moving to the next, 
   errors in one portfolio don't cascade to others. This is critical for maintaining 
   partial results when errors occur.

4. **Audit Trail Clarity**: Sequential processing creates a cleaner, more traceable audit 
   log that's easier to debug and audit.

### Data Flow Strategy

**Holdings as Central Data Source:**
- The `get_portfolio_holdings()` output serves as the primary data source
- It feeds three downstream operations:
  1. Symbol extraction → `get_stock_prices()`
  2. Position data → `calculate_portfolio_value()`
  3. Manager email → `send_notification()`

**Two-Arm Branching for Risk Handling:**
- After risk check, the flow branches:
  - High-risk: Generate report → Send notification → Log completion
  - Low-risk: Skip directly to completion logging

**Data Transformation Pipeline:**
- `extract_symbols()`: Converts holdings list to symbol list (set for deduplication)
- `prepare_portfolio_data()`: Aggregates all results into report-friendly format

### Error Handling Strategy

**Layered Error Handling:**

1. **Top-Level Portfolio Isolation**: Each portfolio is wrapped in try/except, ensuring 
   one portfolio's failure doesn't prevent processing of others.

2. **Exception Type Specificity**: Different exception types are caught separately:
   - `ValueError`: Invalid inputs (invalid portfolio ID, bad data format)
   - `KeyError`: Missing expected keys in data structures
   - General `Exception`: Catches unexpected errors for graceful degradation

3. **Logging at Every Level**: Every error is logged with:
   - Operation name
   - Portfolio ID
   - Error message
   - Exception type
   - Appropriate log level (error/warning)

4. **Graceful Degradation**:
   - Missing prices: Position skipped in value calculation
   - Missing volatility: Assigned 0.0 (conservative, will likely trigger risk check)
   - Notification failure: Logged but doesn't stop portfolio processing

5. **User Feedback**: Console output provides real-time feedback on processing status, 
   making it easy to identify issues during execution.

### Trade-offs Considered

**Parallel vs. Sequential Processing:**
- Considered: Parallel fetching of all portfolios
- Decision: Sequential chosen for reasons above (cleaner dependencies, better error handling)
- Trade-off: Slower execution, but more robust and traceable

**Fail-Fast vs. Continue on Error:**
- Considered: Stopping entire process on any error
- Decision: Continue processing remaining portfolios
- Trade-off: Some alerts may be delayed, but all portfolios get analyzed

**Detailed vs. Minimal Logging:**
- Considered: Only log errors
- Decision: Log all major operations (info level) + errors (error level)
- Trade-off: More verbose logs, but better audit trail and debugging capability

### Code Quality Decisions

1. **Modular Helper Functions**: Extracted `extract_symbols()` and `prepare_portfolio_data()` 
   for reusability and readability.

2. **Configuration as Constants**: RISK_CONFIG and PORTFOLIO_IDS at module level make 
   it easy to modify without changing code logic.

3. **Comprehensive Documentation**: Docstrings explain inputs, outputs, and purpose of 
   each function.

4. **Consistent Output Formatting**: Currency values formatted with commas, percentages 
   with appropriate precision for readability.

5. **Clear Console Feedback**: Print statements provide real-time status updates, helpful 
   for monitoring automated runs.
```