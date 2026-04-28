# first and foremost we need to make sure the right file is read
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
			import re
			ip_match = re.search(r'\b(\d{1,3}\.){3}\d{1,3}\b', line)
			ip = ip_match.group() if ip_match else None

			# EXtracting usernames
			username = "unknown"
			if "for" in line:
				user_part = line.split("for")[1].strip()

				if user_part.startswith("invalid user "):
					username = user_part.split()[2]
				else:
					username = user_part.split()[0]
			elif "Invalid user" in line:
				words = line.split()
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
# Had to learn morea bout lambda for this
all_ips = sorted(ip_failures.items(), key=lambda x: x[1], reverse=True)
for ip, count in all_ips:
	status = "FLAGGED" if count >= threshold else "pass"
	users = ', '.join(ip_usernames[ip])
	print(f"{status} {ip:15} | Attempts: {count:3} | Users: {users}")
print("\n" + "_"*60 + "\n")
