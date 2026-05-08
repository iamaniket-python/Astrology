from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteSettings,
    About,
    AboutFeature,
    Service,
    AstrologyCourse,
    Gallery,
    Product,
    Testimonial,
    ContactInquiry,
)


# ─────────────────────────────────────────────
# Inlines
# ─────────────────────────────────────────────

class AboutFeatureInline(admin.TabularInline):
    model = AboutFeature
    extra = 1
    fields = ("title", "order")


# ─────────────────────────────────────────────
# Site Settings
# ─────────────────────────────────────────────

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("location", "phone", "email", "whatsapp_number")

    def has_add_permission(self, request):
        # Only one settings row allowed
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ─────────────────────────────────────────────
# About
# ─────────────────────────────────────────────

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ("name", "heading", "experience_years", "image_preview")
    inlines = [AboutFeatureInline]

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px;border-radius:6px;" />',
                obj.image.url,
            )
        return "—"
    image_preview.short_description = "Image"

    def has_add_permission(self, request):
        return not About.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ─────────────────────────────────────────────
# Services
# ─────────────────────────────────────────────

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("icon", "title", "price", "order")
    list_editable = ("price", "order")
    ordering = ("order",)
    search_fields = ("title",)


# ─────────────────────────────────────────────
# Courses
# ─────────────────────────────────────────────

@admin.register(AstrologyCourse)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "level", "duration", "mode", "price", "order")
    list_editable = ("price", "order")
    list_filter = ("level", "mode")
    ordering = ("order",)
    search_fields = ("title",)
    fieldsets = (
        ("Course Info", {
            "fields": ("title", "description", "level", "duration", "mode", "students", "price", "order"),
        }),
        ("Visual Styling", {
            "classes": ("collapse",),
            "fields": ("gradient", "badge_bg", "badge_color"),
        }),
    )


# ─────────────────────────────────────────────
# Gallery
# ─────────────────────────────────────────────

@admin.register(Gallery)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("title", "emoji", "image_preview", "span_two_columns", "order")
    list_editable = ("span_two_columns", "order")
    ordering = ("order",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px;border-radius:6px;" />',
                obj.image.url,
            )
        return obj.emoji or "—"
    image_preview.short_description = "Preview"


# ─────────────────────────────────────────────
# Products
# ─────────────────────────────────────────────

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "name", "category", "price", "order")
    list_editable = ("price", "order")
    ordering = ("order",)
    search_fields = ("name", "category")
    fieldsets = (
        ("Product Info", {
            "fields": ("name", "category", "description", "price", "icon", "image", "order"),
        }),
        ("Visual Styling", {
            "classes": ("collapse",),
            "fields": ("gradient",),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height:50px;border-radius:6px;" />',
                obj.image.url,
            )
        return obj.icon or "—"
    image_preview.short_description = "Preview"


# ─────────────────────────────────────────────
# Testimonials
# ─────────────────────────────────────────────

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("emoji", "name", "city", "short_message", "order")
    list_editable = ("order",)
    ordering = ("order",)
    search_fields = ("name", "city")

    def short_message(self, obj):
        return obj.message[:80] + "…" if len(obj.message) > 80 else obj.message
    short_message.short_description = "Message"


# ─────────────────────────────────────────────
# Contact Inquiries
# ─────────────────────────────────────────────

@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "email", "service", "submitted_at", "is_read")
    list_filter = ("is_read", "service", "submitted_at")
    list_editable = ("is_read",)
    search_fields = ("name", "phone", "email")
    readonly_fields = ("name", "phone", "email", "service", "message", "submitted_at")
    ordering = ("-submitted_at",)

    def has_add_permission(self, request):
        return False

    fieldsets = (
        ("Client Details", {
            "fields": ("name", "phone", "email"),
        }),
        ("Inquiry", {
            "fields": ("service", "message"),
        }),
        ("Meta", {
            "fields": ("submitted_at", "is_read"),
        }),
    )