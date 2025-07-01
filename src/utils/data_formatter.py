import pandas as pd


class DataFormatter:
    """
    Utilidades para formatear y mostrar datos del juego de Mus
    """

    @staticmethod
    def format_probability(prob):
        """
        Formatea la probabilidad como porcentaje
        """
        return f"{prob * 100:.4f}%"

    @staticmethod
    def format_dataframe_for_display(df):
        """
        Formatea el DataFrame para mejor visualización
        """
        df_display = df.copy()
        df_display['Probabilidad_%'] = df_display['Probabilidad'].apply(
            DataFormatter.format_probability
        )

        # Reordenar columnas para mejor visualización
        columns_order = ['Mano', 'Probabilidad_%', 'Puntos_de_juego', 'Pares']
        df_display = df_display[columns_order]

        return df_display

    @staticmethod
    def get_summary_stats(df):
        """
        Obtiene estadísticas resumidas del DataFrame
        """
        stats = {
            'manos_totales': len(df),
            'avg_probability': df['Probabilidad'].mean(),
            'avg_points': df['Puntos_de_juego'].mean(),
            'pair_distribution': df['Pares'].value_counts().to_dict()
        }

        return stats