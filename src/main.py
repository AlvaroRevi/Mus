"""
Aplicación principal para analizar las posibilidades de victoria en el Mus

Este módulo genera un DataFrame con todas las manos posibles,
sus probabilidades, valores de juego y tipos de pares.
"""

import pandas as pd
from models.mus_game import MusGame
from utils.data_formatter import DataFormatter


def main():
    """
    Función principal que ejecuta el análisis de manos de Mus
    """
    # Crear instancia del juego
    mus_game = MusGame()

    # Generar DataFrame con todas las manos
    df_hands = mus_game.generar_matriz_probabilidades()

    # Probabilidad de sacar duples
    print("Probabilidad de sacar duples:\n")
    print(df_hands[df_hands['Pares'] == 'Duples']['Probabilidad'].sum())

    # Probabilidad de 'Pares si'
    print("\nProbabilidad de tener pares:\n")
    print(df_hands[df_hands['Pares'] != 'Nada']['Probabilidad'].sum())

    #Probabilidad de 'Juego si'
    print("\nProbabilidad de tener juego:\n")
    print(df_hands[df_hands['Puntos_de_juego'] >= 31]['Probabilidad'].sum())

    #Probabilidad de solomillo
    print("\nProbabilidad de tener solomillo:\n")
    print(df_hands[df_hands['Mano'] == 'RRRA']['Probabilidad'].sum())

    return df_hands


if __name__ == "__main__":
    df_result = main()
