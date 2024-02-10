from django.contrib import admin
from BBMS_APP.models import custom_user, login_session, Bloodbank_System, Bloodbank_Details, Blood_Group_Details, \
    Blood_Stuck_Details, Doctor_Details, Donor_Details


# Register your models here.

#  Here we declare which attributes/fields will be shown in admin page
class UserData(admin.ModelAdmin):
    list_display = ('user_name', 'email', 'phone', 'password', 'timestamp')


class LoginData(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time')


class bbms(admin.ModelAdmin):
    list_display = ('district_id', 'district_name')


class bbms_details(admin.ModelAdmin):
    list_display = ('bloodbank_id', 'district_id', 'bloodbank_name', 'bloodbank_address', 'mobile_number', 'email_id')


class BloodGroup_Details(admin.ModelAdmin):
    list_display = ('product_id', 'product_name', 'donated_blood_to', 'received_blood_from')


class BloodStuck_Details(admin.ModelAdmin):
    list_display = ('blood_group', 'bloodbank', 'quantity', 'amount')


class DoctorDetails(admin.ModelAdmin):
    list_display = ('doctorid', 'd_name', 'gender', 'specialization', 'email', 'phone', 'address')
    

class DonorDetails(admin.ModelAdmin):
    list_display = ('donorid', 'do_name', 'gender', 'blood_group', 'email', 'phone', 'address')


# Here registered site will be show in database
admin.site.register(custom_user)
admin.site.register(login_session)
admin.site.register(Bloodbank_System)
admin.site.register(Bloodbank_Details)
admin.site.register(Blood_Group_Details)
admin.site.register(Blood_Stuck_Details)
admin.site.register(Doctor_Details)
admin.site.register(Donor_Details)
