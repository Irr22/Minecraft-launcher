import minecraft_launcher_lib
import os
import subprocess

# Definir directorio de Minecraft
user_window = os.environ["USERNAME"]
minecraft_directori = f"C:/Users/{user_window}/AppData/Roaming/.minecraftLauncher"

# Obtener versiones instaladas
versiones_instaladas = minecraft_launcher_lib.utils.get_installed_versions(minecraft_directori)
versiones_instaladas_lista = []
for versiones_instaladas in versiones_instaladas:
    versiones_instaladas_lista.append(versiones_instaladas['id'])

if len(versiones_instaladas_lista) == 0:
    print("No hay versiones instaladas.")
    versiones_instaladas_lista.append('sin versiones instaladas')

def instalar_minecraft(version):
    if version:
        minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directori)
        print(f'Se ha instalado la version {version}')
    else:
        print('No se ingreso ninguna version')

def instalar_forge(version):
    forge = minecraft_launcher_lib.forge.find_forge_version(version)
    minecraft_launcher_lib.forge.install_forge_version(forge, minecraft_directori)
    print('Forge instalado')

def ejecutar_minecraft(mine_user, version, ram):
    options = {
        'username': mine_user,
        'uuid': '',
        'token': '',
        'jvmArguments': [f"-Xmx{ram}G", f"-Xms{ram}G"],
        'launcherVersion': "0.0.2"
    }
    
    minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(version, minecraft_directori, options)
    subprocess.run(minecraft_command)

def main():
    while True:
        print("\nMenu:")
        print("1. Instalar versiones de Minecraft")
        print("2. Instalar Forge")
        print("3. Ejecutar Minecraft")
        print("4. Salir")

        choice = input("Selecciona una opción: ")

        if choice == '1':
            print(f"Versiones instaladas: {', '.join(versiones_instaladas_lista)}")
            version = input("Ingresa la versión de Minecraft que deseas instalar: ")
            instalar_minecraft(version)
        
        elif choice == '2':
            print(f"Versiones instaladas: {', '.join(versiones_instaladas_lista)}")
            version = input("Ingresa la versión de Minecraft para instalar Forge: ")
            instalar_forge(version)

        elif choice == '3':
            mine_user = input("Ingresa tu nombre de usuario: ")
            print(f"Versiones instaladas: {', '.join(versiones_instaladas_lista)}")
            version = input("Selecciona una versión: ")
            ram = input("Ingresa la cantidad de RAM (en GB) a usar: ")
            ejecutar_minecraft(mine_user, version, ram)
        
        elif choice == '4':
            print("Saliendo...")
            break
        
        else:
            print("Opción no válida, intenta de nuevo.")

if __name__ == "__main__":
    main()