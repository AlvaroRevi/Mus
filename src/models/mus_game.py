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
    
    # Orden de cartas para comparaciones (de mayor a menor)
    ORDEN_CARTAS = ['R', 'C', 'S', '7', '6', '5', '4', 'A']

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

    def calcular_probabilidad_mano(self, mano):
        """
        Calcula la probabilidad de obtener una mano específica
        """
        count = Counter(mano)
        ways = 1

        for card, qty in count.items():
            ways *= comb(self.MAZO_CARTAS[card], qty)

        return ways / self.manos_totales

    def calcular_puntos_mano(self, mano):
        """
        Calcula los puntos de juego de una mano
        """
        return sum(self.VALOR_CARTAS[c] for c in mano)

    def calcular_pares(self, mano):
        """
        Clasifica el tipo de jugada (Pares)
        """
        conteo = Counter(mano)
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

    def ordenar_mano_para_grandes(self, mano):
        """
        Ordena una mano de mayor a menor para comparar en Grandes
        """
        return sorted(mano, key=lambda x: self.ORDEN_CARTAS.index(x))

    def ordenar_mano_para_chica(self, mano):
        """
        Ordena una mano de menor a mayor para comparar en Chica
        """
        return sorted(mano, key=lambda x: self.ORDEN_CARTAS.index(x), reverse=True)

    def comparar_grandes(self, mano1, mano2):
        """
        Compara dos manos para Grandes
        Retorna: 1 si mano1 > mano2, -1 si mano1 < mano2, 0 si empate
        """
        cartas1 = self.ordenar_mano_para_grandes(mano1)
        cartas2 = self.ordenar_mano_para_grandes(mano2)

        for c1, c2 in zip(cartas1, cartas2):
            pos1 = self.ORDEN_CARTAS.index(c1)
            pos2 = self.ORDEN_CARTAS.index(c2)
            if pos1 < pos2:
                return 1
            elif pos1 > pos2:
                return -1
        return 0

    def comparar_chica(self, mano1, mano2):
        """
        Compara dos manos para Chica
        Retorna: 1 si mano1 > mano2, -1 si mano1 < mano2, 0 si empate
        """
        cartas1 = self.ordenar_mano_para_chica(mano1)
        cartas2 = self.ordenar_mano_para_chica(mano2)

        for c1, c2 in zip(cartas1, cartas2):
            pos1 = self.ORDEN_CARTAS.index(c1)
            pos2 = self.ORDEN_CARTAS.index(c2)
            if pos1 > pos2:  # En chica, menor valor es mejor
                return 1
            elif pos1 < pos2:
                return -1
        return 0

    def obtener_valor_juego(self, mano):
        """
        Obtiene el valor de juego según las reglas: 31>32>40>37>36>35>34>33>30>29...
        """
        puntos = self.calcular_puntos_mano(mano)
        
        # Orden de preferencia para juego (completo)
        orden_juego = [31, 32, 40, 37, 36, 35, 34, 33, 30, 29, 28, 27,
                       26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11,
                       10, 9, 8, 7, 6, 5, 4]
        
        if puntos in orden_juego:
            return orden_juego.index(puntos)  # Retorna la posición en el array
        else:
            return float('inf')  # No debería ocurrir con puntos válidos

    def comparar_juego(self, mano1, mano2):
        """
        Compara dos manos para Juego
        Retorna: 1 si mano1 > mano2, -1 si mano1 < mano2, 0 si empate
        """
        valor1 = self.obtener_valor_juego(mano1)
        valor2 = self.obtener_valor_juego(mano2)
        
        # Comparar posiciones en el array (menor posición = mejor juego)
        if valor1 < valor2:
            return 1
        elif valor1 > valor2:
            return -1
        else:
            return 0

    def calcular_ranking_grandes(self, manos):
        """
        Calcula el ranking para Grandes
        """
        manos_list = list(manos)
        manos_list.sort(key=lambda x: [self.ORDEN_CARTAS.index(c) for c in self.ordenar_mano_para_grandes(x)])

        ranking = {}
        posicion = 1

        for i, mano in enumerate(manos_list):
            if i == 0:
                ranking[mano] = posicion
            else:
                if self.comparar_grandes(mano, manos_list[i-1]) == 0:
                    # Empate, misma posición
                    ranking[mano] = ranking[manos_list[i-1]]
                else:
                    # Nueva posición
                    posicion = i + 1
                    ranking[mano] = posicion

        return ranking

    def calcular_ranking_chica(self, manos):
        """
        Calcula el ranking para Chica
        """
        manos_list = list(manos)
        # Ordenar por chica: de menor a mayor (A es la mejor carta para chica)
        manos_list.sort(key=lambda x: [self.ORDEN_CARTAS.index(c) for c in self.ordenar_mano_para_chica(x)], reverse=True)
        
        ranking = {}
        posicion_actual = 1
        
        for i, mano in enumerate(manos_list):
            if i == 0:
                ranking[mano] = posicion_actual
            else:
                if self.comparar_chica(mano, manos_list[i-1]) == 0:
                    # Empate, misma posición
                    ranking[mano] = ranking[manos_list[i-1]]
                else:
                    # Nueva posición (siguiente número consecutivo)
                    posicion_actual = ranking[manos_list[i-1]] + 1
                    ranking[mano] = posicion_actual
                
        return ranking

    def calcular_ranking_pares(self, manos):
        """
        Calcula el ranking para Pares
        """
        manos_list = list(manos)
        manos_list.sort(key=lambda x: self.obtener_valor_par(x))

        ranking = {}
        posicion = 1

        for i, mano in enumerate(manos_list):
            if i == 0:
                ranking[mano] = posicion
            else:
                if self.comparar_pares(mano, manos_list[i-1]) == 0:
                    # Empate, misma posición
                    ranking[mano] = ranking[manos_list[i-1]]
                else:
                    # Nueva posición
                    posicion = posicion + 1
                    ranking[mano] = posicion

        return ranking

    def calcular_ranking_juego(self, manos):
        """
        Calcula el ranking para Juego
        """
        manos_list = list(manos)
        manos_list.sort(key=lambda x: self.obtener_valor_juego(x))

        ranking = {}
        posicion = 1
        for i, mano in enumerate(manos_list):
            if i == 0:
                ranking[mano] = posicion
            else:
                if self.comparar_juego(mano, manos_list[i-1]) == 0:
                    # Empate, misma posición
                    ranking[mano] = ranking[manos_list[i-1]]
                else:
                    # Nueva posición
                    posicion = posicion + 1
                    ranking[mano] = posicion
                    
        return ranking

    def obtener_valor_par(self, mano):
        """
        Obtiene el valor de la pareja para comparar en Pares
        Retorna: (tipo_par, valor_carta_principal, valor_carta_secundaria)
        """
        conteo = Counter(mano)
        repeticiones = sorted(conteo.values(), reverse=True)
        
        if repeticiones == [4]:
            # Duples de 4 iguales
            carta_par = max(conteo.keys(), key=lambda x: conteo[x])
            return (0, self.ORDEN_CARTAS.index(carta_par), self.ORDEN_CARTAS.index(carta_par))  # No hay segunda carta
        
        elif repeticiones == [2, 2]:
            # Duples de 2 pares
            pares = [carta for carta, count in conteo.items() if count == 2]
            # Ordenar los pares por valor (mejor carta primero)
            pares_ordenados = sorted(pares, key=lambda x: self.ORDEN_CARTAS.index(x))
            carta_principal = pares_ordenados[0]  # Mejor par
            carta_secundaria = pares_ordenados[1]  # Segundo par
            return (0, self.ORDEN_CARTAS.index(carta_principal), self.ORDEN_CARTAS.index(carta_secundaria))
        
        elif repeticiones == [3, 1]:
            # Medias
            carta_par = max(conteo.keys(), key=lambda x: conteo[x])
            # La carta secundaria es la carta suelta
            carta_suelta = min(conteo.keys(), key=lambda x: conteo[x])
            return (1, self.ORDEN_CARTAS.index(carta_par), float('inf'))
        
        elif repeticiones == [2, 1, 1]:
            # Par
            carta_par = max(conteo.keys(), key=lambda x: conteo[x])
            return (2, self.ORDEN_CARTAS.index(carta_par), float('inf'))
        
        else:
            # Nada - todas las manos sin pares están empatadas
            return (3, float('inf'), float('inf'))

    def comparar_pares(self, mano1, mano2):
        """
        Compara dos manos para Pares
        Retorna: 1 si mano1 > mano2, -1 si mano1 < mano2, 0 si empate
        """
        valor1 = self.obtener_valor_par(mano1)
        valor2 = self.obtener_valor_par(mano2)
        
        # Comparar tipo de par primero
        if valor1[0] < valor2[0]:
            return 1
        elif valor1[0] > valor2[0]:
            return -1
        else:
            # Mismo tipo de par
            if valor1[0] == 3:
                # Si ambas son "Nada", están empatadas
                return 0
            elif (valor1[0] == 2 or valor1[0] == 1):
                # Si ambas son "Par" o "Medias", ganan los mas grandes
                if valor1[1] < valor2[1]:
                    return 1
                elif valor1[1] > valor2[1]:
                    return -1
                else:
                    # Si ambas son "Par" con misma carta principal, empate
                    return 0
            else:
                # Si ambas son "Duples", ganan las cartas con mayor valor
                if valor1[1] < valor2[1]:
                    return 1
                elif valor1[1] > valor2[1]:
                    return -1
                else:
                    # Si ambas son "Duples" con misma carta principal, se mira la secundaria
                    if valor1[2] < valor2[2]:
                        return 1
                    elif valor1[2] > valor2[2]:
                        return -1
                    else:
                        # Si ambas son "Duples" con misma carta principal y segunda, empate
                        return 0


    def generar_matriz_probabilidades(self):
        """
        Genera el DataFrame con todas las manos y sus características
        """
        set_manos = self.generar_manos()
        data_manos = []

        # Calcular rankings para cada lance
        ranking_grandes = self.calcular_ranking_grandes(set_manos)
        ranking_chica = self.calcular_ranking_chica(set_manos)
        ranking_pares = self.calcular_ranking_pares(set_manos)
        ranking_juego = self.calcular_ranking_juego(set_manos)

        for mano in set_manos:
            prob = self.calcular_probabilidad_mano(mano)
            points = self.calcular_puntos_mano(mano)
            pair_type = self.calcular_pares(mano)

            data_manos.append({
                'Mano': mano,
                'Probabilidad': prob,
                'Puntos_de_juego': points,
                'Pares': pair_type,
                'Ranking_Grandes': ranking_grandes[mano],
                'Ranking_Chica': ranking_chica[mano],
                'Ranking_Pares': ranking_pares[mano],
                'Ranking_Juego': ranking_juego[mano]
            })

        df = pd.DataFrame(data_manos)
        df = df.sort_values(by="Probabilidad", ascending=False).reset_index(drop=True)

        return df