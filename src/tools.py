MOCK_TRANSACTIONS = {
    "TXN-1001": {
        "transaction_id": "TXN-1001",
        "status": "completed",
        "amount": 250.0,
        "currency": "USD",
        "updated_at": "2026-10-10T14:22:00Z",
    },
    "TXN-1002": {
        "transaction_id": "TXN-1002",
        "status": "pending",
        "amount": 80.5,
        "currency": "USD",
        "updated_at": "2026-10-12T09:05:00Z",
    },
    "TXN-1003": {
        "transaction_id": "TXN-1003",
        "status": "failed",
        "amount": 15.0,
        "currency": "USD",
        "updated_at": "2026-10-11T18:40:00Z",
    },
}


def get_transaction_status(transaction_id: str) -> dict:
    record = MOCK_TRANSACTIONS.get(transaction_id)
    if record is None:
        return {
            "transaction_id": transaction_id,
            "status": "not_found",
            "amount": None,
            "currency": None,
            "updated_at": None,
        }
    return dict(record)
