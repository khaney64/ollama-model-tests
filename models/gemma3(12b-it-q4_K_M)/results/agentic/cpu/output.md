```python
# tools_reference.py (Simulated Tools - DO NOT MODIFY)
import random
import time
from datetime import datetime

def get_stock_prices(symbols: list[str]) -> dict[str, float]:
    """Fetches current market prices for given stock symbols."""
    if not symbols:
        raise ValueError("Symbols list cannot be empty")

    prices = {}
    for symbol in symbols:
        if symbol == "AAPL":
            prices[symbol] = 178.50 + random.uniform(-1, 1)
        elif symbol == "MSFT":
            prices[symbol] = 380.25 + random.uniform(-2, 2)
        elif symbol == "GOOGL":
            prices[symbol] = 2700.00 + random.uniform(-3, 3)
        else:
            prices[symbol] = None
    return prices


def get_portfolio_holdings(portfolio_id: str) -> dict:
    """Retrieves holdings information for a specific portfolio."""
    if portfolio_id not in ["PORT-001", "PORT-002", "PORT-003"]:
        raise ValueError("Invalid portfolio ID")

    if portfolio_id == "PORT-001":
        return {
            "portfolio_id": "PORT-001",
            "client_name": "Alice Smith",
            "manager_email": "alice.manager@firm.com",
            "holdings": [
                {"symbol": "AAPL", "shares": 10, "purchase_price": 150.00},
                {"symbol": "MSFT", "shares": 5, "purchase_price": 250.00}
            ]
        }
    elif portfolio_id == "PORT-002":
        return {
            "portfolio_id": "PORT-002",
            "client_name": "Bob Johnson",
            "manager_email": "bob.manager@firm.com",
            "holdings": [
                {"symbol": "GOOGL", "shares": 2, "purchase_price": 2600.00},
                {"symbol": "AAPL", "shares": 20, "purchase_price": 160.00}
            ]
        }
    else: # PORT-003
        return {
            "portfolio_id": "PORT-003",
            "client_name": "Charlie Brown",
            "manager_email": "charlie.manager@firm.com",
            "holdings": [
                {"symbol": "MSFT", "shares": 10, "purchase_price": 280.00},
                {"symbol": "AAPL", "shares": 5, "purchase_price": 170.00}
            ]
        }


def calculate_portfolio_value(holdings: list[dict], current_prices: dict[str, float]) -> dict:
    """Calculates total portfolio value and individual position values."""
    if not holdings or not current_prices:
        raise ValueError("Holdings or current_prices cannot be empty")

    total_value = 0
    positions = []
    for holding in holdings:
        symbol = holding["symbol"]
        price = current_prices.get(symbol)
        if price is not None:
            position_value = holding["shares"] * price
            total_value += position_value
            gain_loss = position_value - holding["purchase_price"] * holding["shares"]
            gain_loss_percent = (gain_loss / (holding["purchase_price"] * holding["shares"]) ) if (holding["purchase_price"] * holding["shares"]) != 0 else 0.0

            positions.append({
                "symbol": symbol,
                "shares": holding["shares"],
                "current_price": price,
                "position_value": position_value,
                "gain_loss": gain_loss,
                "gain_loss_percent": gain_loss_percent
            })
        else:
            log_operation("price_missing", {"symbol": symbol, "holding": holding}, level="warning")
    return {"total_value": total_value, "positions": positions}


def calculate_volatility_score(symbols: list[str], days: int = 30) -> float:
    """Calculates aggregate volatility score for a set of stocks."""
    if not symbols:
        raise ValueError("Symbols list cannot be empty")
    if days < 1:
        raise ValueError("Days must be greater than or equal to 1")

    # Simulate volatility score based on the number of symbols
    return random.uniform(10.0, 40.0)


def check_risk_threshold(portfolio_value: float, volatility_score: float, risk_config: dict) -> dict:
    """Checks if portfolio exceeds configured risk thresholds."""
    if portfolio_value < 0:
        raise ValueError("Portfolio value cannot be negative")
    if volatility_score < 0:
        raise ValueError("Volatility score cannot be negative")

    is_high_risk = False
    exceeded_thresholds = []
    risk_level = "LOW"

    if volatility_score > risk_config["max_volatility"]:
        is_high_risk = True
        exceeded_thresholds.append("volatility")
    if portfolio_value < risk_config["min_value"]:
        is_high_risk = True
        exceeded_thresholds.append("value_low")
    if portfolio_value > risk_config["max_value"]:
        is_high_risk = True
        exceeded_thresholds.append("value_high")

    if is_high_risk:
        risk_level = "HIGH"

    return {"is_high_risk": is_high_risk, "exceeded_thresholds": exceeded_thresholds, "risk_level": risk_level}


def generate_report(portfolio_data: dict, report_format: str = "markdown") -> str:
    """Generates a formatted risk analysis report."""
    if not all(key in portfolio_data for key in ["portfolio_id", "client_name", "total_value", "volatility_score", "risk_level", "exceeded_thresholds", "positions"]):
        raise ValueError("Missing required fields in portfolio_data")
    if report_format not in ["markdown", "html", "text"]:
        raise ValueError("Invalid report format")

    if report_format == "markdown":
        report = f"""
# Risk Analysis Report
## Portfolio ID: {portfolio_data["portfolio_id"]}
## Client: {portfolio_data["client_name"]}
### Total Value: ${portfolio_data["total_value"]:.2f}
### Volatility Score: {portfolio_data["volatility_score"]:.2f}
### Risk Level: {portfolio_data["risk_level"]}
#### Exceeded Thresholds: {', '.join(portfolio_data["exceeded_thresholds"])}
##### Positions:
"""
        for pos in portfolio_data["positions"]:
            report += f"""- {pos['symbol']}: Shares: {pos['shares']}, Value: ${pos['position_value']:.2f}, Gain/Loss: ${pos['gain_loss']:.2f} ({pos['gain_loss_percent']:.2f}%)"""
        return report
    else:
        return f"Report generated in {report_format} format (not implemented)"


def send_notification(recipient: str, subject: str, message: str, priority: str = "normal") -> dict:
    """Sends notification email to portfolio manager."""
    if not recipient:
        raise ValueError("Recipient cannot be empty")
    if priority not in ["low", "normal", "high"]:
        raise ValueError("Invalid priority level")
    time.sleep(0.1)
    return {"sent": True, "message_id": f"msg-{random.randint(1000, 9999)}", "timestamp": datetime.utcnow().isoformat()}


def log_operation(operation: str, details: dict, level: str = "info") -> None:
    """Logs operations to audit trail."""
    if level not in ["info", "warning", "error"]:
        raise ValueError("Invalid log level")
    timestamp = datetime.utcnow().isoformat()
    log_message = f"[{timestamp}] {level.upper()} - {operation}: {details}"
    print(log_message) #Simulate logging to file.



# -------------------- Main Script --------------------

import tools_reference as tools

def analyze_portfolios():
    """Main orchestration function."""

    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]

    log_operation("analysis_start", {"portfolio_ids": portfolio_ids}, level="info")

    for portfolio_id in portfolio_ids:
        try:
            log_operation(f"portfolio_analysis_start", {"portfolio_id": portfolio_id}, level="info")

            holdings = tools.get_portfolio_holdings(portfolio_id)
            log_operation(f"holdings_retrieved", {"portfolio_id": portfolio_id}, level="info")

            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            prices = tools.get_stock_prices(symbols)
            log_operation(f"stock_prices_retrieved", {"portfolio_id": portfolio_id, "symbols": symbols}, level="info")

            portfolio_data = tools.calculate_portfolio_value(holdings["holdings"], prices)
            log_operation(f"portfolio_value_calculated", {"portfolio_id": portfolio_id}, level="info")

            volatility_score = tools.calculate_volatility_score(symbols)
            log_operation(f"volatility_score_calculated", {"portfolio_id": portfolio_id, "volatility_score": volatility_score}, level="info")

            risk_check = tools.check_risk_threshold(portfolio_data["total_value"], volatility_score, risk_config)
            log_operation(f"risk_threshold_check", {"portfolio_id": portfolio_id, "risk_level": risk_check["risk_level"]}, level="info")

            if risk_check["is_high_risk"]:
                report = tools.generate_report(portfolio_data)
                log_operation(f"report_generated", {"portfolio_id": portfolio_id}, level="info")
                notification_result = tools.send_notification(holdings["manager_email"], f"High Risk Alert: {portfolio_id}", report, priority="high")
                log_operation(f"notification_sent", {"portfolio_id": portfolio_id, "notification_result": notification_result}, level="info")
            else:
                log_operation(f"portfolio_ok", {"portfolio_id": portfolio_id}, level="info")


        except ValueError as e:
            log_operation(f"portfolio_analysis_error", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
        except Exception as e:
            log_operation(f"portfolio_analysis_exception", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")

    log_operation("analysis_end", {}, level="info")



if __name__ == "__main__":
    analyze_portfolios()
```

