"""Mock tool implementations for agentic task evaluation.

These simulated tools represent backend APIs that would be available
to the portfolio risk analysis agent. They return realistic test data
for validation purposes.
"""

import random
from datetime import datetime
from typing import Any


# Mock data for portfolios
PORTFOLIO_DATA = {
    "PORT-001": {
        "portfolio_id": "PORT-001",
        "client_name": "Acme Corporation Pension Fund",
        "manager_email": "sarah.chen@firm.com",
        "holdings": [
            {"symbol": "AAPL", "shares": 500, "purchase_price": 150.00},
            {"symbol": "GOOGL", "shares": 200, "purchase_price": 120.00},
            {"symbol": "MSFT", "shares": 300, "purchase_price": 320.00},
        ]
    },
    "PORT-002": {
        "portfolio_id": "PORT-002",
        "client_name": "Johnson Family Trust",
        "manager_email": "mike.wilson@firm.com",
        "holdings": [
            {"symbol": "AMZN", "shares": 150, "purchase_price": 140.00},
            {"symbol": "META", "shares": 100, "purchase_price": 320.00},
            {"symbol": "AAPL", "shares": 250, "purchase_price": 160.00},
            {"symbol": "TSLA", "shares": 80, "purchase_price": 250.00},
        ]
    },
    "PORT-003": {
        "portfolio_id": "PORT-003",
        "client_name": "Tech Ventures Fund LLC",
        "manager_email": "jennifer.park@firm.com",
        "holdings": [
            {"symbol": "NVDA", "shares": 400, "purchase_price": 450.00},
            {"symbol": "AMD", "shares": 600, "purchase_price": 120.00},
            {"symbol": "GOOGL", "shares": 150, "purchase_price": 135.00},
        ]
    }
}

# Mock stock prices (simulated current market prices)
STOCK_PRICES = {
    "AAPL": 178.50,
    "GOOGL": 142.30,
    "MSFT": 380.25,
    "AMZN": 155.80,
    "META": 485.20,
    "TSLA": 195.50,
    "NVDA": 520.75,
    "AMD": 142.60,
}

# Mock volatility data (symbol -> 30-day volatility percentage)
STOCK_VOLATILITIES = {
    "AAPL": 18.5,
    "GOOGL": 22.3,
    "MSFT": 16.8,
    "AMZN": 28.4,
    "META": 35.2,
    "TSLA": 52.7,
    "NVDA": 38.9,
    "AMD": 41.2,
}


def get_stock_prices(symbols: list[str]) -> dict[str, float]:
    """Fetches current market prices for given stock symbols.

    Args:
        symbols: List of stock ticker symbols

    Returns:
        Dictionary mapping symbols to current prices in USD

    Raises:
        ValueError: If symbols list is empty
    """
    if not symbols:
        raise ValueError("symbols list cannot be empty")

    return {symbol: STOCK_PRICES.get(symbol) for symbol in symbols}


def get_portfolio_holdings(portfolio_id: str) -> dict:
    """Retrieves holdings information for a specific portfolio.

    Args:
        portfolio_id: Portfolio identifier (e.g., "PORT-001")

    Returns:
        Dictionary with portfolio_id, client_name, manager_email, and holdings

    Raises:
        ValueError: If portfolio_id is invalid or not found
    """
    if portfolio_id not in PORTFOLIO_DATA:
        raise ValueError(f"Portfolio {portfolio_id} not found")

    return PORTFOLIO_DATA[portfolio_id].copy()


