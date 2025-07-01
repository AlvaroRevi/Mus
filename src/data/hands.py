from itertools import combinations
from math import comb
from collections import Counter
import pandas as pd

# Mazo real del mus: 40 cartas (sin 8s ni 9s), con valores equivalentes
# Se representan por valor (no palo), considerando que hay 8 "R" (3), 4 "C", 4 "S", 8 "A" (1), y 4 unidades del resto

card_pool = {
    'R': 8,  # Reyes (3s)
    'C': 4,
    'S': 4,
    'A': 8,  # Ases (2s)
    '7': 4,
    '6': 4,
    '5': 4,
    '4': 4
}


# Generamos todas las combinaciones únicas de 4 cartas por valor (ordenadas de mayor a menor)
def generate_hands(pool):
    results = set()
    cards = []
    for card, count in pool.items():
        cards.extend([card] * count)

    # Generamos todas las combinaciones posibles de 4 cartas del mazo sin reemplazo
    for combi in combinations(range(len(cards)), 4):
        hand = [cards[i] for i in combi]
        hand_sorted = ''.join(sorted(hand, key=lambda x: "RCS7654A".index(x)))
        results.add(hand_sorted)
    return results


# Generamos todas las manos válidas
hands_set = generate_hands(card_pool)


# Función para calcular el número de formas de obtener una mano concreta del mazo
def calculate_hand_probability(hand, pool, total_possible_hands):
    count = Counter(hand)
    ways = 1
    for card, qty in count.items():
        ways *= comb(pool[card], qty)
    return ways / total_possible_hands

# Total de combinaciones posibles de 4 cartas de un mazo de 40, sin orden y sin reemplazo
total_hands = comb(40, 4)

# Valor para puntos de juego
card_values = {'R': 10, 'C': 10, 'S': 10, 'A': 1, '7': 7, '6': 6, '5': 5, '4': 4}

# Calculamos probabilidad y puntos para cada mano
hand_data = []
for hand_str in hands_set:
    prob = calculate_hand_probability(hand_str, card_pool, total_hands)
    points = sum(card_values[c] for c in hand_str)
    hand_data.append((hand_str, prob, points))

# Creamos dataframe ordenado por fuerza (opcional) o por nombre
df_hands = pd.DataFrame(hand_data, columns=["Mano", "Probabilidad", "Puntos de juego"])
df_hands = df_hands.sort_values(by="Probabilidad", ascending=False).reset_index(drop=True)


def clasificar_jugada(jugada):
    conteo = Counter(jugada)
    repeticiones = sorted(conteo.values(), reverse=True)

    if repeticiones == [4]:
        return "Duples"
    elif repeticiones == [2, 2]:
        return "Duples"
    elif repeticiones == [3, 1]:
        return "Medias"
    elif repeticiones == [2, 1, 1]:
        return "Par"
    else:
        return "Nada"


df_hands['Pares'] = df_hands['Mano'].apply(clasificar_jugada)

print(df_hands)


