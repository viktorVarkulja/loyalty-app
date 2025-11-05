from rest_framework import serializers
from .models import Product, Store, UserFavoriteStore


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for Product model."""

    class Meta:
        model = Product
        fields = ['id', 'name', 'points', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Store model."""

    class Meta:
        model = Store
        fields = ['id', 'name', 'location', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserFavoriteStoreSerializer(serializers.ModelSerializer):
    """Serializer for UserFavoriteStore model."""

    store = StoreSerializer(read_only=True)
    store_id = serializers.CharField(write_only=True)

    class Meta:
        model = UserFavoriteStore
        fields = ['id', 'store', 'store_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        """Create favorite store relationship."""
        user = self.context['request'].user
        store_id = validated_data.pop('store_id')

        try:
            store = Store.objects.get(id=store_id)
        except Store.DoesNotExist:
            raise serializers.ValidationError({"store_id": "Store not found."})

        favorite, created = UserFavoriteStore.objects.get_or_create(
            user=user,
            store=store
        )

        if not created:
            raise serializers.ValidationError({"detail": "Store is already in favorites."})

        return favorite
