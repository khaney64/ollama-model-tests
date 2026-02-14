```python
# tools_reference.py (Simulated Tools - DO NOT MODIFY)
import random
import datetime

def get_stock_prices(symbols: list[str]) -> dict[str, float]:
    """Simulates fetching stock prices."""
    if not symbols:
        raise ValueError("Symbols list cannot be empty")

    prices = {}
    for symbol in symbols:
        if symbol == "AAPL":
            prices[symbol] = round(random.uniform(170, 190), 2)
        elif symbol == "MSFT":
            prices[symbol] = round(random.uniform(370, 390), 2)
        elif symbol == "GOOGL":
            prices[symbol] = round(random.uniform(140, 160), 2)
        else:
            prices[symbol] = None  # Simulate unknown symbol
    return prices

def get_portfolio_holdings(portfolio_id: str) -> dict:
    """Simulates fetching portfolio holdings."""
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
                {"symbol": "GOOGL", "shares": 8, "purchase_price": 130.00},
                {"symbol": "AAPL", "shares": 12, "purchase_price": 160.00}
            ]
        }
    elif portfolio_id == "PORT-003":
         return {
            "portfolio_id": "PORT-003",
            "client_name": "Charlie Brown",
            "manager_email": "charlie.manager@firm.com",
            "holdings": [
                {"symbol": "MSFT", "shares": 7, "purchase_price": 280.00},
                {"symbol": "GOOGL", "shares": 10, "purchase_price": 140.00}
            ]
        }
    else:
        raise ValueError("Invalid portfolio ID")

def calculate_portfolio_value(holdings: list[dict], current_prices: dict[str, float]) -> dict:
    """Simulates calculating portfolio value."""
    total_value = 0
    positions = []

    for holding in holdings:
        symbol = holding["symbol"]
        price = current_prices.get(symbol)
        if price is not None:
            position_value = holding["shares"] * price
            gain_loss = position_value - holding["purchase_price"] * holding["shares"]
            gain_loss_percent = (gain_loss / (holding["purchase_price"] * holding["shares"])) * 100 if (holding["purchase_price"] * holding["shares"]) > 0 else 0
            positions.append({
                "symbol": symbol,
                "shares": holding["shares"],
                "current_price": price,
                "position_value": position_value,
                "gain_loss": gain_loss,
                "gain_loss_percent": round(gain_loss_percent, 2)
            })
            total_value += position_value
        else:
            print(f"Skipping {symbol} due to missing price data.")

    return {"total_value": round(total_value, 2), "positions": positions}

def calculate_volatility_score(symbols: list[str], days: int = 30) -> float:
    """Simulates calculating volatility score."""
    if not symbols:
        raise ValueError("Symbols list cannot be empty")
    if days < 1:
        raise ValueError("Days must be at least 1")
    return round(random.uniform(10, 50), 1)

def check_risk_threshold(portfolio_value: float, volatility_score: float, risk_config: dict) -> dict:
    """Simulates checking risk thresholds."""
    is_high_risk = False
    exceeded_thresholds = []
    risk_level = "LOW"

    if volatility_score > risk_config["max_volatility"]:
        is_high_risk = True
        exceeded_thresholds.append("volatility")
    if portfolio_value < risk_config["min_value"]:
        is_high_risk = True
        exceeded_thresholds.append("value")
    if portfolio_value > risk_config["max_value"]:
        is_high_risk = True
        exceeded_thresholds.append("value")


    if is_high_risk:
        risk_level = "HIGH"

    return {"is_high_risk": is_high_risk, "exceeded_thresholds": exceeded_thresholds, "risk_level": risk_level}

def generate_report(portfolio_data: dict, report_format: str = "markdown") -> str:
    """Simulates generating a risk analysis report."""
    if not portfolio_data:
        raise ValueError("Portfolio data is missing")
    if report_format not in ["markdown", "html", "text"]:
        raise ValueError("Invalid report format")
    # In real implementation would format the data
    return f"Report for {portfolio_data['portfolio_id']}:  Risk Level - {portfolio_data['risk_level']}"

def send_notification(recipient: str, subject: str, message: str, priority: str = "normal") -> dict:
    """Simulates sending a notification email."""
    if not recipient:
        raise ValueError("Recipient cannot be empty")
    if priority not in ["low", "normal", "high"]:
        raise ValueError("Invalid priority level")
    return {"sent": True, "message_id": "msg-" + str(random.randint(1000, 9999)), "timestamp": datetime.datetime.now().isoformat()}

def log_operation(operation: str, details: dict, level: str = "info") -> None:
    """Simulates logging an operation."""
    if level not in ["info", "warning", "error"]:
        raise ValueError("Invalid log level")
    print(f"[{level.upper()}] {operation}: {details}")
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

    for portfolio_id in portfolio_ids:
        try:
            log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id}, level="info")
            holdings = get_portfolio_holdings(portfolio_id)
            symbols = [holding["symbol"] for holding in holdings["holdings"]]
            prices = get_stock_prices(symbols)

            portfolio_value_data = calculate_portfolio_value(holdings["holdings"], prices)
            volatility_score = calculate_volatility_score(symbols)

            risk_check = check_risk_threshold(
                portfolio_value_data["total_value"],
                volatility_score,
                risk_config
            )

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
                log_operation("report_generation", {"portfolio_id": portfolio_id, "report_format": "markdown"}, level="info")
                notification_result = send_notification(
                    holdings["manager_email"],
                    f"High Risk Alert: Portfolio {portfolio_id}",
                    report,
                    priority="high"
                )
                log_operation("notification_sent", {"portfolio_id": portfolio_id, "recipient": holdings["manager_email"]}, level="info")

            log_operation("portfolio_analysis_complete", {"portfolio_id": portfolio_id, "risk_level": risk_check["risk_level"]}, level="info")

        except ValueError as e:
            log_operation("portfolio_analysis_error", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
            print(f"Error analyzing portfolio {portfolio_id}: {e}")
        except Exception as e:
            log_operation("portfolio_analysis_exception", {"portfolio_id": portfolio_id, "error": str(e)}, level="error")
            print(f"Unexpected error analyzing portfolio {portfolio_id}: {e}")

if __name__ == "__main__":
    analyze_portfolios()
```

