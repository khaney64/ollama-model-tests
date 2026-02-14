## Section 1: Execution Plan (Markdown)

### Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list.

2. **For Each Portfolio:**

   a. **Fetch Holdings**
      - Tool: `get_portfolio_holdings()`
      - Input: portfolio_id
      - Output: holdings data (needed for steps b, c, e)

   b. **Get Stock Prices**
      - Tool: `get_stock_prices()`
      - Input: symbols extracted from holdings
      - Output: current prices (needed for step c)

   c. **Calculate Portfolio Value and Position Details**
      - Tool: `calculate_portfolio_value()`
      - Input: holdings data, current prices
      - Output: total portfolio value and position details

   d. **Calculate Volatility Score**
      - Tool: `calculate_volatility_score()`
      - Input: symbols extracted from holdings, days=30
      - Output: volatility score (needed for step e)

   e. **Check Risk Thresholds**
      - Tool: `check_risk_threshold()`
      - Input: total portfolio value, volatility score, risk_config
      - Output: risk analysis results

   f. **Generate and Send Report (if high-risk)**
      - Tool: `generate_report()` if is_high_risk=True
      - Input: portfolio data
      - Output: formatted report text
      - Tool: `send_notification()` if is_high_risk=True
      - Input: manager email, subject, report text
      - Output: notification status

3. **Maintain Audit Trail**
   - Log each major operation using `log_operation()`
   - Tools used in logging for all steps above

4. **Error Handling Strategy**
   - Wrap each portfolio analysis in a try/except block
   - Catch specific exceptions (e.g., `ValueError`) and log them
   - Continue processing remaining portfolios if one fails

## Section 2: Implementation (Python)

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
    """Main orchestration function."""
    # Initialize configuration
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }

    for portfolio_id in portfolios:
        try:
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "status": "start"}, level="info")

            # Fetch holdings
            portfolio_data = get_portfolio_holdings(portfolio_id)
            if not portfolio_data:
                raise ValueError(f"No holdings data found for portfolio {portfolio_id}")

            # Extract symbols from holdings
            symbols = [holding["symbol"] for holding in portfolio_data["holdings"]]

            # Get stock prices
            current_prices = get_stock_prices(symbols)
            missing_symbols = [sym for sym, price in current_prices.items() if price is None]
            if missing_symbols:
                log_operation("missing_symbol_prices", {"portfolio_id": portfolio_id, "symbols": missing_symbols}, level="warning")

            # Calculate portfolio value and position details
            portfolio_value_data = calculate_portfolio_value(portfolio_data["holdings"], current_prices)
            portfolio_data.update({
                "total_value": portfolio_value_data["total_value"],
                "positions": portfolio_value_data["positions"]
            })

            # Calculate volatility score
            volatility_score = calculate_volatility_score(symbols, days=30)

            # Check risk thresholds
            risk_check_result = check_risk_threshold(
                portfolio_data["total_value"],
                volatility_score,
                risk_config
            )
            portfolio_data.update({
                "volatility_score": volatility_score,
                **risk_check_result
            })

            log_operation("risk_check", {"portfolio_id": portfolio_id, "risk_level": portfolio_data["risk_level"]}, level="info")

            # Generate and send report if high-risk
            if risk_check_result["is_high_risk"]:
                report_text = generate_report(portfolio_data, report_format="markdown")
                notification_result = send_notification(
                    portfolio_data["manager_email"],
                    f"High Risk Alert: Portfolio {portfolio_id}",
                    report_text,
                    priority="high"
                )
                log_operation("report_generation", {"portfolio_id": portfolio_id}, level="info")
                log_operation("notification_sending", {
                    "portfolio_id": portfolio_id,
                    "sent": notification_result["sent"],
                    "message_id": notification_result.get("message_id"),
                    "timestamp": notification_result.get("timestamp")
                }, level="info")

        except ValueError as ve:
            log_operation("error", {"portfolio_id": portfolio_id, "error_message": str(ve)}, level="error")
        finally:
            log_operation("portfolio_analysis", {"portfolio_id": portfolio_id, "status": "complete"}, level="info")

if __name__ == "__main__":
    analyze_portfolios()
```

## Section 3: Design Justification (Markdown)

### Design Justification

#### Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because the task involves multiple interdependent operations such as fetching prices, calculating values, and checking thresholds. This sequence ensures that each portfolio is fully analyzed before moving on to the next one, allowing for easier debugging and error handling.

#### Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) because:
1. The symbols in holdings are needed to fetch current prices.
2. Current prices are required to calculate the portfolio's total value and individual positions' details.
3. Symbols from holdings are used to calculate the volatility score.

This flow ensures that all necessary data is available at each step without any gaps.

#### Error Handling Strategy
I implemented a comprehensive error handling strategy by:
1. Wrapping each portfolio analysis in a try/except block.
2. Catching specific exceptions like `ValueError` and logging them with detailed information.
3. Continuing to process remaining portfolios even if one fails, ensuring that the system remains robust and operational.

#### Trade-offs Considered
- **Sequential vs Parallel Processing**: Sequential processing is chosen for simplicity and ease of error handling, although parallel processing could potentially speed up the analysis for a large number of portfolios.
- **Data Dependency Management**: Ensuring all required data is available at each step simplifies the flow but can lead to more complex code. However, this approach maintains clarity and reduces the risk of errors.

The overall design aims to be robust, maintainable, and aligned with the requirements specified by the financial advisory firm.