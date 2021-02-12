#!/bin/python3
# Being a thing what encapsulates the name of a drum kit, and the corresponding MIDI Control Code.
#
import json

class MidiCC:
    """
    Being a thing what encapsulates the name of a drum kit, and the corresponding MIDI Control Code.
    """
    def __init__(self, kitname, controlcode=-1):
        self.kitName = kitname
        self.controlCode = controlcode
    def __str__(self):
        return f"CC {self.controlCode}: {self.kitName}"
    def __repr__(self):
        return self.__str__()
    @staticmethod
    def decodeFromJSON(s):
        result = []
        for i in json.loads(s):
            sublist = []
            result.append(sublist)
            for k in i:
                sublist.append(MidiCC(k[0], k[1]))
        return result

# Test code.
# The input file should look something like this:
#
# [
# [
#   ["Rock01", 57], ["Rock02", 58], ["Rock03", 59], ["Rock04", 60], ["Rock05", 61], ["Rock06", 62]
# ],
# [
#  ["Techno01", 78], ["Techno02", 79], ["Techno03", 80], ["Techno04", 81], ["Techno05", 82],
#  ["Techno06", 83], ["Techno07", 84], ["Techno08", 85], ["Techno09", 86]
# ],
# ]
#
if __name__ =="__main__":
    filename = "t1.json"
    print(f"Testing parsing JSON file '{filename}'....")
    f = open(filename, "r")
    fcontents = f.read()
    # print(f" read: {fcontents}\n")
    # print(f" json: {json.loads(fcontents)}\n")
    newlist = MidiCC.decodeFromJSON(fcontents)

    print("Parsed:")
    print(newlist)
