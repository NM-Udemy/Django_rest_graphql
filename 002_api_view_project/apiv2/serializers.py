from rest_framework import serializers
from api.models import Item, Product
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class ProductModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = '__all__'


class UserModelSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model()
        return user.objects.create_user(
            validated_data['username'], email=validated_data['email'],
            password=validated_data['password']
        )

    
def check_divide_by_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError("10で割り切れる値にしてください")

class ItemModelSerializer(serializers.ModelSerializer):
    discounted_price = serializers.IntegerField(min_value=0, 
                                                validators=[check_divide_by_ten,]
                                            )

    class Meta:
        model = Item
        # fields = '__all__'
        fields = ['pk', 'name', 'price', 'discounted_price']
        # read_only_fields = ['price']
        # extra_kwargs = {
        #     'name': {'write_only': True, 'required': False}
        # }
        validators = [
            UniqueTogetherValidator(
                queryset=Item.objects.all(),
                fields=['name', 'price'],
                message='nameとpriceの組み合わせは同じ値にしないでください'
            )
        ]
        
    
    def validate_price(self, value): # priceに対するバリデーション
        if self.partial and value is None:
            return value
        # 1桁目が0以外を弾く(11, 12)
        if value % 10 != 0:
            raise serializers.ValidationError("1桁目は0にしてください")
        return value
    
    def validate_name(self, value):
        if self.partial and value is None:
            return value
        if value[0].islower(): # apple, banana
            raise serializers.ValidationError("最初の文字は大文字にしてください")
        return value
    
    def validate(self, data):
        price = data.get('price', self.instance.price if self.instance is not None else None)
        discounted_price = data.get('discounted_price', self.instance.discounted_price if self.instance is not None else None)
        
        if price < discounted_price:
            raise serializers.ValidationError("割引価格は本来の価格以下の値にしてください")
        return data


class LoginSerializer(serializers.Serializer):
    
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(style={'input_type': 'password'},
                                     write_only=True)
    
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        
        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password
                                )
            if not user:
                raise serializers.ValidationError('ログインできません')
        else:
            raise serializers.ValidationError('ユーザー名とパスワードを入力してください')
        data['user'] = user
        return data
    