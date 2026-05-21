Lab 02 - Port Scanner

The Scenario

The task is to fingerprint the box: which TCP ports are open, and what's sitting behind them, what if I didn't use nmap? What if I made my own!

!!! Only point this at boxes you own or have written permission to test. Scanning random infrastructure is obviously illegal, you can use pythons 8080 or use it on your own machine.

---

Questions I ask myself through this process

**Can I edit sock.connect_ex() to fail successfully?**

**IF the limit of ports is 65535 what happens if I hit it?**

**Why does the timeout matter so much more than i'd expect?**

**What breaks if the hostname doesn't resolve?**

