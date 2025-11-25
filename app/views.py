from django.shortcuts import render
from django.views.generic import *
from .forms import *
from .models import *
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from .models import Product  # or whatever your product model is called
# Create your views here.


class HomeView(TemplateView):
    template_name="home.html"

class AdminRegistrationView(CreateView):
    model = User
    form_class = AdminRegistrationForm
    template_name = 'Admin_register.html'
    success_url = reverse_lazy('admin-login')

    def form_valid(self, form):
        return super().form_valid(form)


class RegistrationView(CreateView):
    model = User
    form_class = RegistrationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Additional processing can be done here if needed
        form.instance.role = form.cleaned_data['role']
        return super().form_valid(form)
    
    def get_success_url(self):
        return self.success_url

class AdminHomeView(TemplateView):
    template_name="admin_home.html"


class UserHomeView(TemplateView):
    template_name="user_home.html"

class MechnaicHomeView(TemplateView):
    template_name="mechanic_home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except MechanicProfile.DoesNotExist:
            pass
        return context


class AdminLoginView(FormView):
    template_name = 'admin_login.html'
    form_class = LoginForm
    success_url = reverse_lazy('admin-home')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser == 1:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid username or password for admin.')
            return self.form_invalid(form)

    def get_success_url(self):
        return self.success_url

class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            if user.role == 'mechanic':
                return redirect('mechanic_home')
            elif user.role == 'car_renter':
                return redirect('car_home')
            elif user.role == 'fuels':
                return redirect('fuel')
            else:
                return redirect('user_home')
        else:
            messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)
    
    
def LogoutView(request,*args,**kwargs):
    logout(request)
    return redirect("home")  


class AddLocationView(CreateView):
    model=Location
    form_class=AddLocationForm
    template_name="add_location.html"
    success_url=reverse_lazy('add-locations')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loc']=Location.objects.all()
        return context

def locationdelete(request,**kwargs):
    id=kwargs.get('pk')
    loc=Location.objects.get(id=id)
    loc.delete()
    return redirect('add-locations')

class MechanicProfileAddView(CreateView):
    model = MechanicProfile
    form_class = MechanicProfileForm
    template_name = 'mechanic_profile_add.html'
    success_url = reverse_lazy('mechanic_home')

    # def get_object(self, queryset=None):
    #     return MechanicProfile.objects.filter(user=self.request.user).first()

    def form_valid(self, form):
        print("hii")
        form.instance.user = self.request.user
        return super().form_valid(form) 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['location']=Location.objects.all()
        mech=MechanicProfile.SPECIALIZATION_CHOICES
        print(mech)
        context['mech']=mech
        return context
    

