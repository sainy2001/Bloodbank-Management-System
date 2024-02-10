from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from BBMS_APP.models import custom_user, login_session, Bloodbank_System, Bloodbank_Details, Blood_Group_Details,Blood_Stuck_Details, Doctor_Details, Donor_Details



def login(request):
    if request.method == 'POST':
        user_email = request.POST.get('Email')
        user_password = request.POST.get('Password')
        try:
            user = custom_user.objects.get(email=user_email)
            name = user.user_name
            if user.password == user_password:
                # Create a LoginSession record to store login information
                login_session_instance = login_session(user=user)
                login_session_instance.save()

                # Set a session variable to mark the user as logged in
                request.session['user_email'] = user.email

                return redirect('home')
            else:
                messages.error(request, f"Password doesn't match.", extra_tags='password_login_error')
                return redirect('login')
        except ObjectDoesNotExist:
            messages.error(request, f"User with email {user_email} doesn't exist", extra_tags='user_login_error')
            return redirect('login')

    return render(request, 'login.html')



def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('Firstname')
        lastname = request.POST.get('Lastname')
        user_name = f"{firstname} {lastname}"

        user_email = request.POST.get('Email')
        user_phone = request.POST.get('Phone')
        password1 = request.POST.get('Password1')
        password2 = request.POST.get('Password2')

        user_records = custom_user.objects.all()

        email_exist = 'False'
        phone_exist = 'False'

        for db_email in user_records:
            if db_email.email == user_email:
                email_exist = 'True'
                break

        for db_phone in user_records:
            if db_phone.phone == user_phone:
                phone_exist = 'True'
                break

        if email_exist == 'True':
            messages.error(request, f"Email already exists.", extra_tags='email_error')
            return redirect('register')

        elif phone_exist == 'True':
            messages.error(request, f"Phone number already exists.", extra_tags='phone_error')
            return redirect('register')

        elif password1 != password2:
            messages.error(request, f"Password not same", extra_tags='password_error')
            return redirect('register')

        else:
            records = custom_user(user_name=user_name, email=user_email, phone=user_phone, password=password2)
            records.save()
            messages.success(request, f"successfully records submitted...", extra_tags='success_message')
            return redirect('login')

    return render(request, 'register.html')


def profile(request):
    if request.method == 'POST':
        if 'logout' in request.POST:  # Check if the "logout" button was clicked
            # Get the user's email from the session
            user_email = request.session.get('user_email', None)

            if user_email:
                try:
                    user = custom_user.objects.get(email=user_email)
                    # Get all login sessions associated with the user and update the logout time for each
                    user_login_sessions = login_session.objects.filter(user=user)
                    for user_login_session in user_login_sessions:
                        user_login_session.logout_time = timezone.now()
                        user_login_session.save()

                except custom_user.DoesNotExist:
                    pass  # Handle the case where the user does not exist

            # Clear the user's session to mark them as logged out
            request.session.clear()
            return redirect('index')  # Redirect to the login page

    user_email = request.session.get('user_email', None)
    if user_email:
        try:
            user = custom_user.objects.get(email=user_email)
            context = {
                'user_name': user.user_name,
                'user_email': user.email,
                'user_phone': user.phone,
            }
            return render(request, 'profile.html', context)
        except custom_user.DoesNotExist:
            return redirect('index')
    else:
        return redirect('index')


def bloodbankdetails(request):
    data = {}
    data1 = {}
    data2 = []
    get_name = ''
    if request.method == "POST":
        get_district = request.POST.get('District')
        get_name = request.POST.get('name')
        try:
            if get_district and get_district != "Select an option":
                db_district = Bloodbank_System.objects.get(district_name=get_district)
                bb_details = Bloodbank_Details.objects.filter(district=db_district)

                if bb_details.exists():
                    data = [
                        {
                            'name': detail.bloodbank_name,
                            'address': detail.address,
                            'mobile': detail.mobile,
                            'email': detail.email,
                        }
                        for detail in bb_details
                    ]
                else:
                    return HttpResponse(f'No blood banks found in {get_district}')

            elif get_name and get_name != "Select an option":
                bb_name = Bloodbank_Details.objects.get(bloodbank_name=get_name)
                bb_stuck_details = Blood_Stuck_Details.objects.filter(bloodbank=bb_name)

                if bb_stuck_details.exists():
                    data1 = [
                        {
                            'group_name': detail.blood_group.product_name,
                            'quantity': detail.quantity,
                            'amount': detail.amount,
                        }
                        for detail in bb_stuck_details
                    ]
                    print(data1)  # Add this line for debugging
                else:
                    return HttpResponse(f'No blood stock details found for {get_name}')
            else:
                print("Table-2: No name selected")  # Add this line for debugging

        except Bloodbank_System.DoesNotExist:
            return HttpResponse(f'District with name {get_district} does not exist.')
        except Bloodbank_Details.DoesNotExist:
            return HttpResponse(f'Blood bank details with name {get_name} does not exist.')
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')

    return render(request, 'bloodbankdetails.html', {'data': data, 'data1': data1, 'data2': get_name})


