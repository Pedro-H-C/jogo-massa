import os
import platform
import subprocess

def activate_and_run():
    # Detecta o sistema operacional
    system = platform.system().lower()

    # Determina o caminho para o executável Python dentro do ambiente virtual
    if "windows" in system:
        python_executable = os.path.join("env", "Scripts", "python.exe")
    else:  # Linux ou macOS
        python_executable = os.path.join("env", "bin", "python")

    # Verifica se o executável Python do ambiente virtual existe
    if not os.path.exists(python_executable):
        print("Ambiente virtual não encontrado ou inválido.")
        return

    # Comando para executar o script main.py
    command = [python_executable, "main.py"]
    try:
        # Executa o comando
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    activate_and_run()