def flux_eau_air(NetRad: float, phi_s_aw: float, phi_l_aw: float) -> float:
    """
    Flux interface eau-air φaw (W/m²)
    φaw = NetRad ± φs_aw ± φl_aw
    """
    return NetRad + phi_s_aw + phi_l_aw

def flux_glace_air(NetRad: float, phi_s_ai: float, phi_l_ai: float) -> float:
    """
    Flux interface glace-air φai (W/m²)
    φai = NetRad ± φs_ai ± φl_ai
    """
    return NetRad + phi_s_ai + phi_l_ai
