# Notes — raw scratchpad

Lab 01 - SSH Bruteforce Detection

THe Scenario:
The fictional security team at Osiris&Co suspects someone is brute-forcing SSH logins.
My Goal: write a Python script that parses auth.log, extracts failed SSH login attempts, counts failures per IP, flags any IP exceeding a threshold, and prints a clean report.

The Questions I asked before building

What type of failed login lines stand out as useful?
THere is three patterns -> `Failed password for <user>`, `Invalid user <user>`, and `Failed password for invalid user <user>`. The last one is a mix, it contains both "for" and "invalid user", so username extraction had to handle it carefully or it would pull "invalid" as the username instead of the real one.

Is there a correlating IP address?
Yes, both line types consistently include `from <ip>`, which makes it possible to group everything by attacker.

Is there any other type of failed message or just the one pattern?
At least two that I handled. In a real environment there would also be things like "maximum authentication attempts exceeded" and PAM failures. The script ignores those for now, but something to build on in future.

What would break if the log was bigger than 10GB?
Nothing. Using `with open()` and iterating line by line means Python never loads the whole file into memory. The dictionaries only grow with unique IPs, not file size. Right call made without fully realising it at the time.

Is the script ready to flag the same IP across both line types?
Yes both types feed into the same dictionary so the count accumulates regardless of which pattern triggered it. Confirmed in testing.

---

## Development journal 

I parsed the log line by line, extracted IPs and usernames into dictionaries, printed a report. Got it working but the code was flat and untested bigger logs or adaptable cases.

Bugs found and fixed
- `line.splits()` typo, my first instance of syntax ;) Fixed to `line.split()`.
- Username extraction pulled "invalid" instead of the real username on `Failed password for invalid user` lines. Fixed by checking for the "invalid user " prefix before splitting.
- Sort was ordering by IP string alphabetically instead of by failure count. I basically had to do a little refresher on lambda and added `key=lambda x: x[1]`.
- `except: pass` replaced — was silently swallowing errors with no useful purpose.
- Replaced dot-counting loop with `re.search()`. More reliable.
- Wrapped parsing logic into `parse_log(filepath)` and reporting into `print_report()`. `parse_log` returns the two dictionaries; `print_report` takes them in and handles clean display.
- Hardcoded absolute path replaced — `auth_log_file` was pointing to `/home/peachy/...` which only exists on my machine. Anyone cloning the repo would hit a `FileNotFoundError` immediately. Fixed with `os.path.join(os.path.dirname(__file__), "auth.log")` so the script always looks for `auth.log` relative to wherever the script itself lives, not my specific machine.

---

Testing

Generated a larger auth.log with specific cases to stress-test the script:
- an IP with exactly 4 failures (since threshold is 5, wanted to test)worked!
- IP spreading 6 attempts over 3 hours, flagged!
- Mixed `Invalid user` and `Failed password` for same IP, merged into one entry
- `Failed password for invalid user osiris` reported `osiris`, not `invalid`
- Noise lines (session opened, sudo, accepted) ignored
- All SSH activity sorted by count descending
