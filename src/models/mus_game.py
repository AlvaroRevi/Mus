from itertools import combinations
from math import comb
from collections import Counter
import pandas as pd
import random


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
        self.matriz_probabilidades = self.__generar_matriz_probabilidades()

    def analizar_mano(self,mano: str, posicion: int = 1, n_simulaciones: int = 1000):
        """
        Analiza una mano específica en todos los lances y muestra resultados gráficos

        Args:
            mano: String con la mano a analizar (ej. 'RRAA')
            posicion: Posición en la mesa (1-4)
            n_simulaciones: Número de simulaciones a realizar
        """
        # Crear instancia del juego
        mus_game = MusGame()

        # Generar DataFrame con todas las manos
        df_hands = self.matriz_probabilidades

        # Obtener información de la mano
        info_mano = df_hands[df_hands['Mano'] == mano].iloc[0]

        print(f"Análisis de la mano: {mano}")
        print(f"Probabilidad de obtenerla: {info_mano['Probabilidad'] * 100:.4f}%")
        print(f"Puntos de juego: {info_mano['Puntos_de_juego']}")
        print(f"Tipo de pares: {info_mano['Pares']}")
        print("\nRealizando simulaciones Monte Carlo...")

        # Realizar simulación Monte Carlo
        resultados = self.__simular_lances(mano, df_hands, posicion, n_simulaciones)

        # Mostrar resultados
        print("\nResultados de la simulación Monte Carlo:")
        for lance in resultados:
            print(f"\n{lance.capitalize()}:")
            print(f"  Victoria individual: {resultados[lance]['prob_victoria_individual'] * 100:.2f}%")
            print(f"  Victoria en equipo: {resultados[lance]['prob_victoria_equipo'] * 100:.2f}%")

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

    def __generar_manos(self):
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

    def __calcular_puntos_mano(self, mano):
        """
        Calcula los puntos de juego de una mano
        """
        return sum(self.VALOR_CARTAS[c] for c in mano)

    def __calcular_pares(self, mano):
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

    def __ordenar_mano_para_grandes(self, mano):
        """
        Ordena una mano de mayor a menor para comparar en Grandes
        """
        return sorted(mano, key=lambda x: self.ORDEN_CARTAS.index(x))

    def __ordenar_mano_para_chica(self, mano):
        """
        Ordena una mano de menor a mayor para comparar en Chica
        """
        return sorted(mano, key=lambda x: self.ORDEN_CARTAS.index(x), reverse=True)

    def __comparar_grandes(self, mano1, mano2):
        """
        Compara dos manos para Grandes
        Retorna: 1 si mano1 > mano2, -1 si mano1 < mano2, 0 si empate
        """
        cartas1 = self.__ordenar_mano_para_grandes(mano1)
        cartas2 = self.__ordenar_mano_para_grandes(mano2)

        for c1, c2 in zip(cartas1, cartas2):
            pos1 = self.ORDEN_CARTAS.index(c1)
            pos2 = self.ORDEN_CARTAS.index(c2)
            if pos1 < pos2:
                return 1
            elif pos1 > pos2:
                return -1
        return 0

    def __comparar_chica(self, mano1, mano2):
        """
        Compara dos manos para Chica
        Retorna: 1 si mano1 > mano2, -1 si mano1 < mano2, 0 si empate
        """
        cartas1 = self.__ordenar_mano_para_chica(mano1)
        cartas2 = self.__ordenar_mano_para_chica(mano2)

        for c1, c2 in zip(cartas1, cartas2):
            pos1 = self.ORDEN_CARTAS.index(c1)
            pos2 = self.ORDEN_CARTAS.index(c2)
            if pos1 > pos2:  # En chica, menor valor es mejor
                return 1
            elif pos1 < pos2:
                return -1
        return 0

    def __obtener_valor_juego(self, mano):
        """
        Obtiene el valor de juego según las reglas: 31>32>40>37>36>35>34>33>30>29...
        """
        puntos = self.__calcular_puntos_mano(mano)
        
        # Orden de preferencia para juego (completo)
        orden_juego = [31, 32, 40, 37, 36, 35, 34, 33, 30, 29, 28, 27,
                       26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11,
                       10, 9, 8, 7, 6, 5, 4]
        
        if puntos in orden_juego:
            return orden_juego.index(puntos)  # Retorna la posición en el array
        else:
            return float('inf')  # No debería ocurrir con puntos válidos

    def __comparar_juego(self, mano1, mano2):
        """
        Compara dos manos para Juego
        Retorna: 1 si mano1 > mano2, -1 si mano1 < mano2, 0 si empate
        """
        valor1 = self.__obtener_valor_juego(mano1)
        valor2 = self.__obtener_valor_juego(mano2)
        
        # Comparar posiciones en el array (menor posición = mejor juego)
        if valor1 < valor2:
            return 1
        elif valor1 > valor2:
            return -1
        else:
            return 0

    def __calcular_ranking_grandes(self, manos):
        """
        Calcula el ranking para Grandes
        """
        manos_list = list(manos)
        manos_list.sort(key=lambda x: [self.ORDEN_CARTAS.index(c) for c in self.__ordenar_mano_para_grandes(x)])

        ranking = {}
        posicion = 1

        for i, mano in enumerate(manos_list):
            if i == 0:
                ranking[mano] = posicion
            else:
                if self.__comparar_grandes(mano, manos_list[i - 1]) == 0:
                    # Empate, misma posición
                    ranking[mano] = ranking[manos_list[i-1]]
                else:
                    # Nueva posición
                    posicion = i + 1
                    ranking[mano] = posicion

        return ranking

    def __calcular_ranking_chica(self, manos):
        """
        Calcula el ranking para Chica
        """
        manos_list = list(manos)
        # Ordenar por chica: de menor a mayor (A es la mejor carta para chica)
        manos_list.sort(key=lambda x: [self.ORDEN_CARTAS.index(c) for c in self.__ordenar_mano_para_chica(x)], reverse=True)
        
        ranking = {}
        posicion_actual = 1
        
        for i, mano in enumerate(manos_list):
            if i == 0:
                ranking[mano] = posicion_actual
            else:
                if self.__comparar_chica(mano, manos_list[i-1]) == 0:
                    # Empate, misma posición
                    ranking[mano] = ranking[manos_list[i-1]]
                else:
                    # Nueva posición (siguiente número consecutivo)
                    posicion_actual = ranking[manos_list[i-1]] + 1
                    ranking[mano] = posicion_actual
                
        return ranking

    def __calcular_ranking_pares(self, manos):
        """
        Calcula el ranking para Pares
        """
        manos_list = list(manos)
        manos_list.sort(key=lambda x: self.__obtener_valor_par(x))

        ranking = {}
        posicion = 1

        for i, mano in enumerate(manos_list):
            if i == 0:
                ranking[mano] = posicion
            else:
                if self.__comparar_pares(mano, manos_list[i - 1]) == 0:
                    # Empate, misma posición
                    ranking[mano] = ranking[manos_list[i-1]]
                else:
                    # Nueva posición
                    posicion = posicion + 1
                    ranking[mano] = posicion

        return ranking

    def __calcular_ranking_juego(self, manos):
        """
        Calcula el ranking para Juego
        """
        manos_list = list(manos)
        manos_list.sort(key=lambda x: self.__obtener_valor_juego(x))

        ranking = {}
        posicion = 1
        for i, mano in enumerate(manos_list):
            if i == 0:
                ranking[mano] = posicion
            else:
                if self.__comparar_juego(mano, manos_list[i - 1]) == 0:
                    # Empate, misma posición
                    ranking[mano] = ranking[manos_list[i-1]]
                else:
                    # Nueva posición
                    posicion = posicion + 1
                    ranking[mano] = posicion
                    
        return ranking

    def __obtener_valor_par(self, mano):
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

    def __comparar_pares(self, mano1, mano2):
        """
        Compara dos manos para Pares
        Retorna: 1 si mano1 > mano2, -1 si mano1 < mano2, 0 si empate
        """
        valor1 = self.__obtener_valor_par(mano1)
        valor2 = self.__obtener_valor_par(mano2)
        
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


    def __generar_matriz_probabilidades(self):
        """
        Genera el DataFrame con todas las manos y sus características
        """
        set_manos = self.__generar_manos()
        data_manos = []

        # Calcular rankings para cada lance
        ranking_grandes = self.__calcular_ranking_grandes(set_manos)
        ranking_chica = self.__calcular_ranking_chica(set_manos)
        ranking_pares = self.__calcular_ranking_pares(set_manos)
        ranking_juego = self.__calcular_ranking_juego(set_manos)

        for mano in set_manos:
            prob = self.calcular_probabilidad_mano(mano)
            points = self.__calcular_puntos_mano(mano)
            pair_type = self.__calcular_pares(mano)

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

    def __construir_mazo_sin(self,mano: str) -> dict[str, int]:
        """
        Construye un mazo de cartas reducido, excluyendo las cartas de la mano dada.

        Args:
            mano: String con las cartas de la mano (ej. 'RRAA')

        Returns:
            Diccionario con las cartas restantes y sus cantidades
        """
        # Mazo completo del mus (40 cartas)
        mazo_completo = {
            'R': 8,  # Reyes
            'C': 4,  # Caballos
            'S': 4,  # Sotas
            'A': 8,  # Ases
            '7': 4,
            '6': 4,
            '5': 4,
            '4': 4
        }

        # Contar las cartas en la mano
        contador_mano = Counter(mano)

        # Reducir el mazo
        mazo_reducido = {}
        for carta, cantidad in mazo_completo.items():
            cantidad_restante = cantidad - contador_mano.get(carta, 0)
            if cantidad_restante > 0:
                mazo_reducido[carta] = cantidad_restante

        return mazo_reducido

    def __repartir_3_manos(self,mazo: dict[str, int]) -> list[str]:
        """
        Reparte 3 manos de 4 cartas cada una a partir del mazo reducido.

        Args:
            mazo: Diccionario con las cartas disponibles y sus cantidades

        Returns:
            Lista de 3 strings, cada uno representando una mano
        """
        # Convertir el mazo a una lista de cartas individuales
        cartas_disponibles = []
        for carta, cantidad in mazo.items():
            cartas_disponibles.extend([carta] * cantidad)

        # Mezclar las cartas
        random.shuffle(cartas_disponibles)

        # Repartir las manos (4 cartas por mano)
        manos = []
        for i in range(3):  # 3 jugadores
            if len(cartas_disponibles) >= 4:
                mano = cartas_disponibles[:4]
                cartas_disponibles = cartas_disponibles[4:]
                manos.append(''.join(sorted(mano)))
            else:
                raise ValueError("No hay suficientes cartas para repartir")

        return manos

    def __obtener_compañero_index(self,tu_index: int) -> int:
        """
        Obtiene el índice del compañero basado en el índice del jugador.
        En el mus, si el jugador es 1, el compañero es 3, si es 2, el compañero es 4, etc.

        Args:
            tu_index: Índice del jugador (1-4)

        Returns:
            Índice del compañero (1-4)
        """
        # Regla: compañero está a 2 posiciones (módulo 4, ajustando para base 1)
        return ((tu_index + 1) % 4) + 1

    def __obtener_ranking_grande(self,manos: list[str], df_manos: pd.DataFrame) -> dict[str, int]:
        """
        Obtiene el ranking de las manos para el lance de Grande.

        Args:
            manos: Lista de manos a evaluar
            df_manos: DataFrame con la información de todas las manos posibles

        Returns:
            Diccionario con las manos como claves y su ranking como valores
        """
        return self.__obtener_ranking(manos, df_manos, 'Ranking_Grandes')

    def __obtener_ranking_chica(self,manos: list[str], df_manos: pd.DataFrame) -> dict[str, int]:
        """
        Obtiene el ranking de las manos para el lance de Chica.

        Args:
            manos: Lista de manos a evaluar
            df_manos: DataFrame con la información de todas las manos posibles

        Returns:
            Diccionario con las manos como claves y su ranking como valores
        """
        return self.__obtener_ranking(manos, df_manos, 'Ranking_Chica')

    def __obtener_ranking_pares(self,manos: list[str], df_manos: pd.DataFrame) -> dict[str, int]:
        """
        Obtiene el ranking de las manos para el lance de Pares.

        Args:
            manos: Lista de manos a evaluar
            df_manos: DataFrame con la información de todas las manos posibles

        Returns:
            Diccionario con las manos como claves y su ranking como valores
        """
        return self.__obtener_ranking(manos, df_manos, 'Ranking_Pares')

    def __obtener_ranking_juego(self,manos: list[str], df_manos: pd.DataFrame) -> dict[str, int]:
        """
        Obtiene el ranking de las manos para el lance de Juego.

        Args:
            manos: Lista de manos a evaluar
            df_manos: DataFrame con la información de todas las manos posibles

        Returns:
            Diccionario con las manos como claves y su ranking como valores
        """
        return self.__obtener_ranking(manos, df_manos, 'Ranking_Juego')

    def __obtener_ranking(self,manos: list[str], df_manos: pd.DataFrame, columna_ranking: str) -> dict[str, int]:
        """
        Obtiene el ranking de las manos para un lance específico.

        Args:
            manos: Lista de manos a evaluar
            df_manos: DataFrame con la información de todas las manos posibles
            columna_ranking: Nombre de la columna que contiene el ranking deseado

        Returns:
            Diccionario con las manos como claves y su ranking como valores
        """
        # Obtener el ranking del DataFrame
        ranking = {}
        for mano in manos:
            try:
                ranking[mano] = df_manos[df_manos['Mano'] == mano][columna_ranking].values[0]
            except IndexError:
                # Si la mano no está en el DataFrame, ordenarla para buscarla
                mano_ordenada = ''.join(sorted(mano, key=lambda x: "RCS7654A".index(x)))
                ranking[mano] = df_manos[df_manos['Mano'] == mano_ordenada][columna_ranking].values[0]

        return ranking

    def __determinar_ganador(self,rankings: dict[str, int], orden_jugadores: list[int]) -> tuple[int, str]:
        """
        Determina el jugador ganador basado en los rankings y el orden de mano.
        En caso de empate, gana el jugador con el menor número de orden.

        Args:
            rankings: Diccionario con las manos y sus rankings
            orden_jugadores: Lista con el orden de los jugadores (1-4) para cada mano

        Returns:
            Tupla con (índice del ganador, mano ganadora)
        """
        # Encontrar el mejor ranking (menor número)
        mejor_ranking = min(rankings.values())

        # Encontrar todas las manos con el mejor ranking
        mejores_manos = [mano for mano, rank in rankings.items() if rank == mejor_ranking]

        if len(mejores_manos) == 1:
            # Solo hay un ganador
            mano_ganadora = mejores_manos[0]
            index_ganador = list(rankings.keys()).index(mano_ganadora)
            return orden_jugadores[index_ganador], mano_ganadora
        else:
            # Hay empate, gana el que tenga menor orden de mano
            manos_empatadas = [(mano, orden_jugadores[list(rankings.keys()).index(mano)]) for mano in mejores_manos]
            ganador = min(manos_empatadas, key=lambda x: x[1])
            return ganador[1], ganador[0]

    def __simular_lances(self,tu_mano: str, df_manos: pd.DataFrame, flag_orden, N) -> dict[str, dict[str, float]]:
        """
        Simula N partidas de mus para calcular la probabilidad de ganar en los 4 lances.

        Args:
            tu_mano: String con tu mano (ej. 'RRAA')
            df_manos: DataFrame con información de todas las manos posibles
            flag_orden: Tu posición en la mesa (1-4)
            N: Número de simulaciones a realizar

        Returns:
            Diccionario con las probabilidades de victoria individual y de equipo para cada lance
        """
        # Paso 1: reducir el mazo
        mazo_reducido = self.__construir_mazo_sin(tu_mano)
        # Definir compañero según las reglas
        tu_compañero = self.__obtener_compañero_index(flag_orden)

        # Inicializar contadores de victorias para cada lance
        victorias = {
            'grandes': {'individual': 0, 'equipo': 0},
            'chicas': {'individual': 0, 'equipo': 0},
            'pares': {'individual': 0, 'equipo': 0},
            'juego': {'individual': 0, 'equipo': 0}
        }

        for _ in range(N):
            # Paso 2: Generar manos para los 3 jugadores restantes
            manos_simuladas = self.__repartir_3_manos(mazo_reducido)

            # Asignar manos a los jugadores según su posición
            todas_manos = [tu_mano] + manos_simuladas

            # Crear lista de órdenes para cada jugador (comenzando por tu posición)
            ordenes = [0, 0, 0, 0]  # Inicializar lista
            ordenes[0] = flag_orden  # Tu orden

            # Asignar órdenes a los otros jugadores (2, 3 y 4 en sentido horario)
            for i in range(1, 4):
                ordenes[i] = ((flag_orden + i - 1) % 4) + 1

            # Paso 3: Calcular ranking para cada lance
            rankings_grandes = self.__obtener_ranking_grande(todas_manos, df_manos)
            rankings_chicas = self.__obtener_ranking_chica(todas_manos, df_manos)
            rankings_pares = self.__obtener_ranking_pares(todas_manos, df_manos)
            rankings_juego = self.__obtener_ranking_juego(todas_manos, df_manos)

            # Paso 4: Determinar ganador para cada lance
            ganador_grandes, _ = self.__determinar_ganador(rankings_grandes, ordenes)
            ganador_chicas, _ = self.__determinar_ganador(rankings_chicas, ordenes)
            ganador_pares, _ = self.__determinar_ganador(rankings_pares, ordenes)
            ganador_juego, _ = self.__determinar_ganador(rankings_juego, ordenes)

            # Sumar victorias para cada lance
            # Grandes
            if ganador_grandes == flag_orden:
                victorias['grandes']['individual'] += 1
            if ganador_grandes == flag_orden or ganador_grandes == tu_compañero:
                victorias['grandes']['equipo'] += 1

            # Chicas
            if ganador_chicas == flag_orden:
                victorias['chicas']['individual'] += 1
            if ganador_chicas == flag_orden or ganador_chicas == tu_compañero:
                victorias['chicas']['equipo'] += 1

            # Pares
            if ganador_pares == flag_orden:
                victorias['pares']['individual'] += 1
            if ganador_pares == flag_orden or ganador_pares == tu_compañero:
                victorias['pares']['equipo'] += 1

            # Juego
            if ganador_juego == flag_orden:
                victorias['juego']['individual'] += 1
            if ganador_juego == flag_orden or ganador_juego == tu_compañero:
                victorias['juego']['equipo'] += 1

        # Paso 5: Calcular probabilidades para cada lance
        resultados = {}
        for lance in victorias:
            resultados[lance] = {
                'prob_victoria_individual': victorias[lance]['individual'] / N,
                'prob_victoria_equipo': victorias[lance]['equipo'] / N
            }

        return resultados

