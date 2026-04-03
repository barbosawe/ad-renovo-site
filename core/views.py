from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render

# 1. Função que carrega a página inicial
def index(request):
    return render(request, 'index.html')

# 2. Função que processa o formulário de oração
def enviar_pedido(request):
    if request.method == 'POST':
        # Captura os dados preenchidos no formulário
        nome = request.POST.get('nome', 'Anônimo')
        email_fiel = request.POST.get('email', 'Não informado')
        pedido = request.POST.get('pedido', '')

        # Monta a estrutura do e-mail
        assunto = f'Novo Pedido de Oração - AD Renovo ({nome})'
        mensagem = f'Nome: {nome}\nE-mail: {email_fiel}\n\nPedido de Oração:\n{pedido}'
        
        # O e-mail que vai RECEBER as mensagens
        email_destino = ['wellbarbosaft@gmail.com']

        # Executa o disparo
        send_mail(
            assunto,
            mensagem,
            'wellbarbosaft@gmail.com', # O remetente configurado no settings
            email_destino,
            fail_silently=False,
        )
        
        # Cria uma mensagem de sucesso para mostrar na tela e recarrega a página
        messages.success(request, 'Seu pedido de oração foi enviado para nossa equipe!')
        return redirect('inicio')

    return render(request, 'index.html')

# 3. Função para a Galeria Kids, Jovens, Círculo de Oração e Ministério de Música


# Sua view da página inicial (index) deve estar aqui em cima...

def galeria_kids(request):
    return render(request, 'galeria_kids.html')

def galeria_jovens(request):
    return render(request, 'galeria_jovens.html')

def galeria_circulo(request):
    return render(request, 'galeria_circulo.html')

def galeria_music(request):
    return render(request, 'galeria_music.html')