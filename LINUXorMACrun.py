import os
import platform
import subprocess
import sys

def activate_and_run():
    # Diretório base do projeto (onde o run.py está localizado)
    project_dir = os.path.dirname(os.path.abspath(__file__))

    # Caminho do ambiente virtual (assumindo que "venv" está na raiz do projeto)
    venv_dir = os.path.join(project_dir, "venv")

    # Determina o caminho para o Python no ambiente virtual dependendo do sistema operacional
    if platform.system() == "Windows":
        python_executable = os.path.join(venv_dir, "Scripts", "python.exe")
    else:
        python_executable = os.path.join(venv_dir, "bin", "python3")

    # Caminho para o arquivo main.py
    main_script = os.path.join(project_dir, "main.py")
    if not os.path.exists(main_script):
        print(f"Erro: Arquivo main.py não encontrado no diretório do projeto ({project_dir}).")
        sys.exit(1)

    # Verifica se o executável Python existe
    if not os.path.exists(python_executable):
        print(f"Erro: Executável Python não encontrado no ambiente virtual ({python_executable}).")
        sys.exit(1)
    try:
        # Executa o script main.py usando o Python do ambiente virtual
        print(f"Usando o Python do ambiente virtual: {python_executable}")
        subprocess.run([python_executable, main_script], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    activate_and_run()