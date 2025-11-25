import xml.etree.ElementTree as ET
import sys

def print_line(width=65):
    print("-" * width)

def parse_xml(file_name):
    try:
        tree = ET.parse(file_name)
        root = tree.getroot()
    except:
        print(f"Loi: Khong tim thay file {file_name}")
        return

    # 1. KHOI TAO
    protocols = {
        6:  {'name': 'TCP', 'tx': 0, 'rx': 0, 'bytes': 0, 'delay': 0, 'lost': 0},
        17: {'name': 'UDP', 'tx': 0, 'rx': 0, 'bytes': 0, 'delay': 0, 'lost': 0}
    }
    
    flow_proto_map = {}
    for flow in root.findall("Ipv4FlowClassifier/Flow"):
        flowId = flow.get('flowId')
        proto = int(flow.get('protocol'))
        flow_proto_map[flowId] = proto

    # 2. QUET DU LIEU
    for flow in root.findall("FlowStats/Flow"):
        flowId = flow.get('flowId')
        if flowId not in flow_proto_map: continue
        
        proto = flow_proto_map[flowId]
        if proto not in protocols: continue

        tx = int(flow.get('txPackets'))
        rx = int(flow.get('rxPackets'))
        rx_bytes = int(flow.get('rxBytes'))
        delay_sum = float(flow.get('delaySum')[:-2]) * 1e-9
        
        p = protocols[proto]
        p['tx'] += tx
        p['rx'] += rx
        p['bytes'] += rx_bytes
        p['delay'] += delay_sum
        if tx > 0: p['lost'] += (tx - rx)

    # 3. HIEN THI BANG KET QUA (Da xoa File Source)
    print("\n")
    print("╔" + "═" * 63 + "╗")
    print(f"║ {'WI-FI PERFORMANCE ANALYSIS REPORT':^61} ║")
    print("╚" + "═" * 63 + "╝")
    print("") # Tao khoang trang

    # Tieu de bang
    print_line()
    print(f" {'PROTOCOL':^10} | {'THROUGHPUT':^15} | {'DELAY (ms)':^15} | {'PACKET LOSS':^15} ")
    print_line()

    sim_time = 10.0 

    for proto_id, p in protocols.items():
        throughput = (p['bytes'] * 8) / sim_time / 1000 / 1000 
        
        if p['rx'] > 0:
            avg_delay = (p['delay'] / p['rx']) * 1000 
        else:
            avg_delay = 0
            
        if p['tx'] > 0:
            loss_rate = (p['lost'] / p['tx']) * 100 
        else:
            loss_rate = 0

        print(f" {p['name']:^10} | {throughput:^11.2f} Mbps | {avg_delay:^11.2f} ms | {loss_rate:^12.2f} % ")

    print_line()
    print("\n")

if __name__ == "__main__":
    parse_xml("ketqua-mix.xml")

