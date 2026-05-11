from django.contrib import admin
from .models import DPT, UEP, Poste, Collaborateur, RepriseForm

@admin.register(DPT)
class DPTAdmin(admin.ModelAdmin):
    list_display = ('name', 'hrbp')

@admin.register(UEP)
class UEPAdmin(admin.ModelAdmin):
    list_display = ('name', 'dpt', 'manager')

@admin.register(Poste)
class PosteAdmin(admin.ModelAdmin):
    list_display = ('title', 'uep')

@admin.register(Collaborateur)
class CollaborateurAdmin(admin.ModelAdmin):
    list_display = ('first_name','family_name', 'corporate_id', 'matricule', 'poste')
    search_fields = ('corporate_id', 'name')


admin.site.register(RepriseForm)