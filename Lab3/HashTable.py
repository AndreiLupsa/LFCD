
class HashTable:
    def __init__(self, size):
        self.size = size
        self.hash_table = [[] for _ in range(self.size)]
    def myhash(self,key):
        return sum(ord(ch) for ch in str(key)) % self.size  

    def add(self, key, val):
        hashed_key = self.myhash(key) 
        bucket = self.hash_table[hashed_key]
        found_key = False
        for (index, record) in enumerate(bucket):
            (record_key, record_val) = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket[index] = (key, val)
        else:
            bucket.append((key, val))
    def get(self, key):
        hashed_key = self.myhash(key)
        bucket = self.hash_table[hashed_key]
        found_key = False
        for (index, record) in enumerate(bucket):
            (record_key, record_val) = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            return record_val
        else:
            return "No record found"
  
    def delete(self, key):
        hashed_key = self.myhash(key) 
        bucket = self.hash_table[hashed_key]
        found_key = False
        for (index, record) in enumerate(bucket):
            (record_key, record_val) = record
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return
    def __str__(self):
        return "".join(str(item)+"\n" for item in self.hash_table)
  


