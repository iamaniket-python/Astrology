from .auth_views import admin_login, admin_logout
from .home_views import dashboard

from .about_views import about_edit, about_feature_add, about_feature_delete
from .service_views import service_list, service_add, service_edit, service_delete
from .course_views import course_list, course_add, course_edit, course_delete
from .gallery_views import gallery_list, gallery_add, gallery_edit, gallery_delete
from .product_views import product_list, product_add, product_edit, product_delete
from .testimonial_views import (
    testimonial_list, testimonial_add, testimonial_edit, testimonial_delete
)
from .settings_views import settings_edit
from .inquiry_views import inquiry_list, inquiry_mark_read, inquiry_delete