from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models


MAX_DIMENSION = 1200  # max width/height in pixels
JPEG_QUALITY = 80


def resize_image(image_field):
    """Resize + compress an uploaded image in-memory before it's saved/uploaded.
    Keeps aspect ratio, caps longest side at MAX_DIMENSION, re-encodes as JPEG
    at JPEG_QUALITY to cut file size drastically."""
    if not image_field:
        return image_field

    try:
        img = Image.open(image_field)
        img = img.convert('RGB')  # handles PNG/RGBA -> JPEG safely

        img.thumbnail((MAX_DIMENSION, MAX_DIMENSION), Image.LANCZOS)

        buffer = BytesIO()
        img.save(buffer, format='JPEG', quality=JPEG_QUALITY, optimize=True)
        buffer.seek(0)

        new_name = image_field.name.rsplit('.', 1)[0] + '.jpg'

        return InMemoryUploadedFile(
            buffer, 'ImageField', new_name, 'image/jpeg',
            buffer.getbuffer().nbytes, None
        )
    except Exception:
        # If anything goes wrong, fall back to the original file rather than crash
        return image_field


class SiteSettings(models.Model):
    """Global site settings — singleton (one row only)."""
    location       = models.CharField(max_length=255, default="Lucknow, Uttar Pradesh")
    phone          = models.CharField(max_length=20,  default="+91 9506619555")
    email          = models.EmailField(default="cchengemylife3@gmail.com")
    whatsapp_number = models.CharField(
        max_length=20,
        default="919506619555",
        help_text="Number without '+' for wa.me links",
    )

    class Meta:
        verbose_name        = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"


class About(models.Model):
    """About section — the astrologer's profile (singleton)."""
    name             = models.CharField(max_length=100, default="")
    heading          = models.CharField(max_length=255, default="", help_text="e.g. 'Master of Vedic Astrology'")
    description      = models.TextField(default="")
    experience_years = models.PositiveIntegerField(default=12)
    image            = models.ImageField(upload_to="about/", blank=True, null=True)

    class Meta:
        verbose_name        = "About"
        verbose_name_plural = "About"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            self.image = resize_image(self.image)
        super().save(*args, **kwargs)


class AboutFeature(models.Model):
    """Bullet points listed under the About section."""
    about = models.ForeignKey(About, on_delete=models.CASCADE, related_name="features")
    title = models.CharField(max_length=200, default="")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ["order"]
        verbose_name        = "About Feature"
        verbose_name_plural = "About Features"

    def __str__(self):
        return self.title


class Service(models.Model):
    """Cards in the 'Our Astrology Services' section."""
    icon        = models.CharField(max_length=20,  default="🔮", blank=True, help_text="Emoji icon e.g. 🪐")
    title       = models.CharField(max_length=100, default="")
    description = models.TextField(default="")
    price       = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title


class AstrologyCourse(models.Model):
    """Cards in the 'Astrology Classes & Courses' section."""

    LEVEL_CHOICES = [
        ("Beginner",     "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced",     "Advanced"),
        ("Professional", "Professional"),
    ]

    title       = models.CharField(max_length=150, default="")
    description = models.TextField(default="")
    level       = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="Beginner")
    duration    = models.CharField(max_length=50, default="", blank=True, help_text="e.g. '3 Months'")
    mode        = models.CharField(max_length=50, default="", blank=True, help_text="e.g. 'Online / Offline'")
    students    = models.CharField(max_length=50, default="", blank=True, help_text="e.g. '200+ Enrolled'")
    price       = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    gradient    = models.CharField(max_length=150, default="linear-gradient(135deg,#1c1638,#4a1472)", blank=True)
    badge_bg    = models.CharField(max_length=100, default="rgba(212,175,55,0.15)",                   blank=True)
    badge_color = models.CharField(max_length=50,  default="#d4af37",                                 blank=True)

    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering            = ["order"]
        verbose_name        = "Astrology Course"
        verbose_name_plural = "Astrology Courses"

    def __str__(self):
        return self.title


class Gallery(models.Model):
    """Items in the Photo Gallery section."""
    title           = models.CharField(max_length=150, default="")
    emoji           = models.CharField(max_length=20,  default="🔮", blank=True, help_text="Fallback emoji if no image")
    image           = models.ImageField(upload_to="gallery/", blank=True, null=True)
    gradient        = models.CharField(
        max_length=150,
        default="linear-gradient(135deg,#1c1638,#4a1472)",
        blank=True,
        help_text="Background gradient shown when no image is uploaded",
    )
    span_two_columns = models.BooleanField(
        default=False,
        help_text="Makes this item span 2 columns in the gallery grid",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering            = ["order"]
        verbose_name        = "Gallery Item"
        verbose_name_plural = "Gallery Items"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            self.image = resize_image(self.image)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Cards in the 'Astrology Products' carousel."""
    name        = models.CharField(max_length=150, default="")
    category    = models.CharField(max_length=80,  default="", blank=True, help_text="e.g. 'Gemstone', 'Rudraksha'")
    description = models.TextField(default="")
    price       = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    icon        = models.CharField(max_length=20,  default="", blank=True, help_text="Emoji fallback")
    image       = models.ImageField(upload_to="products/", blank=True, null=True)
    gradient    = models.CharField(max_length=150, default="linear-gradient(135deg,#1c1638,#4a1472)", blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image and hasattr(self.image, 'file'):
            self.image = resize_image(self.image)
        super().save(*args, **kwargs)


class Testimonial(models.Model):
    """Cards in the 'What Our Clients Say' carousel."""
    name      = models.CharField(max_length=100, default="")
    city      = models.CharField(max_length=100, default="", blank=True)
    message   = models.TextField(default="")
    emoji     = models.CharField(max_length=20, default="🙏", blank=True, help_text="Avatar emoji")
    order     = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.name} — {self.city}"


class ContactInquiry(models.Model):
    """Stores submissions from the contact / booking form."""
    name         = models.CharField(max_length=150, default="")
    phone        = models.CharField(max_length=20,  default="")
    email        = models.EmailField(default="")
    service      = models.CharField(max_length=150, default="")
    message      = models.TextField(default="")
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read      = models.BooleanField(default=False)

    class Meta:
        ordering            = ["-submitted_at"]
        verbose_name        = "Contact Inquiry"
        verbose_name_plural = "Contact Inquiries"

    def __str__(self):
        return f"{self.name} ({self.phone}) — {self.submitted_at:%d %b %Y}"