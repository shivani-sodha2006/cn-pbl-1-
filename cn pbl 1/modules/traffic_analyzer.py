from collections import defaultdict
from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP, DNS


def classify_packet(packet):
    """Identify the protocol category of a packet."""

    if packet.haslayer(ARP):
        return "ARP"

    if packet.haslayer(DNS):
        return "DNS"

    if packet.haslayer(TCP):
        # HTTPS
        if packet[TCP].sport == 443 or packet[TCP].dport == 443:
            return "HTTPS"

        # HTTP
        if packet[TCP].sport == 80 or packet[TCP].dport == 80:
            return "HTTP"

        return "TCP"

    if packet.haslayer(UDP):
        return "UDP"

    if packet.haslayer(ICMP):
        return "ICMP"

    return "Other"


def analyze_traffic(interface, duration=15):
    """Capture packets and analyze protocol distribution."""

    protocol_packets = defaultdict(int)
    protocol_bytes = defaultdict(int)

    source_talkers = defaultdict(int)
    destination_talkers = defaultdict(int)

    print("\n" + "=" * 60)
    print("         TRAFFIC COMPOSITION ANALYZER")
    print("=" * 60)

    print(f"\nCapturing traffic on: {interface}")
    print(f"Capture duration: {duration} seconds")
    print("Please generate some network activity while capturing...")
    print("For example: open a website or play a video.\n")

    try:
        packets = sniff(
            iface=interface,
            timeout=duration,
            store=True
        )

    except PermissionError:
        print("\nPermission denied.")
        print("Please run PowerShell or VS Code as Administrator.")
        return

    except Exception as error:
        print(f"\nPacket capture failed: {error}")
        return

    print(f"Captured {len(packets)} packets.\n")

    for packet in packets:

        protocol = classify_packet(packet)
        packet_size = len(packet)

        protocol_packets[protocol] += 1
        protocol_bytes[protocol] += packet_size

        if packet.haslayer(IP):
            source_ip = packet[IP].src
            destination_ip = packet[IP].dst

            source_talkers[source_ip] += packet_size
            destination_talkers[destination_ip] += packet_size

    print("PROTOCOL-WISE BREAKDOWN")
    print("-" * 60)
    print(f"{'Protocol':<15}{'Packets':<15}{'Bytes'}")
    print("-" * 60)

    protocol_order = [
        "TCP",
        "UDP",
        "ICMP",
        "ARP",
        "DNS",
        "HTTP",
        "HTTPS",
        "Other"
    ]

    for protocol in protocol_order:
        print(
            f"{protocol:<15}"
            f"{protocol_packets[protocol]:<15}"
            f"{protocol_bytes[protocol]}"
        )

    print("-" * 60)

    print("\nTOP SOURCE TALKERS")
    print("-" * 60)
    print(f"{'Source IP':<25}{'Bytes'}")
    print("-" * 60)

    top_sources = sorted(
        source_talkers.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

    for ip_address, byte_count in top_sources:
        print(f"{ip_address:<25}{byte_count}")

    print("\nTOP DESTINATION TALKERS")
    print("-" * 60)
    print(f"{'Destination IP':<25}{'Bytes'}")
    print("-" * 60)

    top_destinations = sorted(
        destination_talkers.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

    for ip_address, byte_count in top_destinations:
        print(f"{ip_address:<25}{byte_count}")

    print("\nTraffic analysis completed.")