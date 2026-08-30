import time


def check_latency_alert(target, rtt, threshold):
    """Check whether latency exceeds the configured threshold."""

    if rtt is not None and rtt > threshold:
        print(
            f"\n⚠ ALERT: High latency detected!"
            f"\nTarget: {target}"
            f"\nCurrent latency: {rtt:.2f} ms"
            f"\nThreshold: {threshold:.2f} ms"
        )
        return True

    return False


def check_packet_loss_alert(target, packet_loss, threshold):
    """Check whether packet loss exceeds the configured threshold."""

    if packet_loss > threshold:
        print(
            f"\n⚠ ALERT: High packet loss detected!"
            f"\nTarget: {target}"
            f"\nCurrent packet loss: {packet_loss:.1f}%"
            f"\nThreshold: {threshold:.1f}%"
        )
        return True

    return False


def run_alert_demo():
    """Run a configurable threshold-alert demonstration."""

    print("\n" + "=" * 60)
    print("              THRESHOLD ALERTING")
    print("=" * 60)

    try:
        latency_threshold = float(
            input("\nEnter latency threshold in milliseconds: ")
        )

        packet_loss_threshold = float(
            input("Enter packet loss threshold in percentage: ")
        )

        if latency_threshold <= 0:
            print("Latency threshold must be greater than 0.")
            return

        if packet_loss_threshold < 0 or packet_loss_threshold > 100:
            print("Packet loss threshold must be between 0 and 100.")
            return

        print("\nConfigured thresholds:")
        print(f"Latency     : {latency_threshold:.2f} ms")
        print(f"Packet Loss : {packet_loss_threshold:.1f}%")

        print("\nAlert system is ready.")
        print("Monitoring gateway and public DNS...")
        print("Press Ctrl+C to stop.\n")

        # Import here to avoid circular imports
        from modules.latency import get_default_gateway, ping_target

        gateway = get_default_gateway()

        if gateway is None:
            print("Could not detect the default gateway.")
            return

        targets = [
            gateway,
            "8.8.8.8"
        ]

        while True:

            for target in targets:

                rtt = ping_target(target)

                if rtt is None:
                    packet_loss = 100.0
                    print(
                        f"{target:<20} DOWN | "
                        f"Packet Loss: {packet_loss:.1f}%"
                    )

                    check_packet_loss_alert(
                        target,
                        packet_loss,
                        packet_loss_threshold
                    )

                else:
                    packet_loss = 0.0

                    print(
                        f"{target:<20} UP | "
                        f"Latency: {rtt:.2f} ms | "
                        f"Packet Loss: {packet_loss:.1f}%"
                    )

                    check_latency_alert(
                        target,
                        rtt,
                        latency_threshold
                    )

                    check_packet_loss_alert(
                        target,
                        packet_loss,
                        packet_loss_threshold
                    )

            time.sleep(2)

    except ValueError:
        print("\nPlease enter valid numeric values.")

    except KeyboardInterrupt:
        print("\n\nAlert monitoring stopped.")