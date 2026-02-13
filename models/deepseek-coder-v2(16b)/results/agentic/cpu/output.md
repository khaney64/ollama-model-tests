 # Execution Plan

## 1. **Initialize Configuration**
- Tools: None
- Set up risk thresholds and portfolio list

## 2. **For Each Portfolio:**

### a. **Fetch Holdings**
- Tool: get_portfolio_holdings()
- Input: portfolio_id
- Output: holdings data (needed for steps b, c, e)

### b. **Get Stock Prices**
- Tool: get_stock_prices()
- Input: symbols extracted from holdings
- Output: current prices (needed for step c)

### c. **Calculate Portfolio Value and Position Details**
- Tool: calculate_portfolio_value()
- Input: holdings, current_prices
- Output: portfolio value data (needed for step d)

### d. **Calculate Volatility Score**
- Tool: calculate_volatility_score()
- Input: symbols from holdings, days=30
- Output: volatility score (needed for step e)

### e. **Check Risk Threshold**
- Tool: check_risk_threshold()
- Input: portfolio_value, volatility_score, risk_config
- Output: risk assessment (needed for step f)

### f. **Generate and Send Report**
- Tool: generate_report()
- Input: portfolio data with risk assessment
- Output: formatted report string (needed for step g)

## 3. **Error Handling Strategy**
- Wrap each portfolio in try/except
- Log errors and continue to next portfolio

# Implementation

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
import logging

def analyze_portfolios():
    risk_config = {
        "max_volatility": 35.0,
        "min_value": 50000,
        "max_value": 2000000
    }
    
    portfolios = ["PORT-001", "PORT-002", "PORT-003"]
    
    for portfolio_id in portfolios:
        try:
            # Step a: Fetch Holdings
            holdings = get_portfolio_holdings(portfolio_id)["holdings"]
            symbols = [holding["symbol"] for holding in holdings]
            
            # Step b: Get Stock Prices
            prices = get_stock_prices(symbols)
            
            # Step c: Calculate Portfolio Value and Position Details
            portfolio_value_data = calculate_portfolio_value(holdings, prices)
            
            # Step d: Calculate Volatility Score
            volatility_score = calculate_volatility_score(symbols)
            
            # Step e: Check Risk Threshold
            risk_assessment = check_risk_threshold(portfolio_value_data["total_value"], volatility_score, risk_config)
            
            # Determine if portfolio is high-risk
            if risk_assessment["is_high_risk"]:
                # Step f: Generate and Send Report
                report_data = {
                    "portfolio_id": portfolio_id,
                    "client_name": get_portfolio_holdings(portfolio_id)["client_name"],
                    "total_value": portfolio_value_data["total_value"],
                    "volatility_score": volatility_score,
                    **risk_assessment,
                    "positions": portfolio_value_data["positions"]
                }
                report = generate_report(report_data)
                
                # Step g: Send Notification
                manager_email = get_portfolio_holdings(portfolio_id)["manager_email"]
                notification_result = send_notification(
                    manager_email,
                    "High Risk Alert: Portfolio Analysis",
                    report,
                    priority="high"
                )
                
                # Log operation
                log_operation(
                    "risk_check",
                    {
                        "portfolio_id": portfolio_id,
                        "risk_level": risk_assessment["risk_level"],
                        "exceeded_thresholds": risk_assessment["exceeded_thresholds"]
                    },
                    level="warning"
                )
                
        except ValueError as e:
            logging.error(f"Error processing portfolio {portfolio_id}: {e}")
        except Exception as e:
            logging.error(f"Unexpected error processing portfolio {portfolio_id}: {e}")

if __name__ == "__main__":
    analyze_portfolios()
```

# Design Justification

## Tool Orchestration Sequence
I chose to process portfolios sequentially rather than in parallel because it simplifies the implementation and ensures that each step is executed only after its dependencies are fulfilled. This approach also makes error handling more straightforward since issues with one portfolio do not affect others.

## Data Flow Strategy
Holdings data feeds into three downstream operations (price fetching, value calculation, volatility scoring) to ensure all necessary information is available when needed. This sequential flow allows for clear and manageable data dependencies within the workflow.

## Error Handling Strategy Rationale
Wrapping each portfolio in a try/except block ensures that errors encountered during any step do not halt the entire script. Instead, errors are logged, and processing continues to the next portfolio. This approach provides resilience against unexpected issues while maintaining operational continuity for all portfolios processed.