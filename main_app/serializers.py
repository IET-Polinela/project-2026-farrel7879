from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    # Definisikan field custom yang menggunakan SerializerMethodField
    reporter = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        # Ubah fields menjadi '__all__' agar semua field model tercover otomatis
        fields = "__all__" 
        read_only_fields = ["created_at", "updated_at", "reporter"]
        read_only_fields = ["created_at", "updated_at"]

    def get_reporter(self, obj):
        request = self.context.get("request")
        # 💡 Aturan privasi: Nama asli pelapor HANYA boleh bocor di tab 'my_reports'
        if request and request.query_params.get("tab") == "my_reports":
            if obj.reporter:
                return obj.reporter.username
        return "Warga Anonim"

    def get_reporter_name(self, obj):
        request = self.context.get("request")
        # 💡 Aturan privasi: Nama asli pelapor HANYA boleh bocor di tab 'my_reports'
        if request and request.query_params.get("tab") == "my_reports":
            if obj.reporter:
                return obj.reporter.username
        return "Warga Anonim"

    def get_is_owner(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        if not request.user.is_authenticated:
            return False
        return obj.reporter == request.user

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["reporter"] = request.user
        return super().create(validated_data)