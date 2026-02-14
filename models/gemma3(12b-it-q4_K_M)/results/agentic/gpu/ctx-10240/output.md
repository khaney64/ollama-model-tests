```python
# tools_reference.py (Simulated Tools - Do not modify)
import random
import time
import uuid

class ValueError(Exception):
    pass

def get_stock_prices(symbols: list[str]) -> dict[str, float]:
    """Fetches current market prices for given stock symbols."""
    if not symbols:
        raise ValueError("Symbols list cannot be empty.")
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
        raise ValueError(f"Invalid portfolio ID: {portfolio_id}")

    if portfolio_id == "PORT-001":
        return {
            "portfolio_id": "PORT-001",
            "client_name": "Alice Smith",
            "manager_email": "alice.manager@example.com",
            "holdings": [
                {"symbol": "AAPL", "shares": 10, "purchase_price": 150.00},
                {"symbol": "MSFT", "shares": 5, "purchase_price": 250.00}
            ]
        }
    elif portfolio_id == "PORT-002":
        return {
            "portfolio_id": "PORT-002",
            "client_name": "Bob Johnson",
            "manager_email": "bob.manager@example.com",
            "holdings": [
                {"symbol": "GOOGL", "shares": 2, "purchase_price": 2600.00},
                {"symbol": "AAPL", "shares": 20, "purchase_price": 160.00}
            ]
        }
    else:
        return {
            "portfolio_id": "PORT-003",
            "client_name": "Charlie Brown",
            "manager_email": "charlie.manager@example.com",
            "holdings": [
                {"symbol": "AAPL", "shares": 5, "purchase_price": 170.00},
                {"symbol": "MSFT", "shares": 10, "purchase_price": 300.00},
                {"symbol": "GOOGL", "shares": 1, "purchase_price": 2800.00}
            ]
        }

def calculate_portfolio_value(holdings: list[dict], current_prices: dict[str, float]) -> dict:
    """Calculates total portfolio value and individual position values."""
    if not holdings or not current_prices:
        raise ValueError("Holdings and current prices must not be empty.")

    total_value = 0
    positions = []
    for holding in holdings:
        symbol = holding["symbol"]
        shares = holding["shares"]
        purchase_price = holding["purchase_price"]
        current_price = current_prices.get(symbol)  # handle None values
        if current_price is not None:
            position_value = shares * current_price
            gain_loss = shares * (current_price - purchase_price)
            gain_loss_percent = (gain_loss / (shares * purchase_price)) * 100 if (shares * purchase_price) != 0 else 0
            positions.append({
                "symbol": symbol,
                "shares": shares,
                "current_price": current_price,
                "position_value": position_value,
                "gain_loss": gain_loss,
                "gain_loss_percent": gain_loss_percent
            })
            total_value += position_value
        else:
            log_operation("calculate_portfolio_value", {"symbol": symbol, "error": "Price not available"}, level="warning")

    return {"total_value": total_value, "positions": positions}

def calculate_volatility_score(symbols: list[str], days: int = 30) -> float:
    """Calculates aggregate volatility score for a set of stocks."""
    if not symbols:
        raise ValueError("Symbols list cannot be empty.")
    if days < 1:
        raise ValueError("Days must be at least 1.")
    return random.uniform(10, 40)  # Simulate volatility

def check_risk_threshold(portfolio_value: float, volatility_score: float, risk_config: dict) -> dict:
    """Checks if portfolio exceeds configured risk thresholds."""
    if portfolio_value < 0:
        raise ValueError("Portfolio value cannot be negative.")
    if volatility_score < 0:
        raise ValueError("Volatility score cannot be negative.")

    exceeded_thresholds = []
    risk_level = "LOW"

    if volatility_score > risk_config["max_volatility"]:
        exceeded_thresholds.append("volatility")
        risk_level = "HIGH"
    if portfolio_value < risk_config["min_value"]:
        exceeded_thresholds.append("value")
    if portfolio_value > risk_config["max_value"]:
        exceeded_thresholds.append("value")

    is_high_risk = len(exceeded_thresholds) > 0

    return {"is_high_risk": is_high_risk, "exceeded_thresholds": exceeded_thresholds, "risk_level": risk_level}

def generate_report(portfolio_data: dict, report_format: str = "markdown") -> str:
    """Generates a formatted risk analysis report."""
    if not portfolio_data:
        raise ValueError("Portfolio data is missing")

    if report_format not in ["markdown", "html", "text"]:
        raise ValueError(f"Unsupported report format: {report_format}")

    if report_format == "markdown":
        report = f"""
# Risk Analysis Report

## Portfolio ID: {portfolio_data["portfolio_id"]}
## Client Name: {portfolio_data["client_name"]}

**Total Portfolio Value:** ${portfolio_data["total_value"]:.2f}
**Volatility Score:** {portfolio_data["volatility_score"]:.2f}
**Risk Level:** {portfolio_data["risk_level"]}

**Exceeded Thresholds:** {', '.join(portfolio_data["exceeded_thresholds"]) if portfolio_data["exceeded_thresholds"] else 'None'}

**Positions:**
"""
        for position in portfolio_data["positions"]:
            report += f"""
- {position["symbol"]}: Shares = {position["shares"]}, Value = ${position["position_value"]:.2f}, Gain/Loss = ${position["gain_loss"]:.2f} ({position["gain_loss_percent"]:.2f}%)
"""
        return report
    else:
        return "Simulated report content (format: " + report_format + ")"

def send_notification(recipient: str, subject: str, message: str, priority: str = "normal") -> dict:
    """Sends notification email to portfolio manager."""
    if not recipient:
        raise ValueError("Recipient cannot be empty.")
    if priority not in ["low", "normal", "high"]:
        raise ValueError(f"Invalid priority: {priority}")
    time.sleep(0.1)  # Simulate network delay
    return {"sent": True, "message_id": str(uuid.uuid4()), "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")}

def log_operation(operation: str, details: dict, level: str = "info") -> None:
    """Logs operations to audit trail."""
    if level not in ["info", "warning", "error"]:
        raise ValueError(f"Invalid log level: {level}")
    log_message = f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ')}] {level.upper()} - {operation}: {details}"
    print(log_message)
```