class MechanicProfileDetailView(DetailView):
    model = MechanicProfile
    template_name = 'mechanic_profile_view.html'
    context_object_name = 'data'
    success_url = reverse_lazy('mechanic_home')

    def get_object(self, queryset=None):
        # Retrieve the MechanicProfile object for the current user
        try:
            return get_object_or_404(MechanicProfile, user=self.request.user)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            return redirect('mechanic_home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
            return context
        except MechanicProfile.DoesNotExist:
            pass
            return context


class PendingMechanicView(ListView):
    model = MechanicProfile
    template_name = 'pending_mechanics_list.html'  # Replace 'pending_mechanics_list.html' with your actual template name
    context_object_name = 'data'

    def get_queryset(self):
        return MechanicProfile.objects.filter(status='pending')

class AdminAllMechanicView(ListView):
    model = MechanicProfile
    template_name = 'admin_mech_view.html'  
    context_object_name = 'data_mech'

    def get_queryset(self):
        return MechanicProfile.objects.all()
    

def approve_mechanic(request, pk):
    mechanic_profile = get_object_or_404(MechanicProfile, pk=pk)
    if request.method == 'POST':
        mechanic_profile.status = 'approved'
        mechanic_profile.save()
        return redirect('all-mech')  
    return redirect('pending-list')

def approve_mechanics(request, pk):
    mechanic_profile = get_object_or_404(MechanicProfile, pk=pk)
    mechanic_profile.status = 'approved'
    mechanic_profile.save()
    return redirect('all-mech')  


def reject_mechanic(request, pk):
    mechanic_profile = get_object_or_404(MechanicProfile, pk=pk)
    mechanic_profile.status = 'rejected'
    mechanic_profile.save()
    return redirect('all-mech')  


class MechanicprofileUpdateView(UpdateView):
    model = MechanicProfile
    form_class = MechanicProfileForm
    template_name = 'mechanic_profile_update.html'
    success_url = reverse_lazy('mechanic_home')

    def get_object(self, queryset=None):
        try:
            return MechanicProfile.objects.get(user=self.request.user)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except MechanicProfile.DoesNotExist:
            pass
        return context


class UserProfileAddView(CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile_add.html'
    success_url = reverse_lazy('user_home')

    def get_object(self, queryset=None):
        return UserProfile.objects.filter(user=self.request.user).first()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form) 
    

class UserProfileDetailView(DetailView):
    model = UserProfile
    template_name = 'user_profile_view.html'
    context_object_name = 'data'

    def get_object(self, queryset=None):
        try:
            return get_object_or_404(UserProfile, user=self.request.user)
        except:
             messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=UserProfile.objects.get(user=self.request.user.id)
        except UserProfile.DoesNotExist:
           pass
        return context

    
class UserProfileUpdateView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'user_profile_update.html'
    success_url = reverse_lazy('user_home')

    def get_object(self, queryset=None):
        return UserProfile.objects.get(user=self.request.user)
    
class ApprovedMechanicListView(TemplateView):
    template_name = 'approved_mechanic.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        
        if search_query:
            context['mechanics'] = MechanicProfile.objects.filter(
                status='approved',
                location__name__icontains=search_query  
            )
        else:
            context['mechanics'] = MechanicProfile.objects.filter(status='approved')
        context['search_query'] = search_query        
        return context

class ReqToMechanicCreateView(CreateView):
    model = ReqToMechanic
    form_class = ReqToMechanicForm
    template_name = 'create_req.html'
    success_url = reverse_lazy('user_requests')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mechanic_id = self.kwargs.get('mechanic_id')
        context['mech']=MechanicProfile.objects.get(id=mechanic_id)
        context['location']=Location.objects.all()
        return context
    def form_valid(self, form):
        try:
            mechanic_id = self.kwargs.get('mechanic_id')
            mechanic = MechanicProfile.objects.get(pk=mechanic_id)
            form.instance.mechanic = mechanic
            # form.instance.user = self.request.user.userprofile
            form.instance.user = self.request.user.user_profile
            form.instance.phone=self.request.user.user_profile.phone
            return super().form_valid(form)
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            return redirect('create_req',mechanic_id=mechanic_id)
       
    

class MechanicReqListView(ListView):
    model = ReqToMechanic
    template_name = 'mechanic_req_list.html'
    context_object_name = 'requests'

    def get_queryset(self):
        try:
            mechanic_profile = self.request.user.mechanic_profile
            return ReqToMechanic.objects.filter(mechanic=mechanic_profile).order_by('-datetime')
        except :
                messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except MechanicProfile.DoesNotExist:
            pass
        return context


def update_status_Accept(request, pk):
    req = get_object_or_404(ReqToMechanic, pk=pk)
    
    req.status = 'accepted'
    req.save()
    return redirect('mechanic_requests')


def update_status_Reject(request, pk):
    req = get_object_or_404(ReqToMechanic, pk=pk)
    req.status = 'rejected'
    req.save()
    return redirect('mechanic_requests')


def update_status(request, pk):
    req = get_object_or_404(ReqToMechanic, pk=pk)
    if request.method == 'POST':
        req.status = 'completed'
        req.save()
        return redirect('mechanic_requests')  # Redirect to the pending list page
    return redirect('mechanic_requests')



class UserRequestsListView(ListView):
    model = ReqToMechanic
    template_name = 'user_requests.html'
    context_object_name = 'user_requests'

    def get_queryset(self):
        try:
            return ReqToMechanic.objects.filter(user=self.request.user.user_profile).order_by('-datetime')
        except:
            messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            # return redirect('user_home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=UserProfile.objects.get(user=self.request.user.id)
        except UserProfile.DoesNotExist:
            pass
        return context






class FeedBackCreateView(CreateView):
    model = FeedBack
    form_class = FeedBackForm
    template_name = 'feedback.html'
    # success_url = reverse_lazy('user_requests')

    def get_success_url(self,**kwargs):
        id=self.kwargs.get('pk')
        return reverse_lazy('feedback_form',kwargs={'pk':id})

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        print(id)
        req=ReqToMechanic.objects.get(id=id)
        feed=FeedBack.objects.filter(mechanic=req.mechanic)
        context['feed']=feed
        context['feedback']=FeedBack.options
        try:
            context['profile']=UserProfile.objects.get(user=self.request.user.id)
        except UserProfile.DoesNotExist:
            pass
        return context

        return context
    def form_valid(self, form):
        req_to_mechanic = get_object_or_404(ReqToMechanic, pk=self.kwargs['pk'])
        form.instance.user = self.request.user.user_profile
        form.instance.request = req_to_mechanic
        form.instance.mechanic_id = req_to_mechanic.mechanic.id
        return super().form_valid(form)
    
class FeedbackListView(ListView):
    model = FeedBack
    template_name = 'feedback_list.html'
    context_object_name = 'feedback_list'

    def get_queryset(self):
        try:
            mechanic_profile = self.request.user.mechanic_profile
            return FeedBack.objects.filter(mechanic=mechanic_profile)
        except :
               messages.error(self.request, "User has no User Profile, Complete Profile!!!.")
            #    return redirect('mechanic_home')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except MechanicProfile.DoesNotExist:
            pass
        return context



class BillPaymentCreateView(CreateView):
    model = Bill
    form_class = BillPaymentForm
    template_name = 'create_bill.html'
    success_url = reverse_lazy('mechanic_requests')

    def form_valid(self, form):
        req_id = self.kwargs['pk']
        req = get_object_or_404(ReqToMechanic, pk=req_id)
        form.instance.req = req
        form.instance.mechanic = req.mechanic
        form.instance.customer = req.user
        payment_amount = form.cleaned_data['payment']
        return super().form_valid(form)

class BillPaymentCreateView(CreateView):
    model = Bill
    form_class = BillPaymentForm
    template_name = 'create_bill.html'
    success_url = reverse_lazy('mechanic_requests')

    def form_valid(self, form):
        req_id = self.kwargs['pk']
        req = get_object_or_404(ReqToMechanic, pk=req_id)
        form.instance.req = req
        form.instance.mechanic = req.mechanic
        form.instance.customer = req.user
        req.status='Payment Pending'
        req.save()
        payment_amount = form.cleaned_data['payment']
        return super().form_valid(form)
    


def bil_payment(request, pk):
    req = get_object_or_404(ReqToMechanic, pk=pk)
    bill = get_object_or_404(Bill, req=req)
    
    if request.method == 'POST':
        bill.status = 'completed'
        bill.save()
        return redirect('payment')  # Redirect to the pending list page
    return redirect('user_requests')


class PaymentSuccessView(TemplateView):
    template_name="payment_success.html"





class CustomPasswordChangeView(FormView):
    def get_template_names(self):
        if self.request.user.is_superuser == 1:
            return ['change_password.html']
        elif self.request.user.role == "user":
            return ['user_changepassword.html']
        elif self.request.user.role == "mechanic":
            return ['mechanic_changepassword.html']
        elif self.request.user.role == "fuels":
            return ['fuel_changepassword.html']
        else:
            return ['car_renter_changepassword.html']    
        
    form_class=ChangePasswordForm
    def post(self,request,*args,**kwargs):
        form_data=ChangePasswordForm(data=request.POST)
        if form_data.is_valid():
            current=form_data.cleaned_data.get("current_password")
            print(current)
            new=form_data.cleaned_data.get("new_password")
            confirm=form_data.cleaned_data.get("confirm_password")
            user=authenticate(request,username=request.user.username,password=current)
            print(user)
            if user:
                if new==confirm:
                    user.set_password(new)
                    user.save()
                    # messages.success(request,"password changed")
                    logout(request)
                    return redirect("login")
                else:
                    if self.request.user.role == "admin":
                        return redirect("admin-home")
                    elif self.request.user.role == "user":
                        return redirect("user_home")
                    elif self.request.user.role == "mechanic":
                        return redirect("mechanic_home")
                    else:
                        return redirect("car_home")
                    # messages.error(request,"password mismatches!")
                    # return redirect("change_password")
            else:
                # messages.error(request,"passsword incorrect!")
                return redirect("change_password")
        else:
            return render(request,"change_password.html",{"form":form_data})
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            if self.request.user.role == "user":
                context['profile']=UserProfile.objects.get(user=self.request.user.id)
            else  :
                context['profile']=MechanicProfile.objects.get(user=self.request.user.id)
        except:
            pass
        return context

# class CustomPasswordChangeView(PasswordChangeView):
#     def get_template_names(self):
#         if self.request.user.role == "admin":
#             return ['change_password.html']
#         elif self.request.user.role == "user":
#             return ['user_changepassword.html']
#         elif self.request.user.role == "mechanic":
#             return ['mechanic_changepassword.html']
#         else:
#             return ['car_renter_changepassword.html']

#     def get_success_url(self):
#         # if self.request.user.role == 'admin':
#         #     return reverse_lazy('admin-home')
#         # elif self.request.user.role == 'mechanic':
#         #     return reverse_lazy('mechanic_home')
#         # elif self.request.user.role == 'car_renter':
#         #     return reverse_lazy('car_home')
#         # else:
#         return reverse_lazy('logout')


def mechanic_search(request):
    if request.method == 'GET':
        form = MechanicSearchForm(request.GET)
        if form.is_valid():
            mechanic = form.cleaned_data.get('mechanic')
            print(mechanic)
            # services = MechanicProfile.objects.filter(name__icontains=mechanic)
            services = MechanicProfile.objects.filter(location__name__icontains=mechanic)
            print(services)
            if services:
                return render(request, 'search_results.html', {'mechanics': services})
            else:
                error_message = "No services found for the provided category"
                return render(request, 'search_results.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Invalid search criteria."
            return render(request, 'search_results.html', {'form': form, 'error_message': error_message})
    else:
        form = MechanicSearchForm()
        return render(request, 'search_results.html', {'form': form})    
    

class UserPaymentDetailsView(CreateView):
    model = UserPayment
    form_class = UserPaymentForm
    template_name = 'user_paybill.html'
    context_object_name = 'bill'
    
    def get_success_url(self):
        return reverse_lazy('payment')

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        try:
            id=self.kwargs.get('pk')
            print(id)
            req = ReqToMechanic.objects.get(id=id)
            context['req']=ReqToMechanic.objects.get(id=id)
            print(req)
            context['bill']=Bill.objects.get(req=req)
            bill = Bill.objects.get(req=req)
            context['total'] = bill.payment + bill.platform_fee 
            context['userpayment']=UserPayment.objects.filter(req=req.id,customer=self.request.user.id)
        except Bill.DoesNotExist:
            pass
        return context

    

    def form_valid(self, form):
        req_id = self.kwargs['pk']
        req = get_object_or_404(ReqToMechanic, pk=req_id)
        form.instance.req = req
        form.instance.mechanic = req.mechanic
        form.instance.customer = req.user
        req.status= 'completed'
        req.save()
        return super().form_valid(form)


class UserPaymentView(TemplateView):
    template_name='user_payment_details.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        bill=ReqToMechanic.objects.get(id=id)
        context['data']=UserPayment.objects.get(req=bill)
        return context
    
    

class MechanicHistory(TemplateView):
    template_name='mechanic_history.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        mech=MechanicProfile.objects.get(id=id)
        context['history']=ReqToMechanic.objects.filter(mechanic=mech.id,status="completed")
        return context
    

class MechanicPaymentAdminHistory(TemplateView):
    template_name='admin_view_mechdetails.html'
    def get_context_data(self, **kwargs):
        context =super().get_context_data(**kwargs)
        id=self.kwargs.get('pk')
        mech=MechanicProfile.objects.get(id=id)
        context['history']=Bill.objects.filter(mechanic=mech.id)
        return context
    
    
class FuelHome(TemplateView):
    template_name = 'fuel_home.html'
    
    

def add_fuel(request, fuel_id=None):
    if fuel_id:
        fuel = get_object_or_404(Fuel, id=fuel_id)
        form = FuelForm(request.POST or None, request.FILES or None, instance=fuel)
    else:
        form = FuelForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            fuel = form.save(commit=False)
            fuel.user = request.user
            fuel.save()
            return redirect('fuel_add')  

    fuels = Fuel.objects.filter(user=request.user.id) 
    location = Location.objects.all()
    return render(request, 'fuel_add.html', {'form': form, 'fuels': fuels, 'fuel_id': fuel_id,'location':location})

    

def delete_fuel(request, fuel_id):
    try:
        fuel = Fuel.objects.get(id=fuel_id)
        fuel.delete()
    except Fuel.DoesNotExist:
        pass  
    return redirect('fuel_add')



def view_fuels(request):
    fuels = Fuel.objects.all()  # Get all available fuels
    return render(request, 'view_fuels.html', {'fuels': fuels})

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def fuel_requests(request):
    # Get the user profile
    user_profile = request.user.user_profile
    
    # Filter requests by user and order by datetime (newest first)
    fuel_requests = ReqFuel.objects.filter(user=user_profile.id).order_by('-datetime')
    
    # Implement pagination - 10 requests per page
    paginator = Paginator(fuel_requests, 10)
    page_number = request.GET.get('page', 1)
    
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
    
    # Get count statistics
    pending_count = fuel_requests.filter(status='pending').count()
    approved_count = fuel_requests.filter(status='Order Confirmed').count()
    completed_count = fuel_requests.filter(status='completed').count()
    context = {
        'fuel_requests': page_obj,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'completed_count': completed_count,
        'total_count': fuel_requests.count(),
        'page_obj': page_obj,
    }
    
    return render(request, 'fuel_requests.html', context)


def update_fuel_request(request, request_id):
    """
    Updates the status of a fuel delivery request
    """
    if request.method == 'POST':
        fuel_request = get_object_or_404(ReqFuel, id=request_id)       
        new_status = request.GET.get('status')
        print(new_status)         
        status_choices = dict(ReqFuel.STATUS_CHOICES)
        if new_status in status_choices:
            fuel_request.status = new_status
            fuel_request.save()
            messages.success(request, f"Request status updated to {status_choices[new_status]}")
        else:
            messages.error(request, "Invalid status selected")
    return redirect('fuel_list', pk=fuel_request.fuel.id)

def create_bill_payment(request, request_id):
    """
    Creates a bill for a fuel delivery request
    """
    if request.method == 'POST':
        fuel_request = get_object_or_404(ReqFuel, id=request_id)
        if BillFuel.objects.filter(req=fuel_request).exists():
            messages.warning(request, "A bill already exists for this request")
            return redirect('fuel_list',pk=fuel_request.fuel.id)
        
        fuel_price = fuel_request.fuel.price  # Assuming there's a price field in Fuel model
        quantity = fuel_request.quantity
        total_amount = fuel_price * quantity

        bill = BillFuel.objects.create(
            req=fuel_request,
            fuel=fuel_request.fuel,
            customer = fuel_request.user,
            payment=total_amount,
            status="pending"  
        )
        
        messages.success(request, "Bill created successfully")
        
    return redirect('fuel_list',pk=fuel_request.fuel.id)


class ReqToFuelCreateView(CreateView):
    model = ReqFuel
    form_class = ReqFuelForm
    template_name = 'create_req_fuel.html'
    success_url = reverse_lazy('fuel_requests')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mechanic_id = self.kwargs.get('fuel_id')
        context['fuel']=Fuel.objects.get(id=mechanic_id)
        context['location']=Location.objects.all()
        return context

       
       

class FuelReqListView(ListView):
    model = ReqFuel
    template_name = 'fuel_req_list.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        print(pk)
        context['requests'] = ReqFuel.objects.filter(fuel=pk).order_by('-datetime')
        try:
            context['profile']=User.objects.get(id=self.request.user.id)
        except User.DoesNotExist:
            pass
        return context

def cancel_request(request, request_id):
    try:
        fuel_request = ReqFuel.objects.get(id=request_id, user=request.user.user_profile)
        if fuel_request.status == 'pending':
            fuel_request.status = 'Cancelled'
            fuel_request.save()
            messages.success(request, 'Your fuel request has been cancelled.')
        else:
            messages.error(request, 'Only pending requests can be cancelled.')
    except ReqFuel.DoesNotExist:
        messages.error(request, 'Request not found or you do not have permission to cancel it.')
    
    return redirect('fuel_requests')


class UserFuelPaymentDetailsView(CreateView):
    model = UserPaymentFuel
    form_class = PaymentFuelForm
    template_name = 'user_pay_fuel_bill.html'
    context_object_name = 'bill'
    
    def get_success_url(self):
        return reverse_lazy('payment')

    def get_context_data(self, **kwargs) :
        context= super().get_context_data(**kwargs)
        try:
            id=self.kwargs.get('pk')
            print(id)
            bill = ReqFuel.objects.get(id=id)
            context['req']=ReqFuel.objects.get(id=id)
            print(bill)
            context['bill']=BillFuel.objects.get(req=bill)
        
            context['userpayment']=UserPaymentFuel.objects.filter(req=bill.id,customer=self.request.user.id)
        except BillFuel.DoesNotExist:
            pass
        return context
    
    def form_valid(self, form):
        req_id = self.kwargs['pk']
        req = get_object_or_404(ReqFuel, pk=req_id)
        form.instance.req = req
        form.instance.fuel = req.fuel
        form.instance.customer = req.user
        req.status= 'completed'
        req.save()
        return super().form_valid(form)



def product_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    
    
    if category_id:
        products = Product.objects.filter(category_id=category_id, is_available=True)
    else:
        products = Product.objects.filter(is_available=True)
    
    context = {
        'products': products,
        'categories': categories
    }
    return render(request, 'product_list.html', context)  

# !!!!!!!!!!!!!!!!newly adddedd!!!!!!!!!!!!!!!!!!!!!!!!!!!!!   


def product_list(request):
    query = request.GET.get('q')           # for search
    category_id = request.GET.get('category')  # optional category filter

    products = Product.objects.all()

    if query:
        products = products.filter(name__icontains=query)  # search logic

    if category_id:
        products = products.filter(category_id=category_id)  # category filter logic

    categories = Category.objects.all()

    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories
    })



