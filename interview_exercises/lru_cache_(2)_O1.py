# Implementá una clase LRUCache con capacidad fija capacity, que soporte:


# Ambas operaciones tienen que correr en O(1).

# Arrancá cuando quieras — pensá en voz alta qué estructura necesitás antes de escribir código.

class Node():
    def __init__(self, key: int, value: int):
        self.key: int = key
        self.value: int = value
        self.prev: Node = None
        self.next: Node = None

class LRUCache():
    def __init__(self, capacity: int):
        self.capacity: int = capacity
        self.store: dict[int, Node] = {}
        self.head: Node = Node(0, 0)
        self.tail: Node = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def move_to_head(self, x: Node):
        x.next = self.head.next
        x.prev = self.head
        self.head.next.prev = x
        self.head.next = x

    def remove(self, x: Node):
        x.prev.next = x.next
        x.next.prev = x.prev

    def get(self, key: int) -> int:
    # get(key: int) -> int: devuelve el valor asociado a key si existe, o -1 si no. Además, marca a key como usada recientemente.
        if self.store.get(key) is not None:
            self.remove(self.store.get(key))
            self.move_to_head(self.store.get(key))
            return self.store[key].value
        else:
            return -1

    def put(self, key: int, value: int):
    # put(key: int, value: int) -> None: inserta o actualiza el valor de key. Si al insertar se supera la capacity, hay que descartar el elemento usado menos recientemente antes de agregar el nuevo.
        if (self.store.get(key) is not None):
            node: Node = self.store.get(key)
            node.value = value
            self.remove(node)
            self.move_to_head(node)
            return
        
        if (len(self.store) < self.capacity):
            node: Node = Node(key, value)
            self.store[key] = node
            self.move_to_head(node)
        else:
            lru_node = self.tail.prev
            self.remove(lru_node)
            self.store.pop(lru_node.key)
            node: Node = Node(key, value)
            self.store[key] = node
            self.move_to_head(node)

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

        
