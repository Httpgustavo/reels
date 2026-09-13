[app]

# (str) Título de tu aplicación
title = Descargador de Reels

# (str) Nombre del paquete
package.name = descargadorreels

# (str) Dominio del paquete (invertido, único)
package.domain = org.tuusuario

# (str) Directorio fuente donde está el main.py
source.dir = .

# (list) Extensiones de archivo a incluir
source.include_exts = py,png,jpg,kv,atlas

# (str) Versión de la app
version = 1.0

# (list) Requerimientos - librerías Python que usa tu app
requirements = python3,kivy,yt-dlp,certifi,urllib3,charset_normalizer,idna,requests,mutagen,websockets,pycryptodomex

# (str) Orientación soportada
orientation = portrait

# (bool) Pantalla completa
fullscreen = 0

# (list) Permisos de Android que necesita la app
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,MANAGE_EXTERNAL_STORAGE

# (int) API de Android objetivo
android.api = 33

# (int) API mínima de Android soportada
android.minapi = 21

# (str) SDK de Android (buildozer lo descarga solo)
#android.sdk_path =

# (str) NDK de Android (buildozer lo descarga solo)
#android.ndk_path =

# (str) Arquitecturas a compilar
android.archs = arm64-v8a, armeabi-v7a

# (bool) Aceptar automáticamente las licencias del SDK
android.accept_sdk_license = True

# (str) Ícono de la app (opcional, poné el path si tenés uno)
#icon.filename = %(source.dir)s/icon.png

[buildozer]

# (int) Nivel de log (0 = error, 1 = info, 2 = debug)
log_level = 2

# (int) Mostrar warnings si se corre como root
warn_on_root = 1
