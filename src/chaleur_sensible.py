def chaleur_sensible(Ts: float, Ta: float, va: float) -> float:
    """
    Chaleur sensible φs (W/m²)
    Rimsha-Donchenko (1957)
    φs = 0.4844 * (kn + 3.9 * va) * (Ts - Ta)
    kn = 8.0 + 0.35 * (Ts - Ta)
    """
    kn = 8.0 + 0.35 * (Ts - Ta)
    return 0.4844 * (kn + 3.9 * va) * (Ts - Ta)
