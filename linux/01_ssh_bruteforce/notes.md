Lab 01 - SSH Bruteforce Detection

The scenario I made to give this script a test drive is putting yourself in the shoes of a fictional security team called Peachlab, you can see someone is brute-forcing SSH logins.
You are tasked with writing a Python script that parses the auth.log provided, it has to extract all failed SSH login attempts, count failures per IP, flags any IP exceeding a threshold, and prints a clean report.

The questions I asked before building:

**What type of failed login lines stand out as useful?**
There are three patterns ->`Failed password for <user>`, `Invalid user <user>`, and `Failed password for invalid user <user>`. The last one is a mix, it contains both "for" and "invalid user", so username extraction had to handle it carefully or it would pull "invalid" as the username instead of the real one. (which is why the auth.log for this test has to also be a bit tweaked)

**Is there a correlating IP address?**
Yes, both line types consistently include `from <ip>`, which makes it possible to group everything by attacker.

**Is there any other type of failed message or just the one pattern?**
At least two that I handled. In a real environment there would also be things like "maximum authentication attempts exceeded" and what is called PAM failures. The script ignores those for now, but something to build on in future :)).

**What would break if the log was bigger than 10GB?**
Nothing. Using `with open()` and iterating line by line means Python never loads the whole file into memory, didn't know it was a thing until I learnt more about scanners and nmap with C-based tools.

**Is the script ready to flag the same IP across both line types?**
Yes both types feed into the same dictionary so the count accumulates regardless of which pattern triggered it. Confirmed in testing.

---

## Journal 

- `line.splits()` had typo,fixed to `line.split()`.
- Username extraction pulled "invalid" instead of the real username on `Failed password for invalid user` lines. Fixed by checking for the "invalid user " prefix before splitting.
- Sort was ordering by IP string alphabetically instead of by failure count. I basically had to do a little refresher on lambda and added `key=lambda x: x[1]` xD.
- `except: pass` replaced, it was silently swallowing errors...
- Replaced dot-counting loop with `re.search()`. More reliable based on research beyong my knowledge o.o
- Wrapped parsing logic into `parse_log(filepath)``print_report()``parse_log'`print_report' takes them in and handles clean display.
- absolute path was pushed oups. `auth_log_file` was pointing to `/home/peachy/...` which only exists on my machine. Anyone cloning the repo would hit a error immediately. Fixed it with the `os.path.join(os.path.dirname(__file__), "auth.log")` so the script always looks for `auth.log` relative to wherever the script itself lives, used Claude Code to acknowledge that mistake.

---

## Testing it

- Generated a larger auth.log with specific cases to stress-test the script:
- an IP with exactly 4 failures (since threshold is 5, wanted to test)worked!
- IP spreading 6 attempts over 3 hours, flagged!
- Mixed `Invalid user` and `Failed password` for same IP, merged into one entry
- `Failed password for invalid user osiris` reported `osiris`, not `invalid`
- Noise lines (session opened, sudo, accepted) ignored
- All SSH activity sorted by count descending

thank you for reading
