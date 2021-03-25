# # service\urls.py
# # import 

# from django.urls import path
# from . import views 

# urlpatterns = [
#     path('search_detail', views.search_detail, name="search_detail"),
#     path('search_show', views.search_show, name="search_show"),
#     path('sort_by_year', views.sort_by_year, name="sort_by_year"),
#     path('search_country_graph', views.search_country_graph, name="search_country_graph"),
#     path('search_country_graph_pop', views.search_country_graph_pop, name="search_country_graph_pop")

# ]


# service\urls.py
# import 

from django.urls import path
from . import views 

urlpatterns = [
    
    # GDP_graph
    path('search_main', views.search_main, name="search_main"),
    path('search_detail', views.search_detail, name="search_detail"),
    path('search_show', views.search_show, name="search_show"),
    path('sort_by_year', views.sort_by_year, name="sort_by_year"),
    path('search_country', views.search_country, name="search_country"),
    path('search_country_graph', views.search_country_graph, name="search_country_graph"),
    path('search_country_graph_pop', views.search_country_graph_pop, name="search_country_graph_pop")

]
