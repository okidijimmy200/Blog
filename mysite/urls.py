from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    # namespaces are used to reference to our URLs easily
    path('blog/', include('blog.urls', namespace='blog')),
]