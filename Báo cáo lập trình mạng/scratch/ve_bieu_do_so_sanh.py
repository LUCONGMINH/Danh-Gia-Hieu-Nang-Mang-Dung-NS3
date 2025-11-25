
import matplotlib.pyplot as plt

# --- SO LIEU CHINH THUC TU MO PHONG CUA BAN ---
clients = [10, 20, 40, 60, 80, 100]

# TCP Data
tcp_throughput = [9.80, 7.49, 10.51, 9.22, 4.04, 1.32] 
tcp_delay =      [22.49, 78.94, 94.41, 118.45, 123.90, 129.44]
tcp_loss =       [0.25, 2.99, 3.77, 5.63, 10.91, 17.89]

# UDP Data
udp_throughput = [8.78, 13.11, 15.54, 19.87, 20.79, 22.14]
udp_delay =      [34.54, 251.06, 208.47, 246.51, 201.86, 210.22]
udp_loss =       [0.40, 25.61, 55.92, 62.41, 70.51, 74.88]
# ----------------------------------------------

# 1. VE BIEU DO PACKET LOSS (Quan trong nhat)
plt.figure(figsize=(10, 6))
plt.plot(clients, tcp_loss, marker='o', label='TCP (Tin cậy)', color='blue', linewidth=2)
plt.plot(clients, udp_loss, marker='s', label='UDP (Không kết nối)', color='red', linewidth=2, linestyle='--')
plt.title('So sanh Ty le Mat goi (Packet Loss): TCP vs UDP', fontsize=14)
plt.xlabel('So luong Client', fontsize=12)
plt.ylabel('Packet Loss (%)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('so_sanh_loss.png')
print("Da ve xong: so_sanh_loss.png")

# 2. VE BIEU DO THROUGHPUT
plt.figure(figsize=(10, 6))
plt.plot(clients, tcp_throughput, marker='o', label='TCP', color='blue', linewidth=2)
plt.plot(clients, udp_throughput, marker='s', label='UDP', color='red', linewidth=2, linestyle='--')
plt.title('So sanh Thong luong (Throughput): TCP vs UDP', fontsize=14)
plt.xlabel('So luong Client', fontsize=12)
plt.ylabel('Throughput (Mbps)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('so_sanh_throughput.png')
print("Da ve xong: so_sanh_throughput.png")

# 3. VE BIEU DO DELAY
plt.figure(figsize=(10, 6))
plt.plot(clients, tcp_delay, marker='o', label='TCP', color='blue', linewidth=2)
plt.plot(clients, udp_delay, marker='s', label='UDP', color='red', linewidth=2, linestyle='--')
plt.title('So sanh Do tre (Delay): TCP vs UDP', fontsize=14)
plt.xlabel('So luong Client', fontsize=12)
plt.ylabel('Delay (ms)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend()
plt.savefig('so_sanh_delay.png')
print("Da ve xong: so_sanh_delay.png")