```python
# main.py
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

    portfolio_ids = ["PORT-001", "PORT-002", "PORT-003"]
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    portfolio_managers = {
        "PORT-001": "alice.manager@example.com",
        "PORT-002": "bob.manager@example.com",
        "PORT-003": "charlie.manager@example.com"
    }

    log_operation("portfolio_analysis", {"portfolios": portfolio_ids}, level="info")

    for portfolio_id in portfolio_ids:
        try:
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "start"}, level="info")

            holdings = get_portfolio_holdings(portfolio_id)
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "holdings_retrieved"}, level="info")

            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            prices = get_stock_prices(symbols)
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "prices_retrieved"}, level="info")

            portfolio_value_data = calculate_portfolio_value(holdings["holdings"], prices)
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "value_calculated"}, level="info")

            volatility_score = calculate_volatility_score(symbols)
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "volatility_calculated"}, level="info")

            risk_check = check_risk_threshold(portfolio_value_data["total_value"], volatility_score, risk_config)
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "risk_checked", "risk_level": risk_check["risk_level"]}, level="info")

            portfolio_data = {
                "portfolio_id": holdings["portfolio_id"],
                "client_name": holdings["client_name"],
                "total_value": portfolio_value_data["total_value"],
                "volatility_score": volatility_score,
                "risk_level": risk_check["risk_level"],
                "exceeded_thresholds": risk_check["exceeded_thresholds"],
                "positions": portfolio_value_data["positions"]
            }

            if risk_check["is_high_risk"]:
                report = generate_report(portfolio_data, report_format="markdown")
                log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "report_generated"}, level="info")
                notification_result = send_notification(portfolio_managers[portfolio_id], f"High Risk Alert: {holdings['portfolio_id']}", report, priority="high")
                log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "notification_sent", "notification_result": notification_result}, level="info")

        except ValueError as e:
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "failed", "error": str(e)}, level="error")
            print(f"Error analyzing portfolio {portfolio_id}: {e}")
        except Exception as e:
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "failed", "error": str(e)}, level="error")
            print(f"Unexpected error analyzing portfolio {portfolio_id}: {e}")
        finally:
            log_operation(f"portfolio_analysis_{portfolio_id}", {"status": "completed"}, level="info")

    log_operation("portfolio_analysis", {"status": "finished"}, level="info")

if __name__ == "__main__":
    analyze_portfolios()
```

