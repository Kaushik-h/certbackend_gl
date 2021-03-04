from rest_framework import serializers
from.models import *
from accounts.serializers import *

class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model=Certificates
        fields=('user','csp','level','certname','certid','certified_date','expiry_date','pdf_url','sbu')

class GetCertificateSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Certificates
        fields=('id','user','csp','level','certname','certid','certified_date','expiry_date','pdf_url','sbu')