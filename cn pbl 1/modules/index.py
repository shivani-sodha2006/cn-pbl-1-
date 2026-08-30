import csv
import os
from datetime import datetime
import matplotlib.pyplot as plt


HISTORY_FILE = "network_history.csv"


def save_record(timestamp, target, latency, packet_loss):
    """Save one network measurement to the CSV history file."""

    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "Timestamp",
                "Target",
                "Latency_ms",
                "Packet_Loss_Percent"
            ])

        writer.writerow([
            timestamp,
            target,
            latency,
            packet_loss
        ])


def collect_history(target, samples=10, interval=2):
    """Collect latency and packet-loss measurements."""

    from modules.latency import ping_target

    print("\n" + "=" * 60)
    print("          HISTORICAL NETWORK LOGGING")
    print("=" * 60)

    print(f"\nTarget: {target}")
    print(f"Samples: {samples}")
    print(f"Interval: {interval} seconds")

    print("\nCollecting measurements...\n")

    for i in range(samples):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        rtt = ping_target(target)

        if rtt is None:
            packet_loss = 100.0
            latency = ""
            status = "DOWN"
        else:
            packet_loss = 0.0
            latency = rtt
            status = "UP"

        save_record(
            timestamp,
            target,
            latency,
            packet_loss
        )

        if rtt is None:
            print(
                f"{i + 1}/{samples} | "
                f"{timestamp} | "
                f"{status}"
            )
        else:
            print(
                f"{i + 1}/{samples} | "
                f"{timestamp} | "
                f"{status} | "
                f"Latency: {rtt:.2f} ms"
            )

        if i < samples - 1:
            import time
            time.sleep(interval)

    print("\nHistory saved to:")
    print(os.path.abspath(HISTORY_FILE))


def generate_chart(target):
    """Generate a latency-over-time chart from the CSV file."""

    if not os.path.exists(HISTORY_FILE):
        print("\nNo history file found.")
        return

    timestamps = []
    latencies = []

    with open(HISTORY_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if row["Target"] != target:
                continue

            if row["Latency_ms"] == "":
                continue

            timestamps.append(
                datetime.strptime(
                    row["Timestamp"],
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            latencies.append(
                float(row["Latency_ms"])
            )

    if not latencies:
        print("\nNo latency data available for this target.")
        return

    plt.figure(figsize=(10, 5))

    plt.plot(
        timestamps,
        latencies,
        marker="o"
    )

    plt.title(f"Network Latency History - {target}")
    plt.xlabel("Time")
    plt.ylabel("Latency (ms)")
    plt.grid(True)

    plt.xticks(rotation=45)
    plt.tight_layout()

    chart_file = "latency_history.png"

    plt.savefig(chart_file)

    print("\nChart generated successfully.")
    print(f"Chart saved to: {os.path.abspath(chart_file)}")

    plt.show()


def run_history_module():

    from modules.latency import get_default_gateway

    gateway = get_default_gateway()

    if gateway is None:
        print("\nCould not detect the default gateway.")
        return

    print("\nAvailable history targets:")
    print(f"1. Gateway ({gateway})")
    print("2. Public DNS (8.8.8.8)")

    choice = input("\nSelect target: ")

    if choice == "1":
        target = gateway

    elif choice == "2":
        target = "8.8.8.8"

    else:
        print("Invalid choice.")
        return

    try:
        samples = int(
            input("\nEnter number of samples (example: 10): ")
        )

        interval = int(
            input("Enter interval in seconds (example: 2): ")
        )

        if samples <= 0 or interval <= 0:
            print("Values must be greater than 0.")
            return

    except ValueError:
        print("\nPlease enter valid numbers.")
        return

    collect_history(
        target,
        samples,
        interval
    )

    generate_chart(target)