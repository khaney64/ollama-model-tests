Here's a detailed Python script that accomplishes the Agentic Task:

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

def main():
    # Initialize risk thresholds and portfolio list
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]
    
    # Process each portfolio sequentially
    for i, portfolio in enumerate(portfolios):
        try:
            print(f"Processing portfolio {portfolio}...")
            
            # Get holdings and prices
            holdings = get_portfolio_holdings(portfolio)
            if not holdings:
                raise ValueError("Holdings not found")
            
            current_prices = get_stock_prices([holding["symbol"] for holding in holdings["holdings"]])
            for symbol, price in current_prices.items():
                if price is None:
                    print(f"Skipping {symbol} with no price data")
                else:
                    holdings["holdings"][0]["current_price"] = price
            
            # Calculate portfolio value and positions
            portfolio_value, positions = calculate_portfolio_value(holdings["holdings"], current_prices)
            
            # Calculate volatility score
            volatility_score = calculate_volatility_score([holding["symbol"] for holding in holdings["holdings"]])
            
            # Check risk thresholds
            risk_result = check_risk_threshold(portfolio_value, volatility_score, risk_config)
            
            if risk_result["is_high_risk"]:
                print(f"High-risk portfolio {portfolio} detected!")
                
                # Generate report and send notification
                report_data = {
                    "portfolio_id": portfolio,
                    "total_value": portfolio_value,
                    "volatility_score": volatility_score,
                    "risk_level": "HIGH",
                    "exceeded_thresholds": ["volatility"]
                }
                
                markdown_report = generate_report(report_data)
                print(markdown_report)
                
                send_notification(
                    recipient="manager@firm.com",
                    subject=f"High Risk Alert: Portfolio {portfolio}",
                    message=markdown_report,
                    priority="high"
                )
                
                # Log operation
                log_operation(
                    operation="risk_check",
                    details={"portfolio_id": portfolio, "risk_level": risk_result["risk_level"]},
                    level="warning"
                )
            else:
                print(f"Low-risk portfolio {portfolio} detected!")
            
        except Exception as e:
            print(f"Error processing portfolio {portfolio}: {e}")
            
    # Log final operation
    log_operation(
        operation="all_portfolios_processed",
        details={},
        level="info"
    )

if __name__ == "__main__":
    main()
```

The script includes the following features:

*   **Portfolio Analysis**: Fetches holdings data and current stock prices for each portfolio, calculates total portfolio value and position details, and determines volatility scores.
*   **Risk Thresholds**: Checks if portfolios exceed configured risk thresholds and identifies high-risk portfolios based on these thresholds.
*   **Report Generation and Notification**: For high-risk portfolios, generates markdown-formatted reports and sends notifications to portfolio managers with "high" priority.
*   **Audit Trail**: Maintains an audit trail of all major operations using `log_operation`.

This script assumes that the tools are simulated for this task. In production, these would be real API calls to backend systems.