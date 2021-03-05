from django.urls import include, path
# from . import views
from lab.views import * #HomePageView, UnidadListView
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('unidades', UnidadListView.as_view(), name='unidad-list'),
    # path('unidades', UnidadListView.as_view(), name='unidad-list'),
    # path('unidades', UnidadListView.as_view(), name='unidad-list'),
    # path('<int:pk>/', DetailView.as_view(), name='detail'),
    path('unidades/crear/', UnidadCreate.as_view(),name="unidad-create" ),
    path('unidades/<int:pk>/editar/', UnidadUpdate.as_view(),name="unidad-edit" ),
    path('unidades/<int:pk>/eliminar/', UnidadDelete.as_view(),name="unidad-delete" ),
    # path('<int:pk>/results/', views.ResultsView.as_view(), )
    path('pruebas', PruebaListView.as_view(), name='prueba-list'),
    path('pruebas/crear/', PruebaCreate.as_view(),name="prueba-create" ),
    path('pruebas/<int:pk>/editar/', PruebaUpdate.as_view(),name="prueba-edit" ),
    path('pruebas/<int:pk>/eliminar/', PruebaDelete.as_view(),name="prueba-delete" ),

    path('pacientes', PacienteListView.as_view(), name='paciente-list'),
    path('pacientes/crear/', PacienteCreate.as_view(),name="paciente-create" ),
    path('pacientes/<int:pk>/editar/', PacienteUpdate.as_view(),name="paciente-edit" ),
    path('pacientes/<int:pk>/eliminar/', PacienteDelete.as_view(),name="paciente-delete" ),


    path('ordenes', OrdenListView.as_view(), name='orden-list'),
    path('ordenes/crear/', OrdenCreate.as_view(),name="orden-create" ),
    path('ordenes/<int:pk>/editar/', OrdenUpdate.as_view(),name="orden-edit" ),
    path('ordenes/<int:pk>/eliminar/', OrdenDelete.as_view(),name="orden-delete" ),
    path("select2/", include("django_select2.urls")),
]
