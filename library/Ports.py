import serial.tools.list_ports


class Ports:
    def __init__(self):
        self.dict = {}

    def update(self, detail=False):
        ports = serial.tools.list_ports.comports()
        if not detail:
            for p in ports: self.dict[p.hwid] = p.device
        else:
            self.details = {'device': [], 'description': [], 'hwid': [], 'vid': [], 'pid': [], 'serial_number': [],
                            'location': []}
            for p in ports:
                self.details['device'].append(p.device)
                self.details['description'].append(p.description)
                self.details['hwid'].append(p.hwid)
                self.details['vid'].append(p.vid)
                self.details['pid'].append(p.pid)
                self.details['serial_number'].append(p.serial_number)
                self.details['location'].append(p.location)

    def print(self, prefix='', detail=False):
        self.update(detail=detail)
        if not detail:
            keys = self.dict.keys()
            if not keys: print('<No ports found>')
            for k in keys: print(prefix, k, self.dict[k])
        else:
            print('Device \t\t Hardware ID')
            print('-------\t\t------------')
            for i in range(len(self.details['serial_number'])):
                print(self.details['device'][i], end=' |\t')
                print(self.details['hwid'][i])

    def get_port(self, device):
        self.update()
        keys = self.dict.keys()
        for k in keys:
            if device in k: return self.dict[k]
        return None

    def get_ports(self, devices):
        self.update()
        keys = self.dict.keys()
        found = []
        for k in keys:
            for d in devices:
                if d in k: found.append(self.dict[k])
        return found


def get_port(device):
    ports = Ports()
    port = ports.get_port(device)
    return port


