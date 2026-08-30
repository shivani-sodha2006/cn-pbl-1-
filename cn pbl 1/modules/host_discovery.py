import socket
import ipaddress
import psutil
from scapy.all import ARP, Ether, srp


def get_network_details(interface):
    """Get IPv4 address, subnet mask, network address and host range."""

    addresses = psutil.net_if_addrs().get(interface, [])

    ipv4_address = None
    subnet_mask = None

    for address in addresses:
        if address.family == socket.AF_INET:
            ipv4_address = address.address
            subnet_mask = address.netmask
            break

    if not ipv4_address or not subnet_mask:
        raise RuntimeError(
            f"No IPv4 configuration found for {interface}"
        )

    network = ipaddress.IPv4Network(
        f"{ipv4_address}/{subnet_mask}",
        strict=False
    )

    return ipv4_address, subnet_mask, network


def discover_hosts(network):
    """Discover active devices in the local subnet using ARP."""

    print("\nScanning local subnet...")
    print("Please wait...\n")

    arp_request = ARP(pdst=str(network))
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = broadcast / arp_request

    answered, _ = srp(
        packet,
        timeout=2,
        verbose=False
    )

    devices = []

    for _, received in answered:
        ip_address = received.psrc
        mac_address = received.hwsrc

        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except socket.herror:
            hostname = "Unknown"

        devices.append({
            "ip": ip_address,
            "mac": mac_address,
            "hostname": hostname
        })

    return devices


def run_host_discovery(interface):
    """Display local network details and discovered devices."""

    try:
        ip_address, subnet_mask, network = get_network_details(
            interface
        )

        print("\n" + "=" * 55)
        print("           LOCAL SUBNET HOST DISCOVERY")
        print("=" * 55)

        print(f"\nYour IPv4 Address : {ip_address}")
        print(f"Subnet Mask       : {subnet_mask}")
        print(f"Network Address   : {network.network_address}")
        print(f"Usable Host Range : {network.network_address + 1} "
              f"to {network.broadcast_address - 1}")

        devices = discover_hosts(network)

        print("\nLive Devices:")
        print("-" * 70)
        print(
            f"{'IP Address':<18}"
            f"{'MAC Address':<20}"
            f"{'Hostname'}"
        )
        print("-" * 70)

        if not devices:
            print("No devices discovered.")

        for device in devices:
            print(
                f"{device['ip']:<18}"
                f"{device['mac']:<20}"
                f"{device['hostname']}"
            )

        print("-" * 70)
        print(f"Total Live Devices: {len(devices)}")

    except Exception as error:
        print(f"\nHost discovery failed: {error}")