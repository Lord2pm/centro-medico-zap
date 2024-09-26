from django.shortcuts import HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.sessions.models import Session
from twilio.twiml.messaging_response import MessagingResponse

from .utils import init_sessions, create_prompt


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
def custom_recommendations(request):
    resp = MessagingResponse()
    user_message = request.POST.get("Body")
    if not request.session["question_ia"]:
        answer = "🌟 *Receber Recomendações Personalizadas* (do nosso agente IA 🤖)\n\n🩺 *O que você gostaria de saber sobre lentes, armações ou cuidados com os olhos? Digite sua pergunta e nosso agente fornecerá recomendações personalizadas!* \n\n*Para voltar ao menu, digite voltar.*"
        request.session["question_ia"] = 1
    else:
        answer = create_prompt(user_message)
    resp.message(
        f"{answer}"
    )

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
    Session.objects.all().delete()
    return HttpResponse(str(resp))


@csrf_exempt
@require_POST
def home(request):
    user_message = request.POST.get("Body")
   
    if "i" not in request.session:
        init_sessions(request)
    if request.session["question_ia"]:
        return redirect("custom-recommendations")
    
    if user_message.lower() == "fim":
        return redirect("close-session")

    match request.session["i"]:
        case 0:
            return redirect("start")
        case 1:
            return redirect("menu") 
        case 2:
            match user_message :
                case "1":
                    ...
                case "2":
                    ...
                case "3":
                    return redirect("custom-recommendations")
                case "4":
                    request.session["menu_option"] = 4
                    return redirect("show-about-we")
                case _:
                    return HttpResponse("❌ Opção inválida! Por favor, escolha uma das opções abaixo: 🔄")      
        case _:
            return HttpResponse("Erro")