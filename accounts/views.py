from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import RegisterSerialzer,loginSerilizer
from rest_framework import status
from rest_framework.permissions import AllowAny


class RegisterApiView(APIView):
    permission_classes=[AllowAny]
    def post(self,request):
        try:
            data=request.data
            serializer=RegisterSerialzer(data=data)
            if not serializer.is_valid():
                return Response({'data':serializer.errors,'message':'something went wrong'},status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'message':'your account create succefully'
            },status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
            
            
class LoginApi(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        try:
            data = request.data
            serializer = loginSerilizer(data=data)

            # Validate the input
            if not serializer.is_valid():
                return Response(
                    {'data': serializer.errors, 'message': 'Invalid input'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            response = serializer.get_jwt_token()

            return Response(
                {'data': response['data'], 'message': response['message']},
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                {'data': {}, 'message': f'An error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

            

            
    