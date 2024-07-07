from django.shortcuts import render, redirect
from .forms import SupportTicketForm

def contact_admin(request):
    if request.method == 'POST':
        form = SupportTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')  # Redirect to the success page after form submission
    else:
        form = SupportTicketForm()
    return render(request, 'support.html', {'form': form})

def success(request):
    return render(request, 'success.html')
