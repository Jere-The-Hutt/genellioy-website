from django.shortcuts import render, redirect
from .forms import ContactForm
from .models import UserMessage
from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage

def index(request):
    form = ContactForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message_text = form.cleaned_data['message']

            # Save to database
            UserMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text
            )

            # Send email
            EmailMessage(
                subject=subject,
                body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message_text}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[email],
            ).send()

            messages.success(request, "Viesti lähetetty onnistuneesti!")
            return redirect('index')

        else:
            # Optional: helpful if honeypot triggers
            messages.error(request, "Lomakkeen lähetys epäonnistui.")

    return render(request, "core/index.html", {"form": form})
