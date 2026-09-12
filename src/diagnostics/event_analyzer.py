import json


def load_events(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("events", [])


def analyze_events(events):
    total_events = len(events)

    error_count = sum(
        1 for event in events
        if event.get("level") == "ERROR"
    )

    warning_count = sum(
        1 for event in events
        if event.get("level") == "WARN"
    )

    status_5xx_count = sum(
        1 for event in events
        if event.get("status_code", 0) >= 500
    )

    latencies = [
        event["latency_ms"]
        for event in events
        if event.get("latency_ms") is not None
    ]

    average_latency = (
        round(sum(latencies) / len(latencies), 2)
        if latencies
        else 0
    )

    return {
        "total_events": total_events,
        "error_count": error_count,
        "warning_count": warning_count,
        "status_5xx_count": status_5xx_count,
        "average_latency_ms": average_latency,
    }