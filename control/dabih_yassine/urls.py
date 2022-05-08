from django.urls import path, re_path
from . import views
urlpatterns = [
##list_data
path('home', views.index, name='home'),
path('', views.login_page, name='login'),
path('client', views.clients_list , name='client'),
path('client/search', views.client_search,name='client_search'),
path('compte', views.comptes_list , name='compte'),
path('compte/search', views.compte_search,name='compte_search'),
path('operation', views.operations_list , name='operation'),
path('operation/search', views.operation_search,name='operation_search'),
path('client/details/<int:id>', views.client_details),
path('client/details/<str:mot>', views.client_details_via_nom),
path('client/operation/<int:id>', views.operation_client),
##forms
path('client/add', views.client_forms_add , name='client_forms_add'),
path('compte/add', views.compte_forms_add , name='compte_forms_add'),
path('operation/add', views.operation_forms_add , name='operation_forms_add'),
path('recherche_via_date', views.recherche_form, name='recherche_via_date'),
path('recherche_via_date/result', views.recherche_forms, name='recherche_forms'),
##suppression
path('client/<int:id>', views.client_delete),
path('compte/<int:id>', views.compte_delete),
path('operation/<int:id>', views.operation_delete),

]