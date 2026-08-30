import psutil
import time


def get_interfaces():
    """Return the list of available network interfaces."""
    return list(psutil.net_io_counters(pernic=True).keys())


def calculate_throughput(previous_bytes, current_bytes, interval):
    """Calculate data transfer rate in Mbps."""
    bytes_transferred = current_bytes - previous_bytes
    bits_transferred = bytes_transferred * 8
    bits_per_second = bits_transferred / interval

    return bits_per_second / (1024 * 1024)


def monitor_interface(interface, interval=1):
    """Continuously monitor network traffic."""

    previous = psutil.net_io_counters(pernic=True)[interface]

    print("\nMonitoring:", interface)
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            time.sleep(interval)

            current = psutil.net_io_counters(pernic=True)[interface]

            upload_speed = calculate_throughput(
                previous.bytes_sent,
                current.bytes_sent,
                interval
            )

            download_speed = calculate_throughput(
                previous.bytes_recv,
                current.bytes_recv,
                interval
            )

            packets_sent = current.packets_sent - previous.packets_sent
            packets_received = current.packets_recv - previous.packets_recv

            print(
                f"Upload: {upload_speed:.2f} Mbps | "
                f"Download: {download_speed:.2f} Mbps | "
                f"Packets Sent: {packets_sent} | "
                f"Packets Received: {packets_received}"
            )

            previous = current

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")