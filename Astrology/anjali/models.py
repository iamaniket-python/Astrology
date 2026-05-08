from django.db import models


# =========================
# SERVICES MODEL
# =========================
class Service(models.Model):
    title = models.CharField(max_length=200)
    icon = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    price = models.CharField(max_length=100, blank=True, null=True)

    image = models.ImageField(
        upload_to='services/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# ASTROLOGY COURSES MODEL
# =========================
class AstrologyCourse(models.Model):
    title = models.CharField(max_length=200)

    badge = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    duration = models.CharField(max_length=100)

    mode = models.CharField(
        max_length=100,
        help_text="Online / Offline"
    )

    students = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    price = models.CharField(max_length=100)

    description = models.TextField()

    image = models.ImageField(
        upload_to='courses/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# PRODUCTS MODEL
# =========================
class Product(models.Model):
    CATEGORY_CHOICES = (
        ('Gemstone', 'Gemstone'),
        ('Yantra', 'Yantra'),
        ('Rudraksha', 'Rudraksha'),
        ('Crystal', 'Crystal'),
        ('Book', 'Book'),
        ('Protection', 'Protection'),
        ('Numerology', 'Numerology'),
        ('Ritual', 'Ritual'),
    )

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES
    )

    description = models.TextField()

    price = models.CharField(max_length=100)

    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# =========================
# TESTIMONIAL MODEL
# =========================
class Testimonial(models.Model):
    client_name = models.CharField(max_length=200)

    city = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    review = models.TextField()

    rating = models.IntegerField(default=5)

    image = models.ImageField(
        upload_to='testimonials/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.client_name


# =========================
# CONTACT INQUIRY MODEL
# =========================
class ContactInquiry(models.Model):
    SERVICE_CHOICES = (
        ('Janam Kundali', 'Janam Kundali'),
        ('Kundali Milan', 'Kundali Milan'),
        ('Career Guidance', 'Career Guidance'),
        ('Vastu Shastra', 'Vastu Shastra'),
        ('Numerology', 'Numerology'),
        ('Gemstone Recommendation', 'Gemstone Recommendation'),
        ('Astrology Class', 'Astrology Class'),
        ('Product Order', 'Product Order'),
    )

    full_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    email = models.EmailField()

    service = models.CharField(
        max_length=100,
        choices=SERVICE_CHOICES
    )

    message = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.full_name