def calculate_portfolio_value(holdings: list[dict], current_prices: dict[str, float]) -> dict:
    """Calculates total portfolio value and individual position values.

    Args:
        holdings: List of holdings dictionaries with symbol, shares, purchase_price
        current_prices: Dictionary mapping symbols to current prices

    Returns:
        Dictionary with total_value and positions list

    Raises:
        ValueError: If holdings or current_prices are empty
    """
    if not holdings:
        raise ValueError("holdings list cannot be empty")
    if not current_prices:
        raise ValueError("current_prices dictionary cannot be empty")

    positions = []
    total_value = 0.0

    for holding in holdings:
        symbol = holding["symbol"]
        shares = holding["shares"]
        purchase_price = holding["purchase_price"]
        current_price = current_prices.get(symbol)

        # Skip if price not available
        if current_price is None:
            continue

        position_value = shares * current_price
        cost_basis = shares * purchase_price
        gain_loss = position_value - cost_basis
        gain_loss_percent = (gain_loss / cost_basis * 100) if cost_basis > 0 else 0.0

        positions.append({
            "symbol": symbol,
            "shares": shares,
            "current_price": current_price,
            "position_value": position_value,
            "gain_loss": gain_loss,
            "gain_loss_percent": gain_loss_percent
        })

        total_value += position_value

    return {
        "total_value": total_value,
        "positions": positions
    }


def calculate_volatility_score(symbols: list[str], days: int = 30) -> float:
    """Calculates aggregate volatility score for a set of stocks.

    Args:
        symbols: List of stock symbols in the portfolio
        days: Historical period for volatility calculation (default: 30)

    Returns:
        Float representing volatility score (0-100 scale)

    Raises:
        ValueError: If symbols list is empty or days < 1
    """
    if not symbols:
        raise ValueError("symbols list cannot be empty")
    if days < 1:
        raise ValueError("days must be at least 1")

    # Calculate weighted average volatility
    volatilities = [STOCK_VOLATILITIES.get(symbol, 25.0) for symbol in symbols]

    # Aggregate using weighted average (simulated)
    avg_volatility = sum(volatilities) / len(volatilities)

    # Add slight random variation based on period
    period_factor = 1.0 + (days - 30) * 0.002  # Slight adjustment for different periods

    return round(avg_volatility * period_factor, 2)


def check_risk_threshold(portfolio_value: float, volatility_score: float, risk_config: dict) -> dict:
    """Checks if portfolio exceeds configured risk thresholds.

    Args:
        portfolio_value: Total portfolio value in USD
        volatility_score: Volatility score from calculate_volatility_score
        risk_config: Dict with max_volatility, min_value, max_value

    Returns:
        Dictionary with is_high_risk, exceeded_thresholds, and risk_level

    Raises:
        ValueError: If portfolio_value or volatility_score is negative
    """
    if portfolio_value < 0:
        raise ValueError("portfolio_value cannot be negative")
    if volatility_score < 0:
        raise ValueError("volatility_score cannot be negative")

    exceeded_thresholds = []

    # Check volatility
    if volatility_score > risk_config["max_volatility"]:
        exceeded_thresholds.append("volatility")

    # Check value bounds
    if portfolio_value < risk_config["min_value"]:
        exceeded_thresholds.append("min_value")
    if portfolio_value > risk_config["max_value"]:
        exceeded_thresholds.append("max_value")

    # Determine risk level
    if len(exceeded_thresholds) >= 2:
        risk_level = "HIGH"
        is_high_risk = True
    elif len(exceeded_thresholds) == 1:
        risk_level = "MEDIUM"
        is_high_risk = True if "volatility" in exceeded_thresholds else False
    else:
        risk_level = "LOW"
        is_high_risk = False

    return {
        "is_high_risk": is_high_risk,
        "exceeded_thresholds": exceeded_thresholds,
        "risk_level": risk_level
    }


