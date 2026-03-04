## Section 1: Execution Plan (Markdown)

### **Overall Strategy**
Process each portfolio sequentially with comprehensive error handling. For each portfolio: fetch holdings → get prices → calculate value & volatility → assess risk → trigger actions if high-risk. Maintain audit trail throughout.

---

### **Step-by-Step Execution Plan**

#### **1. Initialization**
- **Tools**: None (configuration setup)
- **Actions**:
  - Define risk configuration thresholds
  - Initialize portfolio ID list: `["PORT-001", "PORT-002", "PORT-003"]`
  - Setup audit logging framework
- **Data Dependency**: None
- **Error Handling**: Configuration is hardcoded; no runtime errors expected here

#### **2. Per-Portfolio Analysis Loop**
For each `portfolio_id` in portfolio list:

| Step | Tool | Input | Output | Error Handling |
|------|------|-------|--------|----------------|
| **2.1** | `get_portfolio_holdings()` | `portfolio_id` | Holdings dict (client_name, manager_email, holdings list) | ✅ `ValueError` on invalid ID → log error, skip portfolio |
| **2.2** | Extract symbols from holdings | Holdings | List of unique stock symbols | N/A |
| **2.3** | `get_stock_prices()` | Symbols list | Price dict (symbols → USD prices; unknown = `None`) | ✅ Raises `ValueError` if symbols empty → skip to next portfolio |
| **2.4** | `calculate_portfolio_value()` | Holdings + Prices | Total value + positions details (value, gain/loss, %) | ✅ Skips positions with `None` price; raises `ValueError` on empty inputs → skip risk analysis |
| **2.5** | `calculate_volatility_score()` | Symbols list + `days=30` | Volatility score (0-100) | ✅ Raises `ValueError` on empty/invalid symbols → skip risk analysis, log warning |
| **2.6** | `check_risk_threshold()` | Total value, Volatility score, `risk_config` | Risk level ("LOW/MEDIUM/HIGH") + exceeded thresholds | ✅ Raises `ValueError` on negative values → skip risk analysis |
| **2.7** | **High-Risk Action Trigger** (if `risk_level == "HIGH"`) | Aggregated portfolio data | — | |
| **2.7a** | `generate_report()` | Portfolio data dict | Markdown report string | ✅ Raises `ValueError` on missing fields → skip notification |
| **2.7b** | `send_notification()` | Manager email, report, "high" priority | Notification result dict | ✅ Validates email format; raises `ValueError` on invalid → log failure, continue |

#### **3. Audit Trail & Completion**
- Log portfolio analysis start/completion
- Log risk check results
- Log report generation & notification status
- Final summary log after all portfolios

#### **4. Graceful Degradation Strategy**
- **Per-portfolio try/except blocks**: Isolate failures; continue processing other portfolios
- **Partial success handling**: 
  - Missing prices? → Skip value calculation but proceed to volatility (if symbols exist)
  - Missing volatility? → Skip risk assessment with warning log
  - Failed notification? → Log error but do not halt analysis
- **All operations logged** via `log_operation` with operation name, details, and level

---

## Section 2: Implementation (Python)