def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    
    context = {
        'product': product,
        'related_products': related_products
    }
    return render(request, 'product_detail.html', context)

from django.contrib.auth.decorators import login_required


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Check if product is already in cart
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    # If product already exists in cart, increase quantity
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f"{product.name} added to your cart!")
    
    # Redirect to either the referring page or the cart page
    next_page = request.GET.get('next', 'view_cart')
    return redirect(next_page)

@login_required
def view_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cart_items.all()
    except Cart.DoesNotExist:
        cart = None
        cart_items = []
    
    context = {
        'cart': cart,
        'cart_items': cart_items
    }
    return render(request, 'cart.html', context)

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, "Item removed from cart")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Cart updated!")
            
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('view_cart')
@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        if not cart.cart_items.exists():
            messages.warning(request, "Your cart is empty!")
            return redirect('product_list')
    except Cart.DoesNotExist:
        messages.warning(request, "Your cart is empty!")
        return redirect('product_list')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()
            
            # Create order items from cart items
            for cart_item in cart.cart_items.all():
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            
            # Clear the cart
            cart.delete()
            
            # Redirect to payment page instead of order confirmation
            messages.success(request, "Shipping information saved. Please complete payment.")
            return redirect('payment_page', order_id=order.id)
    else:
        form = OrderForm()
    
    context = {
        'form': form,
        'cart': cart
    }
    return render(request, 'checkout.html', context)

