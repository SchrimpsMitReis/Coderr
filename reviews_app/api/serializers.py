
from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField

from reviews_app.models import Review


class ReviewListSerializer(ModelSerializer):

    reviewer = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'business_user', 'reviewer', 'rating',
            'description', 'created_at', 'updated_at']

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        if self.instance is None:
            business_user = attrs.get("business_user")

            if business_user is None:
                raise ValidationError({"business_user": ["This field is required."]})
            
            if Review.objects.filter(reviewer=user, business_user=business_user).exists():
                raise ValidationError({"non_field_errors": ["Du hast diesen Anbieter bereits bewertet."]})
        
        return attrs

    # def create(self, validated_data):

    #     return super().create(validated_data)