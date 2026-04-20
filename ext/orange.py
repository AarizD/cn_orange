from pox.core import core
import pox.openflow.libopenflow_01 as of

# Initialize the logger
log = core.getLogger()

class OrangeLogic (object):
    def __init__ (self, connection):
        self.connection = connection
        # Listen to events (like PacketIn) from this specific switch
        connection.addListeners(self)
        log.info("Switch %s connected. Orange Logic active.", connection.dpid)

        # STATIC MAPPING: Matches the default Mininet MACs for a 3-host topo
        # Format: MAC Address -> Switch Port
        self.mapping = {
            '00:00:00:00:00:01': 1,
            '00:00:00:00:00:02': 2,
            '00:00:00:00:00:03': 3
        }

    def _handle_PacketIn (self, event):
        """
        This function is called every time the switch receives a packet 
        it doesn't know how to handle.
        """
        packet = event.parsed
        dst_mac = str(packet.dst)

        # Check if the destination is in our known Orange Table
        if dst_mac in self.mapping:
            out_port = self.mapping[dst_mac]
            
            # Create a Flow Modification message (The "Action")
            msg = of.ofp_flow_mod()
            
            # Set the "Match": Match based on the incoming packet's details
            msg.match = of.ofp_match.from_packet(packet)
            
            # Set the "Action": Send the packet out of the mapped port
            msg.actions.append(of.ofp_action_output(port = out_port))
            
            # Send the rule to the switch
            self.connection.send(msg)
            
            log.info("INSTALLED RULE: Destination %s -> Port %i", dst_mac, out_port)
        else:
            # If the destination is unknown, flood the packet (Standard SDN Fallback)
            msg = of.ofp_packet_out()
            msg.data = event.ofp
            msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
            self.connection.send(msg)

def launch ():
    """
    The entry point that POX calls when you run 'python3 pox.py orange'
    """
    def start_switch (event):
        # Create an instance of our logic for every switch that connects
        OrangeLogic(event.connection)

    # Listen for the 'ConnectionUp' event (when the switch connects to POX)
    core.openflow.addListenerByName("ConnectionUp", start_switch)
    
    log.info("--- ORANGE CONTROLLER IS READY ---")
