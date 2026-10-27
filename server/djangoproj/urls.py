from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # React login page
    path(
        "login/",
        TemplateView.as_view(template_name="index.html"),
        name="login_page"
    ),

    # React registration page
    path(
        "register/",
        TemplateView.as_view(template_name="index.html"),
        name="register_page"
    ),

    # Dealership static pages
    path(
        "contact/",
        TemplateView.as_view(template_name="Contact.html"),
        name="contact"
    ),

    path(
        "about/",
        TemplateView.as_view(template_name="About.html"),
        name="about"
    ),

    # Django admin
    path("admin/", admin.site.urls),

    # Django API routes
    path("djangoapp/", include("djangoapp.urls")),

    # Home page
    path(
        "",
        TemplateView.as_view(template_name="Home.html"),
        name="home"
    ),
]


urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
