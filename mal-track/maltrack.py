# simple_malware_cleanup.py
from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path
import winreg as reg

MALWARE_NAME = "mal-track.exe"
IP_REGEX = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")

REG_PATHS = [
    (reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (reg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
    (reg.HKEY_CURRENT_USER,   r"Software\Microsoft\Windows\CurrentVersion\Run"),
    (reg.HKEY_CURRENT_USER,   r"Software\Microsoft\Windows\CurrentVersion\RunOnce"),
]


def run(cmd: list[str]) -> str:
    """Run a command and return stripped stdout (empty on error)."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout.strip()
    except Exception:
        return ""


def find_pid(image_name: str) -> int:
    """Return PID of first matching image name, or 0 if not found."""
    out = run(["tasklist", "/FI", f"IMAGENAME eq {image_name}", "/FO", "CSV", "/NH"])
    if not out or "No tasks" in out:
        return 0
    first = out.splitlines()[0]
    try:
        row = next(csv.reader([first]))
        return int(row[1])
    except Exception:
        return 0


def get_process_path(pid: int) -> Path | None:
    """Return the executable path for a PID, or None if unavailable."""
    if pid <= 0:
        return None
    out = run(["powershell", "-NoProfile", "-Command", f"(Get-Process -Id {pid}).Path"])
    p = Path(out.strip('"')) if out else None
    return p if p and p.exists() else None


def extract_ips(file_path: Path) -> set[str]:
    """Scan a file for IPv4 literals."""
    ips: set[str] = set()
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                ips.update(IP_REGEX.findall(line))
    except Exception:
        pass
    return ips


def kill(pid: int) -> None:
    """Kill a process by PID (force & terminate tree)."""
    if pid > 0:
        try:
            subprocess.run(["taskkill", "/F", "/PID", str(pid), "/T"], check=True)
        except Exception:
            pass


def scrub_autoruns(keyword: str) -> None:
    """Remove startup entries that reference the given keyword (case-insensitive)."""
    kw = keyword.lower()
    for hive, path in REG_PATHS:
        to_delete: list[str] = []
        try:
            with reg.OpenKey(hive, path, 0, reg.KEY_READ | reg.KEY_SET_VALUE) as key:
                value_count = reg.QueryInfoKey(key)[1]
                for i in range(value_count):
                    name, data, _ = reg.EnumValue(key, i)
                    if isinstance(data, str) and kw in data.lower():
                        to_delete.append(name)
        except FileNotFoundError:
            continue
        except PermissionError:
            print(f"Permission denied: {path} (run as Administrator).")
            continue

        for name in to_delete:
            try:
                with reg.OpenKey(hive, path, 0, reg.KEY_SET_VALUE) as wkey:
                    reg.DeleteValue(wkey, name)
                print(f"Removed startup entry '{name}' from {path}.")
            except FileNotFoundError:
                pass
            except PermissionError:
                print(f"Permission denied removing '{name}' in {path}.")


def main() -> None:
    pid = find_pid(MALWARE_NAME)
    if pid == 0:
        print(f"{MALWARE_NAME}: process not found.")
    else:
        exe = get_process_path(pid)
        if exe:
            ips = extract_ips(exe)
            if ips:
                print(f"{MALWARE_NAME} referenced IPs: {', '.join(sorted(ips))}")
            else:
                print(f"No IPs found in {exe}")
        kill(pid)

    scrub_autoruns(MALWARE_NAME)


if __name__ == "__main__":
    main()
