"""
ANALIZADOR VECTORIAL DE ESPECTROSCOPÍA INFRARROJA
Nivel: universitario
Aplicación: vectores + momento dipolar + campo eléctrico + magnitudes espectroscópicas.

Modelo simplificado:
La intensidad de interacción se relaciona con la proyección del cambio
del momento dipolar vibracional sobre la dirección del campo eléctrico:

    Δμ_parallel = Δμ · ê

Este programa NO reemplaza un cálculo espectroscópico cuántico ni el análisis
de un espectro experimental real. Es una herramienta didáctica y de cálculo.

Requisitos:
    Python 3.x
    numpy
    matplotlib

Instalación:
    pip install numpy matplotlib
"""

import math
import numpy as np
import matplotlib.pyplot as plt

# Constantes SI
C = 299_792_458.0             # m/s
H = 6.626_070_15e-34          # J s
NA = 6.022_140_76e23          # mol^-1
HC_NA = H * C * NA            # J m/mol


def vector_input(nombre, escala=1.0):
    print(f"\nIngrese las componentes de {nombre}:")
    x = float(input("  componente x = "))
    y = float(input("  componente y = "))
    z = float(input("  componente z = "))
    return np.array([x, y, z], dtype=float) * escala


def magnitud(v):
    return float(np.linalg.norm(v))


def unidad(v):
    n = magnitud(v)
    if n == 0:
        raise ValueError("No se puede obtener un vector unitario de magnitud cero.")
    return v / n


def analisis_vectorial():
    print("\n=== 1. ANÁLISIS VECTORIAL DE UNA TRANSICIÓN IR ===")
    print("El cambio de momento dipolar se introduce en C·m.")
    dmu = vector_input("Δμ [C·m]", 1.0)

    print("\nEl campo eléctrico puede introducirse con unidades relativas,")
    print("porque aquí interesa principalmente su dirección.")
    E = vector_input("E [unidades relativas]", 1.0)

    E_hat = unidad(E)
    dmu_mag = magnitud(dmu)

    producto = float(np.dot(dmu, E_hat))
    proyeccion = producto * E_hat
    perpendicular = dmu - proyeccion

    cos_theta = np.clip(producto / dmu_mag, -1.0, 1.0) if dmu_mag else 0.0
    theta = math.degrees(math.acos(cos_theta)) if dmu_mag else float("nan")

    print("\n--- RESULTADOS ---")
    print(f"|Δμ|                  = {dmu_mag:.6e} C·m")
    print(f"E unitario            = {E_hat}")
    print(f"Δμ · ê                = {producto:.6e} C·m")
    print(f"|Δμ paralelo|         = {abs(producto):.6e} C·m")
    print(f"Vector paralelo       = {proyeccion}")
    print(f"|Δμ perpendicular|    = {magnitud(perpendicular):.6e} C·m")
    print(f"Ángulo θ              = {theta:.4f}°")

    if abs(producto) < 1e-20:
        print("Interpretación didáctica: la proyección sobre E es prácticamente nula.")
    else:
        print("Interpretación didáctica: existe una componente de Δμ paralela al campo.")

    return dmu, E_hat, producto


def conversiones_espectrales():
    print("\n=== 2. CONVERSIONES ESPECTRALES ===")
    wn = float(input("Número de onda ṽ [cm⁻¹] = "))

    frecuencia = C * wn * 100.0
    longitud_m = 1.0 / (wn * 100.0)
    longitud_um = longitud_m * 1e6
    energia_foton = H * frecuencia
    energia_mol = energia_foton * NA / 1000.0  # kJ/mol

    print("\n--- RESULTADOS ---")
    print(f"Frecuencia ν          = {frecuencia:.6e} Hz")
    print(f"Longitud de onda λ    = {longitud_um:.6f} μm")
    print(f"Energía por fotón     = {energia_foton:.6e} J")
    print(f"Energía molar         = {energia_mol:.6f} kJ/mol")


