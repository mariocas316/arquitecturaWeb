import reflex as rx
import httpx

API_URL = "http://localhost:8000/api"

class AppState(rx.State):
    """
    Estado global de la aplicación (Frontend).
    Gestiona todas las variables reactivas de la interfaz y las interacciones
    con el backend a través de peticiones HTTP asíncronas.
    """
    
    # Variables de la vista de Creación (index)
    message_to_encrypt: str = ""
    password_encrypt: str = ""
    generated_url: str = ""
    error_message: str = ""

    # Variables de la vista de Lectura (read)
    password_decrypt: str = ""
    decrypted_message: str = ""
    decrypt_error: str = ""

    def set_message_to_encrypt(self, value: str):
        """Asigna el valor al mensaje a encriptar."""
        self.message_to_encrypt = value

    def set_password_encrypt(self, value: str):
        """Asigna la contraseña de encriptación."""
        self.password_encrypt = value

    def set_password_decrypt(self, value: str):
        """Asigna la contraseña para desencriptar."""
        self.password_decrypt = value
    
    @rx.var
    def is_read_mode(self) -> bool:
        """
        Variable computada que verifica si la página actual
        tiene un parámetro 'payload' en la URL.
        """
        return "payload" in self.router.page.params

    async def encrypt_message(self):
        """
        Envía los datos de la vista de creación al backend para cifrarlos y guardarlos.
        Si la petición es exitosa, genera la URL compartible apuntando al ID creado.
        """
        self.error_message = ""
        self.generated_url = ""
        
        # Validación de campos
        if not self.message_to_encrypt or not self.password_encrypt:
            self.error_message = "Por favor, ingresa el mensaje y la contraseña."
            return

        async with httpx.AsyncClient() as client:
            try:
                # Petición HTTP POST al endpoint de creación (C en CRUD)
                response = await client.post(
                    f"{API_URL}/messages",
                    json={"message": self.message_to_encrypt, "password": self.password_encrypt}
                )
                if response.status_code == 200:
                    msg_id = response.json()["id"]
                    host = "localhost:3000"
                    # Ensamblar URL final
                    self.generated_url = f"http://{host}/read?payload={msg_id}"
                    
                    # Limpiar campos tras el éxito
                    self.message_to_encrypt = ""
                    self.password_encrypt = ""
                else:
                    self.error_message = response.json().get("detail", "Error al encriptar")
            except Exception as e:
                self.error_message = f"Error de conexión con el servidor: {str(e)}"

    async def decrypt_message(self):
        """
        Recupera el ID desde los parámetros de la URL y hace una petición
        GET al backend para leer (y destruir) el mensaje asociado.
        """
        self.decrypt_error = ""
        self.decrypted_message = ""
        
        msg_id = self.router.page.params.get("payload")
        
        # Validar la existencia de parámetros
        if not msg_id or not self.password_decrypt:
            self.decrypt_error = "Se requiere el ID en la URL y la contraseña."
            return
            
        async with httpx.AsyncClient() as client:
            try:
                # Petición HTTP GET al endpoint de lectura (R en CRUD)
                response = await client.get(
                    f"{API_URL}/messages/{msg_id}",
                    params={"password": self.password_decrypt}
                )
                if response.status_code == 200:
                    self.decrypted_message = response.json()["message"]
                    self.password_decrypt = ""
                elif response.status_code == 404:
                    self.decrypt_error = "Mensaje no encontrado o ya fue leído y destruido."
                else:
                    self.decrypt_error = response.json().get("detail", "Contraseña incorrecta")
            except Exception as e:
                self.decrypt_error = f"Error de conexión con el servidor: {str(e)}"
