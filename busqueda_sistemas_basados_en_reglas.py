# ============================================
# Sistema inteligente de rutas basado en reglas
# y búsqueda heurística (A*)
# ============================================

import heapq

# ------------------------------
# 1. BASE DE CONOCIMIENTO (HECHOS)
# ------------------------------
# Hechos: estaciones y conexiones entre ellas
# Cada conexión: (origen, destino, tiempo_en_minutos)

conexiones = [
    ("Portal_A", "Estacion_1", 5),
    ("Estacion_1", "Estacion_2", 4),
    ("Estacion_2", "Estacion_3", 6),
    ("Estacion_3", "Estacion_4", 5),
    ("Estacion_2", "Estacion_5", 7),
    ("Estacion_5", "Estacion_6", 3),
    ("Estacion_4", "Estacion_6", 4),
]

# A partir de los hechos de conexión construimos una estructura de vecinos
def construir_grafo(conexiones):
    grafo = {}
    for origen, destino, tiempo in conexiones:
        if origen not in grafo:
            grafo[origen] = []
        if destino not in grafo:
            grafo[destino] = []
        # Suponemos conexiones bidireccionales
        grafo[origen].append((destino, tiempo))
        grafo[destino].append((origen, tiempo))
    return grafo

grafo = construir_grafo(conexiones)

# ------------------------------
# 2. HEURÍSTICA (CONOCIMIENTO APROXIMADO)
# ------------------------------
# Hechos adicionales: estimación de "distancia" al destino (por ejemplo, tiempo aproximado).
# Estos valores son inventados a modo de ejemplo. Tú los puedes ajustar.

heuristica_estimada = {
    "Portal_A": 20,
    "Estacion_1": 18,
    "Estacion_2": 14,
    "Estacion_3": 10,
    "Estacion_4": 4,
    "Estacion_5": 8,
    "Estacion_6": 0,   # Suponemos que Estacion_6 es un posible destino
}

def heuristica(estacion_actual, destino):
    """
    Regla heurística:
    Si tenemos un valor estimado en la tabla, lo usamos.
    Si no, devolvemos 0 (equivale a Dijkstra).
    """
    return heuristica_estimada.get(estacion_actual, 0)

# ------------------------------
# 3. REGLAS (EMBUTIDAS EN FUNCIONES)
# ------------------------------
# Regla 1 (movilidad):
#   Si existe una conexión (X, Y) en la base de conocimiento,
#   entonces desde X puedo ir a Y con un costo asociado.
#
# Regla 2 (extensión de rutas):
#   Si tengo una ruta válida hasta X y X está conectado con Y,
#   entonces puedo generar una nueva ruta que termina en Y.
#
# El motor de inferencia se implementa con el algoritmo A*.

def mejor_ruta_a_estrella(grafo, inicio, destino):
    """
    Implementación del algoritmo A* como motor de inferencia de rutas.
    Busca la ruta de menor costo desde 'inicio' hasta 'destino'.
    """

    # Cola de prioridad: (costo_estimado_total, costo_acumulado, estacion_actual, ruta)
    frontera = []
    heapq.heappush(frontera, (0, 0, inicio, [inicio]))

    # Para recordar el mejor costo hasta cada estación (evita explorar rutas peores)
    mejor_costo = {inicio: 0}

    while frontera:
        costo_estimado_total, costo_acumulado, actual, ruta = heapq.heappop(frontera)

        # Regla de parada: si llegamos al destino, devolvemos la ruta actual
        if actual == destino:
            return ruta, costo_acumulado

        # Aplicar Regla 2: extender la ruta a los vecinos
        for vecino, tiempo in grafo.get(actual, []):
            nuevo_costo = costo_acumulado + tiempo

            # Solo consideramos la nueva ruta si es mejor que lo que ya conocíamos
            if vecino not in mejor_costo or nuevo_costo < mejor_costo[vecino]:
                mejor_costo[vecino] = nuevo_costo
                # Aplicamos la heurística para estimar el costo total
                costo_total_estimado = nuevo_costo + heuristica(vecino, destino)
                nueva_ruta = ruta + [vecino]
                heapq.heappush(frontera, (costo_total_estimado, nuevo_costo, vecino, nueva_ruta))

    # Si no se encuentra ruta
    return None, float("inf")

# ------------------------------
# 4. PROGRAMA PRINCIPAL
# ------------------------------

if __name__ == "__main__":
    print("=== Sistema inteligente de rutas (ejemplo) ===")
    print("Estaciones disponibles:")
    for estacion in grafo.keys():
        print(" -", estacion)

    inicio = input("Ingrese la estación de origen: ")
    destino = input("Ingrese la estación de destino: ")

    if inicio not in grafo or destino not in grafo:
        print("Alguna de las estaciones no existe en la base de conocimiento.")
    else:
        ruta, costo = mejor_ruta_a_estrella(grafo, inicio, destino)
        if ruta is None:
            print("No se encontró una ruta entre", inicio, "y", destino)
        else:
            print("\nMejor ruta encontrada:")
            print(" -> ".join(ruta))
            print("Costo total aproximado (minutos):", costo)
