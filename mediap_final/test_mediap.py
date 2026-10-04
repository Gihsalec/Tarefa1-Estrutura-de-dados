import os
import tempfile
import unittest

from mediap.doubly_linked_list import DoublyLinkedList, Playlist
from mediap.models import Track
from mediap.player import MediaPlayer


def _track(id_, rating=3):
    return Track(id_, f"T{id_}", "Artista", 180, rating, "2025-01-01")


def _player(ratings=(3, 3, 3, 3), playlist=()):
    player = MediaPlayer()
    player.tracks = [_track(i, r) for i, r in enumerate(ratings, start=1)]
    player.biblioteca_carregada = True
    player.playlist_new("p")
    for i in playlist:
        player.playlist_add(i)
    return player


def _estado(player):
    return ([t.id for t in player.playlist], player.playlist.cursor_pos(),
            [t.id for t in player.up_next], list(player.history))


class TestMediaPlayer(unittest.TestCase):

    def test_lista_encadeada_insercoes_e_remocoes(self):
        lista = DoublyLinkedList()
        for letra in "abcd":
            lista.append(letra)
        lista.remove_at(0)
        lista.remove_at(2)
        self.assertEqual(list(lista), ["b", "c"])
        self.assertEqual((lista.index("c"), lista.index("a")), (1, None))
        with self.assertRaises(IndexError):
            lista.remove_at(5)

    def test_cursor_da_playlist(self):
        pl = Playlist()
        for i in (1, 2, 3, 4):
            pl.add(_track(i))
        self.assertIsNone(pl.play_prev())
        self.assertEqual(pl.play_next().id, 2)
        self.assertEqual(pl.play_next().id, 3)
        pl.remove_at(0)
        self.assertEqual((pl.current().id, pl.cursor_pos()), (3, 1))
        self.assertEqual(pl.play_next().id, 4)
        self.assertIsNone(pl.play_next())
        pl.reset_cursor()
        pl.remove_at(0)
        self.assertEqual(pl.current().id, 3)
        pl.set_cursor_pos(1)
        pl.remove_at(1)
        self.assertEqual(pl.current().id, 3)
        pl.remove_at(0)
        self.assertIsNone(pl.current())

    def test_up_next_tem_precedencia_sobre_a_playlist(self):
        player = _player(playlist=(1, 2, 3))
        player.play()
        player.enqueue(4)
        player.enqueue(3)
        player.next()
        player.next()
        self.assertEqual(player.playlist.current().id, 1)
        self.assertEqual(len(player.up_next), 0)
        player.next()
        player.prev()
        player.prev()
        self.assertEqual([h["id"] for h in player.history], [1, 2, 3, 4, 1])
        self.assertEqual([t.id for t in player.playlist], [1, 2, 3])

    def test_historico_descarta_o_mais_antigo(self):
        player = MediaPlayer()
        limite = MediaPlayer.historico_max_len
        for i in range(1, limite + 4):
            player._tocar(_track(i))
        ids = [h["id"] for h in player.history]
        self.assertEqual((len(ids), ids[0], ids[-1]), (limite, limite + 3, 4))
        self.assertIn("timestamp", player.history[0])

    def test_smart_shuffle(self):
        player = _player(ratings=(1, 5, 3, 5))
        player.smart_shuffle(3)
        self.assertEqual([t.id for t in player.playlist], [2, 4, 3])
        player._tocar(player.tracks[1])
        player.smart_shuffle(4)
        self.assertEqual([t.id for t in player.playlist], [4, 2, 3, 1])
        MediaPlayer().smart_shuffle(1)

    def test_save_e_load_preservam_o_estado(self):
        p1 = _player(playlist=(1, 2, 3))
        p1.play()
        p1.next()
        p1.enqueue(4)
        p1.enqueue(1)
        with tempfile.TemporaryDirectory() as pasta:
            caminho = os.path.join(pasta, "estado.json")
            p1.save_estado(caminho)
            p2 = _player()
            p2.load_estado(caminho)
            p2.load_estado(os.path.join(pasta, "nao_existe.json"))
        self.assertEqual(_estado(p1), _estado(p2))
        self.assertEqual(len(p2.up_next), 2)

    def test_biblioteca_e_listagem(self):
        player = MediaPlayer()
        player.carregar_biblioteca("nao_existe.json")
        player.listar_categoria()
        self.assertFalse(player.biblioteca_carregada)
        player.carregar_biblioteca(os.path.join(os.path.dirname(os.path.abspath(__file__)), "mediap", "library.json"))
        ids = [t.id for t in player.tracks]
        for criterio in ("id", "rating", "titulo", "artista", "invalido"):
            player.listar_categoria(criterio)
        self.assertEqual((len(ids), [t.id for t in player.tracks]), (10, ids))

    def test_comandos_com_entradas_invalidas(self):
        player = MediaPlayer()
        player.tracks = [_track(1)]
        for comando in (player.play, player.next, player.prev, player.playlist_show,
                        player.queue_show, player.history_show):
            comando()
        player.playlist_add(1)
        player.playlist_remove(0)
        player = _player(playlist=(1,))
        player.play()
        player.enqueue(2)
        player.playlist_add(99)
        player.playlist_remove(9)
        player.enqueue(99)
        for comando in (player.playlist_show, player.queue_show, player.history_show):
            comando()
        self.assertEqual((len(player.playlist), len(player.up_next), len(player.history)), (1, 1, 1))


if __name__ == "__main__":
    unittest.main()