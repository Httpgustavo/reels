import os
import threading
import certifi
import customtkinter as ctk
import yt_dlp
from customtkinter import filedialog

# Solución para error de certificados SSL
os.environ["SSL_CERT_FILE"] = certifi.where()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class DescargadorReels(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuración de la ventana (un poco más alta para los botones)
        self.title("Descargador de Instagram Reels")
        self.geometry("500x350")
        self.resizable(False, False)

        # Ruta por defecto (Carpeta Descargas del sistema)
        self.ruta_guardado = os.path.join(os.path.expanduser("~"), "Downloads")

        # --- Interfaz Gráfica ---

        # Título principal
        self.label_titulo = ctk.CTkLabel(
            self, text="Descargar Reels", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_titulo.pack(padx=20, pady=15)

        # Campo de texto para la URL
        self.entry_url = ctk.CTkEntry(
            self, width=420, placeholder_text="Pega el enlace del Reel aquí..."
        )
        self.entry_url.pack(padx=20, pady=10)

        # Contenedor para la selección de carpeta
        self.frame_carpeta = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_carpeta.pack(padx=20, pady=10, fill="x")

        # Campo que muestra la ruta seleccionada
        self.entry_ruta = ctk.CTkEntry(self.frame_carpeta, width=310)
        self.entry_ruta.insert(0, self.ruta_guardado)
        self.entry_ruta.configure(state="disabled")
        self.entry_ruta.pack(side="left", padx=(0, 10))

        # Botón para cambiar carpeta
        self.btn_buscar = ctk.CTkButton(
            self.frame_carpeta,
            text="Examinar...",
            width=100,
            command=self.seleccionar_carpeta,
        )
        self.btn_buscar.pack(side="right")

        # Botón de descarga
        self.btn_descargar = ctk.CTkButton(
            self,
            text="Descargar Video",
            width=200,
            command=self.iniciar_descarga_hilo,
        )
        self.btn_descargar.pack(padx=20, pady=10)

        # Botón rápido para abrir carpeta (Inicia deshabilitado)
        self.btn_abrir_carpeta = ctk.CTkButton(
            self,
            text="📁 Abrir Carpeta de Destino",
            width=200,
            fg_color="gray",
            state="disabled",
            command=self.abrir_explorador,
        )
        self.btn_abrir_carpeta.pack(padx=20, pady=5)

        # Texto de estado
        self.label_estado = ctk.CTkLabel(
            self, text="Listo para descargar", font=ctk.CTkFont(size=12)
        )
        self.label_estado.pack(padx=20, pady=10)

    def seleccionar_carpeta(self):
        carpeta_elegida = filedialog.askdirectory(initialdir=self.ruta_guardado)
        if carpeta_elegida:
            self.ruta_guardado = carpeta_elegida
            self.entry_ruta.configure(state="normal")
            self.entry_ruta.delete(0, "end")
            self.entry_ruta.insert(0, self.ruta_guardado)
            self.entry_ruta.configure(state="disabled")

    def abrir_explorador(self):
        """Abre la carpeta seleccionada en el Explorador de Windows."""
        if os.path.exists(self.ruta_guardado):
            os.startfile(self.ruta_guardado)

    def iniciar_descarga_hilo(self):
        url = self.entry_url.get().strip()
        if not url:
            self.label_estado.configure(
                text="⚠️ Por favor, ingresa una URL válida.", text_color="orange"
            )
            return

        # Deshabilitar controles durante la descarga
        self.btn_descargar.configure(state="disabled")
        self.btn_buscar.configure(state="disabled")
        self.btn_abrir_carpeta.configure(state="disabled", fg_color="gray")
        self.label_estado.configure(
            text="Descargando... Por favor espera.", text_color="cyan"
        )

        hilo = threading.Thread(target=self.descargar_video, args=(url,))
        hilo.start()

    def descargar_video(self, url):
        ydl_opts = {
            "format": "mp4/best",
            "outtmpl": os.path.join(self.ruta_guardado, "%(title)s.%(ext)s"),
            "quiet": True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            self.label_estado.configure(
                text="✅ ¡Descarga completada con éxito!", text_color="green"
            )
            self.entry_url.delete(0, "end")

            # Habilitar el botón de abrir carpeta en color verde exitoso
            self.btn_abrir_carpeta.configure(state="normal", fg_color="#2ecc71")

        except Exception as e:
            self.label_estado.configure(
                text="❌ Error al descargar. Revisa el enlace.", text_color="red"
            )
            print(f"Error: {e}")
        finally:
            self.btn_descargar.configure(state="normal")
            self.btn_buscar.configure(state="normal")


if __name__ == "__main__":
    app = DescargadorReels()
    app.mainloop()