def espectro_sintetico():
    print("\n=== 3. SIMULACIÓN DE UN ESPECTRO IR ===")
    print("Se construye un espectro didáctico mediante perfiles gaussianos.")
    n = int(input("Número de bandas a simular [ej. 5] = "))

    centros, intensidades, anchos = [], [], []

    for i in range(n):
        print(f"\nBanda {i+1}")
        centros.append(float(input("  Número de onda [cm⁻¹] = ")))
        intensidades.append(float(input("  Intensidad relativa [0–100] = ")))
        anchos.append(float(input("  Ancho σ [cm⁻¹] = ")))

    # El IR suele representarse con el número de onda decreciendo hacia la derecha.
    x_min = min(centros) - 5 * max(anchos)
    x_max = max(centros) + 5 * max(anchos)
    x = np.linspace(x_max, x_min, 3000)
    y = np.zeros_like(x)

    for centro, intensidad, sigma in zip(centros, intensidades, anchos):
        y += intensidad * np.exp(-0.5 * ((x - centro) / sigma) ** 2)

    plt.figure(figsize=(10, 5))
    plt.plot(x, y, linewidth=1.8)
    plt.xlabel("Número de onda (cm⁻¹)")
    plt.ylabel("Absorbancia relativa")
    plt.title("Espectro IR sintético — modelo gaussiano")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.show()


def caso_integrador():
    print("\n=== 4. CASO INTEGRADOR ===")
    print("Ejemplo modificable: una vibración molecular produce un cambio de")
    print("momento dipolar y se analiza su orientación respecto al campo.")

    dmu = np.array([0.60, 0.80, 0.00]) * 1e-30
    E = np.array([0.80, 0.60, 0.00])
    E_hat = unidad(E)

    producto = float(np.dot(dmu, E_hat))
    theta = math.degrees(
        math.acos(np.clip(producto / magnitud(dmu), -1.0, 1.0))
    )

    wn = 1715.0
    frecuencia = C * wn * 100
    energia_mol = H * frecuencia * NA / 1000

    print("\nDatos del caso:")
    print(f"Δμ = {dmu} C·m")
    print(f"E  = {E}")
    print(f"ṽ  = {wn:.1f} cm⁻¹")

    print("\nResultados:")
    print(f"|Δμ| = {magnitud(dmu):.6e} C·m")
    print(f"Δμ·ê = {producto:.6e} C·m")
    print(f"θ   = {theta:.4f}°")
    print(f"ν   = {frecuencia:.6e} Hz")
    print(f"E   = {energia_mol:.4f} kJ/mol")

    # Representación vectorial 2D del ejemplo
    plt.figure(figsize=(7, 6))
    origen = np.array([[0, 0]])
    plt.quiver(*origen[0], dmu[0]*1e30, dmu[1]*1e30,
               angles="xy", scale_units="xy", scale=1, label="Δμ × 10³⁰")
    plt.quiver(*origen[0], E_hat[0], E_hat[1],
               angles="xy", scale_units="xy", scale=1, label="ê")
    plt.axhline(0, linewidth=0.8)
    plt.axvline(0, linewidth=0.8)
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    plt.xlabel("Componente x")
    plt.ylabel("Componente y")
    plt.title("Orientación vectorial en una transición IR")
    plt.grid(alpha=0.25)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main():
    while True:
        print("\n" + "=" * 68)
        print("     ANALIZADOR VECTORIAL DE ESPECTROSCOPÍA INFRARROJA")
        print("=" * 68)
        print("1. Análisis de Δμ respecto al campo eléctrico")
        print("2. Conversión de número de onda a frecuencia, λ y energía")
        print("3. Simulación de un espectro IR")
        print("4. Caso integrador con representación vectorial")
        print("5. Salir")

        opcion = input("\nSeleccione una opción: ").strip()

        try:
            if opcion == "1":
                analisis_vectorial()
            elif opcion == "2":
                conversiones_espectrales()
            elif opcion == "3":
                espectro_sintetico()
            elif opcion == "4":
                caso_integrador()
            elif opcion == "5":
                print("\nPrograma finalizado.")
                break
            else:
                print("Opción no válida.")
        except ValueError as error:
            print(f"\nDato no válido: {error}")
        except Exception as error:
            print(f"\nSe produjo un error: {error}")


if __name__ == "__main__":
    main()
