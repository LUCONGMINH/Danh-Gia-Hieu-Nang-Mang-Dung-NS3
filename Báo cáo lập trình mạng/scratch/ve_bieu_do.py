import matplotlib.pyplot as plt

# 1. DU LIEU THUC TE CUA BAN (Da tong hop)
clients = [10, 20, 40, 60, 80, 100]
throughput = [1.28, 2.57, 5.09, 5.80, 5.07, 5.09] # Mbps
delay = [4.26, 10.56, 19.10, 166.64, 192.96, 181.08] # ms
packet_loss = [0.00, 0.03, 0.89, 24.78, 50.66, 60.33] # %

# 2. VE BIEU DO PACKET LOSS (Quan trong nhat)
plt.figure(figsize=(10, 6))
plt.plot(clients, packet_loss, marker='o', color='red', linewidth=3, markersize=8)
plt.title('Ty le mat goi (Packet Loss) theo so luong Client', fontsize=14)
plt.xlabel('So luong Client (Nodes)', fontsize=12)
plt.ylabel('Packet Loss (%)', fontsize=12)
plt.grid(True, linestyle='--')
plt.axvline(x=50, color='green', linestyle='--', label='Nguong chiu tai (~50)')
plt.legend()
plt.savefig('bieudo_loss.png') # Luu thanh anh
print("Da ve xong: bieudo_loss.png")

# 3. VE BIEU DO DELAY
plt.figure(figsize=(10, 6))
plt.plot(clients, delay, marker='s', color='blue', linewidth=3, markersize=8)
plt.title('Do tre trung binh (Average Delay)', fontsize=14)
plt.xlabel('So luong Client (Nodes)', fontsize=12)
plt.ylabel('Delay (ms)', fontsize=12)
plt.grid(True, linestyle='--')
plt.savefig('bieudo_delay.png')
print("Da ve xong: bieudo_delay.png")

# 4. VE BIEU DO THROUGHPUT
plt.figure(figsize=(10, 6))
plt.plot(clients, throughput, marker='^', color='purple', linewidth=3, markersize=8)
plt.title('Thong luong mang (Throughput)', fontsize=14)
plt.xlabel('So luong Client (Nodes)', fontsize=12)
plt.ylabel('Throughput (Mbps)', fontsize=12)
plt.grid(True, linestyle='--')
plt.savefig('bieudo_throughput.png')
print("Da ve xong: bieudo_throughput.png")

