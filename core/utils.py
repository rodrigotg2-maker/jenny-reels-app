def safe_join_lines(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items if item)