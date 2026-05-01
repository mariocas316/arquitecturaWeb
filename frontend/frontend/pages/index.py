import reflex as rx
from ..state import AppState
from ..styles import card_style, page_style

def index_page() -> rx.Component:
    return rx.center(
        rx.vstack(
            rx.heading("Secret Share 🔒", size="8", margin_bottom="4"),
            rx.text(
                "Crea un mensaje encriptado y compártelo de forma segura. Sin persistencia en base de datos.",
                color="gray.500",
                margin_bottom="6",
                text_align="center"
            ),
            rx.text_area(
                placeholder="Escribe tu mensaje secreto aquí...",
                value=AppState.message_to_encrypt,
                width="100%",
                min_height="150px"
            ),
            rx.input(
                placeholder="Contraseña para encriptar",
                type="password",
                value=AppState.password_encrypt,
                width="100%"
            ),
            rx.button(
                "Encriptar y Generar Link",
                on_click=AppState.encrypt_message,
                color_scheme="blue",
                width="100%",
                size="3"
            ),
            rx.cond(
                AppState.error_message != "",
                rx.callout(
                    AppState.error_message,
                    icon="alert_triangle",
                    color_scheme="red",
                    width="100%"
                )
            ),
            rx.cond(
                AppState.generated_url != "",
                rx.vstack(
                    rx.text("¡Enlace generado exitosamente!", font_weight="bold", color="green.500"),
                    rx.code(AppState.generated_url, width="100%", overflow_wrap="break-word", padding="2"),
                    rx.button(
                        "Copiar Enlace",
                        on_click=rx.set_clipboard(AppState.generated_url),
                        color_scheme="green",
                        variant="soft"
                    ),
                    width="100%",
                    align_items="center",
                    padding="4",
                    border="1px solid",
                    border_color="gray.200",
                    border_radius="md",
                    background_color="gray.50"
                )
            ),
            style=card_style
        ),
        style=page_style
    )
