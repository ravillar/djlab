from django.urls import path, include
from django.urls import reverse_lazy
# from . import views
from lab.views import * #HomePageView, UnidadListView
from django.contrib.auth import views as auth_views

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

    path('login/', auth_views.LoginView.as_view(),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(),  name='logout'),
    path('changepass/', changepass,  name='changepass'),
    # path('change-password/', auth_views.PasswordChangeView.as_view(), name='change-password'),
    # path('password_change/done/', auth_views.PasswordChangeView.as_view(), name='password_change_done'),
    path("register/", register, name="register"),

]
