from pox.core import core
import pox.openflow.libopenflow_01 as of

# Initialize the logger
log = core.getLogger()

class OrangeLogic (object):
    def __init__ (self, connection):
        self.connection = connection
        # Register the listeners so POX calls _handle_PacketIn
        connection.addListeners(self)
        log.info("--- Orange Logic Initialized for Switch %s ---", connection.dpid)

        # STATIC MAPPING: MAC -> Port
        self.mapping = {
            '00:00:00:00:00:01': 1,
            '00:00:00:00:00:02': 2,
            '00:00:00:00:00:03': 3
        }

    def _handle_PacketIn (self, event):
        packet = event.parsed
        
        # 1. THE AUDIT LOG: Every packet hitting the controller will print this.
        # This proves the connection between Mininet and POX is live.
        log.info("INCOMING: Src %s -> Dst %s (On Port %i)", 
                 packet.src, packet.dst, event.port)

        dst_mac = str(packet.dst)

        # 2. MATCH-ACTION LOGIC
        if dst_mac in self.mapping:
            out_port = self.mapping[dst_mac]
            
            # Create the Flow Modification (Pushing a rule to the switch)
            msg = of.ofp_flow_mod()
            msg.match = of.ofp_match(dl_dst = packet.dst)
            msg.actions.append(of.ofp_action_output(port = out_port))
            
            self.connection.send(msg)
            log.info(">>> SUCCESS: Rule Installed for %s on Port %i", dst_mac, out_port)
        
        else:
            # 3. FALLBACK: If MAC is unknown (like Broadcast/ARP), we must flood
            log.debug("Unknown Destination %s - Flooding to all ports", dst_mac)
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            self.connection.send(msg)

def launch ():
    def start_switch (event):
        OrangeLogic(event.connection)
    
    core.openflow.addListenerByName("ConnectionUp", start_switch)
    log.info("--- ORANGE CONTROLLER SYSTEM: ONLINE ---")
