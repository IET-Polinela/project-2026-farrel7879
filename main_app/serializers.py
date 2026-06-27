from rest_framework import serializers

from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.SerializerMethodField()
    reporter_name = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()

    class Meta:
        model = Report
        fields = [
            "id",
            "title",
            "category",
            "description",
            "location",
            "status",
            "created_at",
            "updated_at",
            "reporter",
            "reporter_name",
            "is_owner",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "reporter",
            "reporter_name",
            "is_owner",
        ]

    def get_reporter(self, obj):
        if obj.reporter:
            return obj.reporter.username
        return "Warga Anonim"

    def get_reporter_name(self, obj):
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
        request = self.context["request"]

        validated_data["reporter"] = request.user

        # kalau frontend kirim status gunakan itu
        # kalau tidak kirim maka default DRAFT
        validated_data.setdefault("status", "DRAFT")

        return super().create(validated_data)

    def update(self, instance, validated_data):
        # reporter tidak boleh diubah
        validated_data.pop("reporter", None)

        return super().update(instance, validated_data)