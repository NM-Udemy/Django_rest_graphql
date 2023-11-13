from django_filters import FilterSet, CharFilter
from .models import Post

class PostFilter(FilterSet):
    title_sw = CharFilter(field_name='title', lookup_expr='startswith')    
    title_ew = CharFilter(field_name='title', lookup_expr='endswith')
    title_ct = CharFilter(field_name='title', lookup_expr='contains')
    content = CharFilter(field_name='content', method='filter_for_content')
    
    class Meta:
        model = Post
        fields = ['title',]

    def filter_for_content(self, queryset, name, value):
        return queryset.filter(comments__comment__contains=value)
