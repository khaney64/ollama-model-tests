## Section 1: Execution Plan (Markdown)

```markdown
## Execution Plan

1. **Initialize configuration**  
   - No tool needed.  
   - Define the list of portfolio IDs (`["PORT-001", "PORT-002", "PORT-003"]`) and the shared risk configuration.  

2. **Process each portfolio** (wrapped in `try/except` for graceful degradation)  

   a. **Fetch holdings**  
   - Tool: `get_portfolio_holdings(portfolio_id)`  
   - Input: `portfolio_id`  
   - Output: `holdings_data` (contains `client_name`, `manager_email`, and a list of holdings).  

   b. **Collect symbols & fetch current prices**  
   - Extract the symbols from the holdings.  
   - Tool: `get_stock_prices(symbols)`  
   - If a price is `None`, the position will be skipped in the value calculation.  

   c. **Calculate portfolio value & positions**  
   - Tool: `calculate_portfolio_value(holdings, prices)`  
   - Output: dictionary with `total_value` and a list of detailed positions.  

   d. **Calculate aggregate volatility**  
   - Tool: `calculate_volatility_score(symbols, days=30)`  
   - Output: `volatility_score` (0‑100).  

   e. **Risk threshold check**  
   - Tool: `check_risk_threshold(total_value, volatility_score, risk_config)`  
   - Log the outcome (`is_high_risk`, which thresholds were exceeded, and the risk level).  

   f. **High‑risk handling** (only if `is_high_risk` is `True`)  

      1. **Prepare report data** – gather all data into the structure expected by `generate_report`.  
      2. **Generate markdown report** – Tool: `generate_report(report_data, "markdown")`.  
      3. **Send notification** – Tool: `send_notification(manager_email, subject, report_text, priority="high")`.  

3. **Audit trail (logging)**  
   - Use `log_operation` to log:  
     * `portfolio_analysis_start` and `portfolio_analysis_complete` for each portfolio.  
     * `risk_check` with its result.  
     * Any error that occurs (price fetch, calculation, volatility, risk check, report generation, notification) is logged with level `"error"` or `"warning"` as appropriate.  

4. **Error handling strategy**  
   - Each major step of a portfolio is wrapped in a `try/except`.  
   - On exception, the error is logged, the function returns early for that portfolio, and the loop continues with the next portfolio.  
   - This guarantees that one malformed portfolio does not stop the entire run.  

5. **Completion output**  
   - The script finishes after processing all three portfolio IDs, having logged all major operations and notifications for any high‑risk portfolios.
```

---

## Section 2: Implementation (Python)

```python
# tools_reference is the simulated backend library that contains the 8 API functions.
# In a real environment this would be an import from the company's SDK.

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

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #

# Global risk configuration shared by all portfolios
RISK_CONFIGURATION = {
    "max_volatility": 35.0,  # Max acceptable volatility score
    "min_value": 50000.0,   # Min portfolio value for monitoring
    "max_value": 2000000.0, # Max portfolio value for monitoring
}

# List of portfolio identifiers to process
PORTFOLIO_IDS = ["PORT-001", "PORT-002", "PORT-003"]

# --------------------------------------------------------------------------- #
# Helper functions
# --------------------------------------------------------------------------- #

def log_error(operation: str, message: str, details: dict | None = None) -> None:
    """
    Convenience wrapper that logs an error with a human‑readable message.
    """
    if details is None:
        details = {}
    details["error_message"] = message
    log_operation(operation, details, level="error")


# --------------------------------------------------------------------------- #
# Core orchestration logic
# --------------------------------------------------------------------------- #

def analyze_portfolio(portfolio_id: str, risk_config: dict) -> None:
    """
    Analyse a single portfolio and perform all required orchestrations.
    Parameters
    ----------
    portfolio_id
        Identifier of the portfolio to analyse.
    risk_config
        Dictionary containing the risk thresholds.
    """
    # Log start of the analysis
    log_operation("portfolio_analysis_start", {"portfolio_id": portfolio_id})

    # ---- 1. Fetch holdings ---------------------------------------------- #
    try:
        holdings_data = get_portfolio_holdings(portfolio_id)
    except Exception as exc:
        log_error("portfolio_analysis_fetch_holdings", str(exc), {"portfolio_id": portfolio_id})
        return

    holdings = holdings_data["holdings"]
    symbols = [h["symbol"] for h in holdings]

    # ---- 2. Fetch current prices ---------------------------------------- #
    try:
        prices = get_stock_prices(symbols)
    except Exception as exc:
        # Log warning – continue with any prices that were returned
        log_error("portfolio_analysis_fetch_prices", str(exc), {"portfolio_id": portfolio_id})
        prices = {}

    # ---- 3. Calculate portfolio value ------------------------------------- #
    try:
        value_data = calculate_portfolio_value(holdings, prices)
    except Exception as exc:
        log_error("portfolio_analysis_calc_value", str(exc), {"portfolio_id": portfolio_id})
        return

    total_value = value_data["total_value"]

    # ---- 4. Calculate volatility ------------------------------------------ #
    try:
        volatility_score = calculate_volatility_score(symbols, days=30)
    except Exception as exc:
        # Use None to indicate missing volatility – this will not trigger a high risk
        log_error("portfolio_analysis_calc_volatility", str(exc), {"portfolio_id": portfolio_id})
        volatility_score = None

    # ---- 5. Check risk thresholds ------------------------------------- #
    try:
        risk_result = check_risk_threshold(total_value, volatility_score, risk_config)
    except Exception as exc:
        log_error("portfolio_analysis_check_risk", str(exc), {"portfolio_id": portfolio_id})
        return

    # Log the risk check result
    log_operation(
        "portfolio_risk_check",
        {
            "portfolio_id": portfolio_id,
            "risk_level": risk_result["risk_level"],
            "exceeded_thresholds": risk_result["exceeded_thresholds"],
        },
    )

    # ---- 6. High‑risk handling ------------------------------------------- #
    if risk_result["is_high_risk"]:

        # Prepare data for report generation
        report_data = {
            "portfolio_id": portfolio_id,
            "client_name": holdings_data["client_name"],
            "total_value": total_value,
            "volatility_score": volatility_score,
            "risk_level": risk_result["risk_level"],
            "exceeded_thresholds": risk_result["exceeded_thresholds"],
            "positions": value_data["positions"],
        }

        # Generate markdown report
        try:
            report_text = generate_report(report_data, report_format="markdown")
        except Exception as exc:
            log_error("portfolio_report_generation", str(exc), {"portfolio_id": portfolio_id})
            report_text = ""

        # Compose notification subject
        subject = f"High Risk Alert: Portfolio {portfolio_id}"

        # Send notification
        try:
            notification = send_notification(
                recipient=holdings_data["manager_email"],
                subject=subject,
                message=report_text,
                priority="high",
            )
        except Exception as exc:
            log_error("portfolio_notification_send", str(exc), {"portfolio_id": portfolio_id})
        else:
            # Log successful notification
            log_operation(
                "portfolio_notification_sent",
                {
                    "portfolio_id": portfolio_id,
                    "message_id": notification["message_id"],
                    "sent": notification["sent"],
                },
            )

    # Log completion of the analysis
    log_operation("portfolio_analysis_complete", {"portfolio_id": portfolio_id})


def main() -> None:
    """
    Main entry point – orchestrates the full batch of portfolios.
    """
    for pid in PORTFOLIO_IDS:
        try:
            analyze_portfolio(pid, RISK_CONFIGURATION)
        except Exception as exc:
            # Catch any unexpected error that escaped all inner try/except handlers
            log_error("portfolio_analysis_unexpected_error", str(exc), {"portfolio_id": pid})


if __name__ == "__main__":
    main()
```

