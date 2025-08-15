from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# --- Master data ---
class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    emirates_id = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    annual_fee_paid = models.BooleanField(default=False)  # track yearly fee
    last_fee_paid_on = models.DateField(null=True, blank=True)
    def __str__(self): return self.name

class Company(models.Model):
    name = models.CharField(max_length=255)
    trade_license_number = models.CharField(max_length=100, unique=True)
    trade_license_expiry = models.DateField(null=True, blank=True)
    establishment_card_number = models.CharField(max_length=100, blank=True)
    establishment_card_expiry = models.DateField(null=True, blank=True)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True)
    contact_person = models.CharField(max_length=255, blank=True)
    contact_phone = models.CharField(max_length=50, blank=True)
    contact_email = models.EmailField(blank=True)
    def __str__(self): return self.name

class Owner(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="owners")
    name = models.CharField(max_length=255)
    passport_no = models.CharField(max_length=100, blank=True)
    visa_no = models.CharField(max_length=100, blank=True)
    visa_expiry = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    def __str__(self): return f"{self.name} ({self.company.name})"

class Employee(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employees")
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255, blank=True)
    passport_no = models.CharField(max_length=100, blank=True)
    visa_no = models.CharField(max_length=100, blank=True)
    visa_expiry = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    def __str__(self): return f"{self.name} ({self.company.name})"

# --- Services & Requests ---
class ServiceType(models.Model):
    name = models.CharField(max_length=255, unique=True)  # e.g., New Visa, Visa Renewal, TL Renewal
    description = models.TextField(blank=True)
    base_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self): return self.name

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("received", "Received"),
        ("processing", "Processing"),
        ("submitted", "Submitted to Govt"),
        ("completed", "Completed"),
        ("rejected", "Rejected"),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="service_requests")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(Owner, on_delete=models.SET_NULL, null=True, blank=True)
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="received")
    created_at = models.DateTimeField(default=timezone.now)
    submitted_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    def __str__(self): return f"{self.company.name} - {self.service_type.name} ({self.status})"

# --- Gov artifacts (optional detail tables you can hook to requests) ---
class Visa(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="visas")
    number = models.CharField(max_length=100, unique=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self): return self.number

class TradeLicense(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="trade_license", null=True, blank=True)
    number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    def __str__(self): return f"{self.company.name} TL"

class EstablishmentCard(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="est_card", null=True, blank=True)
    number = models.CharField(max_length=100, blank=True)
    issue_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    def __str__(self): return f"{self.company.name} EC"

# --- Files ---
def doc_upload_path(instance, filename):
    return f"company_{instance.company_id}/requests/{instance.service_request_id}/{filename}"

class DocumentFile(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name="documents")
    file = models.FileField(upload_to=doc_upload_path)
    note = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(default=timezone.now)

# --- Billing ---
class Invoice(models.Model):
    service_request = models.OneToOneField(ServiceRequest, on_delete=models.CASCADE, related_name="invoice")
    number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    issued_on = models.DateField(default=timezone.now)
    due_on = models.DateField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    def __str__(self): return self.number

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_on = models.DateField(default=timezone.now)
    method = models.CharField(max_length=50, blank=True)  # Cash, Bank, Card
    reference = models.CharField(max_length=100, blank=True)

# --- Tasks & Audit ---
class Task(models.Model):
    STATUS = [("not_started", "Not Started"), ("in_progress", "In Progress"), ("completed", "Completed")]
    title = models.CharField(max_length=255)
    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        related_name="tasks",
        null=True,    # ← add
        blank=True    # ← add
    )
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS, default="not_started")
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    def __str__(self): return self.title

class TaskActivity(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="activities")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    def __str__(self): return f"{self.action} by {self.user.username}"
