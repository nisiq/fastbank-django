from django.core.handlers.wsgi import WSGIRequest
import json
from core.models import User
from rest_framework import status
from django.utils import timezone
from django.http import JsonResponse

""" Middleware que é chamado em cada requisição"""

class LoginAttemptsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest): 
        body = request.body

        response = self.get_response(request)

        if request.path == "/api/token/":
            # obtém o conteúdo da solicitação
            content_type = request.headers.get("Content-Type", '').lower()


            if 'application/json' in content_type:
                try:
                    cpf = json.loads(body.decode('utf-8')).get('cpf')
                except json.JSONDecodeError:
                    cpf = None

            elif 'application/x-www-form-urlencoded' in content_type:
                cpf = request.POST.get('cpf')
            else:
                cpf = None

            # se o cpf for recebido:
            if cpf:
                print('aqui')
                user = User.objects.get(cpf=cpf)

                # # if user was created less than 3 minutes ago
                # if timezone.now() <= (user.created_at + timezone.timedelta(minutes=3)):
                #     return JsonResponse(
                #     {'detail': 'Your account is in analysis. Try again later'},
                #     status=status.HTTP_401_UNAUTHORIZED
                # )    

                # se o login estiver errado:
                if user and response.status_code == status.HTTP_401_UNAUTHORIZED:
                    user.login_attempts += 1
                    user.save()

                    # se errar 3x, bloquear 1 min
                    if user.login_attempts ==3:
                        user.locked_at = timezone.now()
                        user.unlocked_at = timezone.now() + timezone.timedelta(minutes=1)
                        user.save()
                        
                        return JsonResponse(
                            {'detail': 'Conta bloqueada. Tente novamente em 1 minuto'},
                            status=status.HTTP_401_UNAUTHORIZED
                        )
                
                if user.login_attempts >= 3 and user.locked_at != None and user.unlocked_at != None and status.HTTP_200_OK:
                    if timezone.now() >= user.unlocked_at:
                        user.login_attempts = 0
                        user.locked_at = None
                        user.unlocked_at = None
                        user.save()
                    else:
                        return JsonResponse(
                            {'detail': 'Sua conta foi bloqueada. Tente novamente em breve'},
                            status=status.HTTP_418_IM_A_TEAPOT
                        )
        
        return response