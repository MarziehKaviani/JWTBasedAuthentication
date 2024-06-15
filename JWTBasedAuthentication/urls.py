from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from JWTBasedAuthentication import views

swagger_description = """
### JWTBasedAuthentication APIs

* # Core
    
    `Permissions`: JWT authentication required.

`_________________________________________________________________`
    
* # Order
    
    `Permissions`: JWT authentication required.

`_________________________________________________________________`

* # Product
    
    * `Permissions`: JWT authentication required.

    * `Favorite Products`: Favorite Products (for user watch list) is a field in
    Product model that have two detail action in ProductViewSet that allowes to add user
    and remove user for the choosen product. 

    * `Categories`: Categories have a parent field that has a self-referential relationship. 
    The only category that is allowed to have a null parent is the ROOT category. The rest 
    of them have other categories as their parents. Each category has have_child and level 
    fields that show the level (count of each category's parent) and the child status of 
    that category.

`_________________________________________________________________`

* # Authentication
    
    These APIs handle user authentication and session management. 
    For get the jwt token follow up these steps:

    * `1. Get The Anon Token:`
        The anonymous token API is the only API that has no specific
        permissions needed (AllowAny). Before doing anything else,
        you should call this API and set the given anon token in the 
        cookies by name anon_token.

    * `2. Sign Up:`
        The sign-up action requires an Anonymous access token. When a 
        user calls sign-up, it will check if the user is not registered; 
        it will create a user in the database and send a 6-digit OTP to
        the given phone number. If the user already exists, it just sends
        the OTP.

    * `3. Login:`
        Just like sign-up, the login action needs an Anonymous access token.
        It takes the phone number and generated OTP from the sign-up and 
        returns access and refresh tokens. Users can use this access token 
        in the header of their requests (Authorization).
"""

schema_view = get_schema_view(
    openapi.Info(
        title="APIs",
        default_version="v1",
        description=swagger_description,
        contact=openapi.Contact(email=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
    path('user/', include('authentication.urls')),
    path('', include('home.urls')),
    path('', views.welcome_page, name='welcome.page'),
    path('product/', include('core.product_urls')),
    path('order/', include('core.order_urls')),
    path('utility/', include('core.utility_urls')),
    path('company/', include('core.company_urls')),
]
