
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/mobility-module.h"
#include "ns3/config-store-module.h"
#include "ns3/wifi-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("WifiMixTcpUdp");

int main (int argc, char *argv[])
{
  uint32_t nWifi = 10; 
  double simulationTime = 10.0;

  CommandLine cmd;
  cmd.AddValue ("nWifi", "So luong may tram (Client)", nWifi);
  cmd.Parse (argc, argv);

  // 1. Tao Node
  NodeContainer wifiStaNodes;
  wifiStaNodes.Create (nWifi);
  NodeContainer wifiApNode;
  wifiApNode.Create (1);

  // 2. Cau hinh Wifi (802.11ac)
  YansWifiChannelHelper channel = YansWifiChannelHelper::Default ();
  YansWifiPhyHelper phy;
  phy.SetChannel (channel.Create ());

  WifiHelper wifi;
  wifi.SetStandard (WIFI_STANDARD_80211ac);
  
  WifiMacHelper mac;
  Ssid ssid = Ssid ("ns-3-ssid");

  mac.SetType ("ns3::StaWifiMac", "Ssid", SsidValue (ssid), "ActiveProbing", BooleanValue (false));
  NetDeviceContainer staDevices = wifi.Install (phy, mac, wifiStaNodes);

  mac.SetType ("ns3::ApWifiMac", "Ssid", SsidValue (ssid));
  NetDeviceContainer apDevices = wifi.Install (phy, mac, wifiApNode);

  // 3. Mobility
  MobilityHelper mobility;
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (wifiApNode);
  mobility.SetPositionAllocator ("ns3::UniformDiscPositionAllocator", "rho", DoubleValue (50.0), "X", DoubleValue (0.0), "Y", DoubleValue (0.0));
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  mobility.Install (wifiStaNodes);

  // 4. Internet Stack
  InternetStackHelper stack;
  stack.Install (wifiApNode);
  stack.Install (wifiStaNodes);

  Ipv4AddressHelper address;
  address.SetBase ("192.168.1.0", "255.255.255.0");
  Ipv4InterfaceContainer staNodesInterface = address.Assign (staDevices);
  Ipv4InterfaceContainer apNodeInterface = address.Assign (apDevices);

  // 5. CAI DAT UNG DUNG (CHAY SONG SONG)
  uint16_t portUdp = 9;
  uint16_t portTcp = 10;

  // A. SERVER (AP) - Lang nghe ca 2 cong
  // Sink cho UDP
  PacketSinkHelper sinkUdp ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), portUdp));
  ApplicationContainer appSinkUdp = sinkUdp.Install (wifiApNode.Get (0));
  appSinkUdp.Start (Seconds (0.0));
  
  // Sink cho TCP
  PacketSinkHelper sinkTcp ("ns3::TcpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), portTcp));
  ApplicationContainer appSinkTcp = sinkTcp.Install (wifiApNode.Get (0));
  appSinkTcp.Start (Seconds (0.0));


  // B. CLIENT (Station) - Gui ca 2 loai
  // UDP App
  OnOffHelper clientUdp ("ns3::UdpSocketFactory", InetSocketAddress (apNodeInterface.GetAddress (0), portUdp));
  clientUdp.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
  clientUdp.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
  clientUdp.SetAttribute ("DataRate", DataRateValue (DataRate ("1Mbps"))); 
  clientUdp.SetAttribute ("PacketSize", UintegerValue (1024));
  ApplicationContainer appClientUdp = clientUdp.Install (wifiStaNodes);
  appClientUdp.Start (Seconds (1.0)); // UDP chay tu giay thu 1

  // TCP App
  OnOffHelper clientTcp ("ns3::TcpSocketFactory", InetSocketAddress (apNodeInterface.GetAddress (0), portTcp));
  clientTcp.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=1]"));
  clientTcp.SetAttribute ("OffTime", StringValue ("ns3::ConstantRandomVariable[Constant=0]"));
  clientTcp.SetAttribute ("DataRate", DataRateValue (DataRate ("1Mbps"))); 
  clientTcp.SetAttribute ("PacketSize", UintegerValue (1024));
  ApplicationContainer appClientTcp = clientTcp.Install (wifiStaNodes);
  appClientTcp.Start (Seconds (1.0)); // TCP cung chay tu giay thu 1

  // 6. FlowMonitor
  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll ();

  Simulator::Stop (Seconds (simulationTime));
  Simulator::Run ();

  monitor->CheckForLostPackets ();
  Ptr<Ipv4FlowClassifier> classifier = DynamicCast<Ipv4FlowClassifier> (flowmon.GetClassifier ());
  monitor->SerializeToXmlFile("ketqua-mix.xml", true, true);

  Simulator::Destroy ();
  return 0;
}
