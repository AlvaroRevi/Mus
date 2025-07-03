import unittest
import pandas as pd
from collections import Counter
from src.models.mus_game import MusGame


class TestMusGame(unittest.TestCase):
    """
    Tests para la clase MusGame
    """

    def setUp(self):
        """Configuración inicial para cada test"""
        self.mus_game = MusGame()

    def test_inicializacion(self):
        """Test de inicialización correcta de la clase"""
        self.assertEqual(self.mus_game.manos_totales, 91390)  # C(40,4)
        self.assertIsInstance(self.mus_game.MAZO_CARTAS, dict)
        self.assertIsInstance(self.mus_game.VALOR_CARTAS, dict)

    def test_mazo_cartas_total(self):
        """Test que verifica que el mazo tiene 40 cartas en total"""
        total_cartas = sum(self.mus_game.MAZO_CARTAS.values())
        self.assertEqual(total_cartas, 40)

    def test_generar_manos_tipo_retorno(self):
        """Test que verifica el tipo de retorno de generar_manos"""
        manos = self.mus_game.__generar_manos()
        self.assertIsInstance(manos, set)
        self.assertTrue(len(manos) > 0)

    def test_generar_manos_longitud(self):
        """Test que verifica que todas las manos tienen 4 cartas"""
        manos = self.mus_game.__generar_manos()
        for mano in list(manos)[:10]:  # Test solo las primeras 10 por eficiencia
            self.assertEqual(len(mano), 4)

    def test_generar_manos_cartas_validas(self):
        """Test que verifica que todas las cartas generadas son válidas"""
        manos = self.mus_game.__generar_manos()
        cartas_validas = set(self.mus_game.MAZO_CARTAS.keys())

        for mano in list(manos)[:10]:  # Test solo las primeras 10 por eficiencia
            for carta in mano:
                self.assertIn(carta, cartas_validas)

    def test_calcular_probabilidad_mano_casos_conocidos(self):
        """Test de probabilidades para manos específicas conocidas"""
        # Test mano con 4 ases (máxima probabilidad de cuatros)
        prob_4_ases = self.mus_game.calcular_probabilidad_mano("AAAA")
        self.assertGreater(prob_4_ases, 0)
        self.assertLess(prob_4_ases, 1)

        # Test mano mixta
        prob_mixta = self.mus_game.calcular_probabilidad_mano("RCA7")
        self.assertGreater(prob_mixta, 0)
        self.assertLess(prob_mixta, 1)

        prob_solomillo_esperada = 0.03814421709158551
        prob_solomillo_real = self.mus_game.calcular_probabilidad_mano("RRRA")
        self.assertAlmostEqual(prob_solomillo_esperada, prob_solomillo_esperada, places=10)

    def test_calcular_probabilidad_suma_total(self):
        """Test que verifica que la suma de todas las probabilidades es 1"""
        df = self.mus_game.__generar_matriz_probabilidades()
        suma_probabilidades = df['Probabilidad'].sum()
        # Usamos assertAlmostEqual porque pueden haber errores de punto flotante
        self.assertAlmostEqual(suma_probabilidades, 1.0, places=10)

    def test_calcular_puntos_mano_casos_conocidos(self):
        """Test de cálculo de puntos para manos específicas"""
        # Mano con 4 reyes (máximo puntaje)
        puntos_4_reyes = self.mus_game.__calcular_puntos_mano("RRRR")
        self.assertEqual(puntos_4_reyes, 40)

        # Mano con 4 ases (mínimo puntaje)
        puntos_4_ases = self.mus_game.__calcular_puntos_mano("AAAA")
        self.assertEqual(puntos_4_ases, 4)

        # Mano mixta conocida
        puntos_mixta = self.mus_game.__calcular_puntos_mano("RCA7")
        self.assertEqual(puntos_mixta, 28)  # 10 + 10 + 1 + 7

    def test_calcular_pares_casos_conocidos(self):
        """Test de clasificación de pares para casos específicos"""
        # Test Duples (4 iguales)
        self.assertEqual(self.mus_game.__calcular_pares("RRRR"), "Duples")
        self.assertEqual(self.mus_game.__calcular_pares("AAAA"), "Duples")

        # Test Duples (2 pares)
        self.assertEqual(self.mus_game.__calcular_pares("RRAA"), "Duples")
        self.assertEqual(self.mus_game.__calcular_pares("CC77"), "Duples")

        # Test Medias (3 iguales)
        self.assertEqual(self.mus_game.__calcular_pares("RRRA"), "Medias")
        self.assertEqual(self.mus_game.__calcular_pares("AAA7"), "Medias")

        # Test Par (2 iguales)
        self.assertEqual(self.mus_game.__calcular_pares("RRA7"), "Par")
        self.assertEqual(self.mus_game.__calcular_pares("AA76"), "Par")

        # Test Nada
        self.assertEqual(self.mus_game.__calcular_pares("RCA7"), "Nada")
        self.assertEqual(self.mus_game.__calcular_pares("7654"), "Nada")

    def test_generar_matriz_probabilidades_estructura(self):
        """Test de la estructura del DataFrame generado"""
        df = self.mus_game.__generar_matriz_probabilidades()

        # Verificar que es un DataFrame
        self.assertIsInstance(df, pd.DataFrame)

        # Verificar columnas esperadas
        columnas_esperadas = ['Mano', 'Probabilidad', 'Puntos_de_juego', 'Pares',
                              'Ranking_Grandes','Ranking_Chica','Ranking_Pares','Ranking_Juego']
        self.assertEqual(list(df.columns), columnas_esperadas)

        # Verificar que no está vacío
        self.assertGreater(len(df), 0)

        # Verificar que está ordenado por probabilidad (descendente)
        probabilidades = df['Probabilidad'].tolist()
        self.assertEqual(probabilidades, sorted(probabilidades, reverse=True))

    def test_generar_matriz_probabilidades_tipos_datos(self):
        """Test de los tipos de datos en el DataFrame"""
        df = self.mus_game.__generar_matriz_probabilidades()

        # Verificar tipos de datos
        self.assertTrue(df['Mano'].dtype == 'object')
        self.assertTrue(df['Probabilidad'].dtype in ['float64', 'float32'])
        self.assertTrue(df['Puntos_de_juego'].dtype in ['int64', 'int32'])
        self.assertTrue(df['Pares'].dtype == 'object')

    def test_generar_matriz_probabilidades_valores_validos(self):
        """Test de valores válidos en el DataFrame"""
        df = self.mus_game.__generar_matriz_probabilidades()

        # Verificar que todas las probabilidades están entre 0 y 1
        self.assertTrue((df['Probabilidad'] >= 0).all())
        self.assertTrue((df['Probabilidad'] <= 1).all())

        # Verificar que todos los puntos son positivos
        self.assertTrue((df['Puntos_de_juego'] > 0).all())

        # Verificar que todos los puntos son 40 como maximo
        self.assertTrue((df['Puntos_de_juego'] <= 40).all())

        # Verificar que todos los tipos de pares son válidos
        tipos_pares_validos = {'Duples', 'Medias', 'Par', 'Nada'}
        self.assertTrue(set(df['Pares'].unique()).issubset(tipos_pares_validos))

    def test_comparar_grandes(self):
        self.assertEqual(self.mus_game.__comparar_grandes('RRCA', 'RRAA'), 1)
        self.assertEqual(self.mus_game.__comparar_grandes('RCCA', '76AA'), 1)
        self.assertEqual(self.mus_game.__comparar_grandes('RRRA', '76AA'), 1)
        self.assertEqual(self.mus_game.__comparar_grandes('RCCA', 'RRAA'), -1)
        self.assertEqual(self.mus_game.__comparar_grandes('CCSA', 'RAAA'), -1)
        self.assertEqual(self.mus_game.__comparar_grandes('C44A', 'C54A'), -1)
        self.assertEqual(self.mus_game.__comparar_grandes('RCCA', 'RACC'), 0)
        self.assertEqual(self.mus_game.__comparar_grandes('RRRR', 'CCCC'), 1)
        self.assertEqual(self.mus_game.__comparar_grandes('CSSA', 'CSS7'), -1)

    def test_comparar_chica(self):
        self.assertEqual(self.mus_game.comparar_chica('RRAA','764A'),1)
        self.assertEqual(self.mus_game.comparar_chica('RAAA', '44AA'), 1)
        self.assertEqual(self.mus_game.comparar_chica('RCA5', 'AA4R'), -1)
        self.assertEqual(self.mus_game.comparar_chica('AA67', 'AA56'), -1)
        self.assertEqual(self.mus_game.comparar_chica('A467', 'AA56'), -1)
        self.assertEqual(self.mus_game.comparar_chica('AA67', 'AA76'), 0)

    def test_comparar_pares(self):
        self.assertEqual(self.mus_game.__comparar_pares('RR4A', '764A'), 1)
        self.assertEqual(self.mus_game.__comparar_pares('RR4A', 'CC4A'), 1)
        self.assertEqual(self.mus_game.__comparar_pares('RR4A', '7AAA'), -1)
        self.assertEqual(self.mus_game.__comparar_pares('RRRA', '764A'), 1)
        self.assertEqual(self.mus_game.__comparar_pares('RR44', 'RR77'), -1)
        self.assertEqual(self.mus_game.__comparar_pares('RRR4', 'AA77'), -1)
        self.assertEqual(self.mus_game.__comparar_pares('RC44', 'RC77'), -1)
        self.assertEqual(self.mus_game.__comparar_pares('AACC', '6677'), 1)
        self.assertEqual(self.mus_game.__comparar_pares('RR54', 'RRS7'), 0)
        self.assertEqual(self.mus_game.__comparar_pares('RRR4', 'RRR7'), 0)
        self.assertEqual(self.mus_game.__comparar_pares('RS44', 'RS77'), -1)
        self.assertEqual(self.mus_game.__comparar_pares('RRCC', 'RRRR'), -1)

    def test_comparar_juego(self):
        self.assertEqual(self.mus_game.__comparar_juego('RRCA', 'RRAA'), 1)
        self.assertEqual(self.mus_game.__comparar_juego('RRCA', 'RRSA'), 0)
        self.assertEqual(self.mus_game.__comparar_juego('RRCA', '777S'), 0)
        self.assertEqual(self.mus_game.__comparar_juego('RC76', 'RSS5'), -1)
        self.assertEqual(self.mus_game.__comparar_juego('RRCS', 'RRC7'), 1)
        self.assertEqual(self.mus_game.__comparar_juego('RRCS', 'RR57'), -1)
        self.assertEqual(self.mus_game.__comparar_juego('RRAA', 'RRA4'), -1)
        self.assertEqual(self.mus_game.__comparar_juego('RR55', 'RRCA'), -1)
        self.assertEqual(self.mus_game.__comparar_juego('RR55', 'RR54'), 1)
        self.assertEqual(self.mus_game.__comparar_juego('RRC5', 'RRC4'), 1)
        self.assertEqual(self.mus_game.__comparar_juego('RRCS', 'RRCA'), -1)
        self.assertEqual(self.mus_game.__comparar_juego('4466', '775A'), 0)



if __name__ == '__main__':
    unittest.main()