import json
import queue
from collections import deque
from datetime import datetime

from .models import Track
from .doubly_linked_list import Playlist


class MediaPlayer:

    historico_max_len = 20  

    def __init__(self):
        self.tracks = []           
        self.biblioteca_carregada = False

        self.playlists = {}         
        self.playlist_atual_nome = None

        self.up_next = deque()                             
        self.history = deque(maxlen=self.historico_max_len)  

    @property
    def playlist(self):
        if self.playlist_atual_nome is None:
            return None
        return self.playlists[self.playlist_atual_nome]

    def carregar_biblioteca(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arq:
                dados = json.load(arq)
            tracks_carregadas = [Track(**musica) for musica in dados["musicas"]]

            self.tracks = tracks_carregadas
            self.biblioteca_carregada = True
            print(f"Sucesso: {len(tracks_carregadas)} faixas carregadas")
            return tracks_carregadas

        except FileNotFoundError:
            print(f"Erro: o arquivo '{caminho_arquivo}' não foi encontrado.")
        except Exception as erro:
            print(f"Erro: {erro}")


    def listar_categoria(self, tipo="id"):
        try:
            if not self.tracks:
                print("Erro: nenhuma faixa carregada. Use 'library load <arquivo>'.")
                return

            if tipo == "rating":
                ordem_rating = ([], [], [], [], [])
                for musica in self.tracks:
                    if 1 <= musica.rating <= 5:
                        ordem_rating[5 - musica.rating].append(musica)

                for lista_ordenada in ordem_rating:
                    for cada_musica in lista_ordenada:
                        print(f"Nota: {cada_musica.rating} | Título: {cada_musica.titulo}")

            elif tipo == "titulo":
                ordem_titulo = self.tracks[:]
                n = len(ordem_titulo)
                for i in range(n - 1):
                    for j in range(n - 1 - i):
                        atual = ordem_titulo[j].titulo.lower()
                        proximo = ordem_titulo[j + 1].titulo.lower()
                        if atual > proximo:
                            ordem_titulo[j], ordem_titulo[j + 1] = ordem_titulo[j + 1], ordem_titulo[j]

                for cada_musica in ordem_titulo:
                    print(f"Título: {cada_musica.titulo} | Artista: {cada_musica.artista}")

            elif tipo == "artista":
                ordem_artista = self.tracks[:]
                n = len(ordem_artista)
                for i in range(n - 1):
                    for j in range(n - 1 - i):
                        atual = ordem_artista[j].artista.lower()
                        proximo = ordem_artista[j + 1].artista.lower()
                        if atual > proximo:
                            ordem_artista[j], ordem_artista[j + 1] = ordem_artista[j + 1], ordem_artista[j]

                for cada_musica in ordem_artista:
                    print(f"Artista: {cada_musica.artista} | Título: {cada_musica.titulo}")

            elif tipo == "id":
                for cada_musica in sorted(self.tracks, key=lambda t: t.id):
                    print(f"Id: {cada_musica.id} | Título: {cada_musica.titulo}")

            else:
                print(f"Erro: critério de ordenação inválido '{tipo}' (use rating, titulo, artista ou id).")

        except Exception as erro:
            print(f"Erro: {erro}")

    def _buscar_track_por_id(self, track_id):
        for track in self.tracks:
            if track.id == track_id:
                return track
        return None

    def playlist_new(self, nome):
        self.playlists[nome] = Playlist()
        self.playlist_atual_nome = nome
        print(f'Playlist "{nome}" criada.')

    def playlist_add(self, track_id):
        if self.playlist is None:
            print("Erro: nenhuma playlist atual. Use 'playlist new <nome>' primeiro.")
            return
        track = self._buscar_track_por_id(track_id)
        if track is None:
            print(f"Erro: faixa com id {track_id} não existe na biblioteca.")
            return
        self.playlist.add(track)

    def playlist_remove(self, pos):
        if self.playlist is None:
            print("Erro: nenhuma playlist atual.")
            return
        try:
            self.playlist.remove_at(pos)
        except IndexError:
            print(f"Erro: posição {pos} inválida para a playlist atual.")

    def playlist_show(self):
        if self.playlist is None or len(self.playlist) == 0:
            print("Playlist vazia ou inexistente.")
            return
        cursor = self.playlist.cursor_pos()
        for i, track in enumerate(self.playlist):
            marcador = ">" if i == cursor else " "
            print(f"{marcador} {i + 1}. {track.titulo} — {track.artista} ({track.duracao_segundos_formatada()})")

    def _tocar(self, track):
        if track is None:
            return
        print(f'>>> Tocando: "{track.titulo}" — {track.artista} ({track.duracao_segundos_formatada()})')
        self.history.appendleft({
            "id": track.id,
            "titulo": track.titulo,
            "artista": track.artista,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
        })

    def play(self):
        if self.playlist is None or len(self.playlist) == 0:
            print("Erro: nenhuma playlist ativa ou ela está vazia.")
            return
        self._tocar(self.playlist.current())

    def next(self):
        if self.up_next:
            track = self.up_next.popleft()   
            self._tocar(track)
            return
        if self.playlist is None:
            print("Erro: nenhuma playlist ativa.")
            return
        track = self.playlist.play_next()
        if track is not None:
            self._tocar(track)

    def prev(self):
        if self.playlist is None:
            print("Erro: nenhuma playlist ativa.")
            return
        track = self.playlist.play_prev()
        if track is not None:
            self._tocar(track)

    def enqueue(self, track_id):
        track = self._buscar_track_por_id(track_id)
        if track is None:
            print(f"Erro: faixa com id {track_id} não existe na biblioteca.")
            return
        self.up_next.append(track)  

    def queue_show(self):
        if not self.up_next:
            print("Fila Up Next vazia.")
            return
        for i, track in enumerate(self.up_next, start=1):
            print(f"{i}. {track.titulo} — {track.artista}")


    def history_show(self):
        if not self.history:
            print("Histórico vazio.")
            return
        for i, item in enumerate(self.history, start=1):
            print(f"{i}. {item['titulo']} — {item['artista']} [{item['timestamp']}]")

    def _posicao_no_historico(self, track_id):
        for i, item in enumerate(self.history): 
            if item["id"] == track_id:
                return i
        return None

    def smart_shuffle(self, n):
        if not self.tracks:
            print("Erro: nenhuma faixa carregada.")
            return

        fila_prioridade = queue.PriorityQueue()
        contador = 0  
        for track in self.tracks:
            pos_hist = self._posicao_no_historico(track.id)
            penalty_rec = (5 - pos_hist) if pos_hist is not None and pos_hist < 5 else 0
            chave = -10 * track.rating + penalty_rec  
            fila_prioridade.put((chave, contador, track))
            contador += 1

        nova_playlist = Playlist()
        quantidade = min(n, fila_prioridade.qsize())
        for _ in range(quantidade):
            _, _, track = fila_prioridade.get() 
            nova_playlist.add(track)

        self.playlists["smart-shuffle"] = nova_playlist
        self.playlist_atual_nome = "smart-shuffle"
        print(f'Playlist "smart-shuffle" criada com {quantidade} faixas.')

    def save_estado(self, caminho_arquivo):
        estado = {
            "playlists": {
                nome: {
                    "track_ids": [t.id for t in pl],
                    "cursor": pl.cursor_pos(),
                }
                for nome, pl in self.playlists.items()
            },
            "playlist_atual": self.playlist_atual_nome,
            "up_next_ids": [t.id for t in self.up_next],
            "history": list(self.history),  
        }
        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as arq:
                json.dump(estado, arq, ensure_ascii=False, indent=2)
            print(f"Estado salvo em '{caminho_arquivo}'.")
        except Exception as erro:
            print(f"Erro: {erro}")

    def load_estado(self, caminho_arquivo):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arq:
                estado = json.load(arq)

            novas_playlists = {}
            for nome, dados in estado.get("playlists", {}).items():
                pl = Playlist()
                for track_id in dados.get("track_ids", []):
                    track = self._buscar_track_por_id(track_id)
                    if track is not None:
                        pl.add(track)
                pl.set_cursor_pos(dados.get("cursor", 0))
                novas_playlists[nome] = pl
            self.playlists = novas_playlists

            self.playlist_atual_nome = estado.get("playlist_atual")

            self.up_next = deque()
            for track_id in estado.get("up_next_ids", []):
                track = self._buscar_track_por_id(track_id)
                if track is not None:
                    self.up_next.append(track)

            self.history = deque(estado.get("history", []), maxlen=self.historico_max_len)

            print(f"Estado restaurado de '{caminho_arquivo}'.")
        except FileNotFoundError:
            print(f"Erro: o arquivo '{caminho_arquivo}' não foi encontrado.")
        except Exception as erro:
            print(f"Erro: {erro}")
