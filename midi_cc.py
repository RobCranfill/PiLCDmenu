#!/usr/bin/python3
# Being a thing what encapsulates the name of a drum kit, and the corresponding MIDI Control Code.
#
import json

class MidiCC:
    """
    Being a thing what encapsulates the name of a drum kit, and the corresponding MIDI Control Code.
    """
    def __init__(self, kitname, controlcode):
        self.kitName = kitname
        self.controlCode = controlcode

    def __str__(self):
        """This is the method that the menu code will use to render each item.
        """
        return self.kitName

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def decodeFromJSON(s):
        """
        Load the JSON data (in the form of a string) into a list of lists of MidiCC objects.
        """
        result = []
        for i in json.loads(s):
            pageName = i[0]
            print(f"Name is {pageName}")
            result.append(i[1])
            for k in i[1]:
                sublist.append(MidiCC(k[0], k[1]))
        return result


# Test code.
# The input file should look something like this,
#  a list of lists of tuples of a string (the kit name) and an integer (the MIDI control code).
#
# [
#   [
#     "Rock Kit", [["Rock01", 69], ["Rock02", 58], ["Rock03", 59], ["Rock04", 60], ["Rock05", 61], ["Rock06", 62]]
#   ],
#   [
#     "Techno", [["Techno01", 78], ["Techno02", 79], ["Techno03", 80], ["Techno04", 81], ["Techno05", 82]]
#   ]
# ]
#
if __name__ =="__main__":
    filename = "sr18_small_example.json"
    print(f"Testing parsing JSON file '{filename}'....")
    f = open(filename, "r")
    fcontents = f.read()
    # print(f" read: {fcontents}\n")
    # print(f" json: {json.loads(fcontents)}\n")
    newlist = MidiCC.decodeFromJSON(fcontents)

    print("Parsed:")
    print(newlist)
