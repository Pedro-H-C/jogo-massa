import os
import platform
import subprocess

def activate_and_run():
    # Descubra o sistema operacional
    system = platform.system().lower()

    # Determina o caminho para o Python dentro do ambiente virtual
    if "windows" in system:
        python_executable = os.path.join("venv", "Scripts", "python.exe")
    else:  # Linux ou macOS
        python_executable = os.path.join("venv", "bin", "python")

    # Verifica se o executável do Python existe no ambiente virtual
    if not os.path.exists(python_executable):
        print("Ambiente virtual não encontrado ou inválido.")
        return

    try:
        # Executa o script main.py usando o Python do ambiente virtual
        subprocess.run([python_executable, "main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    activate_and_run()
