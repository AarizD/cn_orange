from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class OrangeController (object):
  def __init__ (self, connection):
    self.connection = connection
    connection.addListeners(self)

    # STATIC MAPPING: Define paths to satisfy "Orange" static routing
    # Host MAC -> Switch Port
    self.static_table = {
        '00:00:00:00:00:01': 1,
        '00:00:00:00:00:02': 2,
        '00:00:00:00:00:03': 3
    }

  def _handle_PacketIn (self, event):
    packet = event.parsed
    dst_mac = str(packet.dst)

    # Scenario 1: Allowed Traffic (Static Routing)
    if dst_mac in self.static_table:
      out_port = self.static_table[dst_mac]
      
      # Match-Action Rule Design
      msg = of.ofp_flow_mod()
      msg.match = of.ofp_match.from_packet(packet)
      msg.actions.append(of.ofp_action_output(port = out_port))
      
      self.connection.send(msg)
      log.info("INSTALLED FLOW: Destination %s -> Output Port %i", dst_mac, out_port)
    
    # Scenario 2: Blocking Logic (Optional differentiator)
    # If a destination isn't in our static map, we could explicitly drop it
    else:
      log.warning("BLOCKED: Unknown destination %s", dst_mac)

def launch ():
  def start_switch (event):
    log.info("Switch %s has connected.", event.dpid)
    OrangeController(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
