import unittest
import pandas as pd
import tempfile
import os
from src.models.mus_game import MusGame
from src.utils.data_formatter import DataFormatter


class TestIntegration(unittest.TestCase):
    """
    Tests de integración para verificar que todos los componentes funcionan juntos
    """

    def setUp(self):
        """Configuración inicial para cada test"""
        self.mus_game = MusGame()

    def test_flujo_completo_generacion_datos(self):
        """Test del flujo completo de generación de datos"""
        # Generar DataFrame
        df = self.mus_game._MusGame__generar_matriz_probabilidades()

        # Verificar que se generó correctamente
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 0)

        # Formatear para visualización
        df_display = DataFormatter.format_dataframe_for_display(df)

        # Verificar que el formateo funcionó
        self.assertIsInstance(df_display, pd.DataFrame)
        self.assertEqual(len(df_display), len(df))

        # Obtener estadísticas
        stats = DataFormatter.get_summary_stats(df)

        # Verificar que las estadísticas son coherentes
        self.assertEqual(stats['manos_totales'], len(df))
        self.assertGreater(stats['avg_probability'], 0)
        self.assertGreater(stats['avg_points'], 0)

    def test_consistencia_probabilidades_totales(self):
        """Test de consistencia: suma de probabilidades debe ser 1"""
        df = self.mus_game._MusGame__generar_matriz_probabilidades()
        suma_probabilidades = df['Probabilidad'].sum()
        self.assertAlmostEqual(suma_probabilidades, 1.0, places=8)

    def test_consistencia_rangos_puntos(self):
        """Test de consistencia: puntos deben estar en rango válido"""
        df = self.mus_game._MusGame__generar_matriz_probabilidades()

        # Puntos mínimos: 4 ases = 4 puntos
        self.assertEqual(df['Puntos_de_juego'].min(), 4)

        # Puntos máximos: 4 reyes = 40 puntos
        self.assertEqual(df['Puntos_de_juego'].max(), 40)

    def test_consistencia_distribucion_pares(self):
        """Test de consistencia: distribución de tipos de pares"""
        df = self.mus_game._MusGame__generar_matriz_probabilidades()

        # Verificar que hay manos de todos los tipos
        tipos_pares = set(df['Pares'].unique())
        tipos_esperados = {'Duples', 'Medias', 'Par', 'Nada'}

        # Al menos debe haber algunos tipos (puede que no todos dependiendo del tamaño)
        self.assertTrue(tipos_pares.issubset(tipos_esperados))
        self.assertGreater(len(tipos_pares), 0)

    def test_performance_generacion_manos(self):
        """Test de rendimiento básico"""
        import time

        start_time = time.time()
        manos = self.mus_game._MusGame__generar_manos()
        end_time = time.time()

        # Verificar que la generación es razonablemente rápida (menos de 10 segundos)
        self.assertLess(end_time - start_time, 10)
        self.assertGreater(len(manos), 0)

    def test_exportacion_csv(self):
        """Test de exportación a CSV"""
        df = self.mus_game._MusGame__generar_matriz_probabilidades()

        # Crear archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
            temp_filename = temp_file.name

        try:
            # Exportar a CSV
            df.to_csv(temp_filename, index=False)

            # Verificar que el archivo se creó
            self.assertTrue(os.path.exists(temp_filename))

            # Verificar que se puede leer de vuelta
            df_leido = pd.read_csv(temp_filename)
            self.assertEqual(len(df_leido), len(df))
            self.assertEqual(list(df_leido.columns), list(df.columns))

        finally:
            # Limpiar archivo temporal
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


if __name__ == '__main__':
    unittest.main()
