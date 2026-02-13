
from rest_framework.serializers import ModelSerializer, ValidationError, PrimaryKeyRelatedField

from reviews_app.models import Review


class ReviewListSerializer(ModelSerializer):
    """
    Serializer for Reviews (suitable for list and create operations).
    
    Fields:
    - reviewer is read-only and is typically set automatically from `request.user`
      (e.g., in perform_create within the view or inside serializer.create()).
    
    Validation:
    - On creation (instance is None), the serializer checks whether the current user
      has already reviewed the same business_user (one review per reviewer-business pair).    """

    reviewer = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "business_user",
            "reviewer",
            "rating",
            "description",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        """
        Object-level validation.

        Rule:
        - A reviewer may review a specific Business user only once.
        - This validation is executed only during creation
          (self.instance is None).
        """        
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not request or not user:
            return attrs

        if self.instance is None:
            business_user = attrs.get("business_user")

            if business_user is None:
                raise ValidationError({"business_user": ["This field is required."]})

            if Review.objects.filter(reviewer=user, business_user=business_user).exists():
                raise ValidationError(
                    {"non_field_errors": ["Du hast diesen Anbieter bereits bewertet."]}
                )

        return attrs