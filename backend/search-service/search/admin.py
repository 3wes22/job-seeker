from django.contrib import admin
from .models import SearchIndex, SearchHistory, SearchAnalytics


@admin.register(SearchIndex)
class SearchIndexAdmin(admin.ModelAdmin):
    list_display = ('entity_type', 'entity_id', 'created_at', 'updated_at')
    list_filter = ('entity_type', 'created_at')
    search_fields = ('entity_id',)
    ordering = ('-created_at',)


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'query', 'results_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('query', 'user_id')
    ordering = ('-created_at',)


@admin.register(SearchAnalytics)
class SearchAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('query', 'search_count', 'last_searched_at', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('query',)
    ordering = ('-search_count',) 