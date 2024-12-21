import os
import platform
import subprocess
import sys

def activate_and_run():
    # Diretório base do projeto (onde o script está localizado)
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Caminho do ambiente virtual (assumindo que "venv" está na raiz do projeto)
    venv_dir = os.path.join(project_dir, "venv")

    # Detecta o sistema operacional
    system = platform.system().lower()

    # Determina o caminho para o executável Python dentro do ambiente virtual
    if "windows" in system:
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
    else:  # Para Linux ou macOS
        python_executable = os.path.join(venv_dir, "bin", "python")

    # Verifica se o executável Python do ambiente virtual existe
    if not os.path.exists(python_executable):
        print(f"Erro: Executável Python não encontrado no ambiente virtual ({python_executable}).")
        sys.exit(1)

    # Caminho para o arquivo main.py
    main_script = os.path.join(project_dir, "main.py")
    if not os.path.exists(main_script):
        print(f"Erro: Arquivo main.py não encontrado no diretório do projeto ({project_dir}).")
        sys.exit(1)

    # Comando para executar o script main.py
    command = [python_executable, main_script]

    try:
        # Executa o comando
        print(f"Usando o Python do ambiente virtual: {python_executable}")
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    activate_and_run()
