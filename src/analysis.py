"""Script para analizar manos específicas con la simulación Monte Carlo"""

import pandas as pd
from models.mus_game import MusGame
from models.monte_carlo import simular_todos_lances


def analizar_mano(mano: str, posicion: int = 1, n_simulaciones: int = 10000):
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
    df_hands = mus_game.generar_matriz_probabilidades()

    # Obtener información de la mano
    info_mano = df_hands[df_hands['Mano'] == mano].iloc[0]

    print(f"Análisis de la mano: {mano}")
    print(f"Probabilidad de obtenerla: {info_mano['Probabilidad']*100:.4f}%")
    print(f"Puntos de juego: {info_mano['Puntos_de_juego']}")
    print(f"Tipo de pares: {info_mano['Pares']}")
    print(f"Ranking en Grande: {info_mano['Ranking_Grandes']}")
    print(f"Ranking en Chica: {info_mano['Ranking_Chica']}")
    print(f"Ranking en Pares: {info_mano['Ranking_Pares']}")
    print(f"Ranking en Juego: {info_mano['Ranking_Juego']}")
    print("\nRealizando simulaciones Monte Carlo...")

    # Realizar simulación Monte Carlo
    resultados = simular_todos_lances(mano, df_hands, posicion, n_simulaciones)

    # Mostrar resultados
    print("\nResultados de la simulación Monte Carlo:")
    for lance in resultados:
        print(f"\n{lance.capitalize()}:")
        print(f"  Victoria individual: {resultados[lance]['prob_victoria_individual']*100:.2f}%")
        print(f"  Victoria en equipo: {resultados[lance]['prob_victoria_equipo']*100:.2f}%")


    return resultados



if __name__ == "__main__":
    # Ejemplo de uso: analizar una mano específica
    print("Análisis de una mano específica:\n")
    analizar_mano("RRAA", 1, 20000)
