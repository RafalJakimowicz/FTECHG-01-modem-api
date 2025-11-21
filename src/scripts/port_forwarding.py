from ..api.FiberTechnicAPI import FiberTechnicAPI
import json

class VirtualServer(FiberTechnicAPI):
    def __init__(self, ip:str, username:str, password:str):
        super().__init__(ip, username, password)
        #self.SESSION = self.login_and_get_session()
        self.PROTOCOLS = {
            "TCP": 1,
            "TCP/UDP": 4,
            "UDP": 2
        }

    def get_all_forwarded_ports(self, debug:bool=False) -> dict:
        """
        Gets data about active port forwarding rules ad return json response

        :return: json of device response
        :rtype: dict        
        """

        args = {"module": "port_forwarding"}
        data = self.send_get(args, debug=debug)
        if debug:
            print("[DEBUG] Response:")
            print(json.dumps(data, indent=4))
        if  data != None:
            if data.get("code") != 0:
                return None
            
            return data

        else:
            return None
        
        

    def add_port_forwarding(self, 
                            local_port: int, 
                            remote_port: int, 
                            local_ip: str, 
                            comment:str, 
                            protocol:int=4,
                            debug:bool=False) -> bool:
        """
        Adds port forwarding rule to device

        :param int local_port: port of device in local network
        :param int remote_port: external port to be open
        :param str local_ip: ip adress of device in local network in format xxx.xxx.xxx.xxx
        :param str comment: name of forwarded rule
        :param int protocol: (OPTIONAL Default=4) number of protocol (TCP:1, TCP/UDP:4, UDP:2)
        :param bool debug: (OPTIONAL Default=False) if True prints debug info
        :return: True if success, False if something went wrong
        :rtype: bool
        """

        payload_dict = {
            "module": "port_forwarding",
            "modify_type": 0,
            "cur_port_forwarding_tbl": {
                "comment": comment,
                "remote_port": remote_port,
                "protocol": protocol,
                "local_ip": local_ip,
                "local_port": local_port
            }
        }

        data = self.send_post(payload_dict, debug=debug)
        if debug:
            print("[DEBUG] Response:")
            print(json.dumps(data, indent=4))

        if data != None:
            if data.get("code") != 0:
                return False
            
            return True
        
        else:
            return False