### Section 1: Execution Plan (Markdown)

## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up risk thresholds and portfolio list
   - Data: `risk_config`, `portfolio_ids`

2. **Iterate Through Portfolios**
    -  Loop through each `portfolio_id` in `portfolio_ids`

3. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: `portfolio_id`
   - Output: `holdings_data` (needed for steps b, c, e)
   - Error Handling:  `try/except` block to catch `ValueError` (invalid ID), log error, continue to next portfolio.

4. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: list of symbols extracted from `holdings_data["holdings"]`
   - Output: `current_prices` (needed for step c)
   - Error Handling:  `try/except` block, log any missing stock data as a warning, continue processing.

5. **Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value()`
   - Input: `holdings_data["holdings"]`, `current_prices`
   - Output: `portfolio_value_data` (needed for steps d, e)
   - Error Handling: `try/except` block to catch empty inputs, log error, continue to next portfolio.

6. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: list of symbols from `holdings_data["holdings"]`
   - Output: `volatility_score` (needed for step e)
   - Error Handling: `try/except` block to catch empty symbols, log error, continue to next portfolio.

7. **Check Risk Threshold**
   - Tool: `check_risk_threshold()`
   - Input: `portfolio_value_data["total_value"]`, `volatility_score`, `risk_config`
   - Output: `risk_check_result` (determines if report is needed)
   - Error Handling: `try/except` block to catch negative value errors, log error, continue to next portfolio.

8. **Generate and Send Notification (Conditional)**
   - Tool: `generate_report()`
   - Input: `portfolio_value_data`
   - Output: `report_text` (if `risk_check_result["is_high_risk"]` is True)
   - Tool: `send_notification()`
   - Input: `holdings_data["manager_email"]`, `report_text`, "high" (priority)
   - Output: `notification_result` (if `risk_check_result["is_high_risk"]` is True)
   - Error Handling: `try/except` blocks for both, log errors, continue to next portfolio.

9. **Logging**
   - Tool: `log_operation()`
   - Input: Operation name, relevant details, log level
   - Log all major steps and errors for audit trail.

10. **Analysis Completion**
    - Tool: None
    - Log a completion message.

### Section 2: Implementation (Python)

(See the provided Python code above.  It includes the complete implementation.)

### Section 3: Design Justification (Markdown)

## Design Justification

### Tool Orchestration Sequence

I chose a sequential processing approach for the portfolios because it's the most straightforward way to ensure data dependencies are met.  Each portfolio's analysis builds upon the previous steps.  Parallelization could be considered for performance but would significantly increase complexity, particularly in handling error recovery across multiple processes. This sequential approach prioritizes correctness and simplicity.

### Data Flow Strategy

The data flow is designed to be pipeline-like. The output of one function becomes the input for the next.  For instance, the holdings retrieved by `get_portfolio_holdings()` are used in `calculate_portfolio_value()` and `calculate_volatility_score()`.  This minimizes data duplication and maximizes code reusability.

### Error Handling Strategy

The overarching error handling strategy revolves around *isolation and continuation*. Each portfolio analysis is wrapped in a `try...except` block to prevent a single portfolio's failure from halting the entire process. Specific `ValueError` exceptions are caught to handle validation errors in the API calls.  Generic `Exception` is also caught to handle unexpected errors.  All errors are logged with `log_operation()` with appropriate error levels.  This allows for detailed auditing and debugging while ensuring that other portfolios are processed. If a tool fails and raises an exception, the error is logged, and the execution continues to the next portfolio.

### Trade-offs Considered

*   **Parallelization vs. Sequential Processing:** Parallel processing was considered for potentially faster overall execution time. However, the added complexity of managing shared resources and inter-process communication outweighed the benefits for this task.  Sequential processing was chosen for simplicity and maintainability.
*   **Data Validation:** While the tools perform some basic validation, additional data validation checks could be implemented to improve data quality and prevent errors downstream.
*   **Notification Retries:** The `send_notification()` function does not currently include retry logic. Implementing retries would increase the reliability of notifications.
```