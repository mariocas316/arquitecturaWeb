import reflex as rx

"""
Módulo centralizado de Estilos para el Frontend Reflex.
Cumple con la arquitectura recomendada para mantener el diseño UI
(tokens de diseño, colores, espaciados) completamente separado
de la lógica (estado) y de la estructura (componentes).
"""

bg_color = "gray.100"
card_bg_color = "white"

# Estilo estándar aplicado a las "tarjetas" o contenedores principales
card_style = {
    "width": "100%",
    "max_width": "500px",
    "padding": "8",
    "border_radius": "lg",
    "box_shadow": "lg",
    "background_color": card_bg_color,
}

# Estilo estándar para rellenar la pantalla completa
page_style = {
    "width": "100vw",
    "height": "100vh",
    "background_color": bg_color,
}
