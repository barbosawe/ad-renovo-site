from django.contrib import admin

from .models import AlunoCollege, Aula

@admin.register(AlunoCollege)
class AlunoCollegeAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_ativo', 'id_assinatura']
    list_filter = ['is_ativo']
    search_fields = ['user__username', 'user__email', 'id_assinatura']

@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'data_publicacao', 'ordem']
    ordering = ['ordem', 'data_publicacao']
