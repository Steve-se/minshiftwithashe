from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import Subscribers
from django.template.loader import render_to_string 
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from django.shortcuts import redirect, render
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Subscribers 

from django.http import JsonResponse

def subscribe_to_newsletter(request):
    if request.method == 'POST':
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()

        if not email:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'Email is required!'}, status=400)
            messages.error(request, "Email is required!")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if Subscribers.objects.filter(email=email).exists():
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'This email already exists!'}, status=400)
            messages.error(request, "This email already exists!")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        subscriber = Subscribers(email=email, first_name=first_name, last_name=last_name)
        subscriber.save()

        unsubscribe_url = f"http://127.0.0.1:8000/unsubscribe?token={subscriber.unsubscribed_token}"

        context = {
            "email": email,
            "first_name": first_name,
            "unsubscribe_url": unsubscribe_url,
        }

        email_content = render_to_string('newsletter/subscription_email.html', context)
        subject = "Thank you for subscribing to our newsletter"
        sender_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        sent = send_mail(
            subject,
            '',
            sender_email,
            recipient_list,
            html_message=email_content,
            fail_silently=False
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'message': 'Successfully subscribed!'}, status=200)

        if sent:
            messages.success(request, "Successfully subscribed!")
        else:
            messages.error(request, "Failed to send subscription email. Please try again.")

        return redirect(request.META.get('HTTP_REFERER', '/'))

    return redirect(request.META.get('HTTP_REFERER', '/'))



def unsubscribe(request):
    token = request.GET.get('token')
    if not token:
        return HttpResponse("Invalid unsubscribe request", status=400)
    try:
        subscriber = Subscribers.objects.get(unsubscribed_token=token)
        subscriber.subscribed = False
        subscriber.save()
        return HttpResponse("You have successfully unsubscribed from the newsletter.")
        # OR:
        # return redirect('home')  # or any thank-you page
    except Subscribers.DoesNotExist:
        return HttpResponse("Unsubscribe link is invalid or expired.", status=404)
