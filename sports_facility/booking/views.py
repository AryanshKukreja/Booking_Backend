from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
import datetime

from .models import Sport, Court, TimeSlot, Booking, BookingStatus
from .serializers import SportSerializer, CourtSerializer, TimeSlotSerializer, BookingSerializer


class SportViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing sports"""
    queryset = Sport.objects.all()
    serializer_class = SportSerializer


class TimeSlotViewSet(viewsets.ReadOnlyModelViewSet):
    """API endpoint for listing time slots"""
    queryset = TimeSlot.objects.all().order_by('hour')
    serializer_class = TimeSlotSerializer


@api_view(['GET'])
def court_status_api(request):
    """API endpoint for getting court status"""
    sport_id = request.query_params.get('sport', None)
    date_str = request.query_params.get('date', timezone.now().date().isoformat())

    try:
        booking_date = datetime.date.fromisoformat(date_str)
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=400)

    if not sport_id:
        first_sport = Sport.objects.first()
        if first_sport:
            sport_id = first_sport.id
        else:
            return Response({'error': 'No sports available'}, status=404)

    sports_data = SportSerializer(Sport.objects.all(), many=True).data
    time_slots = TimeSlot.objects.all().order_by('hour')
    time_slots_data = TimeSlotSerializer(time_slots, many=True).data
    courts = Court.objects.filter(sport_id=sport_id)
    bookings = Booking.objects.filter(
        court__sport_id=sport_id,
        date=booking_date
    )

    court_data = []
    for court in courts:
        court_info = {
            'id': court.id,
            'name': court.name,
            'slots': {
                slot.id: {
                    'id': slot.id,
                    'time': slot.formatted_slot,
                    'status': 'available'
                } for slot in time_slots
            }
        }

        for booking in bookings:
            if booking.court_id == court.id:
                court_info['slots'][booking.time_slot_id]['status'] = booking.status

        court_data.append(court_info)

    response_data = {
        'date': date_str,
        'currentTime': timezone.now().strftime('%I:%M %p'),
        'sports': sports_data,
        'selectedSport': sport_id,
        'timeSlots': time_slots_data,
        'courts': court_data
    }

    return Response(response_data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def update_booking_api(request):
    """API endpoint for admins to update booking status"""
    court_id = request.data.get('courtId')
    time_slot_id = request.data.get('timeSlotId')
    new_status = request.data.get('status')
    date_str = request.data.get('date', timezone.now().date().isoformat())

    if new_status not in [choice[0] for choice in BookingStatus.choices]:
        return Response({'error': 'Invalid status'}, status=400)

    try:
        booking_date = datetime.date.fromisoformat(date_str)
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=400)

    booking, created = Booking.objects.update_or_create(
        court_id=court_id,
        time_slot_id=time_slot_id,
        date=booking_date,
        defaults={
            'status': new_status,
            'user': request.user
        }
    )

    return Response({
        'success': True,
        'booking': BookingSerializer(booking).data
    })
