# mal-track

## Overview


Mal-Track is a Windows cleanup utility that helps you find and remove known malware from a lab VM. It can stop malicious processes, clean autoruns, delete files and registry traces, and surface potential attacker IPs for basic triage.

## What Mal-Track Does

### Detect & kill processes
Locates suspicious processes (e.g., known names/signatures) and terminates them.

### Block persistence
Audits startup locations (registry & startup folders) and removes malicious autoruns so the threat doesn’t relaunch after reboot.

### Clean files & registry
Searches for related files/keys and removes leftovers to restore baseline behavior.

### Surface possible attacker IPs
Extracts IPv4 addresses found in the malware file or simple logs (best-effort; obfuscation can hide indicators).

### Requirements

Windows virtual machine (snapshot enabled, isolated).

Python 3.x on the VM and in your PATH.

Administrator privileges to remove autoruns and protected files/keys.

## Usage

Run from an elevated terminal:

`python maltrack.py`


What to expect:

Mal-Track attempts to terminate matching malware processes.

Startup entries are reviewed and malicious ones are removed.

Related files/keys are cleaned up.

Any extracted IPv4 indicators are printed for your notes.

## Configuration

At the top of maltrack.py, adjust constants (e.g., MalwareName) to target specific samples or filenames used in your lab.

### Safety Notes

- Run only inside a controlled VM.

- Review the code and constants before execution.

- This tool can delete files/keys—double-check targets to avoid removing legitimate items.

- Take/restore a VM snapshot before and after testing.
