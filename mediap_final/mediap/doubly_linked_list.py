class DoublyLinkedList:

    class _DoublyNode:
        def __init__(self, elem, prev, next_node):
            self._elem = elem
            self._prev = prev
            self._next = next_node

        @property
        def element(self):
            return self._elem

        @element.setter
        def element(self, elem):
            self._elem = elem

        @property
        def previous(self):
            return self._prev

        @previous.setter
        def previous(self, node):
            self._prev = node

        @property
        def next(self):
            return self._next

        @next.setter
        def next(self, node):
            self._next = node

    def __init__(self, size=0):
        self._header = self._DoublyNode(None, None, None)
        self._trailer = self._DoublyNode(None, None, None)
        self._header.next = self._trailer
        self._trailer.previous = self._header
        self._length = 0
        for _ in range(size):
            self.append(None)

    def __len__(self):
        return self._length

    def index(self, elem):
        result = None
        pos = 0
        this = self._header.next
        while not result and pos < self._length:
            if this.element == elem:
                result = pos
                break
            this = this.next
            pos += 1
        return result

    def empty(self):
        return self._length == 0

    def remove_at(self, index):
        if index < 0 or index >= self._length:
            raise IndexError("Index out of range")
        if index == 0:
            self._header.next = self._header.next.next
            self._header.next.previous = self._header
        elif index == self._length - 1:
            self._trailer.previous = self._trailer.previous.previous
            self._trailer.previous.next = self._trailer
        else:
            aux = self._header.next
            for _ in range(index):
                aux = aux.next
            aux.previous.next = aux.next
            aux.next.previous = aux.previous
        self._length -= 1

    def append(self, item):
        ultimo = self._trailer.previous
        new_node = self._DoublyNode(item, ultimo, self._trailer)
        ultimo.next = new_node
        self._trailer.previous = new_node
        self._length += 1

    def __iter__(self):
        aux = self._header.next
        while aux is not self._trailer:
            yield aux.element
            aux = aux.next


class Playlist:

    def __init__(self):
        self._faixas = DoublyLinkedList()
        self._cursor = None
        self._pos = 0

    def add(self, track):
        self._faixas.append(track)
        if self._cursor is None:
            self._cursor = self._faixas._header.next

    def remove_at(self, pos):
        self._faixas.remove_at(pos)
        if pos < self._pos:
            self._pos -= 1
        elif pos == self._pos:
            if len(self._faixas) == 0:
                self._cursor = None
                self._pos = 0
            elif self._cursor.next is not self._faixas._trailer:
                self._cursor = self._cursor.next
            else:
                self._cursor = self._cursor.previous
                self._pos -= 1

    def current(self):
        if self._cursor is None:
            return None
        return self._cursor.element

    def play_next(self):
        if self._cursor is None or self._cursor.next is self._faixas._trailer:
            print("Erro: já está na última faixa da playlist.")
            return None
        self._cursor = self._cursor.next
        self._pos += 1
        return self.current()

    def play_prev(self):
        if self._pos <= 0:
            print("Erro: já está na primeira faixa da playlist.")
            return None
        self._cursor = self._cursor.previous
        self._pos -= 1
        return self.current()

    def reset_cursor(self):
        self._pos = 0
        self._cursor = self._faixas._header.next if len(self._faixas) else None

    def cursor_pos(self):
        return self._pos

    def set_cursor_pos(self, pos):
        if 0 <= pos < len(self._faixas):
            no = self._faixas._header.next
            for _ in range(pos):
                no = no.next
            self._cursor = no
            self._pos = pos

    def __len__(self):
        return len(self._faixas)

    def __iter__(self):
        return iter(self._faixas)