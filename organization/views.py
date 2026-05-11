from django.contrib.auth.decorators import login_required
from django.shortcuts import render , redirect
from .models import RepriseForm,Collaborateur
from django.db.models import Q,Value
from django.db.models.functions import Concat
from django.http import JsonResponse
from datetime import datetime
from django.contrib import messages
from django.views.decorators.http import require_POST


@login_required
def superadmin_dashboard(request):
    if request.user.role!='SUPERADMIN':
        return redirect('forbidden')
    
    return render(request,'organization/superadmin/dashboard.html')

@login_required
def hrbp_home(request):
    if request.user.role!='HRBP':
        return redirect('forbidden')
    
    return render(request,'organization/hrbp/home.html')


@login_required
def manager_home(request):
    if request.user.role != 'NPLUS1':
        return redirect('forbidden')
    
  
    my_forms = RepriseForm.objects.filter(
        created_by__corporate_id=request.user.corporate_id
    ).select_related(
        'collaborateur__poste__uep__manager', 
        'collaborateur__poste__uep__dpt__hrbp'
    ).annotate(
        full_name=Concat(
            'collaborateur__first_name',Value(' '),'collaborateur__family_name'
        )
    )


    search= request.GET.get('search')

    if search:

        words = search.strip().split()

        for word in words:
        
            my_forms=my_forms.filter(
                Q(full_name__icontains=word) |
                Q(collaborateur__corporate_id__icontains=word)
            )

    my_forms=my_forms.order_by('-created_at')
        
    
    context = {
        'my_forms': my_forms,
        'total_forms': my_forms.count(),
        'maladie_count': my_forms.filter(type_absence='MALADIE').count(),
    }
    
    return render(request, 'organization/manager/home.html', context)





def form_detail(request,pk):
    form=RepriseForm.objects.get(pk=pk)
    return render(request,'organization/manager/form_detail.html',{'form':form})




# def add_form(request):

#     collaborateurs = Collaborateur.objects.select_related(
#         'poste__uep__manager'
#     ).filter(
#         poste__uep__manager__corporate_id=request.user.corporate_id
#     )

#     if request.method == 'POST':

#         collab_id = request.POST.get('collaborateur_id')

#         date_debut = request.POST.get('date_absence_debut')
#         date_fin = request.POST.get('date_absence_fin')

#         type_absence = request.POST.get('type_absence')
#         reason = request.POST.get('reason')

#         is_repetitive = request.POST.get('is_repetitive') == 'on'
#         frequency = request.POST.get('frequency')

#         cons_reorganization = request.POST.get('cons_reorganization') == 'on'
#         cons_recruitment = request.POST.get('cons_recruitment') == 'on'
#         cons_departure = request.POST.get('cons_departure') == 'on'

#         cons_other = request.POST.get('cons_other') == 'on'
#         cons_other_details = request.POST.get('cons_other_details')

#         action_adjustment = request.POST.get('action_adjustment') == 'on'
#         action_training = request.POST.get('action_training') == 'on'
#         action_reassignment = request.POST.get('action_reassignment') == 'on'
#         action_deskilling = request.POST.get('action_deskilling') == 'on'

#         new_missions = request.POST.get('new_missions')

#         decision_reprise = request.POST.get('decision_reprise')

#         medical_visit_required = (
#             decision_reprise == 'medical_visit'
#         )

#         direct_return = (
#             decision_reprise == 'direct_return'
#         )

#         errors = {}

#         if not type_absence:
#             errors['type_absence']="Le type d'absence est obligatoire."
            

#         if not reason:
#             errors['reason']="Le motif de l'absence est obligatoire."


#         if date_debut and date_fin:

#             date_debut_obj = datetime.strptime(
#                 date_debut,
#                 '%Y-%m-%d'
#             ).date()

#             date_fin_obj = datetime.strptime(
#                 date_fin,
#                 '%Y-%m-%d'
#             ).date()

#             if date_fin_obj < date_debut_obj:

