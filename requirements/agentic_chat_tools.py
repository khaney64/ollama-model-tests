"""OpenAI-compatible tool schemas and dispatch for the agentic-chat benchmark.

Defines TOOL_DEFINITIONS (JSON schemas for /api/chat) and TOOL_DISPATCH
(mapping tool names to the actual functions in tools_reference.py).
"""

import json
import os
import sys

# Ensure tools_reference is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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


# OpenAI-compatible tool definitions for Ollama /api/chat
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_prices",
            "description": "Fetches current market prices for given stock symbols.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbols": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of stock ticker symbols (e.g. [\"AAPL\", \"GOOGL\"])"
                    }
                },
                "required": ["symbols"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_portfolio_holdings",
            "description": "Retrieves holdings information for a specific portfolio.",
            "parameters": {
                "type": "object",
                "properties": {
                    "portfolio_id": {
                        "type": "string",
                        "description": "Portfolio identifier (e.g. \"PORT-001\")"
                    }
                },
                "required": ["portfolio_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_portfolio_value",
            "description": "Calculates total portfolio value and individual position values.",
            "parameters": {
                "type": "object",
                "properties": {
                    "holdings": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "symbol": {"type": "string"},
                                "shares": {"type": "integer"},
                                "purchase_price": {"type": "number"}
                            }
                        },
                        "description": "List of holdings with symbol, shares, purchase_price"
                    },
                    "current_prices": {
                        "type": "object",
                        "additionalProperties": {"type": "number"},
                        "description": "Dictionary mapping symbols to current prices in USD"
                    }
                },
                "required": ["holdings", "current_prices"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_volatility_score",
            "description": "Calculates aggregate volatility score for a set of stocks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbols": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "List of stock symbols in the portfolio"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Historical period for volatility calculation (default: 30)"
                    }
                },
                "required": ["symbols"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_risk_threshold",
            "description": "Checks if portfolio exceeds configured risk thresholds.",
            "parameters": {
                "type": "object",
                "properties": {
                    "portfolio_value": {
                        "type": "number",
                        "description": "Total portfolio value in USD"
                    },
                    "volatility_score": {
                        "type": "number",
                        "description": "Volatility score from calculate_volatility_score"
                    },
                    "risk_config": {
                        "type": "object",
                        "properties": {
                            "max_volatility": {"type": "number"},
                            "min_value": {"type": "number"},
                            "max_value": {"type": "number"}
                        },
                        "description": "Risk configuration with max_volatility, min_value, max_value"
                    }
                },
                "required": ["portfolio_value", "volatility_score", "risk_config"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_report",
            "description": "Generates a formatted risk analysis report.",
            "parameters": {
                "type": "object",
                "properties": {
                    "portfolio_data": {
                        "type": "object",
                        "description": "Dict with portfolio_id, client_name, total_value, volatility_score, risk_level, exceeded_thresholds, positions"
                    },
                    "report_format": {
                        "type": "string",
                        "enum": ["markdown", "html", "text"],
                        "description": "Output format (default: markdown)"
                    }
                },
                "required": ["portfolio_data"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_notification",
            "description": "Sends notification email to portfolio manager.",
            "parameters": {
                "type": "object",
                "properties": {
                    "recipient": {
                        "type": "string",
                        "description": "Email address"
                    },
                    "subject": {
                        "type": "string",
                        "description": "Email subject line"
                    },
                    "message": {
                        "type": "string",
                        "description": "Email body"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["low", "normal", "high"],
                        "description": "Notification priority (default: normal)"
                    }
                },
                "required": ["recipient", "subject", "message"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "log_operation",
            "description": "Logs operations to audit trail.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "description": "Operation name (e.g. \"portfolio_analysis\", \"risk_check\")"
                    },
                    "details": {
                        "type": "object",
                        "description": "Dictionary with operation-specific details"
                    },
                    "level": {
                        "type": "string",
                        "enum": ["info", "warning", "error"],
                        "description": "Log level (default: info)"
                    }
                },
                "required": ["operation", "details"]
            }
        }
    },
]

# Map tool names to actual functions
TOOL_DISPATCH = {
    "get_stock_prices": get_stock_prices,
    "get_portfolio_holdings": get_portfolio_holdings,
    "calculate_portfolio_value": calculate_portfolio_value,
    "calculate_volatility_score": calculate_volatility_score,
    "check_risk_threshold": check_risk_threshold,
    "generate_report": generate_report,
    "send_notification": send_notification,
    "log_operation": log_operation,
}


def dispatch_tool_call(name: str, arguments: dict | str) -> dict | str:
    """Execute a tool call, with light type coercion and error wrapping.

    Args:
        name: Tool function name.
        arguments: Either a dict of kwargs or a JSON string to parse.

    Returns:
        The tool's return value (dict, str, float, or None for log_operation),
        or {"error": "..."} on failure.
    """
    if name not in TOOL_DISPATCH:
        return {"error": f"Unknown tool: {name}"}

    # Parse JSON string arguments if needed
    if isinstance(arguments, str):
        try:
            arguments = json.loads(arguments)
        except json.JSONDecodeError as e:
            return {"error": f"Invalid JSON arguments: {e}"}

    if not isinstance(arguments, dict):
        return {"error": f"Arguments must be a dict, got {type(arguments).__name__}"}

    # Light type coercion for common model mistakes
    arguments = _coerce_arguments(name, arguments)

    fn = TOOL_DISPATCH[name]
    try:
        result = fn(**arguments)
        # log_operation returns None
        if result is None:
            return {"status": "ok"}
        return result
    except (ValueError, TypeError, KeyError) as e:
        return {"error": str(e)}


def _coerce_arguments(name: str, args: dict) -> dict:
    """Light type coercion for common model mistakes.

    - String numbers -> int/float where expected
    - Single string -> list where a list is expected
    - String "true"/"false" -> bool
    """
    args = dict(args)  # shallow copy

    # Coerce 'symbols' fields: single string -> list
    if "symbols" in args and isinstance(args["symbols"], str):
        args["symbols"] = [args["symbols"]]

    # Coerce 'days' to int
    if "days" in args:
        try:
            args["days"] = int(args["days"])
        except (ValueError, TypeError):
            pass

    # Coerce numeric fields
    for field in ("portfolio_value", "volatility_score"):
        if field in args:
            try:
                args[field] = float(args[field])
            except (ValueError, TypeError):
                pass

    # Coerce risk_config values
    if "risk_config" in args and isinstance(args["risk_config"], dict):
        rc = dict(args["risk_config"])
        for key in ("max_volatility", "min_value", "max_value"):
            if key in rc:
                try:
                    rc[key] = float(rc[key])
                except (ValueError, TypeError):
                    pass
        args["risk_config"] = rc

    # Coerce holdings: if it's a single dict, wrap in list
    if "holdings" in args and isinstance(args["holdings"], dict):
        args["holdings"] = [args["holdings"]]

    # Coerce current_prices: ensure values are floats
    if "current_prices" in args and isinstance(args["current_prices"], dict):
        cp = {}
        for k, v in args["current_prices"].items():
            try:
                cp[k] = float(v)
            except (ValueError, TypeError):
                cp[k] = v
        args["current_prices"] = cp

    # Coerce holdings list items
    if "holdings" in args and isinstance(args["holdings"], list):
        coerced = []
        for h in args["holdings"]:
            if isinstance(h, dict):
                h = dict(h)
                if "shares" in h:
                    try:
                        h["shares"] = int(h["shares"])
                    except (ValueError, TypeError):
                        pass
                if "purchase_price" in h:
                    try:
                        h["purchase_price"] = float(h["purchase_price"])
                    except (ValueError, TypeError):
                        pass
                coerced.append(h)
            else:
                coerced.append(h)
        args["holdings"] = coerced

    return args
