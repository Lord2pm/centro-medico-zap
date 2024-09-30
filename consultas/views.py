from .models import Consulta
from users.views import get_user_by_phone


def get_consultas_by_user_phone(phone: str):
    user = get_user_by_phone(phone)
    consultas = Consulta.objects.filter(usuario=user)
    string = "👓 *Histórico de Consultas - Centro Óptico Visão Futurista*\n\n"

    if not consultas:
        string += "❌ Nenhuma consulta encontrada para este usuário. ❌"
        return string

    for consulta in consultas:
        string += (
            f"🧑‍⚕️ *Nome do Paciente:* {consulta.nome_paciente}\n"
            f"🎂 *Idade do Paciente:* {consulta.idade} anos\n"
            f"🗓️ *Data da Consulta:* {consulta.data_consulta.strftime('%d de %B de %Y, %H:%M')}\n"
            f"📋 *Tipo da Consulta:* {consulta.tipo.nome}\n"
            f"✅ *Status da Consulta:* {'Concluída' if consulta.status else 'Não Concluída'}\n"
            f"👤 *Solicitante:* {consulta.usuario.nome}\n"
            f"--------------------------------------------\n"
        )

    return string

def register_consultas(nome_paciente, idade, data_consulta, phone, tipo) -> bool:
    user = get_user_by_phone(phone)
    nova_consulta = Consulta(
        nome_paciente=nome_paciente,
        idade=idade,
        data_consulta=data_consulta,
        usuario=user,
        tipo=tipo,
        status=False  # Ou True, dependendo da lógica do seu aplicativo
    )
    try:
        nova_consulta.save()
        return True
    except Exception as e:
        print(e)
        return False