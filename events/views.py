from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *
from rest_framework import permissions
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response


class PostAPIViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        p_objs = Post.objects.filter(p_active=True).order_by('-id')
        serializer = PostListSerializer(p_objs, many=True)
        context = {
            'data': serializer.data,
            'status': status.HTTP_200_OK
        }
        return Response(context, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request.data['p_user'] = request.user.id
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'data': serializer.data,
                'status': status.HTTP_200_OK
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post_detail(self, request, pk=None, *args, **kwargs):
        p_obj = get_object_or_404(Post, id=pk, p_active=True)
        serializer = PostDetailSerializer(p_obj, many=False)
        if p_obj:
            c_objs = Comment.objects.filter(c_post=pk, c_active=True).order_by('id')
            c_serializer = CommentListSerializer(c_objs, many=True)
            context = {
                'data': serializer.data,
                'comments': c_serializer.data,
                'status': True,
            }
            return Response(context, status=status.HTTP_200_OK)


class CommentAPIViewSet(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        request.data['c_user'] = request.user.id
        serializer = CommentCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                'data': serializer.data,
                'status': status.HTTP_200_OK
            }
            return Response(context, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)