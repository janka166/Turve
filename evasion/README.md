# Evasion

Is a project designed to deepen understanding of how antivirus software operates and explore methods of bypassing it for educational purposes.


## How Antiviruses Work

Antivirus software detects viruses:

- Signature-Based Detection:
- Heuristic Analysis
- Behavioral Analysis
- Machine Learning

## How Does Bypass Anti-Virus Detection?

- Encryption
- Self-extraction and execution
- Size increase and delay
- Social Engineering
- System Tools
- Fileless Malware
- Code Injection
- Polymorphic and Metamorphic malware
- Obfuscation

## How to use

The program takes an input executable (for example, notepad.exe) and encrypts its contents using AES, producing an encrypted version of the original file.


### Compile the evasion:

Linux:  `GOOS=windows GOARCH=amd64 go build -o evasion.exe`

Windows: `go build -o evasion.exe`

### Run `evasion.exe testfile`

After running the tool, the generated executable testfile will sleep for 101 seconds.

## Audit
[Audit](https://github.com/01-edu/public/tree/master/subjects/cybersecurity/evasion)