from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
from django.utils.translation import gettext_lazy as _


class SearchIndex(models.Model):
    """
    Search index for full-text search across different entities.
    This model stores searchable content from other services.
    """
    
    ENTITY_TYPE_CHOICES = [
        ('job', _('Job')),
        ('company', _('Company')),
        ('user', _('User')),
    ]
    
    entity_type = models.CharField(max_length=50, choices=ENTITY_TYPE_CHOICES, help_text=_("Type of entity being indexed"))
    entity_id = models.BigIntegerField(help_text=_("ID of the entity from the source service"))
    search_vector = SearchVectorField(blank=True, help_text=_("Full-text search vector"))
    metadata = models.JSONField(default=dict, blank=True, help_text=_("Additional metadata for search"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Search Index')
        verbose_name_plural = _('Search Indexes')
        db_table = 'search_indexes'
        unique_together = ('entity_type', 'entity_id')
        indexes = [
            GinIndex(fields=['search_vector']),
            models.Index(fields=['entity_type', 'entity_id']),
        ]
    
    def __str__(self):
        return f"{self.entity_type} - {self.entity_id}"


class SearchHistory(models.Model):
    """
    Search history for analytics and user experience improvements.
    """
    
    user_id = models.BigIntegerField(help_text=_("User ID from user-service"))
    query = models.TextField(help_text=_("Search query"))
    filters = models.JSONField(default=dict, blank=True, help_text=_("Applied filters"))
    results_count = models.IntegerField(blank=True, null=True, help_text=_("Number of results returned"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Search History')
        verbose_name_plural = _('Search Histories')
        db_table = 'search_history'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id', 'created_at']),
            models.Index(fields=['query']),
        ]
    
    def __str__(self):
        return f"Search by User {self.user_id}: {self.query[:50]}..."


class SearchAnalytics(models.Model):
    """
    Analytics data for search queries and patterns.
    """
    
    query = models.TextField(help_text=_("Search query"))
    search_count = models.IntegerField(default=1, help_text=_("Number of times this query was searched"))
    last_searched_at = models.DateTimeField(auto_now=True, help_text=_("Last time this query was searched"))
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Search Analytics')
        verbose_name_plural = _('Search Analytics')
        db_table = 'search_analytics'
        unique_together = ('query',)
        ordering = ['-search_count']
        indexes = [
            models.Index(fields=['query']),
            models.Index(fields=['search_count']),
        ]
    
    def __str__(self):
        return f"{self.query} - {self.search_count} searches" 