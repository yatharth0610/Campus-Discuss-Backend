from django.contrib.auth import login, logout
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from tokens.models import Token
from .utils import IsLoggedIn
from django.contrib.auth import authenticate

class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        user = IsLoggedIn(request)
        if user is not None :
            print("User is logged in")
            return Response(status = status.HTTP_400_BAD_REQUEST)
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        token = request.data.get("token", "")
        
        try:
            user = User.objects.get(username = username, password = password)
            if user is not None:
                request.session["username"] = username 
                request.session.modified = True                     
                t = Token.objects.filter(token = token)
                print (token)
                print(Token.objects.all())
                if len(t) == 0 and token != "undefined":
                    print("Creating New Token")
                    newtoken = Token(token = token)
                    newtoken.save()
                    newtoken.user.add(user)
                    newtoken.save()
                return Response(status = status.HTTP_200_OK)
            
        except :
            print("No such user")
            return Response(status = status.HTTP_400_BAD_REQUEST)
        
    def get(self, request):
        if IsLoggedIn(request) is not None:
            print("Can't log in")
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status = status.HTTP_200_OK)

class LogoutView(APIView):

    def post(self, request):
        if IsLoggedIn(request) is not None:
            token = request.data.get("token")
            dtoken = Token.objects.filter(token=token)
            if len(dtoken) != 0:
                dtoken[0].delete()
            del request.session["username"]
            print("User logged out successfully!")
            return Response(status = status.HTTP_200_OK)
        return Response(status = status.HTTP_401_UNAUTHORIZED)


