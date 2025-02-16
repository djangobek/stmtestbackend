from django.db import models
# Create your models here.
import random





class BotUserModel(models.Model):
    languages = (
        ('uz',"O'zbek",),
        ('en',"English")
    )
    name = models.CharField(max_length=300,null=True,blank=True,verbose_name="Full Name",help_text="Enter full name")
    telegram_id = models.CharField(max_length=100,unique=True,verbose_name="Telegram ID",help_text="Enter telegram id")
    first_name = models.CharField(max_length=300,verbose_name="First Name",help_text="Enter first name,", null=True,blank=True)
    last_name = models.CharField(max_length=300,verbose_name="Last Name",help_text="Enter last name", default = "user")
    language = models.CharField(max_length=5,default='uz',choices=languages,verbose_name="Language",help_text="Choose language")
    added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        if self.name:
            return f"{self.name}"
        else:
            return f"User with ID:{self.telegram_id}"
    class Meta:
        verbose_name = 'Bot User'
        verbose_name_plural='Bot Users'
class TelegramChannelModel(models.Model):
    channel_id = models.CharField(max_length=150,verbose_name="Channel ID",help_text="Enter channel id",unique=True)
    channel_name = models.CharField(max_length=300,verbose_name="Channel Name",help_text="Enter channel name",null=True,blank=True)
    channel_members_count = models.CharField(max_length=200,null=True,blank=True,verbose_name="Channel Memers Count",help_text="Enter channel members count")
    def __str__(self):
        return f"Channel: {self.channel_id}"
    class Meta:
        verbose_name = 'Telegram Channel'
        verbose_name_plural = 'Telegram Channels'

def generate_unique_code():
    while True:
        # Generate a random 4-digit numeric code
        code = ''.join(random.choices("0123456789", k=4))
        # Ensure the code is unique
        if not Test.objects.filter(code=code).exists():
            return code

class Test(models.Model):
    name = models.CharField(
        max_length=300,
        verbose_name="Name",
        help_text="Enter name",
        default="test"
    )
    code = models.CharField(
        max_length=4,
        unique=True,
        verbose_name="Code",
        help_text="Auto-generated unique 4-digit numeric code"
    )
    answers = models.CharField(max_length=3000, verbose_name="Answers", help_text="Enter answers", blank=True, null=True)
    type = models.CharField(max_length=3000, verbose_name="Type", help_text="Enter type", default="Test")
    count = models.IntegerField(verbose_name="Count", help_text="Enter count",default=0)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    owner = models.ForeignKey(BotUserModel,on_delete=models.CASCADE,verbose_name="Owner")
    status = models.BooleanField(verbose_name="Status", default=True, null=True,blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

    class Meta:
        verbose_name = "Test"
        verbose_name_plural = "Tests"


class TestParticipation(models.Model):
    user = models.ForeignKey(
        BotUserModel,
        on_delete=models.CASCADE,
        related_name="test_participations",
        verbose_name="User",
        help_text="The user participating in the test"
    )
    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,
        related_name="participants",
        verbose_name="Test",
        help_text="The test being participated in"
    )
    participated_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Participation Date",
        help_text="The date and time the user participated in the test"
    )
    correct_answer = models.CharField(max_length=3000,verbose_name="Correct Answer",help_text="Correct answer", null=True,blank=True)
    wrong_answer = models.CharField(max_length=3000,verbose_name="Wrong Answer",help_text="Wrong answer", null=True,blank=True)
    answers = models.CharField(max_length=3000, verbose_name="Answers", help_text="Answers", null=True,blank=True)
    certificate = models.BooleanField(default=False, verbose_name="Certificate")
    def __str__(self):
        return f"{self.user} - {self.test} (Score: {self.answers or 'Not Scored'})"

    class Meta:
        verbose_name = "Test Participation"
        verbose_name_plural = "Test Participations"
        unique_together = ("user", "test")



class FileCollection(models.Model):
    title = models.CharField(max_length=255)
    file_ids = models.JSONField()  # Store multiple file IDs in one field
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title