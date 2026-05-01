import reflex as rx
from .pages.index import index_page
from .pages.read import read_page

# Inicialización de la App. Aquí centralizamos las rutas
app = rx.App()

app.add_page(index_page, route="/", title="Secret Share")
app.add_page(read_page, route="/read", title="Mensaje Secreto")
