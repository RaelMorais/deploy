from django.db import models

"""
Categorias -> Modelo utilizado para armazenar todas as categorias do projeto eLOGiar

Contém:

Nome -> campo para caracteres

__str__ -> retorna de forma humanizada o nome da categoria para o administrador django

"""

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

"""
Usuarios -> Modelo utilizado para armazenar todos os colaboradores que irão fazer parte do sistema

Contém:

Nome -> campo para caracteres

__str__ -> retorna de forma humanizada o nome do usuário para o administrador django

"""
cargos_niveis = [
    ("Gestão", "Gestão"),
    ("Colaborador", "Colaborador")
]
class Usuarios(models.Model):
    nome = models.CharField(max_length=100)
    setor = models.CharField(max_length=100, default='')
    cargo = models.CharField(choices=cargos_niveis, max_length=20, default='')
    
    def __str__(self):
        return self.nome

"""
Votos -> Modelo utilzado para armazenar todos os tipos de votos das três categorias do Website eLOGiar

Contém:

Pessoa votante -> Chave Estrangeira (Usuarios)
Pessoa votada -> Chave estrangeira (Usuarios)
Categoria votada -> Chave Estrangeira (Categorias)
Mensagem -> Campo de texto

unique_together -> junta as três informações, pessoa votante, votada e categoria, para realizarmos uma regra de negócio:
Uma pessoa não pode votar mais do que uma vez em outra pessoa na mesma categoria.

__str__ -> Retorna uma frase humanizada para o administrador django.
Ex: Fulano votou em Ciclano na categoria FaciLOG.

"""

class Votos(models.Model):
    pessoa_votando = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    pessoa_votadas = models.ForeignKey(Usuarios, on_delete=models.CASCADE, related_name='votos_recebidos')
    categoria_votadas = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    mensagem = models.TextField()

    class Meta:
        unique_together = ('pessoa_votando', 'pessoa_votadas', 'categoria_votadas')


    def __str__(self):
        return f"{self.pessoa_votando} votou em {self.pessoa_votadas} na categoria {self.categoria_votadas}"
