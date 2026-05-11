from django import forms
from .models import RepriseForm

class RepriseFormCreate(forms.ModelForm):
    DECISION_CHOICES = [
        ('medical_visit', 'Visite médicale requise'),
        ('direct_return', 'Reprise de poste directe'),
    ]
    
    decision_reprise = forms.ChoiceField(
        choices=DECISION_CHOICES, 
        widget=forms.RadioSelect,
        error_messages={'required': "Veuillez sélectionner une décision de reprise."}
    )

    class Meta:
        model = RepriseForm
        exclude = ['created_by', 'medical_visit_required', 'direct_return']
        widgets = {
            'date_absence_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_absence_fin': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 3}),
            'new_missions': forms.Textarea(attrs={'rows': 3}),
            'cons_other_details': forms.Textarea(attrs={'rows': 2, 'id': 'preciser_autre'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        
        debut = cleaned_data.get("date_absence_debut")
        fin = cleaned_data.get("date_absence_fin")
        if debut and fin and fin < debut:
            self.add_error('date_absence_fin', "La date de fin doit être supérieure ou égale à la date de début.")

        is_repetitive = cleaned_data.get("is_repetitive")
        frequency = cleaned_data.get("frequency")
        if is_repetitive and not frequency:
            self.add_error('frequency', "Veuillez sélectionner la fréquence de l'absence.")

        cons_other = cleaned_data.get("cons_other")
        other_details = cleaned_data.get("cons_other_details")
        if cons_other and not other_details:
            self.add_error('cons_other_details', "Veuillez préciser les autres conséquences.")

        consequences = ['cons_reorganization', 'cons_recruitment', 'cons_departure', 'cons_other']
        if not any(cleaned_data.get(field) for field in consequences):
            self.add_error(None, "Veuillez sélectionner au moins une conséquence.") # Non-field error

        actions = ['action_adjustment', 'action_training', 'action_reassignment', 'action_deskilling']
        if not any(cleaned_data.get(field) for field in actions):
            self.add_error(None, "Veuillez sélectionner au moins une mesure corrective.")

        return cleaned_data