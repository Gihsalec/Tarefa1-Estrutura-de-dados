from .player import MediaPlayer

COMANDOS_DISPONIVEIS = """Comandos disponíveis:
  library load <arquivo> - carrega a biblioteca a partir de CSV/JSON
  library list [--by rating|titulo|artista] - lista as faixas da biblioteca
  playlist new <nome> - cria uma nova playlist e a torna atual
  playlist add <track_id> - adiciona a faixa ao final da playlist atual
  playlist remove <pos> - remove a faixa na posição pos
  playlist show - mostra a playlist atual com o cursor
  play - inicia/retoma a reprodução a partir do cursor
  next - avança (Up Next tem precedência)
  prev - retrocede o cursor da playlist
  enqueue <track_id> - acrescenta a faixa à fila Up Next
  queue show - mostra a fila Up Next
  history - mostra o histórico de reprodução
  smart-shuffle <n> - gera nova playlist com n faixas via fila de prioridade
  save <arquivo> - salva o estado completo em JSON
  load <arquivo> - restaura o estado completo a partir de JSON
  help - mostra esta lista de comandos
  quit - encerra o programa"""


def executar_cli():
    player = MediaPlayer()

    while True:
        try:
            comando = input("mediap> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            print("Encerrando.")
            break
        if not comando:
            continue

        partes = comando.split()

        try:
            if partes[0] == "library" and partes[1] == "load":
                player.carregar_biblioteca(partes[2])

            elif partes[0] == "library" and partes[1] == "list":
                if "--by" in partes:
                    indice = partes.index("--by")
                    categoria = partes[indice + 1]
                else:
                    categoria = "id"
                player.listar_categoria(categoria)

            elif partes[0] == "quit":
                break

            elif partes[0] == "help":
                print(COMANDOS_DISPONIVEIS)

            elif not player.biblioteca_carregada:
                print("Erro: use 'library load <caminho>' para carregar uma base de dados.")

            elif partes[0] == "playlist" and partes[1] == "new":
                nome = partes[2]
                player.playlist_new(nome)

            elif partes[0] == "playlist" and partes[1] == "add":
                track_id = int(partes[2])
                player.playlist_add(track_id)

            elif partes[0] == "playlist" and partes[1] == "remove":
                pos = int(partes[2]) - 1  
                player.playlist_remove(pos)

            elif partes[0] == "playlist" and partes[1] == "show":
                player.playlist_show()

            elif partes[0] == "play":
                player.play()

            elif partes[0] == "next":
                player.next()

            elif partes[0] == "prev":
                player.prev()

            elif partes[0] == "enqueue":
                track_id = int(partes[1])
                player.enqueue(track_id)

            elif partes[0] == "queue" and partes[1] == "show":
                player.queue_show()

            elif partes[0] == "history":
                player.history_show()

            elif partes[0] == "smart-shuffle":
                n = int(partes[1])
                player.smart_shuffle(n)

            elif partes[0] == "save":
                player.save_estado(partes[1])

            elif partes[0] == "load":
                player.load_estado(partes[1])

            else:
                print("Comando inválido, consulte a lista de comandos e digite um comando válido.")

        except ValueError:
            print("Erro: argumento inválido (esperava um número).")
        except IndexError:
            print("Erro: comando incompleto, consulte a lista de comandos.")
        except Exception:
            print("Erro: comando inválido, consulte a lista de comandos e digite um comando válido.")


if __name__ == "__main__":
    executar_cli()
