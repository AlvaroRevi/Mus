import unittest
import pandas as pd
from src.utils.data_formatter import DataFormatter


class TestDataFormatter(unittest.TestCase):
    """
    Tests para la clase DataFormatter
    """

    def setUp(self):
        """Configuración inicial para cada test"""
        # Crear DataFrame de ejemplo para testing
        self.df_ejemplo = pd.DataFrame({
            'Mano': ['RRRR', 'AAAA', 'RCA7'],
            'Probabilidad': [0.0001, 0.0002, 0.0150],
            'Puntos_de_juego': [40, 4, 28],
            'Pares': ['Duples', 'Duples', 'Nada']
        })

    def test_format_probability(self):
        """Test de formateo de probabilidades"""
        # Test casos normales
        self.assertEqual(DataFormatter.format_probability(0.5), "50.0000%")
        self.assertEqual(DataFormatter.format_probability(0.0001), "0.0100%")
        self.assertEqual(DataFormatter.format_probability(1.0), "100.0000%")

        # Test casos extremos
        self.assertEqual(DataFormatter.format_probability(0), "0.0000%")
        self.assertEqual(DataFormatter.format_probability(0.123456), "12.3456%")

    def test_format_dataframe_for_display_estructura(self):
        """Test de estructura del DataFrame formateado"""
        df_formateado = DataFormatter.format_dataframe_for_display(self.df_ejemplo)

        # Verificar que es un DataFrame
        self.assertIsInstance(df_formateado, pd.DataFrame)

        # Verificar columnas esperadas
        columnas_esperadas = ['Mano', 'Probabilidad_%', 'Puntos_de_juego', 'Pares']
        self.assertEqual(list(df_formateado.columns), columnas_esperadas)

        # Verificar que tiene el mismo número de filas
        self.assertEqual(len(df_formateado), len(self.df_ejemplo))

    def test_format_dataframe_for_display_contenido(self):
        """Test de contenido del DataFrame formateado"""
        df_formateado = DataFormatter.format_dataframe_for_display(self.df_ejemplo)

        # Verificar que las probabilidades están formateadas correctamente
        self.assertEqual(df_formateado['Probabilidad_%'].iloc[0], "0.0100%")
        self.assertEqual(df_formateado['Probabilidad_%'].iloc[1], "0.0200%")
        self.assertEqual(df_formateado['Probabilidad_%'].iloc[2], "1.5000%")

        # Verificar que otros campos se mantienen
        self.assertEqual(df_formateado['Mano'].iloc[0], 'RRRR')
        self.assertEqual(df_formateado['Puntos_de_juego'].iloc[0], 40)
        self.assertEqual(df_formateado['Pares'].iloc[0], 'Duples')

    def test_get_summary_stats_estructura(self):
        """Test de estructura de estadísticas resumidas"""
        stats = DataFormatter.get_summary_stats(self.df_ejemplo)

        # Verificar que es un diccionario
        self.assertIsInstance(stats, dict)

        # Verificar claves esperadas
        claves_esperadas = ['manos_totales', 'avg_probability', 'avg_points', 'pair_distribution']
        self.assertEqual(set(stats.keys()), set(claves_esperadas))

    def test_get_summary_stats_valores(self):
        """Test de valores de estadísticas resumidas"""
        stats = DataFormatter.get_summary_stats(self.df_ejemplo)

        # Verificar valores calculados
        self.assertEqual(stats['manos_totales'], 3)
        self.assertAlmostEqual(stats['avg_probability'], 0.0051, places=4)
        self.assertAlmostEqual(stats['avg_points'], 24.0, places=1)

        # Verificar distribución de pares
        self.assertEqual(stats['pair_distribution']['Duples'], 2)
        self.assertEqual(stats['pair_distribution']['Nada'], 1)

    def test_format_dataframe_no_modifica_original(self):
        """Test que verifica que el DataFrame original no se modifica"""
        df_original = self.df_ejemplo.copy()
        DataFormatter.format_dataframe_for_display(self.df_ejemplo)

        # Verificar que el DataFrame original no cambió
        pd.testing.assert_frame_equal(self.df_ejemplo, df_original)


if __name__ == '__main__':
    unittest.main()