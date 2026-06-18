from rest_framework import serializers
from .models import Ticket
from apps.reports.models import Report


class TicketSerializer(serializers.ModelSerializer):
    report_ids = serializers.PrimaryKeyRelatedField(
        queryset=Report.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='reports'
    )
    # Zwraca listę ID przypisanych raportów w odpowiedzi

    reports = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    assigned_id = serializers.ReadOnlyField(source='assigned_to.id')

    class Meta:
        model = Ticket
        fields = [
            'id', 'title', 'description', 'ticket_type', 'created_at',
            'latitude', 'longitude', 'reports', 'report_ids',
            'assigned_id', 'updates', 'status'
        ]

    def create(self, validated_data):
        reports = validated_data.pop('reports', [])

        # Jeśli nie podano lokalizacji w POST, pobierana z pierwszego raportu
        if (validated_data.get('latitude') is None or validated_data.get('longitude') is None) and reports:
            first_report = reports[0]
            validated_data['latitude'] = first_report.latitude
            validated_data['longitude'] = first_report.longitude

        # Domyślna pierwsza aktualizacja w historii
        if not validated_data.get('updates'):
            validated_data['updates'] = ["Ticket created."]

        ticket = Ticket.objects.create(**validated_data)

        for report in reports:
            report.ticket = ticket
            report.save()

        return ticket