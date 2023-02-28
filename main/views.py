from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from .serializers import *
from datetime import date
from .models import *

class UserList(APIView): 
    def get(self, request) :
        login_user = request.user
        user = CustomUser.objects.all().exclude(pk=login_user.pk)
        close_friend = CustomUser.objects.filter(id__in = [user.id for user in login_user.friend_list.all()])

        close_friend_list = []
        for i in close_friend :
            close_friend_list.append(i.username)

        user_serializer = CustomUserSerializers(user, many=True)

        return Response({"data": {
            "user": user_serializer.data,
            "close_friend": close_friend_list
        }}, status=status.HTTP_200_OK)
    
class User(APIView):
    def get(self,request) :
        data = request.user
        serializer = CustomUserSerializers(data)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
    def put(self, request) :
        data = request.data
        login_user = request.user

        friend_list = CustomUser.objects.filter(username__in = data['data'])
        login_user_friend = login_user.friend_list.all()

        for i in friend_list :
            if(i not in login_user_friend) :
                login_user.friend_list.add(i)

        for i in login_user_friend :
            if(i not in friend_list) :
                login_user.friend_list.remove(i)

        login_user.save()
        return Response({"Message": "Succes"}, status= status.HTTP_202_ACCEPTED)

class ContentList(APIView) :
    def get(self, request) :
        data = Content.objects.all()
        serializer = ContentListSerializers(data, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

class ContentListUser(APIView) :
    def get(self, request) :
        user = request.user
        data = Content.objects.filter(user = user)
        serializer = ContentListSerializers(data, many=True)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    
class ContentData(APIView) :
    def post(self, request) :
        data = request.data
        if (len(data['is_close_friend']) > 0 and data['is_close_friend'][0] == "on") :
            content = Content.objects.create(
                user = request.user,
                description = data["description"],
                date = date.today(),
                is_close_friend = True
            )
        else :
             content = Content.objects.create(
                user = request.user,
                description = data["description"],
                date = date.today()
            )
        content.save()
        serializer = ContentSerializers(content)
        return Response({"Message" : "Succes", "data": serializer.data}, status=status.HTTP_202_ACCEPTED)
     
    def delete(self, request, id) :
        content = Content.objects.get(pk = id)
        if(request.user != content.user) :
            return Response({"Message": "Failed"}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = ContentSerializers(content)
        content.delete()
        return Response({"Message": "Succes", "data":serializer.data}, status= status.HTTP_202_ACCEPTED)

    def put(self, request, id) :
        content = Content.objects.get(pk=id)
        if(request.user != content.user) :
            return Response({"Message": "Failed"}, status=status.HTTP_401_UNAUTHORIZED)
        
        data = request.data

        content.description = data['description']
        content.date = date.today()

        content.save()
        serializer = ContentListSerializers(content)

        return Response({"Message": "Succes", "data":serializer.data}, status= status.HTTP_202_ACCEPTED)


class Login(APIView) :
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self,request) :
        data = request.data
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None :
            serializer = CustomUserSerializers(user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={"Message" : "Succes", "token" : token.key, "user" : serializer.data}, status=status.HTTP_200_OK)
        else :
            return Response({"Message" : "Failed"}, status=status.HTTP_401_UNAUTHORIZED)
        
class SignUp(APIView) :
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self,request) :
        data = request.data
        try :
            CustomUser.objects.create_user(username = data['username'], password = data['password'])
            return Response({"Message" : "Succes"}, status=status.HTTP_201_CREATED)
        except :
            return Response({"Message" : "Failed"}, status=status.HTTP_400_BAD_REQUEST)
        
class Logout(APIView) :
    def get(self, request) :
        user = request.user
        token = Token.objects.get(user = user)
        token.delete()

        return Response({"Message" : "Succes"}, status=status.HTTP_200_OK)