def generate_report(portfolio_data: dict, report_format: str = "markdown") -> str:
    """Generates a formatted risk analysis report.

    Args:
        portfolio_data: Dict with portfolio_id, client_name, total_value,
                       volatility_score, risk_level, exceeded_thresholds, positions
        report_format: Output format ("markdown", "html", or "text")

    Returns:
        Formatted report string

    Raises:
        ValueError: If required fields missing or invalid format
    """
    required_fields = ["portfolio_id", "client_name", "total_value",
                      "volatility_score", "risk_level", "exceeded_thresholds", "positions"]

    for field in required_fields:
        if field not in portfolio_data:
            raise ValueError(f"Missing required field: {field}")

    if report_format not in ["markdown", "html", "text"]:
        raise ValueError(f"Invalid report_format: {report_format}")

    if report_format == "markdown":
        return _generate_markdown_report(portfolio_data)
    elif report_format == "html":
        return _generate_html_report(portfolio_data)
    else:
        return _generate_text_report(portfolio_data)


def _generate_markdown_report(data: dict) -> str:
    """Generates markdown formatted report."""
    report = f"""# Portfolio Risk Analysis Report

## Portfolio Summary
- **Portfolio ID**: {data['portfolio_id']}
- **Client Name**: {data['client_name']}
- **Total Value**: ${data['total_value']:,.2f}
- **Volatility Score**: {data['volatility_score']:.2f}
- **Risk Level**: {data['risk_level']}

## Risk Assessment
"""

    if data['exceeded_thresholds']:
        report += f"**⚠️ ALERT**: The following thresholds have been exceeded:\n"
        for threshold in data['exceeded_thresholds']:
            report += f"- {threshold}\n"
    else:
        report += "✅ All thresholds within acceptable limits.\n"

    report += "\n## Portfolio Positions\n\n"
    report += "| Symbol | Shares | Current Price | Position Value | Gain/Loss | Gain/Loss % |\n"
    report += "|--------|--------|---------------|----------------|-----------|-------------|\n"

    for pos in data['positions']:
        gain_loss_sign = "+" if pos['gain_loss'] >= 0 else ""
        report += f"| {pos['symbol']} | {pos['shares']} | ${pos['current_price']:.2f} | "
        report += f"${pos['position_value']:,.2f} | {gain_loss_sign}${pos['gain_loss']:,.2f} | "
        report += f"{gain_loss_sign}{pos['gain_loss_percent']:.2f}% |\n"

    report += f"\n**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"

    return report


def _generate_html_report(data: dict) -> str:
    """Generates HTML formatted report (simplified)."""
    return f"<html><body><h1>Portfolio Report: {data['portfolio_id']}</h1></body></html>"


def _generate_text_report(data: dict) -> str:
    """Generates plain text report."""
    return f"Portfolio Report for {data['portfolio_id']}\nRisk Level: {data['risk_level']}\n"


def send_notification(recipient: str, subject: str, message: str, priority: str = "normal") -> dict:
    """Sends notification email to portfolio manager.

    Args:
        recipient: Email address
        subject: Email subject line
        message: Email body
        priority: "low", "normal", or "high"

    Returns:
        Dictionary with sent status, message_id, and timestamp

    Raises:
        ValueError: If recipient is invalid or priority is invalid
    """
    if not recipient or "@" not in recipient:
        raise ValueError("Invalid email address")

    if priority not in ["low", "normal", "high"]:
        raise ValueError(f"Invalid priority: {priority}")

    # Simulate sending notification
    message_id = f"msg-{random.randint(10000, 99999)}"
    timestamp = datetime.now().isoformat() + "Z"

    return {
        "sent": True,
        "message_id": message_id,
        "timestamp": timestamp
    }


def log_operation(operation: str, details: dict, level: str = "info") -> None:
    """Logs operations to audit trail.

    Args:
        operation: Operation name
        details: Dictionary with operation-specific details
        level: Log level ("info", "warning", "error")

    Raises:
        ValueError: If level is invalid
    """
    if level not in ["info", "warning", "error"]:
        raise ValueError(f"Invalid log level: {level}")

    # Simulate logging (in real system, would write to logging system)
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] [{level.upper()}] {operation}: {details}"

    # In test mode, we just validate the call succeeded
    # In production, this would write to a logging backend
    pass
