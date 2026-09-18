class Node:
    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, Node] = {}  # key -> nodo, acceso O(1)

        # head y tail son centinelas: nodos vacíos que marcan los dos extremos.
        # Todo nodo "real" vive entre ellos. head.next = el más reciente.
        # tail.prev = el menos reciente (el próximo a desalojar).
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        # desengancha 'node' de donde esté, conectando sus vecinos entre sí
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: Node) -> None:
        # engancha 'node' justo después de head (posición "más reciente")
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            print(f"{key} doesn't exist")
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)  # se usó -> pasa a ser la más reciente
        print(f"Moved {node.key} to the front")
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            print(f"Moved {node.key} to the front")
            return

        if len(self.cache) >= self.capacity:
            lru_node = self.tail.prev       # el pegado a tail = el menos reciente
            self._remove(lru_node)
            del self.cache[lru_node.key]
            print(f"Removed {lru_node.key}")

        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_to_front(new_node)
        print(f"Added {new_node.key} to the front")


def test_cases():
    cache = LRUCache(2)          # capacidad 2
    cache.put(1, "a")
    cache.put(2, "b")
    cache.get(1) == "a"     # 1 pasa a ser el más "reciente"
    cache.put(3, "c")            # se llena la capacidad -> se descarta 2 (el menos usado recientemente)
    cache.get(2) == -1      # ya no está
    cache.get(3) == "c"