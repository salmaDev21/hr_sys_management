from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def redirect_by_role(request):
    role=request.user.role

    if role == 'SUPERADMIN':
        return redirect('superadmin_dashboard')
    elif role=='HRBP':
        return redirect('hrbp_dashboard')
    else :
        return redirect('manager_dashboard')
    