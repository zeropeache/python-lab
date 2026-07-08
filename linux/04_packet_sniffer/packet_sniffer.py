from scapy.all import sniff, IP, TCP, UDP, ARP, Raw
from datetime import datetime

def get_http_hint(packet):
	if packet.haslayer(Raw):
		payload = packet[Raw].load.decode(errors="ignore")
		for keyword in ("GET ", "POST ", "PUT ", "DELETE ", "HTTP/"):
			if payload.startswith(keyword):
				return payload.split("\r\n")[0][:80]
	return None

def handle_packet(packet):
	timestamp = datetime.now().strftime("%H:%M:%S")
	size = len(packet)

	if packet.haslayer(IP):
		src_ip = packet[IP].src
		dst_ip = packet[IP].dst

		if packet.haslayer(TCP):
			proto = "TCP"
			src = f"{src_ip}:{packet[TCP].sport}"
			dst = f"{dst_ip}:{packet[TCP].dport}"
		elif packet.haslayer(UDP):
			proto = "UDP"
			src = f"{src_ip}:{packet[UDP].sport}"
			dst = f"{dst_ip}:{packet[UDP].dport}"
		else:
			proto = "IP"
			src = src_ip
			dst = dst_ip

		hint = get_http_hint(packet) if proto == "TCP" else None
		line = f"[{timestamp}] {proto:<5} {src} → {dst}  {size}b"
		if hint:
			line += f"  ← {hint}"
		print(line)

	elif packet.haslayer(ARP):
		arp_proto = "ARP"
		print(f"[{timestamp}] {arp_proto:<5} {packet[ARP].psrc} → {packet[ARP].pdst}  {size}b")

sniff(prn=handle_packet, store=False)
