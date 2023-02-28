from rest_framework import serializers
from.models import *




class CustomUserSerializers(serializers.ModelSerializer) :
    friend_list = serializers.SerializerMethodField('get_username')
    class Meta :
        model = CustomUser
        fields = "__all__"
    
    def get_username(self, obj) :
        friend_list = []
        object = obj.friend_list.all()
        for i in object :
            friend_list.append(i.username)
        return friend_list

class ContentSerializers(serializers.ModelSerializer) :
    class Meta :
        model = Content
        fields = "__all__"

class ContentListSerializers(serializers.Serializer) :
    pk = serializers.IntegerField()
    user = CustomUserSerializers()
    description = serializers.CharField(max_length=500)
    date = serializers.DateField()
    is_close_friend = serializers.BooleanField()

    