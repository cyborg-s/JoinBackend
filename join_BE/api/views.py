from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer, ContactSerializer, SubtaskSerializer, UserRegistrationSerializer, UserProfileSerializer, CustomAuthTokenSerializer
from join_BE.models import Tasks, Contacts, Subtask, UserProfile
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes


@api_view(['PUT', 'DELETE'])
def update_or_delete_subtask(request, pk):
    try:
        subtask_instance = Subtask.objects.get(pk=pk)
    except Subtask.DoesNotExist:
        return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        print("REQUEST DATA:", request.data)
        serializer = SubtaskSerializer(
            subtask_instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subtask_instance.delete()
        return Response({'message': 'Subtask deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def task_view(request):
    print("TASK POST DATA:", request.data)
    if request.method == 'GET':
        tasks = Tasks.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET', 'DELETE', 'PUT'])
def task_single_view(request, pk):
    if request.method == 'GET':
        try:
            task = Tasks.objects.get(pk=pk)
            serializer = TaskSerializer(task)
            return Response(serializer.data)
        except Tasks.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        try:
            task = Tasks.objects.get(pk=pk)
        except Tasks.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

        task_data = request.data
        subtasks_data = task_data.pop('subtask', [])

        serializer = TaskSerializer(task, data=task_data, partial=True)
        if serializer.is_valid():
            serializer.save()

            for subtask_data in subtasks_data:
                subtask_id = subtask_data.get('id', None)

                if subtask_id:

                    try:
                        sub = Subtask.objects.get(id=subtask_id, task=task)
                        sub.title = subtask_data.get('title', sub.title)
                        sub.status = subtask_data.get('status', sub.status)
                        sub.save()
                    except Subtask.DoesNotExist:
                        continue
                else:

                    Subtask.objects.create(
                        task=task,
                        title=subtask_data.get('title', ''),
                        status=subtask_data.get('status', False)
                    )

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        try:
            task = Tasks.objects.get(pk=pk)

            task.subtasks.all().delete()

            task.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Tasks.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def contact_view(request):

    if request.method == 'GET':
        contacts = Contacts.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE', 'PUT'])
@permission_classes([IsAuthenticated])
def contact_single_view(request, pk):
    try:
        contact = Contacts.objects.get(pk=pk)
    except Contacts.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=404)

    if request.method == 'GET':
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ContactSerializer(
            contact, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    elif request.method == 'DELETE':
        contact.delete()
        return Response(status=204)


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()
            token, _ = Token.objects.get_or_create(user=saved_account)

            Contacts.objects.create(
                name=saved_account.first_name,
                email=saved_account.email,
                phone=None
            )

            data = {
                'token': token.key,
                'first_name': saved_account.first_name,
                'email': saved_account.email
            }
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(data)


class CustomLoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'first_name': user.first_name,
            'email': user.email
        })


class UserProfileList(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class CheckTokenView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'first_name': user.first_name,
            'email': user.email,
            'token_valid': True
        })
