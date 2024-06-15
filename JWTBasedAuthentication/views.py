from datetime import datetime

from django.shortcuts import render


def welcome_page(request):
    return render(request, "view_pages/index.html", {"today": datetime.today})
