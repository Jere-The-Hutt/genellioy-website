from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import UserMessage
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail

def index(request):
    form = ContactForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message_text = form.cleaned_data['message']

            # Save to database
            UserMessage.objects.create(
                name=name,
                email=email,
                message=message_text
            )

            # Send email
            send_mail(
                f'New contact from {name}',
                message_text,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Viesti lähetetty onnistuneesti!")
            return redirect('index')

        else:
            # Optional: helpful if honeypot triggers
            messages.error(request, "Lomakkeen lähetys epäonnistui.")

    return render(request, "core/index.html", {"form": form})
