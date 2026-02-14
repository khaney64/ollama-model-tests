# Portfolio Risk Analysis Agent Solution

## Section 1: Execution Plan

### Step-by-Step Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and list of portfolios to analyze.

2. **For Each Portfolio in the List**:
   
   a. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: portfolio ID (e.g., "PORT-001")
   - Output: holdings data, including stock symbols.
   - Error Handling: Catch and log errors for invalid or missing portfolios.

   b. **Extract Symbols from Holdings**
   - Tools: None
   - Extract the list of stock symbols from the holdings for further processing.
   
   c. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: List of symbols extracted in step 2a.
   - Output: Current prices for stocks, necessary for valuation and risk calculations.
   - Error Handling: Handle cases where some stock prices are unavailable (None).

   d. **Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value()`
   - Input: Holdings data and current prices.
   - Output: Total portfolio value and individual position values.
   - Error Handling: Skip positions with missing current prices.

   e. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: List of symbols from holdings.
   - Output: Portfolio volatility score, needed for risk assessment.
   - Error Handling: Handle empty symbol lists or other calculation errors gracefully.

   f. **Check Risk Thresholds**
   - Tool: `check_risk_threshold()`
   - Input: Portfolio value and volatility score, along with predefined risk configuration.
   - Output: Assessment of whether the portfolio is high-risk based on thresholds.
   - Error Handling: Handle invalid or negative values in calculations.

3. **For High-Risk Portfolios**:
   
   g. **Generate Report**
   - Tool: `generate_report()`
   - Input: Portfolio analysis data, including risk metrics and exceeded thresholds.
   - Output: Markdown-formatted report detailing the portfolio's risk status.
   - Error Handling: Ensure all required fields are present before generating the report.

   h. **Send Notification**
   - Tool: `send_notification()`
   - Input: Manager’s email, subject line indicating high-risk alert, and the generated report as message content.
   - Output: Confirmation of notification sent (including metadata such as timestamp).
   - Error Handling: Handle invalid recipient emails or sending failures.

4. **Maintain Audit Trail**
   
   i. **Log Operations**
   - Tool: `log_operation()`
   - Input: Details of each major operation, including successes and any exceptions caught.
   - Output: Logs maintained for auditing purposes.
   - Error Handling: Ensure logs capture both information and error states.

5. **Error Handling Strategy**
   - Use try/except blocks around critical operations to catch specific errors (e.g., `ValueError`).
   - Log each exception with a descriptive message, including portfolio ID where applicable.
   - Continue processing remaining portfolios even if one fails.

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
    log_operation,
)

def analyze_portfolios():
    """Main orchestration function for analyzing multiple portfolios."""
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    
    # Log the start of the analysis process
    log_operation("portfolio_analysis_start", {"portfolios": portfolio_ids}, level="info")
    
    for portfolio_id in portfolio_ids:
        try:
            # Fetch holdings for the current portfolio
            portfolio_data = get_portfolio_holdings(portfolio_id)
            
            # Extract stock symbols from holdings
            symbols = [holding['symbol'] for holding in portfolio_data['holdings']]
            
            # Get current prices of stocks in the portfolio
            current_prices = get_stock_prices(symbols)
            
            # Calculate total portfolio value and position details
            value_info = calculate_portfolio_value(portfolio_data['holdings'], current_prices)
            
            # Calculate volatility score for the portfolio's stocks
            volatility_score = calculate_volatility_score(symbols)
            
            # Check if the portfolio exceeds configured risk thresholds
            risk_check = check_risk_threshold(
                value_info["total_value"], 
                volatility_score, 
                risk_config
            )
            
            # Create a detailed data structure for report generation
            analysis_data = {
                "portfolio_id": portfolio_data['portfolio_id'],
                "client_name": portfolio_data['client_name'],
                "total_value": value_info["total_value"],
                "volatility_score": volatility_score,
                "risk_level": risk_check["risk_level"],
                "exceeded_thresholds": risk_check["exceeded_thresholds"],
                "positions": value_info["positions"]
            }
            
            # If portfolio is high-risk, generate a report and send a notification
            if risk_check['is_high_risk']:
                log_operation("high_risk_identified", analysis_data, level="warning")
                
                # Generate detailed report for the manager
                report = generate_report(analysis_data)
                
                # Send notification to the portfolio manager
                notify_result = send_notification(
                    recipient=portfolio_data["manager_email"],
                    subject=f"High Risk Alert: Portfolio {portfolio_id}",
                    message=report,
                    priority="high"
                )
                
                log_operation("notification_sent", {
                    "portfolio_id": portfolio_id,
                    "recipient": portfolio_data["manager_email"],
                    "sent": notify_result["sent"]
                }, level="info")
            
            # Log successful completion of analysis for the current portfolio
            log_operation("portfolio_analysis_complete", {"portfolio_id": portfolio_id}, level="info")
        
        except ValueError as ve:
            # Log any value errors encountered during processing
            log_operation("error_encountered", {
                "portfolio_id": portfolio_id,
                "error": str(ve)
            }, level="error")

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification

### Tool Orchestration Sequence

The tool orchestration sequence is designed to process each portfolio sequentially. This approach simplifies error handling and ensures comprehensive logging for each step. By processing portfolios one at a time, the script can handle exceptions individually without affecting other portfolios.

### Data Flow Strategy

Data flow between steps is managed by capturing outputs from one operation as inputs to subsequent operations. For instance, stock symbols extracted from holdings are used to fetch current prices, which are then required for portfolio value calculation and volatility scoring. This ensures a coherent data pipeline that maintains context through each phase of the analysis.

### Error Handling Strategy

Errors are handled using try/except blocks around critical sections like fetching holdings, price retrieval, and risk assessment calculations. Specific exceptions such as `ValueError` are caught to prevent program termination on encountering common issues (e.g., missing data). Logging provides visibility into errors for auditing and debugging purposes while allowing the script to continue processing remaining portfolios.

### Trade-offs Considered

The choice of sequential execution over parallel processing prioritizes simplicity, ease of error management, and comprehensive logging. Although parallelization might improve performance by reducing total runtime, it adds complexity in managing concurrent operations and handling errors across threads or processes.

By adhering closely to the given requirements and using structured logging for transparency, this design ensures that all critical information is captured and can be reviewed post-execution. The implementation supports robust risk analysis while maintaining operational clarity and auditability.