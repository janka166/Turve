## About

## Task description

Our job was to import and run it locally in VirtualBox, discover how to access it (there will be no visible IP listed), obtain root privileges, and capture the flag.


###  IP detect
```
ipconfig
nmap -sn 172.20.10.0/24
```
Ip of VM: 172.20.10.4

### Ports
Through nmap, three open ports were discovered: 21, 22,80

I connected to the FTP service, navigated the web directory, and uploaded a file that provided a reverse shell. I first started a listener on my machine using:
ncat -lvn 172.20.10.2 8080
After executing the uploaded file on the VM, I received a remote shell. I examined /etc/passwd, discovered an account named shrek, and changed its password.
Authenticate and perform privilege escalation
Using the updated credentials I logged into the VM. I then uploaded a file called exploit.py, which contains:

import os
# spawn an interactive shell
os.system("/bin/bash")


After running this script on the VM, I was able to escalate privileges and gain root access.
Root privileges were obtained. I find file root.txt. `Flag: 01Talent@nokOpA3eToFrU8r5sW1dipe2aky`

## Audit
[Audit](https://github.com/01-edu/public/tree/master/subjects/cybersecurity/local).