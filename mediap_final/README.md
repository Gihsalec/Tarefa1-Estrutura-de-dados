# mediap - Media Player via linha de comando

Mini projeto 1 (Estrutura de Dados, Prof. Ernesto).

## Estrutura de arquivos
```
mediap/
    __init__.py # transforma mediap em um pacote Python
    __main__.py # ponto que o "python -m mediap" procura
    main.py # lógica de entrada (chamada pelo __main__.py)
    models.py # classe Track
    doubly_linked_list.py # DoublyLinkedList própria + classe Playlist
    player.py # classe MediaPlayer
    cli.py # laço de leitura/parse dos comandos do terminal
    library.json # biblioteca de faixas
README.md
test_mediap.py # testes automatizados (fora do pacote)
```

## Como executar

  Abra o terminal e digite o comando: `python -m mediap`

**Importante:** rode sempre a partir da pasta que contém a pasta `mediap/`, no caso a pasta "mediap_final". O comando `python -m` sempre procura um arquivo `__main__.py` dentro do pacote, por isso existem dois arquivos (`__main__.py` e `main.py`) o primeiro é o que o python encontra, o segundo é onde está a lógica.

  Dentro do programa, carregue a biblioteca com: `library load mediap/library.json` (o caminho é relativo à pasta de onde você rodou o `python -m mediap`).

## Comandos disponíveis:
  ```
  library load <arquivo> - carrega a biblioteca JSON.
  library list [--by rating|titulo|artista] (default: id)- lista as faixas da biblioteca.
  playlist new <nome> - cria uma nova playlist e a torna atual.
  playlist add <track_id> - adiciona a faixa ao final da playlist atual.
  playlist remove <pos> - remove a faixa na posição pos.
  playlist show - mostra a playlist atual com o cursor.
  play - inicia a reprodução a partir do cursor.
  next - avança (Up Next tem precedência).
  prev - retrocede o cursor da playlist.
  enqueue <track_id> - acrescenta a faixa à fila Up Next.
  queue show - mostra a fila Up Next.
  history - mostra o histórico de reprodução.
  smart-shuffle <n> - gera nova playlist com n faixas via fila de prioridade.
  save <arquivo> - salva o estado completo em JSON.
  load <arquivo> - restaura o estado completo a partir de JSON.
  help - mostra esta lista de comandos.
  quit - encerra o programa.
  ```

## Como rodar os testes automatizados

  Para rodar os testes automatizados digite o seguinte comando no terminal (antes de entrar no programa ou depois de digitar `quit`): `python -m unittest test_mediap -v`
  Em que mostra o nome de cada teste e se passou (`ok`) ou falhou


## Exemplo de sessão

```
mediap> library load mediap/library.json
Sucesso: 10 faixas carregadas
mediap> playlist new minha
Playlist "minha" criada.
mediap> playlist add 3
mediap> playlist add 4
mediap> playlist show
> 1. Manchild — Sabrina Carpenter (2:03)
  2. Toxic — Britney Spears (3:18)
mediap> play
>>> Tocando: "Manchild" — Sabrina Carpenter (2:03)
mediap> enqueue 2
mediap> next
>>> Tocando: "like JENNIE" — Jennie (2:03)
mediap> next
>>> Tocando: "Toxic" — Britney Spears (3:18)
mediap> history
1. Toxic — Britney Spears [21:25:01]
2. like JENNIE — Jennie [21:25:01]
3. Manchild — Sabrina Carpenter [21:25:01]
mediap> smart-shuffle 5
Playlist "smart-shuffle" criada com 5 faixas.
mediap> save estado.json
Estado salvo em 'estado.json'.
mediap> load estado.json
Estado restaurado de 'estado.json'.
mediap> quit
```

## Formato aceito pela `library.json`

  O `library load` espera um objeto `{"musicas": [...]}` em que cada faixa tem as chaves `id`, `titulo`, `artista`, `duracao_segundos`, `rating` e `data_adicao`, como a `library.json` deste projeto usa.

## Fórmula do smart-shuffle

  Foi usada exatamente a fórmula sugerida no documento da atividade sem alterações:

  chave(f) = -10 * rating(f) + penalty_rec(f)
  penalty_rec(f) = 5 - pos_hist(f), se pos_hist(f) < 5 (entre as 5 últimas tocadas)
  penalty_rec(f) = 0, caso contrário


  Onde `pos_hist(f) = 0` para a última faixa tocada. A `queue.PriorityQueue` retorna sempre a menor chave primeiro — por isso o rating entra com sinal negativo (rating maior → chave menor → sai primeiro da fila).
  
  Para desempatar faixas com a mesma chave sem comparar objetos `Track` diretamente (o que causaria erro, já que `Track` não é comparável), cada item entra na fila como uma tupla `(chave, contador, track)`, onde `contador` é a ordem de chegada da faixa na biblioteca.

  ## Playlist

  A playlist é uma lista duplamente encadeada com nós sentinela (header e trailer). O cursor guarda a referência ao nó da faixa atual, por isso next e prev são O(1). A playlist não é circular.
