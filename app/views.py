from django.shortcuts import render
# Create your views here.
from rest_framework.viewsets import ModelViewSet
from .serializer import *
from .models import *
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Test
from .serializer import TestSerializer


class BotUserViewset(ModelViewSet):
    queryset = BotUserModel.objects.all()
    serializer_class = BotUserSerializer
class GetUser(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
                serializer = BotUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except BotUserModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
class ChangeUserLanguage(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('telegram_id',None):
            try:
                user = BotUserModel.objects.get(telegram_id=data['telegram_id'])
                user.language = data['language']
                user.save()
                serializer = BotUserSerializer(user, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except BotUserModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)
class TelegramChannelViewset(ModelViewSet):
    queryset = TelegramChannelModel.objects.all()
    serializer_class = TelegramChannelSerializer
class DeleteTelegramChannel(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('channel_id', None):
            try:
                user = TelegramChannelModel.objects.get(channel_id=data['channel_id'])
                user.delete()
                return Response({'status':"Deleted"},status=status.HTTP_200_OK)
            except TelegramChannelModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
class GetTelegramChannel(APIView):
    def post(self,request):
        data = request.data
        data = data.dict()
        if data.get('channel_id',None):
            try:
                channel = TelegramChannelModel.objects.get(channel_id=data['channel_id'])
                serializer = TelegramChannelSerializer(channel, partial=True)
                return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)
            except TelegramChannelModel.DoesNotExist:
                return Response({'error': 'Not found'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error':'Not found'},status=status.HTTP_204_NO_CONTENT)


class UpdateUserDetails(APIView):
    """
    API endpoint to update the first_name and last_name of a user by telegram_id.
    """
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not telegram_id:
            return Response({'error': 'telegram_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(BotUserModel, telegram_id=telegram_id)

        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name

        user.save()
        serializer = BotUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TestCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')  # Get the telegram ID from the request
        try:
            # Check if the user exists using the telegram_id
            owner = BotUserModel.objects.get(telegram_id=telegram_id)
        except BotUserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Add the owner to the request data
        request.data['owner'] = owner.id  # Assign the user to the 'owner' field

        # Serialize the request data
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=owner)  # Save with the correct owner
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        # Get the code from the request query parameters
        code = request.query_params.get('code')
        if not code:
            return Response({'error': 'Code parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the test by code
            test = Test.objects.get(code=code)
        except Test.DoesNotExist:
            return Response({'error': 'Test not found'}, status=status.HTTP_404_NOT_FOUND)

        # Serialize the test data
        serializer = TestSerializer(test)
        return Response(serializer.data, status=status.HTTP_200_OK)

import logging


class TestParticipationView(APIView):
    """
    API for handling Test Participation.
    """
    def get(self, request, test_id, *args, **kwargs):
        """
        Get all participations for a specific test by its ID.
        """
        try:
            participations = TestParticipation.objects.filter(test_id=test_id)
            if not participations.exists():
                return Response(
                    {"error": "No participations found for this test."},
                    status=status.HTTP_404_NOT_FOUND,
                )
                print("error No participations found for this test.")

            serializer = TestParticipationSerializer(participations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, test_id):
        user_id = request.data.get('user_id')
        test_id = request.data.get('test_id')
        answers = request.data.get('answers')
        correct_answer = request.data.get('correct_answer')
        wrong_answer = request.data.get('wrong_answer')
        certificate = request.data.get('certificate')

        if not user_id or not test_id or not answers:
            return Response(
                {"error": "user_id, test_id, and answers are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        participation_data = {
            'user': user_id,
            'test': test_id,
            'answers': answers,
            'correct_answer': correct_answer,
            'wrong_answer': wrong_answer,
            'certificate': certificate,
        }

        serializer = TestParticipationSerializer(data=participation_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTestByCodeView(APIView):
    """
    API to get a test by its unique code.
    """
    def get(self, request, code, *args, **kwargs):
        try:
            test = Test.objects.get(code=code)
            serializer = TestSerializer(test)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Test.DoesNotExist:
            return Response({"error": "Test not found."}, status=status.HTTP_404_NOT_FOUND)

class TestParticipation2View(APIView):
    """
    API to manage test participations.
    """
    def get(self, request, test_id, *args, **kwargs):
        try:
            participations = TestParticipation.objects.filter(test_id=test_id)
            serializer = TestParticipationSerializer(participations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        serializer = TestParticipationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import TestParticipation
from .serializer import TestParticipationSerializer

@api_view(['GET'])
def get_test_participations(request, test_id):
    """
    Fetch all participations for a specific test.
    """
    try:
        # Retrieve participations for the given test ID
        participations = TestParticipation.objects.filter(test_id=test_id)

        if not participations.exists():
            return Response({"message": "No participations found for this test."}, status=404)

        # Serialize the participations data
        serializer = TestParticipationSerializer(participations, many=True)

        return Response(serializer.data)

    except Exception as e:
        # Return an error response if something goes wrong
        return Response({"error": str(e)}, status=500)

import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TestParticipation
from .serializer import TestParticipationSerializer
logger = logging.getLogger(__name__)
import json  # Add this import statement
from django.http import JsonResponse


@csrf_exempt  # Optional: if CSRF protection is not required for API calls
def create_test_participation(request):
    """
    Function-based view to create a new test participation.
    """
    if request.method == 'POST':
        try:
            # Parse incoming JSON data from the request body
            data = json.loads(request.body)  # Use json.loads() to parse the incoming data
            user_id = data.get('user_id')
            test_id = data.get('test_id')
            answers = data.get('answers')
            correct_answer = data.get('correct_answer')
            wrong_answer = data.get('wrong_answer')
            certificate = data.get('certificate')

            # Ensure required fields are provided
            if not user_id or not test_id or not answers:
                return JsonResponse(
                    {"error": "user_id, test_id, and answers are required."},
                    status=400
                )

            # Fetch the user instance
            try:
                user = BotUserModel.objects.get(telegram_id=user_id)
            except BotUserModel.DoesNotExist:
                return JsonResponse({"error": "User not found."}, status=404)

            # Fetch the test instance
            try:
                test = Test.objects.get(id=test_id)
            except Test.DoesNotExist:
                return JsonResponse({"error": "Test not found."}, status=404)

            logger.info(f"Received data: {data}")

            # Prepare the data for the serializer
            participation_data = {
                'user': user,
                'test': test,
                'answers': answers,
                'correct_answer': correct_answer,
                'wrong_answer': wrong_answer,
                'certificate': certificate,
            }

            # Initialize the serializer
            serializer = TestParticipationSerializer(data=participation_data)

            # Validate and save data
            if serializer.is_valid():
                # Save the participation record to the database
                serializer.save()
                return JsonResponse(serializer.data, status=201)

            # If validation fails, return the errors
            return JsonResponse(serializer.errors, status=400)

        except Exception as e:
            # If something goes wrong, return an error response with details
            logger.error(f"Error creating participation: {str(e)}")
            return JsonResponse({"error": f"An error occurred: {str(e)}"}, status=500)

    else:
        return JsonResponse(
            {"error": "Invalid method. Only POST is allowed."},
            status=405
        )



class TestParticipationCreateAPIView(APIView):
    """
    API view to handle the creation of TestParticipation records.
    """

    def post(self, request, *args, **kwargs):
        # Get telegram_id from the request data
        user_id = request.data.get('user_id')
        # Extract other fields from the request
        test_id = request.data.get('test_id')
        answers = request.data.get('answers')
        correct_answer = request.data.get('correct_answer')
        wrong_answer = request.data.get('wrong_answer')
        certificate = request.data.get('certificate', False)  # Default to False if not provided

        if not test_id or not answers:
            return Response({"error": "test_id and answers are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the test by its ID
            test = Test.objects.get(id=test_id)
        except Test.DoesNotExist:
            return Response({"error": "Test not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare data for the serializer
        participation_data = {
            'user': user_id,  # Pass the user ID
            'test': test.id,  # Pass the test ID
            'answers': answers,
            'correct_answer': correct_answer,
            'wrong_answer': wrong_answer,
            'certificate': certificate,
        }

        # Serialize the data
        serializer = TestParticipationSerializer2(data=participation_data)
        if serializer.is_valid():
            # Save the participation record
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # If serializer validation fails, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestListAPIView(APIView):
    def get(self, request, format=None):
        # Fetch all the tests from the database
        tests = Test.objects.all()

        # Serialize the tests using the TestSerializer
        serializer = TestSerializer(tests, many=True)

        # Return the serialized data in a JSON response
        return Response(serializer.data, status=status.HTTP_200_OK)


from django.http import Http404


class UpdateTestStatusAPIView(APIView):
    """
    API to toggle the status of a test.
    """

    def post(self, request, test_id):
        try:
            test = get_object_or_404(Test, id=test_id)

            # Ensure status is a boolean


            # Update the test status
            if test.status == True:
                test.status = False

                test.save()
            else:
                test.status = True
                test.save()



            return Response({
                "success": True,
                "status": test.status,
                "message": f"Test '{test.name}' status updated."
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False,
                "error": str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

