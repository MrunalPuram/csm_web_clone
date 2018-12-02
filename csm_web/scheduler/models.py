from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass


class Attendance(models.Model):
    PRESENT = "PR"
    UNEXCUSED_ABSENCE = "UN"
    EXCUSED_ABSENCE = "EX"
    PRESENCE_CHOICES = (
        (PRESENT, "Present"),
        (UNEXCUSED_ABSENCE, "Unexcused absence"),
        (EXCUSED_ABSENCE, "Excused absence"),
    )
    section = models.ForeignKey("Section", on_delete=models.CASCADE)
    week_start = models.DateField()
    presence = models.CharField(max_length=2, choices=PRESENCE_CHOICES)
    attendee = models.ForeignKey("Profile", on_delete=models.CASCADE)

    @property
    def leader(self):
        return self.section.mentor


class Course(models.Model):
    name = models.SlugField(max_length=100)
    valid_until = models.DateField()
    enrollment_start = models.DateTimeField()
    enrollment_end = models.DateTimeField()

    def __str__(self):
        return self.name


class Profile(models.Model):
    STUDENT = "ST"
    JUNIOR_MENTOR = "JM"
    SENIOR_MENTOR = "SM"
    COORDINATOR = "CO"
    ROLE_CHOICES = (
        (STUDENT, "Student"),
        (JUNIOR_MENTOR, "Junior Mentor"),
        (SENIOR_MENTOR, "Senior Mentor"),
        (COORDINATOR, "Coordinator"),
    )
    leader = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="follower", blank=True, null=True
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=ROLE_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    section = models.ForeignKey(
        "Section",
        related_name="students",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "%s %s %s" % (self.role, self.course.name, self.user.username)


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mentor = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="mentor_sections",
        limit_choices_to={
            "role__in": [
                Profile.JUNIOR_MENTOR,
                Profile.SENIOR_MENTOR,
                Profile.COORDINATOR,
            ],
        },
    )
    default_spacetime = models.OneToOneField("Spacetime", on_delete=models.CASCADE)
    capacity = models.PositiveSmallIntegerField()

    @property
    def current_student_count(self):
        return self.students.count()

    @property
    def leader(self):
        return self.mentor

    def __str__(self):
        return "%s %s" % (self.course.name, str(self.default_spacetime))


class Spacetime(models.Model):
    MONDAY = "M"
    TUESDAY = "TU"
    WEDNESDAY = "W"
    THURSDAY = "TH"
    FRIDAY = "F"
    SATURDAY = "SA"
    SUNDAY = "SU"
    DAY_OF_WEEK_CHOICES = (
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    )
    location = models.CharField(max_length=100)
    start_time = models.TimeField()
    duration = models.DurationField()
    day_of_week = models.CharField(max_length=2, choices=DAY_OF_WEEK_CHOICES)

    def __str__(self):
        return "%s %s %s for %s min" % (
            self.location,
            self.day_of_week,
            str(self.start_time),
            str(self.duration),
        )


class Override(models.Model):
    spacetime = models.OneToOneField(Spacetime, on_delete=models.CASCADE)
    week_start = models.DateField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)

    @property
    def leader(self):
        return self.section.mentor
