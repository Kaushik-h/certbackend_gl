from rest_framework import serializers
from.models import *

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Certificates
        fields=('user','csp','level','certname','certid','certified_date','expiry_date','pdf_url')