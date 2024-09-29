from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from twilio.twiml.messaging_response import MessagingResponse

from .utils import init_sessions, create_prompt
from users.views import register_user
from consultas.views import get_consultas_by_user_phone
from consultas.models import TipoConsulta


@csrf_exempt
@require_POST
def schedule_appointment(request):
    tipos_consulta = TipoConsulta.objects.all()
    resp = MessagingResponse()
    user_message = request.POST.get("Body")

    match request.session["consulta_i"]:
        case 0:
            resp.message(
                "🧑‍⚕️ *Agendamento de Consulta*\n\n"
                "Por favor, informe o *nome completo* do paciente:"
            )
            request.session["consulta_i"] += 1
        case 1:
            request.session["dados_consulta"]["nome"] = user_message
            resp.message("🎂 Agora, informe a *idade* do paciente:")
            request.session["consulta_i"] += 1
        case 2:
            request.session["dados_consulta"]["idade"] = user_message
            if tipos_consulta.exists():
                message = "📝 *Escolha o tipo de consulta desejado*:\n\n"
                for tipo in tipos_consulta:
                    message += f"{tipo.id}. {tipo.nome} - {tipo.preco:.2f} Kz\n"

                resp.message(message)
                request.session["consulta_i"] += 1
            else:
                resp.message(
                    "⚠️ *Desculpe*, no momento não há tipos de consulta disponíveis. Tente novamente mais tarde."
                )
        case 3:
            request.session["dados_consulta"]["tipo"] = tipos_consulta.get(
                id=int(user_message)
            )
            print(request.session["dados_consulta"]["tipo"])
            resp.message("🗓️ *Informe a Data da consulta | dd/mm/aaaa hh:mm*")
            request.session["consulta_i"] += 1
        case 4:
            ...

    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def show_start_message(request):
    resp = MessagingResponse()
    user_name = request.POST.get("ProfileName")
    user_phone = request.POST.get("From").split(":")[-1]

    register_user(user_name, user_phone)

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
    request.session["menu_option"] = None
    request.session["question_ia"] = None
    request.session["dados_consulta"] = {}
    request.session["consulta_i"] = 0
    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def custom_recommendations(request):
    resp = MessagingResponse()
    user_message = request.POST.get("Body")
    if not request.session["question_ia"]:
        answer = "🌟 *Receber Recomendações Personalizadas* (do nosso agente IA 🤖)\n\n🩺 *O que você gostaria de saber sobre lentes, armações ou cuidados com os olhos? Digite sua pergunta e nosso agente fornecerá recomendações personalizadas!* \n\n*Para voltar ao menu, digite 0.*"
        request.session["question_ia"] = 1
    else:
        answer = create_prompt(user_message)
    resp.message(f"{answer}")

    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def show_about_we(request):
    resp = MessagingResponse()
    resp.message(
        "Sobre Nós 🌟\n\n*Bem-vindo(a) ao Centro Óptico Visão Futurista!* 👓\nComprometidos com a saúde ocular e o bem-estar dos nossos pacientes.\n\n*O que nos diferencia:*\n\n✨ **Atendimento Personalizado:** Cada paciente é único, e nossas consultas são adaptadas às suas necessidades específicas. 👩‍⚕👨‍⚕\n\n🛠️ **Tecnologia de Ponta:** Utilizamos equipamentos modernos e técnicas avançadas para garantir diagnósticos precisos e tratamentos eficazes. 💻🔬\n\n🌟 **Produtos de Qualidade:** Oferecemos uma ampla gama de lentes e armações das melhores marcas, sempre priorizando conforto e estilo. 🕶️🔝\n\n📚 **Educação e Conscientização:** Estamos aqui para informar e educar nossos pacientes sobre cuidados com a visão, garantindo que você faça escolhas informadas. 👁‍🗨\n\n*Localização:*\nRua da Saúde, 123, Centro, Cidade, Estado.\n\n*Contato:*\n📞 (00) 1234-5678\n📧 contato@visao-futurista.com\n\nAcreditamos que uma boa visão é essencial para a qualidade de vida.\nJunte-se a nós na jornada para uma visão mais saudável! 💖"
    )
    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def close_session(request):
    resp = MessagingResponse()
    resp.message(
        "🔒 Sessão Encerrada 🔒\n\nObrigado por visitar o *Centro óptico Visão Futurista*! Se precisar de mais assistência, não hesite em entrar em contato. 👁️‍🗨️✨"
    )
    init_sessions(request)
    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def home(request):
    resp = MessagingResponse()
    user_message = request.POST.get("Body")
    user_phone = request.POST.get("From").split(":")[-1]

    if "i" not in request.session:
        init_sessions(request)

    if user_message.lower() == "fim":
        return redirect("close-session")

    if user_message == "0":
        return redirect("menu")

    if request.session["question_ia"]:
        return redirect("custom-recommendations")

    match request.session["i"]:
        case 0:
            return redirect("start")
        case 1:
            return redirect("menu")
        case 2:
            request.session["menu_option"] = (
                user_message
                if not request.session["menu_option"] and user_message.lower() != "v"
                else request.session["menu_option"]
            )
            match request.session["menu_option"]:
                case "1":
                    return redirect("schedule-appointment")
                case "2":
                    resp.message(get_consultas_by_user_phone(user_phone))
                    return HttpResponse(str(resp))
                case "3":
                    return redirect("custom-recommendations")
                case "4":
                    request.session["menu_option"] = 4
                    return redirect("show-about-we")
                case _:
                    resp.message(
                        "❌ Opção inválida! Por favor, escolha uma das opções contida no menu🔄"
                    )
                    return HttpResponse(str(resp))
        case _:
            return HttpResponse("Erro")