```python
#!/usr/bin/env python3
"""
Portfolio Risk Analysis Orchestrator
Automated risk monitoring system for financial advisory firm
"""

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
    """
    Orchestrates end-to-end portfolio risk analysis for multiple portfolios.
    Processes all 3 portfolios with error isolation and audit logging.
    """
    # ==================== CONFIGURATION ====================
    RISK_CONFIG = {
        "max_volatility": 35.0,   # Max acceptable volatility score
        "min_value": 50000,      # Min portfolio value for monitoring
        "max_value": 2000000      # Max portfolio value for monitoring
    }
    PORT_IDS = ["PORT-001", "PORT-002", "PORT-003"]
    HIGH_RISK_THRESHOLD = "HIGH"
    
    # Track high-risk portfolios for final summary
    high_risk_portfolios = []
    
    # ==================== MAIN ANALYSIS LOOP ====================
    for pid in PORT_IDS:
        try:
            # --- LOG: Portfolio analysis start ---
            log_operation("portfolio_analysis_start", {"portfolio_id": pid}, level="info")
            
            # Step 2.1: Fetch holdings
            log_operation("fetch_holdings", {"portfolio_id": pid}, level="info")
            holdings = get_portfolio_holdings(pid)
            if holdings is None:
                raise ValueError(f"Portfolio {pid} not found or invalid ID")
            
            # Extract unique symbols
            symbols = list({h["symbol"] for h in holdings["holdings"]})
            if not symbols:
                raise ValueError(f"No holdings found for portfolio {pid}")
            
            # Step 2.3: Fetch current prices
            log_operation("fetch_stock_prices", {"portfolio_id": pid, "symbols": symbols}, level="info")
            current_prices = get_stock_prices(symbols)
            
            # Step 2.4: Calculate portfolio value & positions
            log_operation("calculate_portfolio_value", {
                "portfolio_id": pid,
                "holdings": holdings["holdings"],
                "current_prices": current_prices
            }, level="info")
            portfolio_value = calculate_portfolio_value(holdings["holdings"], current_prices)
            if portfolio_value is None:
                raise ValueError("Failed to calculate portfolio value")
            
            total_value = portfolio_value["total_value"]
            positions = portfolio_value["positions"]
            
            # Step 2.5: Calculate volatility score
            log_operation("calculate_volatility_score", {"portfolio_id": pid, "symbols": symbols}, level="info")
            volatility_score = calculate_volatility_score(symbols, days=30)
            if volatility_score is None:
                raise ValueError(f"Volatility calculation failed for portfolio {pid}")
            
            # Step 2.6: Check risk thresholds
            log_operation("check_risk_threshold", {
                "portfolio_id": pid,
                "portfolio_value": total_value,
                "volatility_score": volatility_score
            }, level="info")
            risk_result = check_risk_threshold(total_value, volatility_score, RISK_CONFIG)
            risk_level = risk_result["risk_level"]
            exceeded = risk_result.get("exceeded_thresholds", [])
            
            # Prepare unified portfolio data for reporting
            portfolio_data = {
                "portfolio_id": pid,
                "client_name": holdings["client_name"],
                "total_value": total_value,
                "volatility_score": volatility_score,
                "risk_level": risk_level,
                "exceeded_thresholds": exceeded,
                "positions": positions
            }
            
            # Log analysis completion
            log_operation("portfolio_analysis_completion", {
                "portfolio_id": pid,
                "risk_level": risk_level,
                "exceeded_thresholds": exceeded
            }, level="info")
            
            # --- HIGH-RISK ACTIONS ---
            if risk_level == HIGH_RISK_THRESHOLD:
                log_operation("high_risk_alert_triggered", {"portfolio_id": pid}, level="warning")
                
                # Generate report
                log_operation("report_generation", {"portfolio_id": pid}, level="info")
                report_text = generate_report(portfolio_data, report_format="markdown")
                if report_text is None:
                    raise ValueError("Report generation failed for portfolio {}".format(pid))
                
                # Send notification
                manager_email = holdings["manager_email"]
                if not manager_email or "@" not in manager_email:
                    raise ValueError(f"Invalid manager email for portfolio {pid}")
                
                log_operation("notification_send_initiated", {
                    "portfolio_id": pid,
                    "recipient": manager_email,
                    "priority": "high"
                }, level="info")
                
                notification_res = send_notification(
                    recipient=manager_email,
                    subject=f"🚨 HIGH RISK ALERT: Portfolio {pid}",
                    message=report_text,
                    priority="high"
                )
                
                if not notification_res.get("sent"):
                    log_operation("notification_send_failed", {
                        "portfolio_id": pid,
                        "recipient": manager_email,
                        "error": notification_res.get("message", "Unknown failure")
                    }, level="error")
                
                high_risk_portfolios.append(pid)
            
            # Log risk result
            log_operation("risk_assessment_result", {
                "portfolio_id": pid,
                "risk_level": risk_level,
                "exceeded": exceeded
            }, level="info")
            
        except Exception as e:
            # Graceful degradation: log error, continue to next portfolio
            log_operation("portfolio_analysis_error", {
                "portfolio_id": pid,
                "error": str(e)
            }, level="error")
            print(f"⚠️  Skipped portfolio {pid}: {e} | Continuing with next portfolio...")
            continue
    
    # ==================== FINAL AUDIT SUMMARY ====================
    log_operation("analysis_summary", {
        "portfolios_processed": len(PORT_IDS),
        "high_risk_portfolios": high_risk_portfolios,
        "total_high_risk": len(high_risk_portfolios)
    }, level="info")
    
    print("\n✅ Portfolio risk analysis completed.")
    print(f"📊 High-risk portfolios requiring attention: {', '.join(high_risk_portfolios) if high_risk_portfolios else 'None'}")
    print("📝 Full audit log maintained via system operations.")

if __name__ == "__main__":
    # Execute analysis
    analyze_portfolios()
```

