
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


from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import SetUsernameAndPasswordForm
from django.contrib import messages


from .models import Donation
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
        messages.success(request, "Your action was successful!")

        return redirect('home')



def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:  # Ensures only staff/admin users can log in
                login(request, user)
                return redirect('admin_dashboard')  # Redirect to the dashboard
            else:
                messages.error(request, "You are not authorized to access this page.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    
    total_users = User.objects.count()
    users = User.objects.all()


    # Set how many users to display per page
    paginator = Paginator(users, 2)  # Show 10 users per page

    # Get the current page number from the request
    page_number = request.GET.get('page')
    
    # Get the users for the current page
    page_obj = paginator.get_page(page_number)

    total_donations = Donation.objects.aggregate(total_amount=Sum('amount'))
    total_amount = total_donations['total_amount'] or 0
    return render(request, 'admin.html',{'total_amount': total_amount,"users_total":total_users,"users":users,'page_obj': page_obj})

@login_required
def admin_dashboard_donations(request):
    if not request.user.is_staff:
        return redirect('admin_login')
    
  

    donations = Donation.objects.all()

    paginator = Paginator(donations, 10)  # Show 10 donations per page

    # Get the current page number from the request
    page_number = request.GET.get('page')

    # Get the donations for the current page
    page_obj = paginator.get_page(page_number)
    return render(request, 'donations.html',{'page_obj': page_obj})



def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def set_username_and_password(request):
    if request.method == "POST":
        form = SetUsernameAndPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = request.user

            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                form.add_error('username', 'This username is already taken.')
            else:
                user.username = username
                user.set_password(password)  # Save password securely
                user.save()

                # Re-login the user since the password has changed
                login(request, user)
                return redirect('home')  # Redirect to your desired page
    else:
        form = SetUsernameAndPasswordForm()
    
    return render(request, 'set_username_and_password.html', {'form': form})

