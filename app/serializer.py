from rest_framework.serializers import ModelSerializer
from .models import BotUserModel,TelegramChannelModel
class BotUserSerializer(ModelSerializer):
    class Meta:
        model = BotUserModel
        fields = '__all__'
class TelegramChannelSerializer(ModelSerializer):
    class Meta:
        model = TelegramChannelModel
        fields = '__all__'

from rest_framework import serializers
from .models import Test


class BotUserModelSerializer(serializers.ModelSerializer):
    """Serializer for the BotUserModel to include full_name and telegram_id."""
    class Meta:
        model = BotUserModel
        fields = ['id', 'first_name','last_name', 'telegram_id']

class TestSerializer(serializers.ModelSerializer):
    telegram_id = serializers.IntegerField(write_only=True, required=False)  # Incoming telegram ID
    owner = BotUserModelSerializer(read_only=True)  # Use the nested serializer for owner details

    class Meta:
        model = Test
        fields = ['id', 'name', 'code', 'answers', 'type', 'count', 'created', 'telegram_id', 'owner','status']

    def create(self, validated_data):
        telegram_id = validated_data.get('telegram_id')
        owner = None
        if telegram_id:
            try:
                owner = BotUserModel.objects.get(telegram_id=telegram_id)  # Find the user by telegram_id
            except BotUserModel.DoesNotExist:
                raise serializers.ValidationError("User with this telegram_id does not exist.")

        # Remove the telegram_id from validated data and set the owner
        validated_data.pop('telegram_id', None)
        validated_data['owner'] = owner

        # Create the Test instance with the owner
        return super().create(validated_data)

    def update(self, instance, validated_data):
        telegram_id = validated_data.get('telegram_id')
        if telegram_id:
            try:
                owner = BotUserModel.objects.get(telegram_id=telegram_id)
                validated_data['owner'] = owner
            except BotUserModel.DoesNotExist:
                raise serializers.ValidationError("User with this telegram_id does not exist.")

        return super().update(instance, validated_data)



from rest_framework import serializers
from .models import TestParticipation

class BotUserSerializer2(serializers.ModelSerializer):
    """
    Serializer for BotUserModel to include first_name and last_name.
    """
    class Meta:
        model = BotUserModel
        fields = ['first_name', 'last_name']

class TestParticipationSerializer(serializers.ModelSerializer):
    user = BotUserSerializer()  # Nesting BotUserSerializer to include user details

    class Meta:
        model = TestParticipation
        fields = ['user', 'test', 'answers', 'correct_answer', 'wrong_answer', 'certificate','participated_at']

class TestParticipationSerializer2(serializers.ModelSerializer):
 # Nesting BotUserSerializer to include user details
    class Meta:
        model = TestParticipation
        fields = ['user', 'test', 'answers', 'correct_answer', 'wrong_answer', 'certificate']

class CreateTestParticipationSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    test_code = serializers.CharField(max_length=10)
    answers = serializers.CharField(max_length=3000)

    def create(self, validated_data):
        # Find user by Telegram ID
        telegram_id = validated_data['telegram_id']
        user = BotUserModel.objects.filter(telegram_id=telegram_id).first()
        if not user:
            raise serializers.ValidationError({"error": "User not found with this Telegram ID."})

        # Find test by code
        test_code = validated_data['test_code']
        test = Test.objects.filter(code=test_code).first()
        if not test:
            raise serializers.ValidationError({"error": "Test not found with this code."})

        # Check if the user has already participated in the test
        if TestParticipation.objects.filter(user=user, test=test).exists():
            raise serializers.ValidationError({"error": "User has already participated in this test."})

        # Create participation record
        participation = TestParticipation.objects.create(
            user=user,
            test=test,
            answers=validated_data['answers'],
        )
        return participation


class TestParticipationSerializerforpost(serializers.ModelSerializer):
    class Meta:
        model = TestParticipation
        fields = ['user', 'test', 'answers', 'correct_answer', 'wrong_answer', 'certificate','telegram_id']

class TestSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['id', 'name', 'code', 'answers', 'type', 'count', 'created', 'owner', 'status']
        read_only_fields = ['id', 'created']

class TestStatusSerializer(serializers.ModelSerializer):
    status = serializers.BooleanField()

    class Meta:
        model = Test
        fields = ['test_id','status']