import subprocess
import platform
import time
import statistics
from collections import deque
import subprocess
import platform
import time
import statistics
import re
from collections import deque

def get_default_gateway():
    """Automatically detect the default gateway on Windows."""

    try:
        result = subprocess.run(
            ["route", "print", "0.0.0.0"],
            capture_output=True,
            text=True
        )

        for line in result.stdout.splitlines():
            parts = line.split()

            if len(parts) >= 3 and parts[0] == "0.0.0.0":
                gateway = parts[2]

                if gateway != "0.0.0.0":
                    return gateway

    except Exception:
        pass

    return None

def ping_target(target):
    """Send one ping and return the RTT in milliseconds."""

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", "1000", target]
    else:
        command = ["ping", "-c", "1", "-W", "1", target]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return None

        output = result.stdout

        # Find the time value from the ping response
        for part in output.split():
            if "time=" in part:
                value = part.split("=")[1]
                value = value.replace("ms", "")
                return float(value)

            if "time<" in part:
                value = part.split("<")[1]
                value = value.replace("ms", "")
                return float(value)

    except Exception:
        return None

    return None


def calculate_statistics(rtts, total_pings):
    """Calculate min, average, max, jitter and packet loss."""

    successful = [rtt for rtt in rtts if rtt is not None]

    if not successful:
        return None, None, None, None, 100.0

    minimum = min(successful)
    average = statistics.mean(successful)
    maximum = max(successful)

    # Jitter = average difference between consecutive RTT values
    if len(successful) > 1:
        differences = [
            abs(successful[i] - successful[i - 1])
            for i in range(1, len(successful))
        ]
        jitter = statistics.mean(differences)
    else:
        jitter = 0.0

    packet_loss = (
        (total_pings - len(successful)) / total_pings
    ) * 100

    return minimum, average, maximum, jitter, packet_loss


def monitor_targets(targets, window_size=10, interval=2):
    """Continuously monitor all configured targets."""

    history = {
        target: deque(maxlen=window_size)
        for target in targets
    }

    total_pings = {
        target: 0
        for target in targets
    }

    while True:
        print("\n" + "=" * 90)
        print("              REACHABILITY & LATENCY MONITOR")
        print("=" * 90)

        print(
            f"{'Target':<25}"
            f"{'Status':<10}"
            f"{'Min':<10}"
            f"{'Avg':<10}"
            f"{'Max':<10}"
            f"{'Jitter':<10}"
            f"{'Loss':<10}"
        )

        print("-" * 90)

        for target in targets:

            rtt = ping_target(target)

            history[target].append(rtt)
            total_pings[target] += 1

            minimum, average, maximum, jitter, packet_loss = (
                calculate_statistics(
                    history[target],
                    len(history[target])
                )
            )

            if rtt is None:
                status = "DOWN"
            else:
                status = "UP"

            if minimum is None:
                print(
                    f"{target:<25}"
                    f"{status:<10}"
                    f"{'-':<10}"
                    f"{'-':<10}"
                    f"{'-':<10}"
                    f"{'-':<10}"
                    f"{packet_loss:.1f}%"
                )
            else:
                print(
                    f"{target:<25}"
                    f"{status:<10}"
                    f"{minimum:.2f} ms{'':<4}"
                    f"{average:.2f} ms{'':<4}"
                    f"{maximum:.2f} ms{'':<4}"
                    f"{jitter:.2f} ms{'':<4}"
                    f"{packet_loss:.1f}%"
                )

        print("\nRefreshing every 2 seconds...")
        print("Press Ctrl+C to stop.")

        time.sleep(interval)