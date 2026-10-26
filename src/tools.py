import re

TOOL_NAME = "transaction_status_lookup"

MOCK_TRANSACTIONS = {
    "TXN-DEMO-001": {"status": "pending", "last_updated": "2026-01-15 10:30 UTC"},
    "TXN-DEMO-002": {"status": "completed", "last_updated": "2026-01-15 09:05 UTC"},
    "TXN-DEMO-003": {"status": "reversed", "last_updated": "2026-01-14 18:45 UTC"},
}


def transaction_status_lookup(transaction_id: str) -> dict:
    if not re.fullmatch(r"TXN-DEMO-[0-9]{3}", str(transaction_id)):
        return {
            "ok": False,
            "error": "Invalid demo transaction ID format",
            "simulation": True,
        }
    record = MOCK_TRANSACTIONS.get(transaction_id)
    if record is None:
        return {
            "ok": False,
            "transaction_id": transaction_id,
            "error": "Demo record not found",
            "simulation": True,
        }
    return {
        "ok": True,
        "transaction_id": transaction_id,
        **record,
        "simulation": True,
    }


def dispatch_tool(tool_name: str, arguments: dict) -> dict:
    if tool_name != TOOL_NAME:
        return {"ok": False, "error": "Tool is not allowlisted", "simulation": True}
    if set(arguments) != {"transaction_id"}:
        return {"ok": False, "error": "Expected only transaction_id", "simulation": True}
    return transaction_status_lookup(arguments["transaction_id"])
