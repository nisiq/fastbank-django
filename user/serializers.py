"""
Toda vez que mandamos uma requisição,
esses dados podem retornar em JSON, xml, matriz...
Temos que serializar esses dados, transformando em JSON e etc
"""

"""
Serializers for thhe user API View
"""

from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

from django.utils.translation import gettext as _ 


class UserSerializer(serializers.ModelSerializer):
    """ Serializer for the user object """

    #Classe de configuração
    class Meta:
        model = get_user_model()
        # Campos que vamos enviar/receber
        fields = ['email', 'password', 'first_name', 'last_name', 'cpf', 'created_at']
        extra_kwargs = {
            # Configs campos
            # Apenas escrever, não visualizar
            'password': {'write_only': True, 'min_lenght': 6},
            # Podemos apenas ler, não modificar
            'is_active': {'read_only': True} 
            'created_at': {'read_only': True}
        }

        def create(self, validated_data):
            """ Create and Return a new user with encrypted password """
            # core.models - user manager
            return get_user_model().objects.create_user(**validated_data)

        def updated(self, instance, validated_data):
            """ Update and Return a user """
            password = validated_data.pop('password', None)
            user = super().update(instance, validated_data)
            
            if password:
                user.set_password(password)
                user.save()

            return user




