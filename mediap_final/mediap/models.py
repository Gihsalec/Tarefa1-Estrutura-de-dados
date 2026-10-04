class Track:
    def __init__(self, id, titulo, artista, duracao_segundos, rating, data_adicao, **kwargs):
        self.id = id
        self.titulo = titulo
        self.artista = artista
        self.duracao_segundos = duracao_segundos
        self.rating = rating
        self.data_adicao = data_adicao

    def duracao_segundos_formatada(self):
        minutos = self.duracao_segundos // 60
        segundos = self.duracao_segundos % 60
        return f"{minutos}:{segundos:02d}"

    def __repr__(self):
        return f"Track(id={self.id}, titulo='{self.titulo}', artista='{self.artista}')"

    def __str__(self):
        return f'"{self.titulo}" — {self.artista} ({self.duracao_segundos_formatada()})'
