from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiParameter

from .models import Product, Store, UserFavoriteStore
from .serializers import ProductSerializer, StoreSerializer, UserFavoriteStoreSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for Product CRUD operations."""

    queryset = Product.objects.filter(status='ACTIVE')
    serializer_class = ProductSerializer

    def get_permissions(self):
        """Admin only for create, update, delete. Authenticated users for list/retrieve."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @extend_schema(
        summary="List all active products",
        description="Get a list of all active products with their point values.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get product details",
        description="Retrieve details of a specific product by ID.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create new product (Admin only)",
        description="Create a new product with name, points, and status.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update product (Admin only)",
        description="Update an existing product's details.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update product (Admin only)",
        description="Partially update an existing product's details.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete product (Admin only)",
        description="Delete a product from the system.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        summary="Search products by name",
        description="Search for products by name (case-insensitive partial match).",
        parameters=[
            OpenApiParameter(name='q', description='Search query', required=True, type=str)
        ]
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search products by name."""
        query = request.query_params.get('q', '')
        if not query:
            return Response(
                {"detail": "Search query parameter 'q' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        products = Product.objects.filter(
            name__icontains=query,
            status='ACTIVE'
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)


class StoreViewSet(viewsets.ModelViewSet):
    """ViewSet for Store CRUD operations."""

    queryset = Store.objects.all()
    serializer_class = StoreSerializer

    def get_permissions(self):
        """Admin only for create, update, delete. Authenticated users for list/retrieve."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @extend_schema(
        summary="List all stores",
        description="Get a list of all stores.",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Get store details",
        description="Retrieve details of a specific store by ID.",
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Create new store (Admin only)",
        description="Create a new store with name and location.",
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(
        summary="Update store (Admin only)",
        description="Update an existing store's details.",
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Partially update store (Admin only)",
        description="Partially update an existing store's details.",
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @extend_schema(
        summary="Delete store (Admin only)",
        description="Delete a store from the system.",
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


@extend_schema(
    summary="List user's favorite stores",
    description="Get all stores marked as favorite by the authenticated user.",
    responses={200: UserFavoriteStoreSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_favorite_stores(request):
    """Get user's favorite stores."""
    favorites = UserFavoriteStore.objects.filter(user=request.user)
    serializer = UserFavoriteStoreSerializer(favorites, many=True)
    return Response(serializer.data)


@extend_schema(
    summary="Add store to favorites",
    description="Mark a store as favorite for the authenticated user.",
    request=UserFavoriteStoreSerializer,
    responses={
        201: UserFavoriteStoreSerializer,
        400: OpenApiResponse(description="Validation error or store already in favorites")
    }
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_store(request):
    """Add a store to user's favorites."""
    serializer = UserFavoriteStoreSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    summary="Remove store from favorites",
    description="Remove a store from the authenticated user's favorites.",
    responses={
        204: OpenApiResponse(description="Store removed from favorites"),
        404: OpenApiResponse(description="Favorite store not found")
    }
)
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite_store(request, favorite_id):
    """Remove a store from user's favorites."""
    try:
        favorite = UserFavoriteStore.objects.get(id=favorite_id, user=request.user)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except UserFavoriteStore.DoesNotExist:
        return Response(
            {"detail": "Favorite store not found."},
            status=status.HTTP_404_NOT_FOUND
        )
