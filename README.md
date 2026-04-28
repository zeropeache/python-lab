SSH Bruteforce Detection

A Python script that parses Linux `auth.log` files to detect SSH brute-force attempts, identify attacking IPs, and generate a report.

What it does

- Parses `Failed password` and `Invalid user` log lines
- Counts failed attempts per IP address
- Flags any IP that exceeds a configurable threshold (default: 5)
- Extracts targeted usernames per IP
- Prints a sorted report of all SSH activity

Usage

```bash
python3 ssh_bruteforce.py
```

Edit and update the `auth_log_file` path and `threshold` at the top of the script as needed.

Output

```
SSH FAILED LOGIN REPORT
____________________________________________________________

FLAGGED IPs (5 or more attempts):

 IP ADDRESS: 185.220.101.5
 FAILED ATTEMPTS: 10
 TARGETED USERNAMES: root, admin, test, guest, ubuntu, pi

____________________________________________________________
ALL SSH ACTIVITY:

FLAGGED 185.220.101.5   | Attempts:  10 | Users: root, admin, test, guest, ubuntu, pi
pass    77.88.99.10     | Attempts:   4 | Users: root, admin, ubuntu
```

Detects

- Repeated failed password attempts from a single IP
- Invalid user probing (username enumeration)
- Low-and-slow attacks spread across time
- Mixed attack patterns on the same IP
