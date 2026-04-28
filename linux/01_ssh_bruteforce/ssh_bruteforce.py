import re
import os

auth_log_file = os.path.join(os.path.dirname(__file__), "auth.log")
threshold = 5

def parse_log(filepath):
	ip_failures = {}
	ip_usernames = {}

	with open(filepath, 'r') as file:
		for line in file:
			if "Failed password" in line or "Invalid user" in line:

				ip_match = re.search(r'\b(\d{1,3}\.){3}\d{1,3}\b', line)
				ip = ip_match.group() if ip_match else None

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

				if ip:
					if ip not in ip_failures:
						ip_failures[ip] = 0
						ip_usernames[ip] = []

					ip_failures[ip] += 1
					if username not in ip_usernames[ip]:
						ip_usernames[ip].append(username)

	return ip_failures, ip_usernames

def print_report(ip_failures, ip_usernames, threshold):
	print("SSH FAILED LOGIN REPORT")
	print("_"*60 + "\n")

	flagged = []
	for ip in ip_failures:
		if ip_failures[ip] >= threshold:
			flagged.append(ip)

	if flagged:
		print(f"FLAGGED IPs ({threshold} or more attempts):\n")
		for ip in flagged:
			print(f" IP ADDRESS: {ip}")
			print(f" FAILED ATTEMPTS: {ip_failures[ip]}")
			print(f" TARGETED USERNAMES: {', '.join(ip_usernames[ip])}")
	else:
		print("NO SUSPICIOUS IPs found\n")

	print("\n" + "_"*60)
	print("ALL SSH ACTIVITY:\n")
	all_ips = sorted(ip_failures.items(), key=lambda x: x[1], reverse=True)
	for ip, count in all_ips:
		status = "FLAGGED" if count >= threshold else "pass"
		users = ', '.join(ip_usernames[ip])
		print(f"{status} {ip:15} | Attempts: {count:3} | Users: {users}")
	print("\n" + "_"*60 + "\n")

ip_failures, ip_usernames = parse_log(auth_log_file)
print_report(ip_failures, ip_usernames, threshold)
