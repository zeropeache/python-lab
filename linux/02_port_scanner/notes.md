Lab 02 - Port Scanner

The Scenario

The task is to fingerprint the box: which TCP ports are open, and what's sitting behind them, what if I didn't use nmap? What if I made my own!

!!! Only point this at boxes you own or have written permission to test. Scanning random infrastructure is obviously illegal, you can use pythons 8080 or use it on your own machine.

---

Questions I ask myself through this process

**Can I edit sock.connect_ex() to fail successfully?**

Yes, connect_ex() doesn't raise an exception on failure like connect() does, it just returns an error code. 0 means the port is open, anything else is closed or filtered. So "failing successfully" means getting a non-zero back and just moving on, which is what the script does.

---

**IF the limit of ports is 65535 what happens if I hit it?**

It would of just rejected it. I added a check in parse_ports() so if you pass something over 65535 it prints an error and bails out early instead of letting the socket blow, at some point in my editing it would just ignore the limit and post the result.

---

**Why does the timeout matter so much more than i'd expect?**

Because filtered ports don't say no, they just go silent. So if a port is filtered and your timeout is 1 second, you're waiting a full second per port. Scan 1024 ports and that's potentially 17 minutes just on filtered ones. The timeout is a necessary tool for scans many of them use it.

---

**What breaks if the hostname doesn't resolve?**

socket.gethostbyname() throws a gaierror and the script crashes hard with no useful message. Wrapping it in a try/except and printing something readable was one of the first things I fixed.

