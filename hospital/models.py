from django.db import models


# ==========================
# Patient
# ==========================
class Patient(models.Model):
    CHOOSE_GENDER = [
        ('male', 'Male'),
        ('female', 'Female')
    ]

    CHOOSES_BLOOD_GROUP = [
        ('A+', 'A+'), ('B+', 'B+'), ('O+', 'O+'), ('AB+', "AB+"),
        ('A-', 'A-'), ('B-', 'B-'), ('O-', 'O-'), ('AB-', "AB-")
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=6, choices=CHOOSE_GENDER)
    dob = models.DateField()
    blood_group = models.CharField(max_length=5, choices=CHOOSES_BLOOD_GROUP)
    address = models.TextField()
    emergency_contact = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# ==========================
# Department
# ==========================
class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ==========================
# Doctor
# ==========================
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors')
    specialization = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    qualification = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    active_time = models.TimeField()

    def __str__(self):
        return self.name


# ==========================
# Appointment
# ==========================
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'PENDING'),
        ('confirmed', 'CONFIRMED'),
        ('cancelled', 'CANCELLED'),
        ('completed', 'COMPLETED')
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return f"Appointment: {self.patient.first_name} with {self.doctor.name}"


# ==========================
# Schedule
# ==========================
class Schedule(models.Model):
    WEEKDAYS = [
        ('mon', 'MONDAY'),
        ('tue', 'TUESDAY'),
        ('wed', 'WEDNESDAY'),
        ('thu', 'THURSDAY'),
        ('fri', 'FRIDAY'),
        ('sat', 'SATURDAY'),
        ('sun', 'SUNDAY'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    weekday = models.CharField(max_length=3, choices=WEEKDAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.doctor.name} - {self.weekday}"


# ==========================
# Ward
# ==========================
class Ward(models.Model):
    WARD_CHOOSE = [
        ('general', 'GENERAL'),
        ('icu', 'ICU'),
        ('cabin', 'CABIN')
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=WARD_CHOOSE)

    def __str__(self):
        return self.name


# ==========================
# Room
# ==========================
class Room(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='rooms')
    room_no = models.CharField(max_length=10)
    bed_count = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room {self.room_no} ({self.ward.name})"


# ==========================
# Admission
# ==========================
class Admission(models.Model):
    STATUS_CHOOSE = [
        ('admitted', 'ADMITTED'),
        ('discharged', 'DISCHARGED'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='admissions')
    admitted_at = models.DateTimeField(auto_now_add=True)
    discharged_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOOSE, default='admitted')

    def __str__(self):
        return f"Admission: {self.patient.first_name}"


# ==========================
# Treatment
# ==========================
class Treatment(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='treatments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='treatments')
    description = models.TextField()
    treatment_date = models.DateField()

    def __str__(self):
        return f"Treatment for {self.admission.patient.first_name}"


# ==========================
# Medication
# ==========================
class Medication(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='medications')
    medicine_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)

    def __str__(self):
        return self.medicine_name


# ==========================
# Nurse
# ==========================
class Nurse(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='nurses')
    assign_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True, related_name='nurses')

    def __str__(self):
        return self.name


# ==========================
# Lab Test
# ==========================
class LabTest(models.Model):
    test_name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.test_name


# ==========================
# Lab Report
# ==========================
class LabReport(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_reports')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='lab_reports')
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='lab_reports')
    report_file = models.FileField(upload_to='reports/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Lab Report for {self.patient.first_name}"


# ==========================
# Prescription
# ==========================
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    notes = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.patient.first_name}"


# ==========================
# Invoice
# ==========================
class Invoice(models.Model):
    STATUS_CHOOSE = [
        ('paid', 'PAID'),
        ('unpaid', 'UNPAID'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    admission = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    total_amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS_CHOOSE, default='unpaid')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice - {self.patient.first_name}"


# ==========================
# Payment
# ==========================
class Payment(models.Model):
    METHOD_CHOOSE = [
        ('cash', 'CASH'),
        ('card', 'CARD'),
        ('online', 'ONLINE'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.FloatField()
    method = models.CharField(max_length=10, choices=METHOD_CHOOSE)
    paid_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for {self.invoice.id}"
