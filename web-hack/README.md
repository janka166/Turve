# Deploy Web Application
## Install Apache, PHP:
```
sudo apt update  
sudo apt install apache2 php libapache2-mod-php
```  

## Deploy the app

Move the application (for example, DVWA) into the web root and set ownership to the web user:

```
sudo mv ~/Downloads/DVWA-master /var/www/html/  
sudo chown -R www-data:www-data /var/www/html/DVWA-master
```  
Open the setup page in your browser:
```
http://localhost/DVWA-master/setup.php  
```


## Vulnerabilities Found and Exploited

1. Command Injection

#### Description
User-supplied input is executed directly within system commands without proper validation or sanitization.

### Exploitation:
Access the command execution module.
Enter ; ls to list files in the server directory.
### Mitigation:
Sanitize user input using libraries like filter_var or parameterized queries.

2. File Upload Vulnerability
#### Description:
The application allows unrestricted file uploads, enabling attackers to upload malicious scripts.

### Exploitation:
Upload a malicious PHP shell (e.g., php-shell.php).
Access the shell via:
```
http://localhost/uploads/php-shell.php
```
### Mitigation:
Validate file extensions and MIME types on the server.
Store uploaded files outside the web-accessible directory.

3. Cross-Site Scripting (XSS)
Description:
User input is not sanitized, allowing injection of malicious JavaScript.

### Exploitation:
Inject <script>alert('XSS')</script> into an input field.
### Mitigation:
HTML-encode user-generated content before rendering.
Implement Content Security Policy (CSP) headers.

## Audit

 [Audit](https://github.com/01-edu/public/tree/master/subjects/cybersecurity/web-hack/audit)