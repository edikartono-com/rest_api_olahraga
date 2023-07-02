from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _
from django.shortcuts import redirect

from knox.models import AuthToken as Token

from rest_framework import status
# from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Model
from . import serializers as ser


# Create your views here.
def index(request):
    return redirect('documentation/')

@api_view(['POST'])
def Add(request):
    serializer = ser.SerializerModel(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status':'data telah ditambahkan',
            'id':serializer.data['id'],
            'nama cabang':serializer.data['nama_cabang'],
            'deskripsi':serializer.data['deskripsi'],
            'sejarah':serializer.data['sejarah'],
            'gambar':serializer.data['gambar']
        })
    return Response(serializer.errors)
@api_view(['GET'])
def List(request):
    ModelObject=Model.objects.all()
    SerializerObject = ser.SerializerModel(ModelObject,many=True)
    return Response(SerializerObject.data)
@api_view(['PUT'])
def Update(request, id):
    try:
        ModelObject = Model.objects.get(id=id)
    except Model.DoesNotExist:
        status = {'status':'data tidak ditemukan'}
        return Response(status)
    serializer = ser.SerializerModel(ModelObject, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['DELETE'])
def Delete(request, id):
    try:
        ModelObject = Model.objects.get(id=id)
    except Model.DoesNotExist:
        status = {'status':'data tidak ditemukan'}
        return Response(status)
    ModelObject.delete()
    return Response({
        'status':'data telah dihapus'
    })

User = get_user_model()

class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ser.RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()
        return Response(
            {
                'success': True,
                'messages': f'''
                    {serializer.data['username']} berhasil dibuat.
                '''
            },
            status=status.HTTP_201_CREATED
        )
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        username = serializer.get('username')
        password = serializer.get('password')

        if username is None or password is None:
            return Response(
                {
                    'success': False,
                    'messages': 'Harap masukkan username dan password'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {
                    'success': False,
                    'messages': _("A user with that username already exists.")
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if serializer.is_valid():
            return self.perform_create(serializer)
        else:
            return Response(
                {
                    'success': False,
                    'messages': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {
                    'success': False,
                    'messages': 'Harap masukkan username dan password'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(
            username=username,
            password=password
        )
        if not user:
            return Response(
                {
                    'success': False,
                    'messages': _('Invalid credentials')
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        token, created = Token.objects.get_or_create(user=user)
        return Response(
            {
                'success': True,
                'messages': _('Login successful'),
                'data': {
                    'token': token.key
                }
            },
            status=status.HTTP_200_OK
        )