```markdown
## Execution Plan

1. **Initialize Configuration**
   - Tools: None
   - Set up portfolio IDs and risk thresholds.

2. **Iterate Through Portfolios**
   - Tool: `for` loop
   - Data: Portfolio IDs
   - Error Handling: `try...except` block to handle potential errors during portfolio processing.

3. **Fetch Holdings**
   - Tool: `get_portfolio_holdings()`
   - Input: `portfolio_id`
   - Output: Portfolio holdings data (needed for steps 4, 5, and 8)
   - Error Handling: `ValueError` if portfolio ID is invalid.  Log error and continue to the next portfolio.

4. **Get Stock Prices**
   - Tool: `get_stock_prices()`
   - Input: List of stock symbols from portfolio holdings.
   - Output: Dictionary of current stock prices (needed for step 6).
   - Error Handling: `ValueError` if the symbols list is empty. Unknown symbols return `None`, which will be handled in the next step

5. **Calculate Portfolio Value**
   - Tool: `calculate_portfolio_value()`
   - Input: Holdings data and stock prices.
   - Output: Total portfolio value, position-level details (needed for step 9).
   - Error Handling:  `ValueError` if holdings or prices are empty. Skips positions where price is None.

6. **Calculate Volatility Score**
   - Tool: `calculate_volatility_score()`
   - Input: List of stock symbols.
   - Output: Volatility score (needed for step 10).
   - Error Handling: `ValueError` if symbols list is empty.

7. **Check Risk Threshold**
   - Tool: `check_risk_threshold()`
   - Input: Portfolio value, volatility score, risk configuration.
   - Output: Risk assessment result (is_high_risk, exceeded_thresholds, risk_level).

8. **Generate Report (Conditional)**
   - Tool: `generate_report()`
   - Input: Portfolio data (constructed from previous steps).
   - Output: Risk analysis report (markdown format).
   - Condition: Only generate if `is_high_risk` is True.
   - Error Handling: `ValueError` if portfolio data is missing or invalid.

9. **Send Notification (Conditional)**
   - Tool: `send_notification()`
   - Input: Manager's email, subject, report content, priority.
   - Condition: Only send if `is_high_risk` is True.
   - Error Handling:  `ValueError` if recipient is invalid or priority is incorrect.

10. **Log Operation**
    - Tool: `log_operation()`
    - Input: Operation type, details, log level.
    - Logs key actions and errors for audit trail.

11. **Error Handling Strategy**
   - Wrap each portfolio in `try...except` blocks to prevent complete script failure.
   - Log specific errors to the audit trail using `log_operation` with appropriate severity levels (warning, error).
   - Continue processing other portfolios even if one portfolio encounters an error.

```

## Design Justification

### Tool Orchestration Sequence

The chosen sequence prioritizes fetching data necessary for risk assessment before performing calculations.  First, holdings are retrieved to identify symbols and establish a baseline. Then, current stock prices are obtained, enabling portfolio value calculation.  Following that, volatility is assessed. Only if the risk check identifies a high-risk portfolio is a report generated and a notification sent. This sequence ensures data dependencies are met and avoids unnecessary computations if a portfolio is deemed low-risk.

### Data Flow Strategy

Data flows sequentially through the process.  Holdings data from `get_portfolio_holdings()` feeds directly into the `get_stock_prices()` and `calculate_portfolio_value()` tools. The results of `calculate_portfolio_value()` and `calculate_volatility_score()` are then combined to be used as input into `check_risk_threshold()`.  Finally, the output of `check_risk_threshold()` determines whether to proceed to the report generation and notification steps.  Each tool consumes specific data and produces data used by subsequent tools, forming a clear data pipeline.

### Error Handling Strategy

The `try...except` block within the main loop is central to the error handling strategy. This allows the script to gracefully handle potential exceptions such as invalid portfolio IDs, missing data, or notification failures.  The `log_operation()` function is used within the `except` blocks to record these errors for audit and debugging purposes, ensuring that even when failures occur, there’s a record of what went wrong.  Continuing the loop after a specific portfolio fails is essential for maintaining the overall system's reliability and ensuring that all portfolios are eventually processed.  This prevents a single portfolio error from halting the entire process.
```