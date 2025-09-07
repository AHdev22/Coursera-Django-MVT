from rest_framework import serializers

class ReservationSerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.TimeField(
        input_formats=["%I:%M %p", "%H:%M"],  # accepts "1:30 PM" and "13:30"
    )
    guests = serializers.IntegerField()
    special_request = serializers.CharField(required=False, allow_blank=True)