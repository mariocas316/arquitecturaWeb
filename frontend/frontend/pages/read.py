import reflex as rx
from ..state import AppState
from ..styles import card_style, page_style

def read_page() -> rx.Component:
    """
    Componente visual para la ruta de lectura ('/read').
    Permite al usuario ingresar una contraseña para descifrar y visualizar
    el mensaje encriptado cuya ID viene codificada en la URL de la página.
    
    Returns:
        rx.Component: El árbol de componentes renderizado.
    """
    return rx.center(
        rx.vstack(
            rx.heading("Mensaje Secreto 📩", size="8", margin_bottom="4"),
            rx.text(
                "Ingresa la contraseña para desencriptar el mensaje de la URL.",
                color="gray.500",
                margin_bottom="6",
                text_align="center"
            ),
            
            # Input para que el receptor introduzca la clave
            rx.input(
                placeholder="Contraseña",
                type="password",
                value=AppState.password_decrypt,
                on_change=AppState.set_password_decrypt,
                width="100%"
            ),
            
            # Invoca la función asíncrona que hace un GET a la API
            rx.button(
                "Desencriptar",
                on_click=AppState.decrypt_message,
                color_scheme="blue",
                width="100%",
                size="3"
            ),
            
            # Mensaje de error (ej: Contraseña inválida o mensaje destruido)
            rx.cond(
                AppState.decrypt_error != "",
                rx.callout(
                    AppState.decrypt_error,
                    icon="alert_triangle",
                    color_scheme="red",
                    width="100%"
                )
            ),
            
            # Si el descifrado es exitoso, muestra el mensaje
            rx.cond(
                AppState.decrypted_message != "",
                rx.vstack(
                    rx.text("Mensaje Descifrado:", font_weight="bold", color="green.600"),
                    rx.box(
                        rx.text(AppState.decrypted_message, white_space="pre-wrap"),
                        width="100%",
                        padding="4",
                        border_radius="md",
                        background_color="green.50",
                        border="1px solid",
                        border_color="green.200"
                    ),
                    width="100%",
                    align_items="flex-start"
                )
            ),
            
            # Navegación hacia atrás
            rx.link(
                "← Crear nuevo mensaje",
                href="/",
                color="blue.500",
                margin_top="4"
            ),
            style=card_style
        ),
        style=page_style
    )
