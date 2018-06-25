import six

class BirthMark:
    '''
    aliu: embedding vector for a birthmark of a block
    '''
    def __init__(self, pc_cantor, def_cantor, use_cantor, call_count, du_cantor, uu_cantor, update_call, use_call, call_finalize):
        self.path_condition_mark = pc_cantor
        self.def_mark = def_cantor
        self.use_mark = use_cantor
        self.call_mark = call_count
        self.du_mark = du_cantor
        self.uu_mark = uu_cantor
        self.update_call_mark = update_call
        self.use_call_mark = use_call
        self.call_finalize_mark = call_finalize

    def get_path_condition_mark(self):
        return self.path_condition_mark

    def get_def_mark(self):
        return self.def_mark

    def get_use_mark(self):
        return self.use_mark

    def get_call_mark(self):
        return self.call_mark

    def get_du_mark(self):
        return self.du_mark

    def get_uu_mark(self):
        return self.uu_mark

    def get_update_call_mark(self):
        return self.update_call_mark

    def get_use_call_mark(self):
        return self.use_call_mark

    def get_call_finalize_mark(self):
        return self.call_finalize_mark

    def get_vector(self):
        return [self.path_condition_mark, self.def_mark, self.use_mark, self.call_mark, self.du_mark, self.uu_mark, self.update_call_mark, self.use_call_mark, self.call_finalize_mark]
    '''
    def display(self):
        six.print_(self.inst)
        if hasattr(self, 'storage'):
            six.print_("[storage]: " + str(self.storage) + ", " + str(self.access))
        if hasattr(self, 'recipient'):
            six.print_("[recipient]: " + str(self.recipient))
    '''