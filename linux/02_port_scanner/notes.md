Lab 02 - Port Scanner

The task is to make scanner that finds which TCP ports are open on a box, retrieve that information and then you can utilise that info to close or block a port. THis kind of script you can do some recon for pentesting, like before attacking a box you need to know the attack surface. Which ports are open tells you what services could be running, the usual ones like SSH on 22, a web server on 80/443. 
OR you can do network scanning, like if you have unexpected ports listening. I am learning how tcp works so writing one from scratch shows the TCP handshake, what "open" vs "filtered" vs "closed" actually means at the socket level. I can understand nmap even more now.  nmap does everything my script does but faster. Of course with deeper detection, service version detection, and scripting.  

My script is essentially a baby nmap. If you find yourself on a machine that specifically doesn't have nmap installed and you can run my script! like a ctf or something. :)

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

---
Edits i've done

## Exemple of what it looks like in use

You can do a default ports 1-1024 scan on your own machine
python port_scanner.py -p 1-1024 -t 5.0 127.0.0.1
OR
python3 port_scanner.py -p 1-1024 -t 5.0 127.0.0.1
 
```
Resolving hostname...
Target: 127.0.0.1 (127.0.0.1)
Scanning 1024 ports...

[OPEN] Port 22 — SSH-2.0-OpenSSH_8.9
[OPEN] Port 80
[OPEN] Port 443

__________________________________________________
SCAN COMPLETE
Open ports found: 3
__________________________________________________
```

nice :)
