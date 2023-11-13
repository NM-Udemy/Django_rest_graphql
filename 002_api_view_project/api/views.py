from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ItemSerializer
from rest_framework import status
from .models import Item

class ItemView(APIView):
    
    serializer_class = ItemSerializer

    def get(self, request): # 一覧(http://localhost/api/item/)
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        # print(items)
        # print(serializer)
        return Response(serializer.data)

    def post(self, request): # データを保存
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        print(serializer)
        
        # バリデーション
        # print(serializer.is_valid(raise_exception=True))
        # print(serializer.errors)
        if serializer.is_valid(raise_exception=True):
            serializer.save() # 保存(create) or 更新
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data)

    def put(self, request):
        return Response({'method': 'put'})

    def delete(self, request):
        return Response({'method': 'delete'})

    def patch(self, request):
        return Response({'method': 'patch'})


class ItemDetailView(APIView):
    
    serializer_class = ItemSerializer
    
    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = self.serializer_class(item)
        return Response(serializer.data)
    
    def put(self, request, pk):
        item = Item.objects.get(pk=pk)
        serializer = self.serializer_class(item, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, pk):
        item = Item.objects.get(pk=pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        item = Item.objects.get(pk=pk)
        print(request.data)
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)
    
