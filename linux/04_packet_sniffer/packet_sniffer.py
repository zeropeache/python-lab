from scapy.all import sniff, IP, TCP, UDP, ARP
from datetime import datetime

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

		print(f"[{timestamp}] {proto:<5} {src} → {dst}  {size}b")

  	elif packet.haslayer(ARP):
         		arp_proto = "ARP"
         		print(f"[{timestamp}] {arp_proto:<5} {packet[ARP].psrc} → {packet[ARP].pdst}  {size}b")

sniff(prn=handle_packet, store=False)
