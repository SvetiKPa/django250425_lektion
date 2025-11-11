from django.db import models
from django.utils import timezone


class Event(models.Model):
    title = models.CharField(max_length=255, verbose_name="Название события")
    description = models.TextField(verbose_name="Описание")
    date = models.DateField(verbose_name="Дата события")
    library = models.ForeignKey('Library', on_delete=models.SET_NULL, null=True, related_name='events')
    books = models.ManyToManyField('Book', related_name='events', blank=True)

    class Meta:
        db_table = 'events'
        verbose_name = "Event"
        verbose_name_plural = "Events"
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} ({self.date})"


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, related_name='participants')
    member = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name='event_participations')
    registration_date = models.DateField(default=timezone.now, verbose_name="Дата регистрации")

    class Meta:
        db_table = 'event_participants'
        verbose_name = "Event Participant"
        verbose_name_plural = "Event Participants"
        unique_together = [['event', 'member']]
        ordering = ['-registration_date']

    def __str__(self):
        event_title = self.event.title if self.event else "N/A"
        member_name = f"{self.member.last_name[0]}. {self.member.first_name}" if self.member else "N/A"
        return f"{event_title} - {member_name}"
