from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.core.validators import RegexValidator

# class UserRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username', 'email', 'password', 'confirm_password']


#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         user.role = 'user'
#         if commit:
#             user.save()
#         return user

# class MechanicRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username', 'email', 'password', 'confirm_password']


#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         user.role = 'mechanic'
#         if commit:
#             user.save()
#         return user

# class CarRenterRegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput)
#     confirm_password = forms.CharField(widget=forms.PasswordInput)

#     class Meta:
#         model = User
#         fields = ['first_name','last_name','username', 'email', 'password', 'confirm_password']

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")
#         return cleaned_data

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data['password'])
#         user.role = 'car_renter'
#         if commit:
#             user.save()
#         return user
    
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('user', 'User'), ('mechanic', 'Mechanic'), ('car_renter', 'Car Renter'),('fuels','Fuels')])

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password', 'role']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user
    

class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.role = "admin"
        user.is_staff = True
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class MechanicProfileForm(forms.ModelForm):
    location = forms.ModelChoiceField(queryset=Location.objects.all(), required=True)
    SPECIALIZATION_CHOICES = [
        ("two_wheeler", "Two Wheeler"),
        ("four_wheeler", "Four Wheeler"),
        ("heavy_vehicle", "Heavy Vehicle"),
    ]
    specialized_in = forms.ChoiceField(choices=SPECIALIZATION_CHOICES)
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  # Example: Matches numbers like +1234567890 or 1234567890
        message="Enter a valid phone number (e.g., +1234567890 or 1234567890)."
    )
    phone = forms.CharField(
        max_length=10,
        validators=[phone_validator],  
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = MechanicProfile
        fields = ['name','location', 'phone', 'dob', 'skills', 'experience', 'specialized_in', 'bio', 'profile_pic']


class AddLocationForm(forms.ModelForm):
    class Meta:
        model=Location
        fields=['name',]


class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  # Example: Matches numbers like +1234567890 or 1234567890
        message="Enter a valid phone number (e.g., +1234567890 or 1234567890)."
    )
    phone = forms.CharField(
        max_length=10,
        validators=[phone_validator],  
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    class Meta:
        model = UserProfile
        fields = ['name', 'address', 'phone', 'dob', 'profile_pic']


class ReqToMechanicForm(forms.ModelForm):
    class Meta:
        model = ReqToMechanic
        fields = ['discription', 'location','latitude','longtitude','address','link']

    
class FeedBackForm(forms.ModelForm):
    class Meta:
        model = FeedBack
        fields = ['text', 'rating']

class BillPaymentForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = ['payment']

class UserPaymentForm(forms.ModelForm):
    class Meta:
        model = UserPayment
        fields = ['acholdername','accno','cvv','exp','amount']

class MechanicSearchForm(forms.Form):
    mechanic = forms.CharField(max_length=30, required=False)



class ChangePasswordForm(forms.Form):
    current_password=forms.CharField(max_length=50,label="current password",widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control"}))
    new_password=forms.CharField(max_length=50,label="new password",widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control"}))
    confirm_password=forms.CharField(max_length=50,label="confirm password",widget=forms.PasswordInput(attrs={"placeholder":"Password","class":"form-control"}))


class FuelForm(forms.ModelForm):
    class Meta:
        model = Fuel
        exclude = ['user']
        


class ReqFuelForm(forms.ModelForm):
    class Meta:
        model = ReqFuel
        fields = ['phone', 'latitude', 'longitude', 'address', 'link','quantity','user','fuel']

    def __init__(self, *args, **kwargs):
        super(ReqFuelForm, self).__init__(*args, **kwargs)

class PaymentFuelForm(forms.ModelForm):
    class Meta:
        model = UserPaymentFuel
        exclude =['customer','req','fuel']
        
        
class OrderForm(forms.ModelForm):
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  # Example: Matches numbers like +1234567890 or 1234567890
        message="Enter a valid phone number (e.g., +1234567890 or 1234567890)."
    )
    
    class Meta:
        model = Order
        fields = ['address', 'phone']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }
    phone = forms.CharField(
        max_length=10,
        validators=[phone_validator],  
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
        
class OrderPaymentForm(forms.ModelForm):
    class Meta:
        model = OrderPayment
        fields = ['account_holder_name', 'account_number', 'cvv', 'expiry_date']
        widgets = {
            'account_holder_name': forms.TextInput(attrs={'class': 'form-control'}),
            'account_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'cvv': forms.NumberInput(attrs={'class': 'form-control', 'maxlength': '3'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YYYY'}),
        }