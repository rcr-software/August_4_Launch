from xbee import XBee, ZigBee
import serial
import time

def data_callback(data):
    print(data)


class radio():
    def __init__(self, baudrate=9800):
        self.baudrate = baudrate
        self.serial = serial.Serial('/dev/ttyAMA0', baudrate)
        self.xbee = XBee(self.serial, callback=data_callback)

    def __str__(self):
        return "---Radio Information---\nSerial Port: " + str(self.serial) + "\nXbee: " + str(self.xbee)

    def __enter__(self):
        return self

    def __exit__(self):
        self.xbee.halt()
        self.serial.close()

    def Escape(self, msg):
        escaped = bytearray()
        reserved = bytearray(b"\x7E\x7D\x11\x13")

        escaped.append(msg[0])
        for m in msg[1:]:
            if m in reserved:
                escaped.append(0x7D)
                escaped.append(m ^ 0x20)
            else:
                escaped.append(m)

        return escaped

    def format(self, msg):
        return " ".join("{:02x}".format(b) for b in msg)

    def Send(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
        if not msg:
            return 0

        hexs = "7E 00 {:02X} 01 {:02X} {:02X} {:02X} {:02X}".format(
            len(msg) + 5,          # LSB (length)
            frameid,
            (addr & 0xFF00) >> 8,  # Destination address high byte
            addr & 0xFF,           # Destination address low byte
            options
            )

        frame = bytearray.fromhex(hexs)

        # Append message content
        frame.extend(msg)

        # Calculate checksum byte
        frame.append(0xFF - (sum(frame[3:]) & 0xFF))

        # Escape any btes containing reserved characters
        frame = self.Escape(frame)

        print("Tx: " + self.format(frame))
        self.serial.write(frame)
        self.serial.close()
        print("test")
        return 1

    def sendString(self, msg, addr=0xFFFF, options=0x01, frameid=0x00):
        return self.Send(msg.encode('utf-8'), addr, options, frameid)

    def Validate(self, msg):
        # 9 bytes in Minimum length to be a valid Rx frame
        # LSB, MSB, Type, Source Address(2), RSSI
        # Options, 1 byte data, checksum
        if(len(msg) - msg.count(bytes(b'0x7D'))) < 9:
            return False

        # All bytes in message must be unescaped before validating content
        frame = self.Unescape(msg)

        LSB = frame[1]

        # Frame(minus checksum) must contain at least length equal to LSB
        if LSB > (len(frame[2:]) - 1):
            return False

        # Validate checksum
        if (sum(frame[2:3+LSB]) & 0xFF) != 0xFF:
            return False

        print("Rx: " + self.format(bytearray(b'\x7E') + msg))
        self.RxMessages.append(frame)
        return True

    def Unescape(self, msg):
        if msg[-1] == 0x7D:
            # Last byte indicates an escape, can't unescape that
            return None

        out = bytearray()
        skip = False
        for i in range(len(msg)):
            if skip:
                skip = False
                continue

            if msg[i] == 0x7D:
                out.append(msg[i+1] ^ 0x20)
                skip = True
            else:
                out.append(msg[i])

        return out

    def Receive(self):
        x = self.serial.readline()
        print x, "test"
        
    def data_callback(self, data):
        print data

    def Receive(self):
        remaining = self.serial.inWaiting()
        
        while remaining:
            chunk = self.serial.read(remaining)
            remaining -= len(chunk)
            self.RxBuff.extend(chunk)

        msgs = self.RxBuff.split(bytes(b'\x7E'))
        for msg in msgs[:-1]:
            self.Validate(msg)

        self.RxBuff = (bytearray() if self.Validate(msgs[-1]) else msgs[-1])

        if self.RxMessages:
            return self.RxMessages.popleft()
        else:
            return None

    def run(self):
        self.xbee.run()

def main():
    xbee = radio()
"""    print(xbee)
    while True:
        print("Receiving... ")
        xbee.Receive()
        print("WAIT")
        time.sleep(0.25)"""

main()

"""
    def recieve(self):
        while True:
            try:
                time.sleep(0.0001) #print self.xbee.wait_read_frame()
            except KeyboardInterrupt:
                break

"""
