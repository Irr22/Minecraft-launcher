import minecraft_launcher_lib
import os
import subprocess
import customtkinter as ctk
from tkinter import messagebox

# Configuración de estilos
ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema de color

# Configuración de la ventana principal
ventana = ctk.CTk()
ventana.geometry('500x500')  # Tamaño de la pantalla
ventana.title('Lanzador de Minecraft')
ventana.resizable(False, False)  # Para que no se pueda cambiar el tamaño

user_window = os.environ["USERNAME"]
minecraft_directori = f"C:/Users/{user_window}/AppData/Roaming/.minecraftLauncher"

# Creación de los widgets
bt_ejecutar_minecraft = ctk.CTkButton(ventana, text='Iniciar', text_color="white", fg_color="#3b82f6")
bt_instalar_versiones = ctk.CTkButton(ventana, text='Instalar versiones', text_color="white", fg_color="#10b981")
bt_instalar_forge = ctk.CTkButton(ventana, text='Instalar Forge', text_color="white", fg_color="#ef4444")

label_nombre = ctk.CTkLabel(ventana, text='Tu nombre:', text_color="white", font=("Arial", 12))
label_ram = ctk.CTkLabel(ventana, text='RAM a usar (GB):', text_color="white", font=("Arial", 12))

entry_nombre = ctk.CTkEntry(ventana, placeholder_text="Introduce tu nombre")
entry_ram = ctk.CTkEntry(ventana, placeholder_text="Introduce la RAM")

# Ver todas las versiones que tengo instaladas y mostrarlas en un desplegable
versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)
versiones_instaladas_lista = [version['id'] for version in versiones_instaladas]

if len(versiones_instaladas_lista) != 0:
    vers = ctk.StringVar(value=versiones_instaladas_lista[0])
else:
    vers = ctk.StringVar(value='sin versiones instaladas')
    versiones_instaladas_lista.append('sin versiones instaladas')

versiones_menu_desplegable = ctk.CTkOptionMenu(ventana, variable=vers, values=versiones_instaladas_lista)
versiones_menu_desplegable.configure()

# Definición de las funciones
def instalar_minecraft():
    version = entry_versiones.get()
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directori)
        print(f'Se ha instalado la versión {version}')
        messagebox.showinfo("Éxito", f'Se ha instalado la versión {version}')
    else:
        messagebox.showerror("Error", "No se ingresó ninguna versión")

def instalar_forge():
    version = entry_versiones.get()
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    if forge:
        minecraft_launcher_lib.forge.install_forge_version(forge, minecraft_directori)
        print('Forge instalado')
        messagebox.showinfo("Éxito", 'Forge instalado')
    else:
        messagebox.showerror("Error", "No se encontró una versión de Forge para esta versión de Minecraft")

def ejecutar_minecraft():
    mine_user = entry_nombre.get()
    ram = entry_ram.get()
    
    if not mine_user:
        messagebox.showerror("Error", "Por favor, introduce tu nombre")
        return
    if not ram:
        messagebox.showerror("Error", "Por favor, introduce la cantidad de RAM a usar")
        return

    version = vers.get()

    options = {
        'username': mine_user,
        'uuid': '',
        'token': '',
        'jvmArguments': [f"-Xmx{ram}G",f"-Xms{ram}G"],
        'launcherVersion': "0.0.2"
    }

    ventana.destroy()
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, options)
    subprocess.run(minecraft_command)

def instalar_versiones_normales():
    ventana_versiones = ctk.CTkToplevel(ventana)
    ventana_versiones.geometry('300x150')
    ventana_versiones.title('Instalar versión')
    ventana_versiones.grab_set()  # Para que quede por encima

    global entry_versiones
    entry_versiones = ctk.CTkEntry(ventana_versiones, placeholder_text="Introduce la versión")
    entry_versiones.pack(pady=10)

    bt_instalar_vers = ctk.CTkButton(ventana_versiones, command=instalar_minecraft, text='Instalar')
    bt_instalar_vers.pack(pady=10)

def instalar_versiones_forge():
    ventana_versiones = ctk.CTkToplevel(ventana)
    ventana_versiones.geometry('300x150')
    ventana_versiones.title('Instalar Forge')
    ventana_versiones.grab_set()  # Para que quede por encima

    global entry_versiones
    entry_versiones = ctk.CTkEntry(ventana_versiones, placeholder_text="Introduce la versión")
    entry_versiones.pack(pady=10)

    bt_instalar_vers = ctk.CTkButton(ventana_versiones, command=instalar_forge, text='Instalar')
    bt_instalar_vers.pack(pady=10)

# Configuración del menú
def menu():
    bt_instalar_versiones.configure(command=instalar_versiones_normales)
    bt_instalar_versiones.place(x=300, y=20)

    bt_instalar_forge.configure(command=instalar_versiones_forge)
    bt_instalar_forge.place(x=300, y=70)

    label_nombre.place(x=20, y=20)
    entry_nombre.place(x=20, y=50)

    label_ram.place(x=20, y=100)
    entry_ram.place(x=20, y=130)

    bt_ejecutar_minecraft.configure(command=ejecutar_minecraft)
    bt_ejecutar_minecraft.place(x=200, y=450)
    versiones_menu_desplegable.place(x=20, y=450)

    ventana.mainloop()

menu()