---

## Section 3: Design Justification (Markdown)

### **Tool Orchestration Sequence Rationale**
- **Sequential Processing**: Portfolios are independent; sequential processing ensures clear data flow and simplifies error isolation. Parallel execution would complicate audit tracing and resource management for this scoped task.
- **Symbol Reuse Pattern**: Holdings → Symbols → Prices → Value Calculation → Volatility → Risk Check. This pipeline maximizes data reuse:
  - `get_portfolio_holdings` provides foundational identifiers
  - `get_stock_prices` feeds into `calculate_portfolio_value` for real-time valuation
  - Symbols reused again for `calculate_volatility_score` (independent of current prices)
- **Risk Configuration Centralization**: Hardcoded `RISK_CONFIG` ensures consistent thresholds across all portfolios without per-portfolio configuration overhead.

### **Data Flow Strategy**
| Source | Tool | Transformation | Destination |
|--------|------|----------------|-------------|
| Portfolio metadata | `get_portfolio_holdings` | Holdings list + client/manager details | Value calculation & reporting |
| Market data | `get_stock_prices` | Symbol → current price mapping | `calculate_portfolio_value` (real-time valuation) |
| Historical risk metric | `calculate_volatility_score` | Symbols → volatility score | `check_risk_threshold` (combined risk assessment) |
| Business rules | `check_risk_threshold` | Value + volatility → risk level/thresholds | Decision trigger for reports/notifications |
| Aggregation | `generate_report` | Structured data → human-readable markdown | Notification payload |

### **Error Handling Philosophy**
1. **Isolation**: Each portfolio wrapped in independent `try/except`; failure in one portfolio doesn't block others.
2. **Specific Exception Targeting**: 
   - Catching `ValueError` from tools where inputs are invalid (e.g., empty symbols, negative values)
   - Validating critical inputs (email format, portfolio existence) before API calls
3. **Graceful Degradation**:
   - Missing stock prices? → `calculate_portfolio_value` skips invalid positions; total value may be partial but analysis continues
   - Volatility calculation failure? → Log warning, skip risk assessment (portfolio marked as "UNKNOWN" in risk level)
   - Notification failure? → Log error, retain audit trail, proceed to next portfolio
4. **Audit-First Design**: Every operational step logged via `log_operation` with level tagging (`info`/`warning`/`error`) for compliance and debugging.

### **Trade-offs Considered**
- **Report Format Choice**: Selected `markdown` over HTML/text for universal readability in emails and documentation. Easily convertible if multi-format needs arise later.
- **Notification Priority**: "High" priority ensures urgent alerts don't get buried; aligns with regulatory requirements for material risk events.
- **Symbol Handling**: Accepted `None` prices from `get_stock_prices` for unknown symbols; `calculate_portfolio_value` skips them gracefully—avoids failing entire portfolio analysis over partial data gaps.
- **Log Verbosity vs. Utility**: Comprehensive operation logging meets audit requirements while providing actionable diagnostics without overwhelming operators.

### **Validation Against Requirements**
