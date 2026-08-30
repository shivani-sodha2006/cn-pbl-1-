import socket
import ipaddress
from datetime import datetime
import psutil

from modules.index import run_history_module
from modules.traffic_monitor import get_interfaces, monitor_interface
from modules.host_discovery import run_host_discovery
from modules.latency import monitor_targets, get_default_gateway
from modules.traffic_analyzer import analyze_traffic
from modules.alerts import run_alert_demo


def show_system_info(selected_interface):
    """
    Display the student's system information.
    This information is generated dynamically from the computer.
    """

    hostname = socket.gethostname()

    ip_address = None
    subnet_mask = None

    # Get IPv4 information of the selected interface
    for address in psutil.net_if_addrs().get(selected_interface, []):
        if address.family == socket.AF_INET:
            ip_address = address.address
            subnet_mask = address.netmask
            break

    print("\n" + "-" * 60)
    print("                 SYSTEM INFORMATION")
    print("-" * 60)

    print(f"Hostname        : {hostname}")

    if ip_address and subnet_mask:
        print(f"IP Address      : {ip_address}")
        print(f"Subnet Mask     : {subnet_mask}")

        try:
            network = ipaddress.IPv4Network(
                f"{ip_address}/{subnet_mask}",
                strict=False
            )

            print(f"Network Range   : {network.network_address}/{network.prefixlen}")

        except ValueError:
            print("Network Range   : Unable to determine")

    else:
        print("IP Address      : Not available")
        print("Subnet Mask     : Not available")
        print("Network Range   : Not available")

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print(f"Date & Time     : {current_time}")

    print("-" * 60)


def main():

    print("=" * 45)
    print("       NETWORK MONITORING TOOL")
    print("=" * 45)

    # -------------------------------------------------
    # STEP 1: GET NETWORK INTERFACES
    # -------------------------------------------------

    interfaces = get_interfaces()

    print("\nAvailable Network Interfaces:")

    for i, interface in enumerate(interfaces, start=1):
        print(f"{i}. {interface}")

    # -------------------------------------------------
    # STEP 2: SELECT NETWORK INTERFACE
    # -------------------------------------------------

    while True:

        try:
            choice = int(input("\nSelect an interface: "))

            if 1 <= choice <= len(interfaces):
                selected_interface = interfaces[choice - 1]
                break

            print("Invalid choice. Try again.")

        except ValueError:
            print("Please enter a number.")

    print("\nSelected interface:", selected_interface)

    # -------------------------------------------------
    # SHOW SYSTEM INFORMATION
    # -------------------------------------------------

    show_system_info(selected_interface)

    # -------------------------------------------------
    # STEP 3: SELECT MODULE
    # -------------------------------------------------

    print("\n1. Interface Traffic Monitor")
    print("2. Local Subnet Host Discovery")
    print("3. Reachability & Latency Monitor")
    print("4. Traffic Composition Analyzer")
    print("5. Threshold Alerting")
    print("6. Historical Logging & Charting")

    module_choice = input("\nSelect module: ")

    # -------------------------------------------------
    # C1 - INTERFACE TRAFFIC MONITOR
    # -------------------------------------------------

    if module_choice == "1":

        print("\nStarting Interface Traffic Monitor...")
        monitor_interface(selected_interface)

    # -------------------------------------------------
    # C2 - LOCAL SUBNET HOST DISCOVERY
    # -------------------------------------------------

    elif module_choice == "2":

        run_host_discovery(selected_interface)

    # -------------------------------------------------
    # C3 - REACHABILITY & LATENCY MONITOR
    # -------------------------------------------------

    elif module_choice == "3":

        gateway = get_default_gateway()

        if gateway is None:

            print("\nCould not automatically detect the gateway.")
            print("C3 cannot start without a gateway.")

        else:

            targets = [
                gateway,
                "8.8.8.8",
                "google.com"
            ]

            print("\nTargets being monitored:")
            print(f"Gateway     : {gateway}")
            print("Public DNS  : 8.8.8.8")
            print("Website     : google.com")

            monitor_targets(targets)

    # -------------------------------------------------
    # C4 - TRAFFIC COMPOSITION ANALYZER
    # -------------------------------------------------

    elif module_choice == "4":

        analyze_traffic(selected_interface)

    # -------------------------------------------------
    # E1 - THRESHOLD ALERTING
    # -------------------------------------------------

    elif module_choice == "5":

        run_alert_demo()

    # -------------------------------------------------
    # E3 - HISTORICAL LOGGING & CHARTING
    # -------------------------------------------------

    elif module_choice == "6":

        run_history_module()

    # -------------------------------------------------
    # INVALID MODULE
    # -------------------------------------------------

    else:

        print("Invalid module choice.")


if __name__ == "__main__":
    main()