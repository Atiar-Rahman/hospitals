from rest_framework import serializers
from .models import (
    Patient, Department, Doctor, Appointment,
    Schedule, Ward, Room, Admission,
    Treatment, Medication, Nurse,
    LabTest, LabReport, Prescription,
    Invoice, Payment
)
from datetime import date

# -------------------------------
# Patient Serializer
# -------------------------------
class PatientSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'name', 'email', 'phone',
            'gender', 'dob', 'age', 'blood_group', 'address',
            'emergency_contact', 'created_at'
        ]
        read_only_fields = ['created_at']

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    def get_age(self, obj):
        if obj.dob:
            return date.today().year - obj.dob.year
        return None


# -------------------------------
# Department Serializer
# -------------------------------
class DepartmentSerializer(serializers.ModelSerializer):
    doctor_count = serializers.IntegerField(source='doctors.count', read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'description', 'doctor_count']


# -------------------------------
# Doctor Serializer
# -------------------------------
class DoctorSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'phone', 'department', 'department_name',
            'specialization', 'qualification', 'is_active', 'active_time'
        ]


# -------------------------------
# Appointment Serializer
# -------------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'doctor', 'date', 'time', 'status', 'notes',
            'patient_detail', 'doctor_detail'
        ]

    def validate(self, data):
        doctor = data.get('doctor')
        if doctor and not doctor.is_active:
            raise serializers.ValidationError({"doctor": "Selected doctor is not active."})
        return data


# -------------------------------
# Schedule Serializer
# -------------------------------
class ScheduleSerializer(serializers.ModelSerializer):
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Schedule
        fields = ['id', 'doctor', 'doctor_detail', 'weekday', 'start_time', 'end_time']


# -------------------------------
# Ward Serializer
# -------------------------------
class WardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ward
        fields = ['id', 'name', 'type']


# -------------------------------
# Room Serializer
# -------------------------------
class RoomSerializer(serializers.ModelSerializer):
    ward_detail = WardSerializer(source='ward', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'ward', 'ward_detail', 'room_no', 'bed_count', 'is_available']


# -------------------------------
# Admission Serializer
# -------------------------------
class AdmissionSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    room_detail = RoomSerializer(source='room', read_only=True)

    class Meta:
        model = Admission
        fields = [
            'id', 'patient', 'patient_detail', 'room', 'room_detail',
            'admitted_at', 'discharged_at', 'status'
        ]


# -------------------------------
# Treatment Serializer
# -------------------------------
class TreatmentSerializer(serializers.ModelSerializer):
    admission_detail = AdmissionSerializer(source='admission', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)

    class Meta:
        model = Treatment
        fields = ['id', 'admission', 'admission_detail', 'doctor', 'doctor_detail', 'description', 'treatment_date']


# -------------------------------
# Medication Serializer
# -------------------------------
class MedicationSerializer(serializers.ModelSerializer):
    treatment_detail = TreatmentSerializer(source='treatment', read_only=True)

    class Meta:
        model = Medication
        fields = ['id', 'treatment', 'treatment_detail', 'medicine_name', 'dosage', 'frequency']


# -------------------------------
# Nurse Serializer
# -------------------------------
class NurseSerializer(serializers.ModelSerializer):
    department_detail = DepartmentSerializer(source='department', read_only=True)
    assign_room_detail = RoomSerializer(source='assign_room', read_only=True)

    class Meta:
        model = Nurse
        fields = ['id', 'name', 'phone', 'department', 'department_detail', 'assign_room', 'assign_room_detail']


# -------------------------------
# LabTest Serializer
# -------------------------------
class LabTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabTest
        fields = ['id', 'test_name', 'description', 'price']


# -------------------------------
# LabReport Serializer
# -------------------------------
class LabReportSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)
    test_detail =  LabTestSerializer(source='test', read_only=True)

    class Meta:
        model = LabReport
        fields = ['id', 'patient', 'patient_detail', 'doctor', 'doctor_detail', 'test', 'test_detail', 'report_file', 'created_at']


# -------------------------------
# Prescription Serializer
# -------------------------------
class PrescriptionSerializer(serializers.ModelSerializer):
    appointment_detail = serializers.PrimaryKeyRelatedField(read_only=True)
    doctor_detail = DoctorSerializer(source='doctor', read_only=True)
    patient_detail = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Prescription
        fields = ['id', 'appointment', 'appointment_detail', 'doctor', 'doctor_detail', 'patient', 'patient_detail', 'notes', 'created_at']


# -------------------------------
# Invoice Serializer
# -------------------------------
class InvoiceSerializer(serializers.ModelSerializer):
    patient_detail = PatientSerializer(source='patient', read_only=True)
    admission_detail = AdmissionSerializer(source='admission', read_only=True)
    payments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = ['id', 'patient', 'patient_detail', 'admission', 'admission_detail', 'total_amount', 'status', 'created_at', 'payments']


# -------------------------------
# Payment Serializer
# -------------------------------
class PaymentSerializer(serializers.ModelSerializer):
    invoice_detail = InvoiceSerializer(source='invoice', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'invoice', 'invoice_detail', 'amount', 'method', 'paid_at']
