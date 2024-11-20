from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import Blogserializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
            
class BlogApiview(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes=[JWTAuthentication]

    def post(self, request):
        data = request.data
        user = request.user

        if not user or user.is_anonymous:
            return Response(
                {'message': 'User not authenticated'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Attach the user ID to the data
        data['user'] = user.id

        # Validate serializer
        serializer = Blogserializers(data=data)
        if not serializer.is_valid():
            return Response(
                {'data': serializer.errors, 'message': 'Validation failed'},
                status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(
            {'data': serializer.data, 'message': 'Blog created successfully'},
            status=status.HTTP_201_CREATED)
    def get(self,request):
        try:
            blogs=Blog.objects.filter(user=request.user)
            if request.GET.get('search'):
                search_key=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains = search_key)|Q(blog_text__icontains = search_key))
            serializer=Blogserializers(blogs,many=True)
            return Response({
                'data':serializer.data,
                'message':'blog fetched succefully'
            },status=status.HTTP_200_OK)
        except Exception as e:
             return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
             

    def patch(self, request):
        try:
            data = request.data

            uid = data.get('uid')
            if not uid:
                return Response({
                    'data': {},
                    'message': 'UID is required to update the blog.'
                }, status=status.HTTP_400_BAD_REQUEST)

            blog = Blog.objects.filter(uid=uid).first()
            if not blog:
                return Response({
                    'data': {},
                    'message': 'Blog does not exist.'
                }, status=status.HTTP_404_NOT_FOUND)

            if request.user != blog.user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to update this blog.'
                }, status=status.HTTP_403_FORBIDDEN)

            serializer = Blogserializers(blog, data=data, partial=True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Validation failed.'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'Blog updated successfully.'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                'data': {},
                'message': f'Something went wrong: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

             
    def delete(self, request):
        try:
            data = request.data
            uid = data.get('uid')
            if not uid:
                return Response({
                    'data': {},
                    'message': 'UID is required to update the blog.'
                }, status=status.HTTP_400_BAD_REQUEST)

            blog = Blog.objects.filter(uid=uid).first()
            if not blog:
                return Response({
                    'data': {},
                    'message': 'Blog does not exist.'
                }, status=status.HTTP_404_NOT_FOUND)

            if request.user != blog.user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to update this blog.'
                }, status=status.HTTP_403_FORBIDDEN)
            blog.delete()
            return Response({
                'message': 'Blog deleted successfully.'
            }, status=status.HTTP_200_OK)


           
        except Exception as e:
            return Response({
                'data': {},
                'message': f'Something went wrong: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                   
                
                
class PublicBlog(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        try:
            blogs=Blog.objects.all().order_by('?')
            if request.GET.get('search'):
                search_key=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains = search_key)|Q(blog_text__icontains = search_key))
            page_number=request.GET.get('page',1)
            paginator=Paginator(blogs,2)
            serializer=Blogserializers(paginator.page(page_number),many=True)
            return Response({
                'data':serializer.data,
                'message':'blog fetched succefully'
            },status=status.HTTP_200_OK)
        except Exception as e:
             return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)