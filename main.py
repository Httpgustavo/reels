import os
import threading
import certifi
import yt_dlp
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.utils import platform

# Solución para certificados en red
os.environ["SSL_CERT_FILE"] = certifi.where()

class DescargadorAndroidApp(App):
    def build(self):
        self.title = "Descargador de Reels"
        
        # Contenedor principal vertical
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # Título
        self.label_titulo = Label(text="Descargar Instagram Reels", font_size='20sp', size_hint_y=None, height=40)
        layout.add_widget(self.label_titulo)
        
        # Campo para pegar la URL
        self.entry_url = TextInput(hint_text="Pega el enlace del Reel aquí...", multiline=False, size_hint_y=None, height=50)
        layout.add_widget(self.entry_url)
        
        # Botón para descargar
        self.btn_descargar = Button(text="Descargar Video", background_color=(0.2, 0.6, 1, 1), size_hint_y=None, height=50)
        self.btn_descargar.bind(on_press=self.iniciar_descarga_hilo)
        layout.add_widget(self.btn_descargar)
        
        # Texto de estado
        self.label_estado = Label(text="Listo para descargar", font_size='14sp', size_hint_y=None, height=40)
        layout.add_widget(self.label_estado)
        
        return layout

    def iniciar_descarga_hilo(self, instance):
        url = self.entry_url.text.strip()
        if not url:
            self.label_estado.text = "⚠️ Por favor, ingresa una URL válida."
            return
            
        self.btn_descargar.disabled = True
        self.label_estado.text = "Descargando... Por favor espera."
        
        # Hilo para no congelar la pantalla del celular
        hilo = threading.Thread(target=self.descargar_video, args=(url,))
        hilo.start()

    def descargar_video(self, url):
        # En Android, guardamos en la carpeta pública de Descargas del teléfono
        if platform == 'android':
            from android.storage import primary_external_storage_path
            ruta_descargas = os.path.join(primary_external_storage_path(), 'Download')
        else:
            # Por si lo pruebas primero en la PC
            ruta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")

        ydl_opts = {
            'format': 'mp4/best',
            'outtmpl': os.path.join(ruta_descargas, '%(title)s.%(ext)s'),
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.label_estado.text = "✅ ¡Descarga completada en tu carpeta Descargas!"
            self.entry_url.text = ""
        except Exception as e:
            self.label_estado.text = "❌ Error al descargar. Revisa el enlace."
            print(f"Error: {e}")
        finally:
            self.btn_descargar.disabled = False

if __name__ == '__main__':
    DescargadorAndroidApp().run()