@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = product.price
            order.save()
            
            # Create a single order item
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=1,
                price=product.price
            )
            
            messages.success(request, "Shipping information saved. Please complete payment.")
            return redirect('payment_page', order_id=order.id)  # Redirect to payment page
    else:
        form = OrderForm()
    
    context = {
        'form': form,
        'product': product
    }
    return render(request, 'buy_now.html', context)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order
    }
    return render(request, 'order_confirmation.html', context)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user,status ="shipped" ) | Order.objects.filter(user=request.user,status ="processing" ) | Order.objects.filter(user=request.user,status ="delivered" ).order_by('-created_at')
    
    context = {
        'orders': orders
    }
    return render(request, 'order_history.html', context)


@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        form = OrderPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.order = order
            payment.amount = order.total_price
            payment.save()
            order.status = 'processing'  
            order.save()
            
            messages.success(request, "Payment successful! Your order is confirmed.")
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = OrderPaymentForm()
    
    context = {
        'form': form,
        'order': order
    }
    return render(request, 'payment_page_shop.html', context)


from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password/password_reset.html'
    email_template_name = 'password/password_reset_email.html'
    subject_template_name = 'password/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password/password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password/password_reset_complete.html'

def cancel_request_mech(request, request_id):
    if request.method == 'POST':
        service_request = get_object_or_404(ReqToMechanic, id=request_id)        
        if service_request.user.user == request.user:
            if service_request.status in ['pending', 'accepted']:
                service_request.status = 'cancelled'
                service_request.save()
                messages.success(request, 'Your service request has been cancelled successfully.')
            else:
                messages.error(request, 'This request cannot be cancelled in its current state.')
        else:
            messages.error(request, 'You do not have permission to cancel this request.')
            
    return redirect('user_requests')