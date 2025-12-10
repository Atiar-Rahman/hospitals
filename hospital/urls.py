from rest_framework_nested import routers
from django.urls import path, include
from .views import (
    PatientViewSet, DepartmentViewSet, DoctorViewSet, AppointmentViewSet,
    ScheduleViewSet, WardViewSet, RoomViewSet, AdmissionViewSet,
    TreatmentViewSet, MedicationViewSet, NurseViewSet,
    LabTestViewSet, LabReportViewSet, PrescriptionViewSet,
    InvoiceViewSet, PaymentViewSet
)

router = routers.DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'schedules', ScheduleViewSet)
router.register(r'wards', WardViewSet)
router.register(r'rooms', RoomViewSet)
router.register(r'admissions', AdmissionViewSet)
router.register(r'treatments', TreatmentViewSet)
router.register(r'medications', MedicationViewSet)
router.register(r'nurses', NurseViewSet)
router.register(r'labtests', LabTestViewSet)
router.register(r'labreports', LabReportViewSet)
router.register(r'prescriptions', PrescriptionViewSet)
router.register(r'invoices', InvoiceViewSet)
router.register(r'payments', PaymentViewSet)

# Nested routers example:

# 1. Doctors under Department
departments_router = routers.NestedDefaultRouter(router, r'departments', lookup='department')
departments_router.register(r'doctors', DoctorViewSet, basename='department-doctors')
departments_router.register(r'nurses', NurseViewSet, basename='department-nurses')

# 2. Appointments under Patient
patients_router = routers.NestedDefaultRouter(router, r'patients', lookup='patient')
patients_router.register(r'appointments', AppointmentViewSet, basename='patient-appointments')
patients_router.register(r'prescriptions', PrescriptionViewSet, basename='patient-prescriptions')
patients_router.register(r'invoices', InvoiceViewSet, basename='patient-invoices')
patients_router.register(r'labreports', LabReportViewSet, basename='patient-labreports')
patients_router.register(r'admissions', AdmissionViewSet, basename='patient-admissions')

# 3. Treatments under Admission
admissions_router = routers.NestedDefaultRouter(router, r'admissions', lookup='admission')
admissions_router.register(r'treatments', TreatmentViewSet, basename='admission-treatments')

# 4. Medications under Treatment
treatments_router = routers.NestedDefaultRouter(router, r'treatments', lookup='treatment')
treatments_router.register(r'medications', MedicationViewSet, basename='treatment-medications')

# 5. Payments under Invoice
invoices_router = routers.NestedDefaultRouter(router, r'invoices', lookup='invoice')
invoices_router.register(r'payments', PaymentViewSet, basename='invoice-payments')

# 6. Schedules under Doctor
doctors_router = routers.NestedDefaultRouter(router, r'doctors', lookup='doctor')
doctors_router.register(r'schedules', ScheduleViewSet, basename='doctor-schedules')
doctors_router.register(r'appointments', AppointmentViewSet, basename='doctor-appointments')
doctors_router.register(r'prescriptions', PrescriptionViewSet, basename='doctor-prescriptions')
doctors_router.register(r'labreports', LabReportViewSet, basename='doctor-labreports')
doctors_router.register(r'treatments', TreatmentViewSet, basename='doctor-treatments')

urlpatterns = [
    path(r'api/v1/', include(router.urls)),
    path(r'api/v1/', include(departments_router.urls)),
    path(r'api/v1/', include(patients_router.urls)),
    path(r'api/v1/', include(admissions_router.urls)),
    path(r'api/v1/', include(treatments_router.urls)),
    path(r'api/v1/', include(invoices_router.urls)),
    path(r'api/v1/', include(doctors_router.urls)),
]
