# Obfuscator

Obfuscator is an educational cybersecurity project that demonstrates polymorphic encryption techniques and dynamic program signature modification with each execution.


## Understanding Polymorphic Encryption
Polymorphic encryption is an advanced cryptographic approach that dynamically alters its encryption patterns to generate unique ciphertext outputs for the same plaintext. Unlike traditional encryption methods that produce consistent results, polymorphic encryption modifies its algorithm or parameters during each encryption operation. This adaptive behavior—often implemented through variable encryption logic or instance-specific keys—effectively evades signature-based detection systems. While frequently employed in malware obfuscation, these techniques also have legitimate applications in cybersecurity for protecting against static analysis.

## Execution-Based Signature Variation
This project implements signature variation by modifying the program's identifiable characteristics each time it executes. The technique involves altering non-functional program elements—such as appending null bytes or modifying padding sections—to create a unique binary signature for every instance. Commonly used in polymorphic and metamorphic malware, these methods enable programs to bypass static signature-based detection systems and complicate reverse engineering efforts.

## Key Features
- Dynamic Signature Modification: Each execution modifies the program's binary signature by reading the executable content, appending a null byte, and replacing the original file

- Reverse Shell Connectivity: After signature alteration, the program establishes a reverse shell connection to a specified endpoint

- Educational Focus: Designed for studying cybersecurity concepts in controlled environments

## System Requirements

  OS: Linux
  Netcat needs to be installed on the attacker's machine

## Setup Instructions
### Environment Configuration

- Deploy a Linux virtual machine to serve as the victim system

- Ensure the attacker system has netcat installed

### Program Configuration

Edit obfuscator.go and specify the attacker's IP address and port (lines 47-48)

Compile the program using:

```
go build obfuscator.go
```
Transfer the compiled binary to the victim system

### Execution Procedure

On the attacker system, start a netcat listener:

```
nc -lvnp <port>
```
Execute the program on the victim system

The attacker's netcat session will receive a reverse shell connection, enabling command execution on the victim machine


## Audit
[Audit](https://github.com/01-edu/public/tree/master/subjects/cybersecurity/obfuscator/audit)
