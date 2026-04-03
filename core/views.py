from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
import json

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse

from .models import AlunoCollege, Aula
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

# 4. Funções Renovo College
def college_cadastro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        if User.objects.filter(username=email).exists():
            messages.error(request, 'E-mail já cadastrado!')
            return redirect('college_cadastro')
            
        user = User.objects.create_user(username=email, email=email, password=senha, first_name=nome)
        user.is_active = False # Proteção contra Spam (bloqueia login)
        user.save()
        
        AlunoCollege.objects.create(user=user, is_ativo=False) # Status de pagamento inativo
        
        # Gerar link de ativação
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link_ativacao = request.build_absolute_uri(
            reverse('college_ativar', kwargs={'uidb64': uid, 'token': token})
        )
        
        # Enviar e-mail
        assunto = 'Ative sua conta no Renovo College'
        mensagem = f'Olá {nome}!\n\nPor favor, confirme seu cadastro clicando no link abaixo:\n\n{link_ativacao}\n\nSe você não se cadastrou, ignore este e-mail.'
        send_mail(
            assunto,
            mensagem,
            'wellbarbosaft@gmail.com', # O remetente configurado no settings
            [email],
            fail_silently=False,
        )
        
        return render(request, 'college_aguardando_email.html')
        
    return render(request, 'college_cadastro.html')

def college_ativar_conta(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'E-mail confirmado com sucesso! Faça seu login.')
        return redirect('college_login')
    else:
        messages.error(request, 'Link de ativação inválido ou expirado.')
        return redirect('college_login')

def college_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        # Checar manualmente se o e-mail existe mas não confirmou
        try:
            tentativa_user = User.objects.get(username=email)
            if not tentativa_user.is_active:
                messages.error(request, 'Sua conta não foi confirmada. Verifique seu e-mail (ou Lixo Eletrônico)!')
                return render(request, 'college_login.html')
        except User.DoesNotExist:
            pass # Continua pro authenticate para dar usuário inválido
            
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            login(request, user)
            return redirect('college_dashboard')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
            
    return render(request, 'college_login.html')

def college_logout(request):
    logout(request)
    return redirect('college_login')

@login_required(login_url='college_login')
def college_dashboard(request):
    try:
        aluno = request.user.alunocollege
    except AlunoCollege.DoesNotExist:
        # Se por algum motivo for admin ou não tiver perfil, cria um inativo
        aluno = AlunoCollege.objects.create(user=request.user, is_ativo=False)

    if not aluno.is_ativo and not request.user.is_superuser:
        return render(request, 'college_bloqueado.html')
        
    aulas = Aula.objects.all()
    return render(request, 'college_dashboard.html', {'aulas': aulas, 'aluno': aluno})

@csrf_exempt
def webhook_mercadopago(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            # Lógica para Mercado Pago
            # O webhook envia type="payment" e os dados. 
            # Você precisa extrair o e-mail ou o id do cliente.
            
            # Exemplo (pseudocódigo):
            # if dados.get('type') == 'payment':
            #     email_pagador = dados['data']['payer']['email']
            #     status = dados['data']['status']
            #     
            #     aluno = AlunoCollege.objects.filter(user__email=email_pagador).first()
            #     if aluno:
            #         if status == 'approved':
            #             aluno.is_ativo = True
            #         elif status in ['rejected', 'cancelled', 'refunded']:
            #             aluno.is_ativo = False
            #         aluno.save()

            return HttpResponse(status=200)
        except Exception as e:
            print("Erro webhook:", e)
            return HttpResponse(status=400)
    return HttpResponse(status=405)