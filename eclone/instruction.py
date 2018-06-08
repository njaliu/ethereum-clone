import six

class Instruction:
    def __init__(self, inst_str):
        self.inst = inst_str

    def get_inst_str(self):
        return self.inst

    # aliu [address: storage address, access: read (SLOAD) or write (SSTORE)]
    def set_storage_access(self, address, access):
        self.storage = address
        self.access = access

    def get_storage_access(self):
        return {"storage": self.storage, "access": self.access}

    # aliu: recipient of a CALL instruction
    def set_recipient(self, call_recipient):
        self.recipient = call_recipient

    def get_recipient(self):
        return self.recipient

    def display(self):
        six.print_(self.inst)
        if hasattr(self, 'storage'):
            six.print_("[storage]: " + str(self.storage) + ", " + str(self.access))
        if hasattr(self, 'recipient'):
            six.print_("[recipient]: " + str(self.recipient))