import unittest
import pandas as pd
from collections import Counter
from src.models.monte_carlo import (
    construir_mazo_sin,
    repartir_3_manos,
    obtener_compañero_index,
    determinar_ganador,
    obtener_ranking,
    obtener_ranking_grande,
    obtener_ranking_chica,
    obtener_ranking_pares,
    obtener_ranking_juego
)


class TestMonteCarlo(unittest.TestCase):
    """Tests para las funciones de simulación Monte Carlo"""

    def test_construir_mazo_sin(self):
        """Test para verificar que el mazo se reduce correctamente"""
        # Test con una mano simple
        mano = "RRAA"
        mazo_reducido = construir_mazo_sin(mano)

        # Verificar que se quitaron las cartas correctas
        self.assertEqual(mazo_reducido['R'], 6)  # 8 reyes - 2 = 6
        self.assertEqual(mazo_reducido['A'], 6)  # 8 ases - 2 = 6
        self.assertEqual(mazo_reducido['C'], 4)  # No se quitaron caballos

        # Test con una mano de 4 cartas iguales
        mano = "RRRR"
        mazo_reducido = construir_mazo_sin(mano)
        self.assertEqual(mazo_reducido['R'], 4)  # 8 reyes - 4 = 4
        self.assertEqual(mazo_reducido['A'], 8)  # No se quitaron ases

    def test_repartir_3_manos(self):
        """Test para verificar que se reparten 3 manos correctamente"""
        # Crear un mazo reducido para la prueba
        mazo_reducido = {
            'R': 6,
            'C': 4,
            'S': 4,
            'A': 6,
            '7': 4,
            '6': 4,
            '5': 4,
            '4': 4
        }

        # Repartir manos
        manos = repartir_3_manos(mazo_reducido)

        # Verificar que se repartieron 3 manos
        self.assertEqual(len(manos), 3)

        # Verificar que cada mano tiene 4 cartas
        for mano in manos:
            self.assertEqual(len(mano), 4)

        # Verificar que las manos son distintas
        self.assertNotEqual(manos[0], manos[1])
        self.assertNotEqual(manos[0], manos[2])
        self.assertNotEqual(manos[1], manos[2])

    def test_obtener_compañero_index(self):
        """Test para verificar que se obtiene correctamente el índice del compañero"""
        self.assertEqual(obtener_compañero_index(1), 3)
        self.assertEqual(obtener_compañero_index(2), 4)
        self.assertEqual(obtener_compañero_index(3), 1)
        self.assertEqual(obtener_compañero_index(4), 2)

    def test_determinar_ganador(self):
        """Test para verificar que se determina correctamente el ganador"""
        # Caso sin empate
        rankings = {'RRAA': 1, 'CCSS': 2, '7766': 3, '4455': 4}
        orden = [1, 2, 3, 4]
        ganador, mano = determinar_ganador(rankings, orden)
        self.assertEqual(ganador, 1)
        self.assertEqual(mano, 'RRAA')

        # Caso con empate, gana el de menor orden
        rankings = {'RRAA': 1, 'CCSS': 1, '7766': 3, '4455': 4}
        orden = [2, 1, 3, 4]
        ganador, mano = determinar_ganador(rankings, orden)
        self.assertEqual(ganador, 1)
        self.assertEqual(mano, 'CCSS')


if __name__ == '__main__':
    unittest.main()
