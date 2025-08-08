from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import SearchIndex, SearchHistory, SearchAnalytics


@api_view(['GET'])
@permission_classes([AllowAny])
def search(request):
    """Search across different entities"""
    query = request.GET.get('q', '')
    entity_type = request.GET.get('type', '')
    
    if not query:
        return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Create search query
    search_query = SearchQuery(query, config='english')
    
    # Filter by entity type if specified
    queryset = SearchIndex.objects.filter(search_vector=search_query)
    if entity_type:
        queryset = queryset.filter(entity_type=entity_type)
    
    # Rank results
    queryset = queryset.annotate(rank=SearchRank('search_vector', search_query)).order_by('-rank')
    
    # Limit results
    results = queryset[:50]
    
    # Save search history if user is authenticated
    if request.user.is_authenticated:
        SearchHistory.objects.create(
            user_id=request.user.id,
            query=query,
            filters={'type': entity_type} if entity_type else {},
            results_count=len(results)
        )
    
    # Update search analytics
    analytics, created = SearchAnalytics.objects.get_or_create(query=query)
    if not created:
        analytics.search_count += 1
        analytics.save()
    
    return Response({
        'query': query,
        'results': [{'entity_type': item.entity_type, 'entity_id': item.entity_id, 'rank': item.rank} for item in results],
        'total_results': len(results)
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_history(request):
    """Get search history for the current user"""
    history = SearchHistory.objects.filter(user_id=request.user.id).order_by('-created_at')[:20]
    return Response([{
        'query': item.query,
        'filters': item.filters,
        'results_count': item.results_count,
        'created_at': item.created_at
    } for item in history])


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_analytics(request):
    """Get search analytics"""
    analytics = SearchAnalytics.objects.order_by('-search_count')[:20]
    return Response([{
        'query': item.query,
        'search_count': item.search_count,
        'last_searched_at': item.last_searched_at
    } for item in analytics]) 