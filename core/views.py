from django.shortcuts import render, redirect
from .forms import ContactForm
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from .models import UserMessage  # <-- import the model

def index(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        message_text = form.cleaned_data['message']
        
        # Save to the database
        UserMessage.objects.create(
            name=name,
            email=email,
            message=message_text
        )
        
        # Send email (for now use console backend)
        send_mail(
            f'New contact from {name}',
            message_text,
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

        messages.success(request, "Viesti lähetetty onnistuneesti!")
        return redirect('index')  # <-- Redirect after POST

    return render(request, "core/index.html", {"form": form})
