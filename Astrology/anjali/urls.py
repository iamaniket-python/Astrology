from django.urls import path
from . import views

urlpatterns = [
    # ---------- Public site ----------
    path('', views.index, name='index'),

    # ---------- Admin auth ----------
    path('dashboard/login/', views.admin_login, name='admin_login'),
    path('dashboard/logout/', views.admin_logout, name='admin_logout'),

    # ---------- Dashboard home ----------
    path('dashboard/', views.dashboard, name='dashboard'),

    # ---------- About ----------
    path('dashboard/about/', views.about_edit, name='about_edit'),
    path('dashboard/about/feature/add/', views.about_feature_add, name='about_feature_add'),
    path('dashboard/about/feature/<int:pk>/delete/', views.about_feature_delete, name='about_feature_delete'),

    # ---------- Services ----------
    path('dashboard/services/', views.service_list, name='service_list'),
    path('dashboard/services/add/', views.service_add, name='service_add'),
    path('dashboard/services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('dashboard/services/<int:pk>/delete/', views.service_delete, name='service_delete'),

    # ---------- Courses ----------
    path('dashboard/courses/', views.course_list, name='course_list'),
    path('dashboard/courses/add/', views.course_add, name='course_add'),
    path('dashboard/courses/<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('dashboard/courses/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # ---------- Gallery ----------
    path('dashboard/gallery/', views.gallery_list, name='gallery_list'),
    path('dashboard/gallery/add/', views.gallery_add, name='gallery_add'),
    path('dashboard/gallery/<int:pk>/edit/', views.gallery_edit, name='gallery_edit'),
    path('dashboard/gallery/<int:pk>/delete/', views.gallery_delete, name='gallery_delete'),

    # ---------- Products ----------
    path('dashboard/products/', views.product_list, name='product_list'),
    path('dashboard/products/add/', views.product_add, name='product_add'),
    path('dashboard/products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('dashboard/products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # ---------- Testimonials ----------
    path('dashboard/testimonials/', views.testimonial_list, name='testimonial_list'),
    path('dashboard/testimonials/add/', views.testimonial_add, name='testimonial_add'),
    path('dashboard/testimonials/<int:pk>/edit/', views.testimonial_edit, name='testimonial_edit'),
    path('dashboard/testimonials/<int:pk>/delete/', views.testimonial_delete, name='testimonial_delete'),

    # ---------- Settings ----------
    path('dashboard/settings/', views.settings_edit, name='settings_edit'),

    # ---------- Inquiries ----------
    path('dashboard/inquiries/', views.inquiry_list, name='inquiry_list'),
    path('dashboard/inquiries/<int:pk>/mark-read/', views.inquiry_mark_read, name='inquiry_mark_read'),
    path('dashboard/inquiries/<int:pk>/delete/', views.inquiry_delete, name='inquiry_delete'),
]