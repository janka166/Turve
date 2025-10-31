
# Injector

Injector is a Go program that merges two executables into one. It reads both binaries, embeds their bytes into a generated wrapper, and builds a new executable that runs the first program and then the second, sequentially.

## How It Works

    go run injector.go `executable file1` `executable file2`

## Audit

[Audit](https://github.com/01-edu/public/tree/master/subjects/cybersecurity/injector/audit)
