from itertools import combinations
from math import comb
from collections import Counter
import pandas as pd


class MusGame:
    """
    Clase principal para manejar la lógica del juego de Mus
    """

    # Mazo real del mus: 40 cartas (sin 8s ni 9s), con valores equivalentes
    MAZO_CARTAS = {
        'R': 8,  # Reyes (3s)
        'C': 4,
        'S': 4,
        'A': 8,  # Ases (2s)
        '7': 4,
        '6': 4,
        '5': 4,
        '4': 4
    }

    # Valores para puntos de juego
    VALOR_CARTAS = {'R': 10, 'C': 10, 'S': 10, 'A': 1, '7': 7, '6': 6, '5': 5, '4': 4}

    def __init__(self):
        self.manos_totales = comb(40, 4)  # Total de combinaciones posibles

    def generar_manos(self):
        """
        Genera todas las combinaciones únicas de 4 cartas
        """
        resultados = set()
        cartas = []

        for carta, count in self.MAZO_CARTAS.items():
            cartas.extend([carta] * count)

        # Generamos todas las combinaciones posibles de 4 cartas del mazo sin reemplazo
        for combi in combinations(range(len(cartas)), 4):
            mano = [cartas[i] for i in combi]
            mano_ordenada = ''.join(sorted(mano, key=lambda x: "RCS7654A".index(x)))
            resultados.add(mano_ordenada)

        return resultados

    def calcular_probabilidad_mano(self, hand):
        """
        Calcula la probabilidad de obtener una mano específica
        """
        count = Counter(hand)
        ways = 1

        for card, qty in count.items():
            ways *= comb(self.MAZO_CARTAS[card], qty)

        return ways / self.manos_totales

    def calcular_puntos_mano(self, hand):
        """
        Calcula los puntos de juego de una mano
        """
        return sum(self.VALOR_CARTAS[c] for c in hand)

    def calcular_pares(self, hand):
        """
        Clasifica el tipo de jugada (Pares)
        """
        conteo = Counter(hand)
        repeticiones = sorted(conteo.values(), reverse=True)

        if repeticiones == [4]:
            return "Duples"
        elif repeticiones == [2, 2]:
            return "Duples"
        elif repeticiones == [3, 1]:
            return "Medias"
        elif repeticiones == [2, 1, 1]:
            return "Par"
        else:
            return "Nada"

    def generar_matriz_probabilidades(self):
        """
        Genera el DataFrame con todas las manos y sus características
        """
        set_manos = self.generar_manos()
        data_manos = []

        for mano in set_manos:
            prob = self.calcular_probabilidad_mano(mano)
            points = self.calcular_puntos_mano(mano)
            pair_type = self.calcular_pares(mano)

            data_manos.append({
                'Mano': mano,
                'Probabilidad': prob,
                'Puntos_de_juego': points,
                'Pares': pair_type
            })

        df = pd.DataFrame(data_manos)
        df = df.sort_values(by="Probabilidad", ascending=False).reset_index(drop=True)

        return df