
# Enunciado
# Implementar las siguientes dos funciones:
# add(int m)
# check(int n)

# add(m) recibe un integer m y lo guarda en memoria.
# check(n) recibe un integer n. Devuelve true si y sólo si existen dos elementos a y b que fueron previamente agregados usando add() tal que, sumados, son iguales a n. Si no, devuelve false.

# Flujo esperado del ejercicio

# El primer objetivo es que el candidato pueda resolver el ejercicio sin importar si es con la solución óptima. Cualquiera sea la solución a la que se llegó, evaluar si el candidato tiene noción de la complejidad runtime. Está OK ayudar al candidato. El mejor escenario posible es que el candidato lo pueda explicar solo; está bien si lo puede hacer con ayuda; el peor escenario es que, ni siquiera con ayuda, lo pueda entender.
# Asumiendo que la solución no es la óptima, una vez que el candidato entienda que la complejidad es mejorable, iterar la solución para encontrar una mejor.
# Pedirle al candidato que valide que su solución funciona como se espera. El objetivo es que el candidato sepa cómo hacer esa validación, por ejemplo, escribiendo tests unitarios. Pedirle que piense algunos casos de prueba y pedirle que escriba o que detalle cómo haría 1 ó 2 tests.
# Si eventualmente el candidato llegara a la solución óptima muy rápidamente, se puede seguir complejizando el enunciado durante el tiempo que reste para extraer la mayor información posible sobre el candidato. Por ejemplo, pedirle que implemente la solución multi-threaded. 
import pytest

class CustomStore():
    def __init__(self):
        self.store: dict[int, int] = {}
        pass

    def add(self, m: int):
        if self.store.get(m) is not None:
            self.store[m] += 1
        else:
            self.store[m] = 1

    def check(self, n: int) -> bool:
        for a in self.store:
            b = n - a
            if (b == a):
                if (self.store[a] > 1):
                    return True
            else:
                if self.store.get(b) is not None:
                    return True
        return False

def test_cases():
    customStore = CustomStore()
    assert customStore.check(4) is False
    customStore.add(1)
    customStore.add(3)
    assert customStore.check(4)
    assert customStore.check(5) is False
    assert customStore.check(2) is False
    customStore.add(5)
    customStore.add(5)
    assert customStore.check(10)


