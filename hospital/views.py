from rest_framework import viewsets
from .models import (
    Patient, Department, Doctor, Appointment,
    Schedule, Ward, Room, Admission,
    Treatment, Medication, Nurse,
    LabTest, LabReport, Prescription,
    Invoice, Payment
)
from .serializers import (
    PatientSerializer, DepartmentSerializer, DoctorSerializer, AppointmentSerializer,
    ScheduleSerializer, WardSerializer, RoomSerializer, AdmissionSerializer,
    TreatmentSerializer, MedicationSerializer, NurseSerializer,
    LabTestSerializer, LabReportSerializer, PrescriptionSerializer,
    InvoiceSerializer, PaymentSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all().order_by('first_name', 'last_name')
    serializer_class = PatientSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by('name').prefetch_related('doctors', 'nurses')
    serializer_class = DepartmentSerializer


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('department').all()
    serializer_class = DoctorSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient', 'doctor__department').all().order_by('-date', '-time')
    serializer_class = AppointmentSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.select_related('doctor__department').all()
    serializer_class = ScheduleSerializer


class WardViewSet(viewsets.ModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.select_related('ward').prefetch_related('nurses').all()
    serializer_class = RoomSerializer


class AdmissionViewSet(viewsets.ModelViewSet):
    queryset = Admission.objects.select_related('patient', 'room__ward').all().order_by('-admitted_at')
    serializer_class = AdmissionSerializer


class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.select_related('admission__patient', 'doctor').all()
    serializer_class = TreatmentSerializer


class MedicationViewSet(viewsets.ModelViewSet):
    queryset = Medication.objects.select_related('treatment__admission__patient', 'treatment__doctor').all()
    serializer_class = MedicationSerializer


class NurseViewSet(viewsets.ModelViewSet):
    queryset = Nurse.objects.select_related('department', 'assign_room__ward').all()
    serializer_class = NurseSerializer


class LabTestViewSet(viewsets.ModelViewSet):
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer


class LabReportViewSet(viewsets.ModelViewSet):
    queryset = LabReport.objects.select_related('patient', 'doctor', 'test').all().order_by('-created_at')
    serializer_class = LabReportSerializer


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('appointment', 'doctor', 'patient').all().order_by('-created_at')
    serializer_class = PrescriptionSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.select_related('patient', 'admission__room__ward').prefetch_related('payments').all().order_by('-created_at')
    serializer_class = InvoiceSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('invoice__patient').all().order_by('-paid_at')
    serializer_class = PaymentSerializer
