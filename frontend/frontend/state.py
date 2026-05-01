import reflex as rx
import httpx
import urllib.parse

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
                    f"{API_URL}/encrypt",
                    json={"message": self.message_to_encrypt, "password": self.password_encrypt}
                )
                if response.status_code == 200:
                    payload = response.json()["url_payload"]
                    
                    # We can use localhost:3000 as the default if we can't reliably get self.router.page.host in background task
                    host = "localhost:3000"
                    
                    self.generated_url = f"http://{host}/read?payload={urllib.parse.quote(payload)}"
                    self.message_to_encrypt = ""
                    self.password_encrypt = ""
                else:
                    self.error_message = response.json().get("detail", "Error al encriptar")
            except Exception as e:
                self.error_message = f"Error de conexión con el servidor: {str(e)}"

    async def decrypt_message(self):
        self.decrypt_error = ""
        self.decrypted_message = ""
        
        payload = self.router.page.params.get("payload")
        if not payload or not self.password_decrypt:
            self.decrypt_error = "Se requiere el payload (en la URL) y la contraseña."
            return
            
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{API_URL}/decrypt",
                    json={"url_payload": payload, "password": self.password_decrypt}
                )
                if response.status_code == 200:
                    self.decrypted_message = response.json()["message"]
                    self.password_decrypt = ""
                else:
                    self.decrypt_error = response.json().get("detail", "Error al desencriptar")
            except Exception as e:
                self.decrypt_error = f"Error de conexión con el servidor: {str(e)}"
