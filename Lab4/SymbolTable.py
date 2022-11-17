from HashTable import HashTable
class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.hash_table=HashTable(size)
    def add(self,key,value):
        return self.hash_table.add(key,value)
    def get(self,key):
        return self.hash_table.get(key)
    def myhash(self,key):
        return self.hash_table.myhash(key)
    def delete(self,key):
        return self.hash_table.delete(key)
    def __str__(self):
        return "SymbolTable:"+str(self.hash_table)
