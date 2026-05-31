import socket
import argparse

def parse_ports(port_str):
	ports = []
	for part in port_str.split(","):
		if "-" in part:
			start, end = part.split("-") 
			ports.extend(range(int(start), int(end) + 1))
		else:
			ports.append(int(part))
	return ports

def grab_banner(sock):
	try:
		banner = sock.recv(1024).decode(errors="ignore").strip()
		return banner
	except:
		return ""

def scan_port(target, port, timeout):
	sock = socket.socket()
	sock.settimeout(timeout)
	try:
		result = sock.connect_ex((target, port))
		if result == 0:
			banner = grab_banner(sock)
			sock.close()
			return True, banner
		sock.close()
		return False, ""
	except OSError:
		return False, ""

def main():
	parser = argparse.ArgumentParser(description="Simple port scanner")
	parser.add_argument("target", help="IP address or hostname to scan")
	parser.add_argument("-p", "--ports", default="1-65535", help="POrts to scan: 22, 20-100, or 22,80,443")
	parser.add_argument("-t", "--timeout", type=float, default=1.0, help="TImeout per por in seconds")
	args = parser.parse_args()

	print("Resolving hostname...")
	try:
		target_ip = socket.gethostbyname(args.target)
	except socket.gaierror:
		print(f"ERror: could not resolve '{args.target}'")
		return

	ports = parse_ports(args.ports)
	if not ports:
		return
	print(f"Scanning {len(ports)} ports ...\n")

	open_ports = []

	for port in ports:
		print(f"Checking port {port} ...", end="\r")
		is_open, banner = scan_port(target_ip, port, args.timeout)
		if is_open:
			if banner:
				print(f"[OPEN] Port {port} - {banner[:60]}")
			else:
				print(f"[OPEN] Port {port}")
			open_ports.append((port, banner))

	print("SCAN COMPLETE")
	print(f"Open ports found: {len(open_ports)}")

if __name__ == "__main__":
	main()
