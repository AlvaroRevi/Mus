import pandas as pd
import random
from collections import Counter
from typing import List, Dict, Tuple

def construir_mazo_sin(mano: str) -> Dict[str, int]:
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

def repartir_3_manos(mazo: Dict[str, int]) -> List[str]:
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

def obtener_compañero_index(tu_index: int) -> int:
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

def obtener_ranking_grande(manos: List[str], df_manos: pd.DataFrame) -> Dict[str, int]:
    """
    Obtiene el ranking de las manos para el lance de Grande.

    Args:
        manos: Lista de manos a evaluar
        df_manos: DataFrame con la información de todas las manos posibles

    Returns:
        Diccionario con las manos como claves y su ranking como valores
    """
    return obtener_ranking(manos, df_manos, 'Ranking_Grandes')

def obtener_ranking_chica(manos: List[str], df_manos: pd.DataFrame) -> Dict[str, int]:
    """
    Obtiene el ranking de las manos para el lance de Chica.

    Args:
        manos: Lista de manos a evaluar
        df_manos: DataFrame con la información de todas las manos posibles

    Returns:
        Diccionario con las manos como claves y su ranking como valores
    """
    return obtener_ranking(manos, df_manos, 'Ranking_Chica')

def obtener_ranking_pares(manos: List[str], df_manos: pd.DataFrame) -> Dict[str, int]:
    """
    Obtiene el ranking de las manos para el lance de Pares.

    Args:
        manos: Lista de manos a evaluar
        df_manos: DataFrame con la información de todas las manos posibles

    Returns:
        Diccionario con las manos como claves y su ranking como valores
    """
    return obtener_ranking(manos, df_manos, 'Ranking_Pares')

def obtener_ranking_juego(manos: List[str], df_manos: pd.DataFrame) -> Dict[str, int]:
    """
    Obtiene el ranking de las manos para el lance de Juego.

    Args:
        manos: Lista de manos a evaluar
        df_manos: DataFrame con la información de todas las manos posibles

    Returns:
        Diccionario con las manos como claves y su ranking como valores
    """
    return obtener_ranking(manos, df_manos, 'Ranking_Juego')

def obtener_ranking(manos: List[str], df_manos: pd.DataFrame, columna_ranking: str) -> Dict[str, int]:
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

def determinar_ganador(rankings: Dict[str, int], orden_jugadores: List[int]) -> Tuple[int, str]:
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

def simular_grandes(tu_mano: str, df_manos: pd.DataFrame, flag_orden: int = 1, N: int = 100000) -> Dict[str, float]:
    """
    Simula N partidas de mus para calcular la probabilidad de ganar el lance de Grande.

    Args:
        tu_mano: String con tu mano (ej. 'RRAA')
        df_manos: DataFrame con información de todas las manos posibles
        flag_orden: Tu posición en la mesa (1-4)
        N: Número de simulaciones a realizar

    Returns:
        Diccionario con las probabilidades de victoria individual y de equipo
    """
    # Usar la simulación general pero devolver solo los resultados para grandes
    resultados = simular_todos_lances(tu_mano, df_manos, flag_orden, N)
    return {
        'prob_victoria_individual': resultados['grandes']['prob_victoria_individual'],
        'prob_victoria_equipo': resultados['grandes']['prob_victoria_equipo']
    }

def simular_todos_lances(tu_mano: str, df_manos: pd.DataFrame, flag_orden: int = 1, N: int = 100000) -> Dict[str, Dict[str, float]]:
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
    mazo_reducido = construir_mazo_sin(tu_mano)

    # Definir compañero según las reglas
    tu_compañero = obtener_compañero_index(flag_orden)

    # Inicializar contadores de victorias para cada lance
    victorias = {
        'grandes': {'individual': 0, 'equipo': 0},
        'chicas': {'individual': 0, 'equipo': 0},
        'pares': {'individual': 0, 'equipo': 0},
        'juego': {'individual': 0, 'equipo': 0}
    }

    for _ in range(N):
        # Paso 2: Generar manos para los 3 jugadores restantes
        manos_simuladas = repartir_3_manos(mazo_reducido)

        # Asignar manos a los jugadores según su posición
        todas_manos = [tu_mano] + manos_simuladas

        # Crear lista de órdenes para cada jugador (comenzando por tu posición)
        ordenes = [0, 0, 0, 0]  # Inicializar lista
        ordenes[0] = flag_orden  # Tu orden

        # Asignar órdenes a los otros jugadores (2, 3 y 4 en sentido horario)
        for i in range(1, 4):
            ordenes[i] = ((flag_orden + i - 1) % 4) + 1

        # Paso 3: Calcular ranking para cada lance
        rankings_grandes = obtener_ranking_grande(todas_manos, df_manos)
        rankings_chicas = obtener_ranking_chica(todas_manos, df_manos)
        rankings_pares = obtener_ranking_pares(todas_manos, df_manos)
        rankings_juego = obtener_ranking_juego(todas_manos, df_manos)

        # Paso 4: Determinar ganador para cada lance
        ganador_grandes, _ = determinar_ganador(rankings_grandes, ordenes)
        ganador_chicas, _ = determinar_ganador(rankings_chicas, ordenes)
        ganador_pares, _ = determinar_ganador(rankings_pares, ordenes)
        ganador_juego, _ = determinar_ganador(rankings_juego, ordenes)

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