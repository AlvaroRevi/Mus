"""
Aplicación principal para analizar las posibilidades de victoria en el Mus

Este módulo genera un DataFrame con todas las manos posibles,
sus probabilidades, valores de juego y tipos de pares.
"""
import pandas as pd
from models.mus_game import MusGame
from models.monte_carlo import simular_grandes, simular_todos_lances
from analysis import analizar_mano

def main():
    """
    Función principal que ejecuta el análisis de manos de Mus
    """
    # # Crear instancia del juego
    # mus_game = MusGame()
    # #
    # # Generar DataFrame con todas las manos
    # df_hands = mus_game.generar_matriz_probabilidades()

    analizar_mano('RCSA')


if __name__ == "__main__":
    df_result = main()