def get_bloodbank_options(request):
    selected_district = request.POST.get('District')
    try:
        if selected_district and selected_district != "Select an option":
            db_district = Bloodbank_System.objects.get(district_name=selected_district)
            bb_details = Bloodbank_Details.objects.filter(district=db_district)

            if bb_details.exists():
                options_data = [
                    {'value': detail.bloodbank_name, 'text': detail.bloodbank_name}
                    for detail in bb_details
                ]
                return JsonResponse(options_data, safe=False)
            else:
                return JsonResponse({'error': f'No blood banks found in {selected_district}'})
        else:
            return JsonResponse({'error': 'Invalid request'})
    except Bloodbank_System.DoesNotExist:
        return JsonResponse({'error': f'District with name {selected_district} does not exist.'})
    except Exception as e:
        return JsonResponse({'error': f'An error occurred: {str(e)}'})
    

def blooddetails(request):
    data1 = []
    blood_group_data = Blood_Group_Details.objects.all()
    if request.method == "POST":
        blood_name = request.POST.get('blood')
        try:
            blood_details = Blood_Group_Details.objects.filter(product_id=blood_name)
            if blood_details.exists():
                data1 = [
                    {
                        'product_name': detail.product_name,
                        'receive': detail.received_blood_from,
                        'donate': detail.donated_blood_to,
                    }
                    for detail in blood_details
                ]
            else:
                return HttpResponse(f'No blood group details found for {blood_name}')
        except Blood_Group_Details.DoesNotExist:
            return HttpResponse(f'Blood group details with ID {blood_name} does not exist.')
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')

    return render(request, 'blooddetails.html', {'blood_group_data': blood_group_data, 'data1': data1})


def doctordetails(request):
    data1 = []
    doctor = Doctor_Details.objects.all()

    if request.method == "POST":
        doctor_name = request.POST.get('doctor')
        try:
            doctor_details = Doctor_Details.objects.filter(doctorid=doctor_name)
            if doctor_details.exists():
                data1 = [
                    {
                        'doctor_name': detail.d_name,
                        'gender': detail.gender,
                        'specialization': detail.specialization,
                        'email': detail.email,
                        'phone': detail.phone,
                        'address': detail.address,
                    }
                    for detail in doctor_details
                ]
            else:
                return HttpResponse(f'No doctor details found for {doctor_name}')
        except Doctor_Details.DoesNotExist:
            return HttpResponse(f'Doctor details with ID {doctor_name} do not exist.')
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')

    return render(request, 'doctordetails.html', {'doctor': doctor, 'data1': data1})


def donordetails(request):
    data1 = []
    donor = Donor_Details.objects.all()

    if request.method == "POST":
        donor_name = request.POST.get('donor')
        try:
            donor_details = Donor_Details.objects.filter(donorid=donor_name)
            if donor_details.exists():
                data1 = [
                    {
                        'donor_name': detail.do_name,
                        'gender': detail.gender,
                        'bloodgroup': detail.blood_group,
                        'email': detail.email,
                        'phone': detail.phone,
                        'address': detail.address,
                    }
                    for detail in donor_details
                ]
            else:
                return HttpResponse(f'No doctor details found for {donor_name}')
        except Doctor_Details.DoesNotExist:
            return HttpResponse(f'Doctor details with ID {donor_name} do not exist.')
        except Exception as e:
            return HttpResponse(f'An error occurred: {str(e)}')

    return render(request, 'donordetails.html', {'donor': donor, 'data1': data1})


def index(request):
    return render(request, 'index.html')


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def blog(request):
    return render(request, 'blog.html')


def blog_single(request):
    return render(request, 'blog_single.html')


def contact(request):
    return render(request, 'contact.html')


def portfolio(request):
    return render(request, 'portfolio.html')


def portfolio_details(request):
    return render(request, 'portfolio_details.html')


def pricing(request):
    return render(request, 'pricing.html')


def services(request):
    return render(request, 'services.html')


def team(request):
    return render(request, 'team.html')


def testimonials(request):
    return render(request, 'testimonials.html')