#                 errors['date']="La date de fin doit être supérieure ou égale à la date de début."
              

#         if is_repetitive and not frequency:

#             errors['repetitive']="Veuillez sélectionner la fréquence de l'absence."
        

#         if cons_other and not cons_other_details:

#             errors['cons_other']="Veuillez préciser les autres conséquences."
            

#         if not (
#             cons_reorganization or
#             cons_recruitment or
#             cons_departure or
#             cons_other
#         ):
#             errors['consequences']="Veuillez sélectionner au moins une conséquence."

#         if not (
#             action_adjustment or
#             action_training or
#             action_reassignment or
#             action_deskilling
#         ):
#             errors['actions']="Veuillez sélectionner au moins une mesure corrective."

#         if not (
#             medical_visit_required or
#             direct_return
#         ):
#             errors['conclusion']="Veuillez sélectionner une décision de reprise."

    

#         if errors:
#             return render(
#                 request,
#                 'organization/manager/add_form.html',
#                 {
#                     'collaborateurs': collaborateurs,
#                     'errors': errors
#                 }
#             )

#         collaborateur = Collaborateur.objects.get(
#             corporate_id=collab_id
#         )

#         RepriseForm.objects.create(

#             collaborateur=collaborateur,
#             created_by=request.user,

#             date_absence_debut=date_debut,
#             date_absence_fin=date_fin,

#             type_absence=type_absence,
#             reason=reason,

#             is_repetitive=is_repetitive,
#             frequency=frequency,

#             cons_reorganization=cons_reorganization,
#             cons_recruitment=cons_recruitment,
#             cons_departure=cons_departure,
#             cons_other=cons_other,
#             cons_other_details=cons_other_details,

#             action_adjustment=action_adjustment,
#             action_training=action_training,
#             action_reassignment=action_reassignment,
#             action_deskilling=action_deskilling,
#             new_missions=new_missions,

#             medical_visit_required=medical_visit_required,
#             direct_return=direct_return,
#         )

        

#         return redirect('manager_dashboard')

#     return render(
#         request,
#         'organization/manager/add_form.html',
#         {
#             'collaborateurs': collaborateurs
#         }
#     )

from .forms import RepriseFormCreate

@login_required
def add_form(request):
    collaborateurs = Collaborateur.objects.filter(
        poste__uep__manager__corporate_id=request.user.corporate_id
    ).select_related('poste__uep__manager')

    if request.method == 'POST':
        form = RepriseFormCreate(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            
            decision = form.cleaned_data.get('decision_reprise')
            instance.medical_visit_required = (decision == 'medical_visit')
            instance.direct_return = (decision == 'direct_return')
            
            instance.save()
            messages.success(request, "Formulaire enregistré avec succès.")
            return redirect('manager_dashboard')
    else:
        form = RepriseFormCreate()



    return render(request, 'organization/manager/add_form.html', {
        'form': form,
        'collaborateurs': collaborateurs
    })




    


def get_collab_info(request, collab_id):
    collab = Collaborateur.objects.select_related(
        'poste__uep__dpt__hrbp', 
        'poste__uep__manager'
    ).get(corporate_id=collab_id)

    data = {
        'first_name': collab.first_name,
        'family_name': collab.family_name,
        'matricule': collab.matricule,
        'corporate_id': collab.corporate_id,
        'departement': collab.poste.uep.dpt.name,
        'poste_title': collab.poste.title,
        'manager': f"{collab.poste.uep.manager.first_name} {collab.poste.uep.manager.last_name}",
        'hrbp': f"{collab.poste.uep.dpt.hrbp.first_name} {collab.poste.uep.dpt.hrbp.last_name}"
    }

    return JsonResponse(data)




@login_required
@require_POST
def delete_form(request,id):
    form=RepriseForm.objects.get(pk=id)
    form.delete()
    messages.success(request,"Le formulaire a été supprimé avec succès.")
    return redirect('manager_dashboard')













def access_denied(request):
    return render(request, 'organization/errors/forbidden.html')
