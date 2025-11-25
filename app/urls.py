from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

        # Admin URLs
        path("home/admin", AdminHomeView.as_view(), name="admin-home"),
        path("register/admin", AdminRegistrationView.as_view(), name="admin-registration"),
        path('login/admin', AdminLoginView.as_view(), name='admin-login'),
        path('add/locations', AddLocationView.as_view(), name="add-locations"),
        path('approval/<int:pk>', approve_mechanic, name="approve"),
        path('approval-mech/<int:pk>', approve_mechanics, name="approve_mechanic"),
        path('reject/<int:pk>', reject_mechanic, name="reject"),
        path('location-delete/<int:pk>', locationdelete, name="locdel"),
        path('all-pending-mech/', AdminAllMechanicView.as_view(), name="all-mech"),

        # Mechanic URLs
        path("mechanic/home", MechnaicHomeView.as_view(), name="mechanic_home"),
        path("add/profile/<int:pk>", MechanicProfileAddView.as_view(), name="add-profile"),
        path("profile/view/<int:pk>", MechanicProfileDetailView.as_view(), name="view-profile"),
        path("profile/<int:pk>/update", MechanicprofileUpdateView.as_view(), name="update-profile"),
        path('pending', PendingMechanicView.as_view(), name="pending-list"),
        path('my-requests/', MechanicReqListView.as_view(), name='mechanic_requests'),
        path('status_accept/<int:pk>/', update_status_Accept, name='req_accept'),
        path('status_reject/<int:pk>/', update_status_Reject, name='req_reject'),
        path('mechanicapproval/<int:pk>', update_status, name="mech-approve"),
        path('feedback-list/', FeedbackListView.as_view(), name='feedback_list'),
        path('create-bill-payment/<int:pk>/', BillPaymentCreateView.as_view(), name='create_bill_payment_mech'),


        # User URLs
        path("user/home", UserHomeView.as_view(), name="user_home"),
        path("user/registration", RegistrationView.as_view(), name="user_registration"),
        path("useradd/profile/<int:pk>", UserProfileAddView.as_view(), name="useradd-profile"),
        path("userprofile/view/<int:pk>", UserProfileDetailView.as_view(), name="userview-profile"),
        path("userprofile/update/<int:pk>", UserProfileUpdateView.as_view(), name="userupdate-profile"),
        path('approved-mechanics/', ApprovedMechanicListView.as_view(), name='approved_mechanics'),
        path("create/req/<int:mechanic_id>", ReqToMechanicCreateView.as_view(), name="create_req"),
        path('requests/', UserRequestsListView.as_view(), name='user_requests'),
        path('feedback/<int:pk>/', FeedBackCreateView.as_view(), name='feedback_form'),
        path('bill-payment/<int:pk>/', bil_payment, name='bill_payment'),
        path('userpayment/<int:pk>/',UserPaymentDetailsView.as_view(), name='user_payment'),
        path('userpaymentdetails/<int:pk>/',UserPaymentView.as_view(), name='payment_details'),
        path('mechanichistory/<int:pk>/',MechanicHistory.as_view(), name='mechistory'),
        path('mechanichistory-admin/<int:pk>/',MechanicPaymentAdminHistory.as_view(), name='mechistory-admin'),


        #fuel

        path('fuel-home/',FuelHome.as_view(),name='fuel'),
        path('fuel-add/',add_fuel,name='fuel_add'),
        path('add_fuel/<int:fuel_id>/', add_fuel, name='edit_fuel'),
        path('fuel-delete/<int:fuel_id>/',delete_fuel,name='fuel_del'),
        path('view_fuels/', view_fuels, name='view_fuels'),
        path('req-fuel/<int:fuel_id>/', ReqToFuelCreateView.as_view(), name='req_fuel'),
        path('fuel_requests/', fuel_requests, name='fuel_requests'),
        path('req-list-fuel/<int:pk>/', FuelReqListView.as_view(), name='fuel_list'),
        path('update_fuel_request/<int:request_id>/', update_fuel_request, name='update_fuel_request'),
        path('create_bill_payment/<int:request_id>/', create_bill_payment, name='create_bill_payment'),
        path('cancel_request/<int:request_id>/', cancel_request, name='cancel_request'),
        path('fuel_payment/<int:pk>/', UserFuelPaymentDetailsView.as_view(), name='fuel_payment'),
        path('cancel-request-mech/<int:request_id>/', cancel_request_mech, name='cancel_request_mech'),

        #  Shop
        
        path('products/',product_list, name='product_list'),
        path('product/<int:product_id>/',product_detail, name='product_detail'),
        path('cart/',view_cart, name='view_cart'),
        path('cart/add/<int:product_id>/',add_to_cart, name='add_to_cart'),
        path('cart/update/<int:item_id>/',update_cart_item, name='update_cart_item'),
        path('cart/remove/<int:item_id>/',remove_from_cart, name='remove_from_cart'),
        path('checkout/',checkout, name='checkout'),
        path('buy-now/<int:product_id>/', buy_now, name='buy_now'),
        path('payment/<int:order_id>/', payment_page, name='payment_page'),
        path('order-confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
        path('orders/',order_history, name='order_history'),
        path('products/', product_list, name='products'),

        # Common URLs
        path("",HomeView.as_view(),name="home"),
        path('login/', LoginView.as_view(), name='login'),
        path('logout/', LogoutView, name='logout'), 
        path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
        path("payment/sucess/",PaymentSuccessView.as_view(),name="payment"),
        path('search/',mechanic_search, name='mechanic_search'),
        path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
        path('password-reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
        path('password-reset/confeedfirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path('password-reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
