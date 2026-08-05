class Database:

    def load(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def update(self, unit: TextUnit):
        raise NotImplementedError