from django.shortcuts import render, get_object_or_404, redirect
from .models import Categoria, Usuarios, Votos
from django.db.models import Count
from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.admin.views.decorators import staff_member_required

"""
Listar Categorias:
Obtém todos os objetos da model Categoria
Renderiza todos os objetos em uma oágina HTML chamada 'listar_categorias.html'
Em formato {'chave':'valor'}

"""

def listar_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'listar_categorias.html', {
        'categorias': categorias,
    })


"""
Indicar Usuário:
Obtém um objeto categoria a partir de um id (InovaLOG, FaciLOG, LogiMAX)
Obtém um objeto usuário, onde se encontra todos os usuários cadastrados

Recebe um método POST com as informações de quem está votando, quem está sendo votado, a categoria e uma mensagem,
Verifica se o votante não está tentando votar nele mesmo, ou se ele já votou na pessoa em quem está tentando votar

Caso contrário, cria um novo objeto Voto, contendo todas as informações da ação realizada (registra o voto).

"""
def indicar_usuario(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    usuarios = Usuarios.objects.all().order_by('nome')  # Feat: Ordernar por nome 

    if request.method == 'POST':
        votante_id = request.POST['votante']
        votado_id = request.POST['votado']
        categoria_id = request.POST['categoria']
        mensagem = request.POST['mensagem']

        votante = Usuarios.objects.get(id=votante_id)
        votado = Usuarios.objects.get(id=votado_id)
        
        if votante_id == votado_id:
            return render(request, 'indicacao_invalida.html', {
                'mensagem': 'Você não pode votar em si mesmo!'
            })

        if Votos.objects.filter(pessoa_votando=votante, pessoa_votadas=votado, categoria_votadas=categoria).exists():
            return render(request, 'erro_indicacao.html', {
                'mensagem': 'Você já votou nesta pessoa na mesma categoria.'
            })

        # Caso contrário, registra o voto
        Votos.objects.create(
            pessoa_votando=votante,
            pessoa_votadas=votado,
            categoria_votadas=categoria,
            mensagem=mensagem
        )

        return redirect('listar_indicacoes_realizadas')

    return render(request, 'indicar_usuario.html', {
        'categoria': categoria,
        'usuarios': usuarios,
    })

def indicar_usuario(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    usuarios = Usuarios.objects.all().order_by('nome') # --> Para filtrar por ordem alfabetica 

    if request.method == 'POST':
        votante_id = request.POST['votante']
        votado_id = request.POST['votado']
        categoria_id = request.POST['categoria']
        mensagem = request.POST['mensagem']

        votante = Usuarios.objects.get(id=votante_id)
        votado = Usuarios.objects.get(id=votado_id)
        
        if votante_id == votado_id:
            return render(request, 'indicacao_invalida.html',{
                'mensagem': 'Você não pode votar em si mesmo!'
            })

        if Votos.objects.filter(pessoa_votando=votante, pessoa_votadas=votado, categoria_votadas=categoria).exists():
            return render(request, 'erro_indicacao.html', {
                'mensagem': 'Você já votou nesta pessoa na mesma categoria.'
            })

        # Caso contrário, registra o voto
        Votos.objects.create(
            pessoa_votando=votante,
            pessoa_votadas=votado,
            categoria_votadas=categoria,
            mensagem=mensagem
        )

        return redirect('listar_indicacoes_realizadas')

    return render(request, 'indicar_usuario.html', {
        'categoria': categoria,
        'usuarios': usuarios,
    })

"""
Listar Indicações Realizadas

Obtém todos os objetos da model Votos
Retorna os valores em padrão {'chave':'valor'} para ser utilizado na página listar.html

"""

def listar_indicacoes_realizadas(request):
    indicacoes = Votos.objects.all()

    return render(request, 'listar.html', {
        'indicacoes': indicacoes,
    })

"""
Index:
Retorna a página inicial do site

"""

def index(request): 
    return render(request, 'index.html')

"""
Carregamento:
Pequena página para permitir que dados de outras páginas carreguem corretamente antes de serem renderizados

"""

def carregamento(request):
    return render(request, 'carregamento.html')

"""
Exportar Votos para Excel:

É necessário estar logado para utilizar.
Somente métodos GET são permitidos.

Gera um arquivo Excel contendo:
- **Resumo de Votos**: Quantidade total de votos por usuário em cada categoria.
- **Mensagens dos Votos**: Detalhes dos votos, incluindo votante, votado, categoria e mensagem.

Funcionalidade:
- Recupera todos os usuários, categorias e votos do banco de dados.
- Cria uma planilha com duas abas:
  - 'Resumo de Votos': Tabela com usuários e contagem de votos por categoria.
  - 'Mensagens dos Votos': Lista com votante, votado, categoria e mensagem associada.
- Retorna o arquivo Excel como uma resposta HTTP para download.

Args:
    request: Requisição HTTP contendo informações do usuário autenticado.

Returns:
    HttpResponse: Resposta com o arquivo Excel ('votosElogiar.xlsx') para download.

"""
# feat: Adicionado para exportar no excel por ordem alfabetica. 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exportar_votos_para_excel(request):
    usuarios = Usuarios.objects.all().order_by('nome')  
    categorias = Categoria.objects.all()
    votos = Votos.objects.select_related('pessoa_votadas', 'categoria_votadas', 'pessoa_votando').all().order_by('pessoa_votadas__nome')

    wb = Workbook()

    # Resumo de votos gerais
    ws_resumo = wb.active
    ws_resumo.title = "Resumo de Votos"

    header = ['Nome do Usuário', 'Setor', 'Cargo'] + [categoria.nome for categoria in categorias]
    ws_resumo.append(header)

    for usuario in usuarios:
        row = [usuario.nome, usuario.setor, usuario.get_cargo_display()]  # get_cargo_display() para pegar o cargo, por ser uma choice field 
        for categoria in categorias:
            count = Votos.objects.filter(pessoa_votadas=usuario, categoria_votadas=categoria).count()
            row.append(count)
        ws_resumo.append(row)

    # Mensagens detalhadas
    ws_detalhes = wb.create_sheet(title="Mensagens dos Votos")
    ws_detalhes.append(['Votante', 'Setor Votante', 'Cargo Votante', 'Votado', 'Setor Votado', 'Cargo Votado', 'Categoria', 'Mensagem'])

    for voto in votos:
        ws_detalhes.append([
            voto.pessoa_votando.nome,
            voto.pessoa_votando.setor,
            voto.pessoa_votando.get_cargo_display(),
            voto.pessoa_votadas.nome,
            voto.pessoa_votadas.setor,
            voto.pessoa_votadas.get_cargo_display(),
            voto.categoria_votadas.nome,
            voto.mensagem,
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="votosElogiar.xlsx"'
    wb.save(response)

    return response

"""
Página de votos do administrador
-> Pode exportar os votos para Excel
-> Pode resetar todos os votos

"""

def votos_page(request):
    return render(request, 'votos.html')

"""
Página de Login do administrador

"""

def login_page(request):
    return render(request, 'login.html')

"""
Página de retorno quando os votos são resetados

"""

def delete_page(request):
    return render (request, 'delete.html')

"""
Resetar Votos:

É necessário ser SuperUser (administrador) para utilizar essa função
Caso não seja SuperUser, é redirecionado para a tela de login

É obtido todos os votos da model e eles são deletados.
Após o delete, o usuário é redirecionado para a página de delete, confirmando a ação

"""

@staff_member_required 
def resetar_votos(request):
    Votos.objects.all().delete()
    return redirect('delete')


"""
Avisos Importantes:
Uma vez logado no django admin, fica salvo no cache que esta logado, 
ou seja, a sessão vai dar como superuser, apagar o cache. 

-> tentar apagar a cache toda vez que o usuário fecha o navegador (sugestão).
// Mudança feita no settings.py para apagar automaticamente o cache quando fechar o navegador. 

"""

# @login_required (login_url='/login/') 
# #Se o usuario n estiver logado, redireciona para tela de login
# def resetar_votos(request): ## Erro: Caso tente acessar direto pela URL, e o usuario nao estiver logado e logar, ele redireciona para pag de login 
#     Votos.objects.all().delete()
#     return redirect('delete')
