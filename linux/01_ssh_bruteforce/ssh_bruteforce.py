# first and foremost we need to read the log
auth_log_file = "/home/peachy/Projects/python-lab/linux/01_ssh_bruteforce/auth.log"

# making a dictionary of ip addresses fails and usernames in the log
ip_failures = {}
ip_usernames = {}

# read log
with open(auth_log_file, 'r') as file:
	for line in file:
		# Checking failed attempts
		if "Failed password" in line or "Invalid user" in line:

			# Exctracting IP adresses 
			ip = None
			parts = line.split()
			for part in parts: 
				if part.count('.') ==3: # ip addresses have 3 dots so I am looking for lines with 3 dots...Learnt this from a random reddit post
					try:
						numbers = part.split('.')
						if len(numbers) == 4:
							ip = part
							break	
					except: 
						pass
			# EXtracting usernames
			username = "unknown"
			if "for" in line:
				user_part = line.split("for")[1].split()[0]
				username= user_part
			elif "Invalid user" in line:
				words = line.splits()
				for i, word in enumerate(words):
					if word == "Invalid" and i+2 < len(words):
						username = words[i+2]
						break

			# If ip found, add it to dictionary ip_failures
			if ip:
				if ip not in ip_failures:
					ip_failures[ip] = 0
					ip_usernames[ip] = []

				ip_failures[ip] += 1
				if username not in ip_usernames[ip]:
					ip_usernames[ip].append(username)

threshold = 5

# Start of the report
print("SSH FAILED LOGIN REPORT")
print("_"*60 + "\n")

# Flagged IPs
flagged = []
for ip in ip_failures:
	if ip_failures[ip] >= threshold:
		flagged.append(ip)

# PRint IPs
if flagged:
	print(f"FLAGGED IPs (5 or more attempts):\n")
	for ip in flagged:
		print(f" IP ADDRESS: {ip}")
		print(f" FAILED ATTEMPTS: {ip_failures[ip]}")
		print(f" TARGETED USERNAMES: {', '.join(ip_usernames[ip])}")
else:
	print("NO SUSPICIOUS IPs found\n")

print("\n" + "_"*60)
print("ALL SSH ACTIVITY:\n")

all_ips = sorted(ip_failures.items(), reverse=True)
for ip, count in all_ips:
	status = "FLAGGED" if count >= threshold else "pass"
	users = ', '.join(ip_usernames[ip])
	print(f"{status} {ip:15} | Attempts: {count:3} | Users: {users}")
print("\n" + "_"*60 + "\n")
