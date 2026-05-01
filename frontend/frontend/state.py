import reflex as rx
import httpx

API_URL = "http://localhost:8000/api"

class AppState(rx.State):
    message_to_encrypt: str = ""
    password_encrypt: str = ""
    generated_url: str = ""
    error_message: str = ""

    password_decrypt: str = ""
    decrypted_message: str = ""
    decrypt_error: str = ""

    def set_message_to_encrypt(self, value: str):
        self.message_to_encrypt = value

    def set_password_encrypt(self, value: str):
        self.password_encrypt = value

    def set_password_decrypt(self, value: str):
        self.password_decrypt = value
    
    @rx.var
    def is_read_mode(self) -> bool:
        return "payload" in self.router.page.params

    async def encrypt_message(self):
        self.error_message = ""
        self.generated_url = ""
        if not self.message_to_encrypt or not self.password_encrypt:
            self.error_message = "Por favor, ingresa el mensaje y la contraseña."
            return

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{API_URL}/messages",
                    json={"message": self.message_to_encrypt, "password": self.password_encrypt}
                )
                if response.status_code == 200:
                    msg_id = response.json()["id"]
                    host = "localhost:3000"
                    self.generated_url = f"http://{host}/read?payload={msg_id}"
                    self.message_to_encrypt = ""
                    self.password_encrypt = ""
                else:
                    self.error_message = response.json().get("detail", "Error al encriptar")
            except Exception as e:
                self.error_message = f"Error de conexión con el servidor: {str(e)}"

    async def decrypt_message(self):
        self.decrypt_error = ""
        self.decrypted_message = ""
        
        msg_id = self.router.page.params.get("payload")
        if not msg_id or not self.password_decrypt:
            self.decrypt_error = "Se requiere el ID en la URL y la contraseña."
            return
            
        async with httpx.AsyncClient() as client:
            try:
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
