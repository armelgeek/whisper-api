# Transcritor de Áudio em Lote com Whisper

Este script Python automatiza a transcrição de múltiplos arquivos de áudio contidos em um diretório especificado, utilizando o modelo Whisper da OpenAI.

## Funcionalidades

*   **Transcreve em Lote:** Processa todos os arquivos de áudio com extensões comuns (veja `AUDIO_EXTENSIONS` no script) encontrados em um diretório.
*   **Modelo Whisper:** Utiliza o poderoso modelo Whisper para realizar a transcrição.
*   **Configurável:** Permite definir o modelo Whisper a ser usado (`MODELO`), o idioma do áudio (`IDIOMA`) e o formato de saída (`OUTPUT_FORMAT`) diretamente no script.
*   **Detecção de Idioma:** Pode detectar automaticamente o idioma se `IDIOMA` for definido como `None`.
*   **Evita Retrabalho:** Verifica se um arquivo de transcrição já existe e não está vazio antes de processar o áudio correspondente, pulando a transcrição se for o caso.
*   **Saída Organizada:** Salva os arquivos de transcrição no mesmo diretório dos arquivos de áudio originais.
*   **Feedback:** Exibe o progresso e informa sobre sucessos e erros durante a execução.

## Pré-requisitos

*   **Python 3:** Certifique-se de ter o Python 3 instalado.
*   **Whisper:** Instale a biblioteca Whisper da OpenAI:
    ```bash
    pip install -U openai-whisper
    ```
*   **(Opcional) FFmpeg:** O Whisper requer o FFmpeg para processar diversos formatos de áudio. Instale-o através do gerenciador de pacotes do seu sistema:
    *   **Debian/Ubuntu:** `sudo apt update && sudo apt install ffmpeg`
    *   **Fedora:** `sudo dnf install ffmpeg`
    *   **macOS (usando Homebrew):** `brew install ffmpeg`
    *   **Windows (usando Chocolatey):** `choco install ffmpeg`
    *   Ou baixe diretamente do [site oficial do FFmpeg](https://ffmpeg.org/download.html).

## Configuração

Antes de executar, você pode ajustar as seguintes constantes no início do script `transcreve_audios.py`:

*   `MODELO`: Define qual modelo Whisper usar (ex: "tiny", "base", "small", "medium", "large"). Modelos maiores são mais precisos, mas exigem mais recursos (RAM/VRAM) e tempo. O padrão atual é "medium".
*   `IDIOMA`: O código do idioma do áudio (ex: "pt" para português, "en" para inglês). Defina como `None` para detecção automática (pode ser menos preciso). O padrão atual é "pt".
*   `OUTPUT_FORMAT`: O formato desejado para os arquivos de transcrição (ex: "txt", "vtt", "srt", "tsv", "json"). O padrão atual é "txt".
*   `AUDIO_EXTENSIONS`: Tupla com as extensões de arquivo de áudio a serem procuradas.

## Como Usar

1.  **Salve o script:** Certifique-se de que o arquivo `transcreve_audios.py` esteja salvo em seu sistema.
2.  **Navegue até o diretório:** Abra um terminal ou prompt de comando.
3.  **Execute o script:** Use o seguinte comando, substituindo `<diretorio_com_arquivos_audio>` pelo caminho real para a pasta que contém seus arquivos de áudio:

    ```bash
    python /caminho/para/transcreve_audios.py <diretorio_com_arquivos_audio>
    ```

    **Exemplo:**

    ```bash
    python /home/wcruz/whisper_open_ai/transcreve_audios.py /home/wcruz/meus_audios
    ```

4.  **Aguarde:** O script buscará os arquivos de áudio, exibirá as configurações e iniciará o processo de transcrição. O progresso será exibido no terminal. Os arquivos de texto (`.txt` por padrão) com as transcrições serão salvos no mesmo diretório dos arquivos de áudio originais.

## Observações

*   O modelo "large" é muito intensivo em recursos. Certifique-se de que sua máquina tenha RAM e/ou VRAM suficientes.
*   Se ocorrer um erro durante a transcrição de um arquivo, o script tentará remover o arquivo de saída potencialmente incompleto e continuará com os próximos arquivos.
*   O script sairá com um código de erro se alguma transcrição falhar.
