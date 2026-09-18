# Implementá una clase LRUCache con capacidad fija capacity, que soporte:


# Ambas operaciones tienen que correr en O(1).

# Arrancá cuando quieras — pensá en voz alta qué estructura necesitás antes de escribir código.

class LRUCache():
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.store: dict[int, dict[str,int]] = {}
        self.clock: int = 0

    def getTimestamp(self):
        self.clock += 1
        return self.clock

    def get(self, key: int) -> int:
    # get(key: int) -> int: devuelve el valor asociado a key si existe, o -1 si no. Además, marca a key como usada recientemente.
        if self.store.get(key) is not None:
            self.store[key]["timestamp"] = self.getTimestamp()
            return self.store[key]["value"]
        else:
            return -1

    def put(self, key: int, value: int):
    # put(key: int, value: int) -> None: inserta o actualiza el valor de key. Si al insertar se supera la capacity, hay que descartar el elemento usado menos recientemente antes de agregar el nuevo.
        if len(self.store) < self.capacity:
            self.store[key] = {"value": value, "timestamp": self.getTimestamp()}
            return

        less_used_value: dict[str, int] = {"value": 0, "timestamp": self.getTimestamp()}
        less_used_key: int
        for x in self.store:
            if self.store[x]["timestamp"] < less_used_value["timestamp"]:
                less_used_value["value"] = self.store[x]["value"]
                less_used_value["timestamp"] = self.store[x]["timestamp"]
                less_used_key = x
        self.store.pop(less_used_key)
        self.store[key] = {"value": value, "timestamp": self.getTimestamp()}

def test_cases():
    lru_cache = LRUCache(2)
    lru_cache.put(1,2)
    assert len(lru_cache.store) == 1
    assert lru_cache.get(1) == 2
    lru_cache.put(2,3)
    assert len(lru_cache.store) == 2
    assert lru_cache.get(2) == 3
    lru_cache.put(3,4)
    assert len(lru_cache.store) == 2
    assert lru_cache.get(1) == -1
    assert lru_cache.get(2) == 3
    assert lru_cache.get(3) == 4

        
