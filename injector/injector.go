package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
)

func main() {
	if len(os.Args) != 3 {
		fmt.Println("How to run: go run injector.go executable file1 executable file2")
		return
	}

	bin1, err := os.ReadFile(os.Args[1])
	if err != nil {
		log.Fatal(err)
	}

	bin2, err := os.ReadFile(os.Args[2])
	if err != nil {
		log.Fatal(err)
	}

	tmp, err := os.CreateTemp("", "inject-*.go")
	if err != nil {
		log.Fatal(err)
	}
	tmpName := tmp.Name()

	if _, err = tmp.WriteString(combinedCode(bin1, bin2)); err != nil {
		tmp.Close()
		os.Remove(tmpName)
		log.Fatal(err)
	}
	if err = tmp.Close(); err != nil {
		os.Remove(tmpName)
		log.Fatal(err)
	}

	cmd := exec.Command("go", "build", "-o", os.Args[1], tmpName)
	if out, err := cmd.CombinedOutput(); err != nil {
		os.Remove(tmpName)
		log.Fatalf("go build failed: %v\n%s", err, string(out))
	}

	os.Remove(tmpName)
}

func combinedCode(bin1, bin2 []byte) string {
	return fmt.Sprintf(`
package main

import (
	"log"
	"os"
	"os/exec"
)

func main() {
	if err := runBinary(%#v); err != nil {
		log.Fatal(err)
	}
	if err := runBinary(%#v); err != nil {
		log.Fatal(err)
	}
}

func runBinary(data []byte) error {
	_ = os.Remove("tmpexec")
	if err := os.WriteFile("tmpexec", data, 0755); err != nil {
		return err
	}
	cmd := exec.Command("./tmpexec")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr
	if err := cmd.Run(); err != nil {
		_ = os.Remove("tmpexec")
		return err
	}
	_ = os.Remove("tmpexec")
	return nil
}
`, bin1, bin2)
}
