
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect,HttpResponse,redirect
from .models import Donation
from .generate_pdf import generate_certificate
from django.core.mail import EmailMessage   
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.db.models import Sum
from django.core.paginator import Paginator


from django.contrib.auth.models import User,Group
from django.contrib.auth import login
from .forms import SetUsernameAndPasswordForm,UserForm
from django.contrib import messages


from .models import Donation,PendingGroupRequest
# Create your views here.


razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID , settings.RAZORPAY_SECRET_KEY))

def home(request):
    return render(request,'index.html')


def donate(request):
    if request.method == "POST":
        donor_name = request.POST.get('name')
        email = request.POST.get('email')
        amount = float(request.POST.get('amount')) * 100  # Convert to paisa (Razorpay's unit)

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount": int(amount),  # Amount in paisa
            "currency": "INR",
            "payment_capture": "1"  # Auto-capture
        })

        # Save donation details
        donation = Donation.objects.create(
            donor_name=donor_name,
            email=email,
            amount=amount / 100,  # Save in rupees
            payment_id=razorpay_order['id']
        )

        # Pass order details to the template
        context = {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount,
            'donor_name': donor_name,
            'email': email,
        }
        return render(request, 'payment.html', context)
    pdf_buffer = generate_certificate("amit", 5000)

    # Create the email
    subject = "Thank You for Your Donation!"
    message = f"Dear Amit,\n\nThank you for your generous donation of ₹500.\nPlease find attached your certificate of appreciation.\n\nBest regards,\nNGO Team"
    email = EmailMessage(
        subject,
        message,
        'kamit896837@gmail.com',  # Sender email
        ["kamit896837@outlook.com"],         # Recipient email
    )

    # Attach the certificate
    email.attach("Certificate_amit.pdf", pdf_buffer.getvalue(), 'application/pdf')
    email.send()
 
    return render(request, 'donate.html')

def payment_success(request,pay_id):

        # Update donation statu
        messages.success(request, "Your payemnt is successful was successful!")

        return redirect('home')







def request_group_membership(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        
            subject = "Thank You for Registration for Volunteer"
            message = f"Dear f{request.POST.get('name')},\n\nThank for showing interset in our volunteer group we will provide.\n \n We will notify you through email after you application reviewed by our team \n \n Thank you"
            email = EmailMessage(
                subject,
                message,
                'kamit896837@gmail.com',  # Sender email
                [request.POST.get("email")],         # Recipient email
                 )

            email.send()
            messages.success(request,"You have successfully registered for our Volunter.Our Team will verify your detail")
            return redirect('home')
    form = UserForm()
    return render(request, "request_group.html", {"groups": form})

