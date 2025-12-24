from pathlib import Path
from datetime import datetime


def log_script_location(message: str) -> None:
    """
    Log the current working directory with a timestamp and a message.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    cwd = Path.cwd()

    log_entry = f"{timestamp} | cd '{cwd}'\t| {message}\n"

    print(log_entry, end="")

    log_file = Path.home() / "script_addresses.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    with log_file.open("a", encoding="utf-8") as f:
        f.write(log_entry)

    print(f"Script address is saved to: {log_file}")
