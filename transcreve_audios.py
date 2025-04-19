#!/usr/bin/env python3
import os
import sys
import subprocess
import argparse

# --- Configurações ---
MODELO = "medium"  # Modelo Whisper a ser usado
IDIOMA = "pt"     # Idioma do áudio ('None' para detecção automática)
OUTPUT_FORMAT = "txt" # Formato de saída desejado

# Formatos de áudio comuns a serem procurados (case-insensitive)
AUDIO_EXTENSIONS = (
    ".opus", ".mp3", ".wav", ".m4a", ".ogg",
    ".flac", ".aac", ".aiff", ".wma"
)

def find_audio_files(directory):
    """Encontra arquivos de áudio com as extensões especificadas em um diretório."""
    audio_files = []
    try:
        for filename in os.listdir(directory):
            # Ignora subdiretórios e verifica a extensão (case-insensitive)
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath) and filename.lower().endswith(AUDIO_EXTENSIONS):
                audio_files.append(filepath)
    except FileNotFoundError:
        print(f"Erro: Diretório '{directory}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao listar arquivos em '{directory}': {e}", file=sys.stderr)
        sys.exit(1)
    return audio_files

def transcribe_file(audio_path, output_dir):
    """Executa o comando whisper para transcrever um único arquivo, pulando se já existir."""
    print(f"Processando: {audio_path}")

    # Constrói o nome esperado do arquivo de saída
    base_name = os.path.splitext(os.path.basename(audio_path))[0]
    output_filename = f"{base_name}.{OUTPUT_FORMAT}"
    output_filepath = os.path.join(output_dir, output_filename)

    # Verifica se o arquivo de saída já existe e não está vazio
    if os.path.exists(output_filepath) and os.path.getsize(output_filepath) > 0:
        print(f"Arquivo '{output_filename}' já existe e não está vazio. Pulando.")
        return True # Considera como sucesso para a contagem, pois o arquivo já existe

    # Monta o comando usando o executável Python atual para rodar whisper como módulo
    command = [
        sys.executable,  # Usa o mesmo interpretador Python que está rodando este script
        "-m",            # Flag para executar módulo
        "whisper",       # Nome do módulo whisper
        # Argumentos originais do whisper:
        audio_path,      # O arquivo de áudio deve vir ANTES das opções no modo módulo
        "--model", MODELO,
        "--language", IDIOMA,
        "--output_format", OUTPUT_FORMAT,
        "--output_dir", output_dir
        # Adicione outras opções se necessário, ex: "--device", "cuda"
    ]

    try:
        # Executa o comando whisper
        # stdout e stderr do whisper serão mostrados no terminal
        result = subprocess.run(command, check=False) # check=False para capturar o erro manualmente

        if result.returncode == 0:
            print(f"Transcrição de '{os.path.basename(audio_path)}' concluída.")
            return True
        else:
            print(f"ERRO ao transcrever '{os.path.basename(audio_path)}'. Código de saída: {result.returncode}", file=sys.stderr)
            # Tenta remover o arquivo de saída potencialmente vazio ou incompleto em caso de erro
            if os.path.exists(output_filepath):
                try:
                    os.remove(output_filepath)
                    print(f"Arquivo de saída incompleto '{output_filename}' removido.")
                except OSError as e:
                    print(f"Aviso: Não foi possível remover o arquivo de saída incompleto '{output_filename}': {e}", file=sys.stderr)
            return False

    except ModuleNotFoundError:
        print(f"Erro: O módulo 'whisper' parece não estar instalado no ambiente Python atual: {sys.executable}", file=sys.stderr)
        print(f"Execute: pip install -U openai-whisper", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Erro inesperado ao executar o Whisper para '{audio_path}': {e}", file=sys.stderr)
        return False

def main():
    """Função principal para parsear argumentos e orquestrar a transcrição."""
    parser = argparse.ArgumentParser(
        description=f"Transcreve arquivos de áudio em um diretório usando Whisper (Modelo: {MODELO}).",
        usage="%(prog)s <diretorio_com_arquivos_audio>"
    )
    parser.add_argument(
        "target_dir",
        metavar="diretorio_com_arquivos_audio",
        help="Caminho para o diretório contendo os arquivos de áudio a serem transcritos."
    )

    args = parser.parse_args()
    target_dir = args.target_dir
    output_dir = target_dir # Salva os TXTs no mesmo diretório dos originais

    # Verifica se o diretório de destino existe
    if not os.path.isdir(target_dir):
        print(f"Erro: Diretório '{target_dir}' não encontrado ou não é um diretório válido.", file=sys.stderr)
        sys.exit(1)

    print(f"Buscando por arquivos de áudio ({', '.join(AUDIO_EXTENSIONS)}) em: {target_dir}")

    audio_files = find_audio_files(target_dir)

    if not audio_files:
        print(f"Nenhum arquivo de áudio nos formatos especificados foi encontrado em '{target_dir}'.")
        sys.exit(0)

    print(f"\nIniciando a transcrição de {len(audio_files)} arquivos de áudio encontrados...")
    print(f"Modelo Whisper: {MODELO}")
    print(f"Idioma: {IDIOMA}")
    print(f"Formato de Saída: {OUTPUT_FORMAT}")
    print(f"Diretório de Saída: {output_dir}")
    if MODELO.lower() == "large":
        print("AVISO: O modelo 'large' exige recursos computacionais significativos (RAM/VRAM) e levará tempo.")
    print("-" * 40)

    success_count = 0
    error_count = 0

    for audio_file in audio_files:
        if transcribe_file(audio_file, output_dir):
            success_count += 1
        else:
            error_count += 1
        print("-" * 40) # Separador entre arquivos

    print("Processo de transcrição finalizado.")
    print(f"Arquivos processados com sucesso: {success_count}")
    if error_count > 0:
        print(f"Arquivos com erro na transcrição: {error_count}")

    if error_count > 0:
        sys.exit(1) # Sai com erro se alguma transcrição falhou
    else:
        sys.exit(0) # Sai com sucesso

if __name__ == "__main__":
    main()