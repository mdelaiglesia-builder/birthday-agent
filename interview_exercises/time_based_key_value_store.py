import bisect

class TimeMap:
    def __init__(self):
        self.timestamps: dict[str, list[int]] = {}
        self.values: dict[str, list[str]] = {}

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.timestamps:
            self.timestamps[key] = []
            self.values[key] = []
        self.timestamps[key].append(timestamp)
        self.values[key].append(value)

    def get(self, key: str, timestamp: int) -> str:
        ts_list = self.timestamps.get(key, [])
        idx = bisect.bisect_right(ts_list, timestamp)
        if idx == 0:
            return ""
        return self.values[key][idx - 1]

def test_various():
    tm = TimeMap()
    tm.set("a", "valor1", 1)
    assert tm.get("a", 1) == "valor1"
    assert tm.get("a", 3) == "valor1"
    tm.set("a", "valor2", 4)
    assert tm.get("a", 4)  == "valor2"
    assert tm.get("a", 5)  == "valor2"