```markdown
## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Define portfolio IDs, risk configuration, and portfolio manager email addresses.

2. **For Each Portfolio (PORT-001, PORT-002, PORT-003):**

   a. **Fetch Holdings**
     - Tool: get_portfolio_holdings()
     - Input: portfolio_id
     - Output: holdings data (needed for steps b, c, e)
     - Error Handling: Try/Except to catch ValueError (invalid portfolio ID). Log error, continue to next portfolio.

   b. **Get Stock Prices**
     - Tool: get_stock_prices()
     - Input: symbols extracted from holdings
     - Output: current prices (needed for step c)
     - Error Handling: Try/Except to catch ValueError (empty symbols list).  Handle None prices from get_stock_prices() by logging a warning and skipping that position.

   c. **Calculate Portfolio Value**
     - Tool: calculate_portfolio_value()
     - Input: holdings, current prices
     - Output: portfolio value data (needed for step e)
     - Error Handling: Try/Except to catch ValueError (empty holdings or prices).

   d. **Calculate Volatility Score**
     - Tool: calculate_volatility_score()
     - Input: symbols
     - Output: volatility score (needed for step e)
     - Error Handling: Try/Except to catch ValueError (empty symbols list or invalid days).

   e. **Check Risk Threshold**
     - Tool: check_risk_threshold()
     - Input: total portfolio value, volatility score, risk configuration
     - Output: risk check result (needed for step f)
     - Error Handling: Try/Except to catch ValueError (negative value/volatility).

   f. **Generate and Send Report (Conditional)**
     - Tool: generate_report()
     - Input: portfolio data
     - Output: report string (needed for send_notification)
     - Tool: send_notification()
     - Input: recipient email, report, priority = "high"
     - Output: notification result
     - Conditional: Only generate and send if risk_check["is_high_risk"] is True
     - Error Handling: Try/Except blocks for both generate_report() and send_notification(), logging any failures.

3. **Maintain Audit Trail**
   - Tool: log_operation()
   - Log start and completion of portfolio analysis, risk checks, report generation, and notification sending.
   - Use different log levels (info, warning, error) to indicate the severity of events.

4. **Error Handling Strategy**
   - Wrap each portfolio analysis in a try/except block.
   - Log errors and continue processing other portfolios.
   - Overall script error handling to catch unexpected exceptions.

## Design Justification

### Tool Orchestration Sequence

The orchestration sequence is designed to follow the natural order of analysis.  First, the holdings are fetched.  Then, the stock prices for those holdings are retrieved.  Next, the portfolio value and position details are calculated.  Volatility is calculated using the holdings symbols. Finally, the risk threshold is checked and a report generated and sent if necessary. This linear approach ensures that data dependencies are respected and minimizes the need for complex data transformations or re-processing.

### Data Flow Strategy

Data flows sequentially through the pipeline. The output of `get_portfolio_holdings()` is used as input to `calculate_portfolio_value()` and `calculate_volatility_score()`.  The `get_stock_prices()` tool's output is essential for calculating the portfolio's total value, position-level details, and identifying potential gains/losses. The `check_risk_threshold()` tool relies on the calculated portfolio value and volatility score to determine the overall risk profile.  The risk check results are then fed to `generate_report()` and `send_notification()`.

### Error Handling Strategy Rationale

The primary goal is to ensure that a failure in analyzing one portfolio does not halt the entire process. Therefore, each portfolio's analysis is encapsulated within a `try...except` block. This allows the script to gracefully handle errors such as invalid portfolio IDs or missing stock price data and to continue processing the remaining portfolios. Specific `ValueError` exceptions are caught to handle potential errors from the API tools, and a generic `Exception` block is included to catch unexpected errors.  Log messages are written to the audit trail to provide insights into any errors that occur.  The `finally` block ensures that a completion status is logged even in error cases, providing a comprehensive audit trail.
```