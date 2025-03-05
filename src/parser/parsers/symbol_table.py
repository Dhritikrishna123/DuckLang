class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def set(self, name, value):
        self.symbols[name] = value

    def get(self, name):
        return self.symbols.get(name)

    def dump(self):
        print("\n📄 [Symbol Table Dump]")
        for var, value in self.symbols.items():
            print(f"🔑 {var} = {value}")

    def __repr__(self):
        return str(self.symbols)
