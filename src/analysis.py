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


def analizar_varias_manos(manos: list, posicion: int = 1, n_simulaciones: int = 20000):
    """
    Compara varias manos en un lance específico

    Args:
        manos: Lista de manos a comparar
        posicion: Posición en la mesa (1-4)
        n_simulaciones: Número de simulaciones a realizar
    """
    # Crear instancia del juego
    mus_game = MusGame()

    # Generar DataFrame con todas las manos
    df_hands = mus_game.generar_matriz_probabilidades()

    # Realizar simulaciones para cada mano
    resultados = []

    for mano in manos:
        resultado = simular_todos_lances(mano, df_hands, posicion, n_simulaciones)
        resultados.append({
            'Mano': mano,
            'Grande - Ind (%)': round(resultado['grandes']['prob_victoria_individual'] * 100, 2),
            'Grande - Eq (%)': round(resultado['grandes']['prob_victoria_equipo'] * 100, 2),
            'Chica - Ind (%)': round(resultado['chicas']['prob_victoria_individual'] * 100, 2),
            'Chica - Eq (%)': round(resultado['chicas']['prob_victoria_equipo'] * 100, 2),
            'Pares - Ind (%)': round(resultado['pares']['prob_victoria_individual'] * 100, 2),
            'Pares - Eq (%)': round(resultado['pares']['prob_victoria_equipo'] * 100, 2),
            'Juego - Ind (%)': round(resultado['juego']['prob_victoria_individual'] * 100, 2),
            'Juego - Eq (%)': round(resultado['juego']['prob_victoria_equipo'] * 100, 2)
        })

    # Convertir a DataFrame y mostrar resultados
    df_resultados = pd.DataFrame(resultados)
    print("\nComparación de manos:")
    print(df_resultados)

    # Crear gráficos por lance
    lances = ['Grande', 'Chica', 'Pares', 'Juego']

    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    axes = axes.flatten()

    for i, lance in enumerate(lances):
        ind_col = f'{lance} - Ind (%)'
        eq_col = f'{lance} - Eq (%)'

        ax = axes[i]
        x = range(len(manos))
        width = 0.35

        ax.bar([i - width/2 for i in x], df_resultados[ind_col], width, label='Individual')
        ax.bar([i + width/2 for i in x], df_resultados[eq_col], width, label='Equipo')

        ax.set_xlabel('Mano')
        ax.set_ylabel('Probabilidad de Victoria (%)')
        ax.set_title(f'Probabilidad de Victoria en {lance}')
        ax.set_xticks(x)
        ax.set_xticklabels(manos)
        ax.legend()
        ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.show()

    return df_resultados


if __name__ == "__main__":
    # Ejemplo de uso: analizar una mano específica
    print("Análisis de una mano específica:\n")
    analizar_mano("RRAA", 1, 20000)

    # Ejemplo de uso: comparar varias manos
    print("\n\nComparación de varias manos:\n")
    manos_ejemplo = ["RRRR", "RRRA", "RRAA", "CCSS", "AAAA"]
    analizar_varias_manos(manos_ejemplo, 1, 10000)
