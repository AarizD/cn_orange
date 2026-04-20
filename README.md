# Software Defined Networking (SDN) Flow Controller

## 🌐 Project Overview
This project explores the fundamental principles of **Software Defined Networking (SDN)** by decoupling the network's **Control Plane** from the **Data Plane**. Using the **POX** controller and **Mininet** emulation environment, I have implemented a system that transitions from a reactive learning model to a high-performance proactive flow-management architecture.

## 🧠 SDN Architectural Logic

### 1. Control Plane vs. Data Plane
In a traditional network, each switch makes its own independent routing decisions. In this SDN implementation:
* **The Control Plane (POX):** Acts as the "Brain," dictating exactly where packets should go based on global network knowledge.
* **The Data Plane (Mininet/OVS):** Acts as the "Muscle," strictly forwarding packets according to the flow rules pushed by the controller.

### 2. Reactive Learning Mode (`orange.py`)
This implementation follows the **On-Demand** philosophy:
* The switch begins with an empty flow table.
* When an unknown packet arrives, the switch generates an `OFPT_PACKET_IN` message to ask the controller for instructions.
* The controller computes the path, installs a rule, and the packet is forwarded.
* **Outcome:** High initial latency for the first packet, but dynamic adaptability to new hosts.

### 3. Proactive Flow Management (`orange2.py`)
This implementation follows the **Pre-Provisioned** philosophy:
* Upon connection (`ConnectionUp`), the controller immediately pushes explicit `ofp_flow_mod` instructions to the switch.
* Routing paths for all hosts (H1, H2, H3) are mapped to physical ports (Port 1, 2, 3) before any traffic is generated.
* **Outcome:** Zero-latency forwarding and 0% packet loss on initial contact, as the "highway" is built before the "cars" arrive.



## 🛠 Functional Behavior & Validation

### Explicit Flow Rules
The core of this project is the manual installation of **Match + Action** pairs. By matching the **Destination MAC Address** (`dl_dst`) and assigning an **Output Action** (`ofp_action_output`), we ensure deterministic routing. This bypasses the traditional "Learning Switch" broadcast storm and reduces overhead on the Control Plane.

### Performance & Scalability
Validation through `iperf` demonstrates that once flow rules are installed, traffic moves at line-rate speeds within the switch hardware. The controller is only involved during the setup phase, proving that an SDN architecture can handle high-bandwidth data transfers without the controller becoming a bottleneck.

### Network Resilience (Regression)
The system's stability was verified through **Path Persistence** testing. By restarting the control plane and observing that the data plane's forwarding rules remained consistent, we confirmed that the controller logic is deterministic. Even after a state reset, the network accurately re-provisions the same optimized paths, ensuring long-term reliability.



## 📖 Key Takeaways
* **Granular Control:** SDN allows for direct manipulation of the switch's flow table via OpenFlow.
* **Efficiency:** Proactive rule installation eliminates the "First Packet Drop" common in reactive networks.
* **Transparency:** Tools like Wireshark and `ovs-ofctl` allow for real-time inspection of the binary instructions (FlowMods) that govern the network.


## OUTPUTS
<img width="927" height="344" alt="ss1" src="https://github.com/user-attachments/assets/28ed2440-e056-40f7-80f8-447d9e892e3e" />
<img width="927" height="551" alt="ss2" src="https://github.com/user-attachments/assets/36060995-cb69-4b4d-8e38-73dcdf618bf1" />
<img width="1317" height="165" alt="ss3" src="https://github.com/user-attachments/assets/7027262a-1dc3-4f8e-aa38-6b701b8ef0c9" />
<img width="1317" height="600" alt="ss5" src="https://github.com/user-attachments/assets/80c5286a-3989-47af-930f-30dcc4659723" />
<img width="1854" height="860" alt="ss6" src="https://github.com/user-attachments/assets/9b6e9abd-7c79-4e03-a163-7ce2b5c9222f" />






