## Section 1: Execution Plan

1. **Initialize Configuration**:
   - Tools: None
   - Set up risk thresholds dictionary and portfolio IDs list.

2. **Process Each Portfolio:** (For portfolios "PORT-001", "PORT-002", "PORT-003")
   a. **Fetch Holdings**:
      - Tool: `get_portfolio_holdings()`
      - Input: Current portfolio ID.
      - Output: Portfolio holdings data (list of dictionaries) including symbols, shares, and purchase prices.
   b. **Get Stock Prices**: 
      - Tool: `get_stock_prices()`
      - Input: List of stock symbols from holdings data.
      - Output: Dictionary mapping symbols to current market prices (float values).
   c. **Calculate Portfolio Value and Risk Metrics**:
      - Tool: `calculate_portfolio_value()`
      - Input: Holdings data and fetched stock prices dictionary.
      - Output: Dictionary containing total portfolio value, position details (including gain/loss), and volatility score calculated using `calculate_volatility_score()`.
   d. **Check Risk Thresholds**:
      - Tool: `check_risk_threshold()`
      - Input: Portfolio value, calculated volatility score, and risk configuration dictionary.
      - Output: Dictionary indicating whether the portfolio exceeds any thresholds ("is_high_risk"), a list of exceeded thresholds, and an overall risk level ("LOW", "MEDIUM", or "HIGH").

3. **Generate Report and Send Notification (If High Risk)**
   a. **Create Report**: 
      - Tool: `generate_report()`
      - Input: Portfolio data (from step c) formatted as required by the tool, along with specified risk level and exceeded thresholds.
      - Output: Markdown formatted report string.
   b. **Send Notification**: 
      - Tool: `send_notification()`
      - Input: Manager email address, subject line ("High Risk Alert"), body containing report contents, and "high" priority.
      - Output: Dictionary confirming successful delivery (sent status, message ID, timestamp).

4. **Log All Operations**:
   - Tool: `log_operation()`
   - Each step will log its execution with details about the portfolio analyzed and any relevant parameters or results.


### Error Handling Strategy

- **Portfolio Analysis Failure:** A `try/except` block around each portfolio iteration will catch exceptions raised by the tools (e.g., invalid ID, missing data). 
   - The script will log the error, print a message indicating failure for that specific portfolio, and continue processing remaining portfolios.

- **Missing Stock Prices:** If `get_stock_prices()` returns `None` for any symbol, the corresponding position value will be skipped in the calculation of portfolio value and volatility score. 
   - A warning log message will be recorded indicating the missing price.

- **Notification Failure:** A `try/except` block around `send_notification()` will catch potential errors during sending (e.g., invalid email address). 
   - An error log message will record the failure, and a notification attempt will not be made for subsequent portfolios if there is ongoing issue with the notification service.

## Section 2: Implementation (Python)


```python
from tools_reference import get_stock_prices, get_portfolio_holdings, calculate_portfolio_value, calculate_volatility_score, check_risk_threshold, generate_report, send_notification, log_operation

RISK_CONFIG = {
    "max_volatility": 35.0,
    "min_value": 50000,
    "max_value": 2000000
}

PORTFOLIO_IDS = ["PORT-001", "PORT-002", "PORT-003"]


def analyze_portfolios():
    for portfolio_id in PORTFOLIO_IDS:
        try:
            holdings = get_portfolio_holdings(portfolio_id) 
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id})
            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            prices = get_stock_prices(symbols)  

            portfolio_value_data = calculate_portfolio_value(holdings["holdings"], prices)
            volatility_score = calculate_volatility_score(symbols, days=30)
            risk_check = check_risk_threshold(portfolio_value_data["total_value"], volatility_score, RISK_CONFIG) 

            if risk_check["is_high_risk"]:
                report = generate_report(
                    {
                        "portfolio_id": portfolio_id,
                        "client_name": holdings["client_name"],
                        **portfolio_value_data,  # Include all calculated values from step c
                        "risk_level": risk_check["risk_level"], 
                        "exceeded_thresholds": risk_check["exceeded_thresholds"]
                    },
                    report_format="markdown"
                )

                send_notification(
                    recipient=holdings["manager_email"],  
                    subject="High Risk Alert: Portfolio {}".format(portfolio_id), 
                    message=report,
                    priority="high"
                )
            else:
                log_operation("risk_check", {"portfolio_id": portfolio_id, "risk_level": risk_check["risk_level"]})

        except Exception as e:
            print(f"Error processing portfolio {portfolio_id}: {e}")
            log_operation("portfolio_analysis_error", {"portfolio_id": portfolio_id, "error": str(e)})


if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification



### Tool Orchestration Sequence

I chose a sequential processing order for portfolios because the risk analysis logic for each portfolio is independent. Processing one portfolio does not depend on the results of another. This approach simplifies the code and allows parallel execution if needed in a production setting.


### Data Flow Strategy

Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because this data is essential to all these calculations. 
- The fetched stock prices are then used to calculate portfolio value and individual position values. 
- Finally, the calculated portfolio value and holdings information are combined with the volatility score to check risk thresholds.

### Error Handling Strategy Rationale

The `try/except` blocks are designed to handle potential errors gracefully:

- They prevent program crashes caused by tool failures or invalid data.
- They log specific error details for debugging purposes. 


