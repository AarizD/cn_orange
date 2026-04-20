from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class OrangeProactive (object):
    def __init__ (self, connection):
        self.connection = connection
        connection.addListeners(self)
        
        # Static mapping for proactive rules
        mapping = {
            '00:00:00:00:00:01': 1,
            '00:00:00:00:00:02': 2,
            '00:00:00:00:00:03': 3
        }

        log.info("--- STARTING PROACTIVE INSTALLATION for Switch %s ---", connection.dpid)

        for mac, port in mapping.items():
            msg = of.ofp_flow_mod()
            # Ensure we use the EthAddr helper for the match
            msg.match = of.ofp_match(dl_dst = of.EthAddr(mac))
            msg.actions.append(of.ofp_action_output(port = port))
            
            self.connection.send(msg)
            log.info("PROACTIVE RULE: Packets for %s -> Port %d", mac, port)

        log.info("--- ALL RULES DEPLOYED ---")

    def _handle_PacketIn (self, event):
        # Fallback flood for any unknown traffic (like ARP broadcasts)
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
        self.connection.send(msg)

def launch ():
    def start_switch (event):
        OrangeProactive(event.connection)
    
    core.openflow.addListenerByName("ConnectionUp", start_switch)
    log.info("--- ORANGE2 PROACTIVE CONTROLLER: ONLINE ---")
