"""
Aplicación principal para analizar las posibilidades de victoria en el Mus

Este módulo genera un DataFrame con todas las manos posibles,
sus probabilidades, valores de juego y tipos de pares.
"""
import pandas as pd
from models.mus_game import MusGame
import time

def main():
    """
    Función principal que ejecuta el análisis de manos de Mus
    """
    # # Crear instancia del juego
    mus_game = MusGame()
    start = time.perf_counter()       # Marca el tiempo inicial con alta precisión
    mus_game.analizar_mano('RCSA')
    end = time.perf_counter()         # Marca el tiempo final
    print(f"Tiempo de análisis: {end - start:.4f} segundos")


if __name__ == "__main__":
    df_result = main()
