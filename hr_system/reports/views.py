from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

class ExportCSVView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"status": "CSV export endpoint placeholder"})

