import six

class MetaData:
    '''
    aliu: embedding vector for a basic block
            path_condition: embedding for a path condition (to be refined)
            arithmeticOP: 0s yellow paper
            logicOP: 10s yellow paper
            envOP: 30s yellow paper
            chainOP: 40s yellow paper
            stackOP: 50/60/70/80/90s yellow paper
            memoryProp: based on 50s yellow paper
            storageProp: based on 50s yellow paper
            callProp: based on f0s yellow paper
    '''
    def __init__(self, arithmeticOP, logicOP, envOP, chainOP, stackOP, memoryProp):
        self.arithmetic = arithmeticOP
        self.logic = logicOP
        self.env = envOP
        self.chain = chainOP
        self.stack = stackOP
        self.memory = memoryProp

    def get_arithmetic_value(self):
        return self.arithmetic

    def get_logic_value(self):
        return self.logic

    def get_env_value(self):
        return self.env

    def get_chain_value(self):
        return self.chain

    def get_stack_value(self):
        return self.stack

    def get_memory_value(self):
        return self.memory

    '''
    def display(self):
        six.print_(self.inst)
        if hasattr(self, 'storage'):
            six.print_("[storage]: " + str(self.storage) + ", " + str(self.access))
        if hasattr(self, 'recipient'):
            six.print_("[recipient]: " + str(self.recipient))
    '''