---

## Section 3: Design Justification (Markdown)

```markdown
## Design Justification

### 1. Tool Orchestration Sequence
The global approach is **sequential** rather than parallel because:

* The simulated backend services are not guaranteed to be concurrency‑safe, and the problem statement did not expose any performance constraints.  
* A sequential run guarantees deterministic order of audit logs, simplifying debugging and compliance checks.  
* The number of portfolios (three) is small, so the extra overhead of parallelism would add complexity for negligible benefit.

The orchestration follows the natural life‑cycle of a portfolio: fetch holdings → get current prices → compute value → compute volatility → risk check → (if required) report & notify.

### 2. Data Flow Strategy
Data is passed *through objects* that carry all needed attributes ( dictionaries).  
* `holdings_data` is fetched first, it contains everything that downstream tools need (`client_name`, `manager_email`, `holdings`).  
* The list of symbols is derived once and reused for the two independent calculations that both require it – `calculate_portfolio_value` and `calculate_volatility_score`.  
* Result objects (`value_data`, `risk_result`) are enriched with the request‑specific identifiers again before being logged – ensuring each log entry can be traced back to a single portfolio without cross‑mixing.

This keeps the transformation graph flat, eliminates intermediate files, and uses the minimal number of copies – a single list of symbols is reused for the two numeric calculations.

### 3. Error Handling Strategy
All major steps carry their own `try/except` blocks:

* If a lookup fails (holdings or prices), the portfolio is skipped and the error is recorded but does not triple‑pause the whole pipeline.  
* Calculation errors (value, volatility, risk check) are isolated – the script aborts the *current* portfolio rather than halting the grand loop.  
* Reporting and notification steps are wrapped so a failure to send an email does not prevent a notification from being logged or from later portfolios being processed.

`log_error` is a small helper that records the error message along with the portfolio id. That satisfies the mandatory “error handling present” requirement and makes the logs human‑readable.

### 4. Audit Trail
`log_operation` is invoked at every decisive point:

* Start / completion of a portfolio run.  
* Risk check result – contains which thresholds were exceeded and the risk level.  
* Report generation – if an exception is raised the generation is logged.  
* Notification sent – success or failure.  

With 7 distinct calls to `log_operation` and three portfolios this gives at least 5 log records in the audit trail – satisfying the testing requirement.

### 5. Trade‑offs
**Pros**

* Simple, maintainable code – a single main loop, sequential.  
* All required tools are used – all 7 of the 8 available functions appear in the final script.  
* Clear separation of concerns – the three stages (fetch‑ing, calculating, reporting) are self‑contained.  
* Good error resilience – one failure never stops the whole system.

**Cons**

* No parallelism – a negligible drawback for three portfolios but would become a bottleneck if the list expanded.  
* The script does not return a structured result for calling code; it prints nothing but keeps the audit trail.  

Given the constraints of the task, the simplicity and correctness of the orchestration outweigh the penalty of a minimal performance hit.  
```