from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

mac_to_port = {}
paths = {}

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    if packet.type == 0x88cc:
        return

    src = str(packet.src)
    dst = str(packet.dst)
    dpid = event.connection.dpid
    in_port = event.port

    mac_to_port.setdefault(dpid, {})
    mac_to_port[dpid][src] = in_port

    if dst in mac_to_port[dpid]:
        out_port = mac_to_port[dpid][dst]
    else:
        out_port = of.OFPP_FLOOD

    key = (src, dst)
    if key not in paths:
        paths[key] = []
    if dpid not in paths[key]:
        paths[key].append(dpid)

    log.info("Path %s -> %s : %s", src, dst, paths[key])

    # 🔥 SEND PACKET
    msg = of.ofp_packet_out()
    msg.data = event.ofp
    msg.in_port = in_port
    msg.actions.append(of.ofp_action_output(port=out_port))
    event.connection.send(msg)

    # install flow
    if out_port != of.OFPP_FLOOD:
        flow = of.ofp_flow_mod()
        flow.match = of.ofp_match.from_packet(packet, in_port)
        flow.idle_timeout = 10
        flow.hard_timeout = 30
        flow.actions.append(of.ofp_action_output(port=out_port))
        event.connection.send(flow)

def launch():
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
    log.info("Path tracing controller started")