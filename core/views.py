from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.sessions.models import Session
from twilio.twiml.messaging_response import MessagingResponse

from .utils import init_sessions


@csrf_exempt
@require_POST
def show_start_message(request):
    resp = MessagingResponse()
    user_name = request.POST.get("ProfileName")
    resp.message(
        f"👁️‍🗨️✨ Olá, *{user_name}*, Seja bem-vindo(a) ao *Centro Óptico Visão Futurista*!\n\nÉ um prazer tê-lo(a) conosco! 🩺👓 Estamos aqui para ajudar a cuidar da sua visão 👁️ com precisão e cuidado, de forma simples e eficiente. 🔍👨‍⚕️👩‍⚕️\n\n📝 *Digite qualquer coisa para continuar* 📝"
    )
    request.session["i"] = 1
    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def show_menu(request):
    resp = MessagingResponse()
    resp.message(
        "💡 Como podemos lhe ajudar hoje?\n\n1️⃣ Agendar uma consulta com um de nossos especialistas.\n\n2️⃣ Consultar o histórico de suas consultas.\n\n3️⃣ Receber recomendações personalizadas (da nossa IA 🤖) de lentes, armações e de cuidados com os seus olhos 👁️‍🗨️✨.\n\n4️⃣ Saiba mais sobre nós."
    )
    request.session["i"] = 2
    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def close_session(request):
    resp = MessagingResponse()
    resp.message(
        "🔒 Sessão Encerrada 🔒\n\nObrigado por visitar o *Centro óptico Visão Futurista*! Se precisar de mais assistência, não hesite em entrar em contato. 👁️‍🗨️✨"
    )
    Session.objects.all().delete()
    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def home(request):
    user_message = request.POST.get("Body")

    if "i" not in request.session:
        init_sessions(request)

    if user_message.lower() == "fim":
        return redirect("close-session")

    match request.session["i"]:
        case 0:
            return redirect("start")
        case 1:
            return redirect("menu")
        case _:
            return HttpResponse("Erro")
