from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .data import MEDICOS
from babel.dates import format_datetime

def _format_dt(dt):
    try:
        return format_datetime(dt, "EEEE, d 'de' MMMM 'a las' HH:mm", locale='es')
    except Exception:
        return dt.strftime('%Y-%m-%d %H:%M')
    
def home(request):
    context = {
        'clinic_name': 'Clínica San Salud',
        'description': 'Atención privada con especialistas y horarios flexibles. Reserve su cita fácilmente.',
    }
    return render(request, 'proyectos/home.html', context)

def citas(request):
    medicos = []
    for m in MEDICOS:
        mcopy = m.copy()
        mcopy['horario_str'] = _format_dt(m['horario'])
        medicos.append(mcopy)
    return render(request, 'proyectos/citas.html', {'medicos': medicos})

def reservar(request, medico_id):
    if request.method != 'POST':
        return redirect('proyectos:citas')
    
    email = request.POST.get('email')
    medico = next((m for m in MEDICOS if m['id'] == medico_id), None)

    if not medico:
        return render(request, 'proyectos/confirmation.html', {'message': 'Médico no encontrado.'})
    
    if medico['vacaciones'] or medico['cupos'] <= 0:
        return render(request, 'proyectos/confirmation.html', {'message': 'No disponible para reservar. '})
    
    medico['cupos'] -= 1
    horario = _format_dt(medico['horario'])

    subject = f'Confirmación de cita - {medico["nombre"]}'
    body = f'Cita confirmada con {medico["nombre"]} ({medico["especialidad"]})\\nHorario: {horario}'

    send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])

    return render(request, 'proyectos/confirmation.html', {
        'message': f'Cita reservada y correo enviado a {email}.',
        'medico': medico,
    })

# Create your views here.
