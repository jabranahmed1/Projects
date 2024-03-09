import calendar
from django.shortcuts import render
from .models import CityInfos
from django.db.models.functions import ExtractMonth

from django.http import FileResponse
from django.core.paginator import Paginator
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/accounts/login")
def index(request):
    labels=[]
    data=[]
    time=[]

    queryset= CityInfos.objects.all()
    for var in queryset:
        data.append(var.temperature)
        labels.append(var.humidity)
        month_name = calendar.month_abbr[var.c_date.month]
        formatted_date = f"{month_name} {var.c_date.day}"
        time.append(formatted_date)
    
    context={
            'labels': labels,
            'data': data,
            'time': time,
        }
    return render(request, 'example.html', context)

def search(request):
    if request.method=='POST':
        city= request.POST['citycountry']
        labels=[]
        data=[]
        time=[]
       
        queryset= CityInfos.objects.filter(cityname=city)
        for var in queryset:
            data.append(var.temperature)
            labels.append(var.humidity)
            month_name = calendar.month_abbr[var.c_date.month]
            formatted_date = f"{month_name} {var.c_date.day}"
            time.append(formatted_date)

    context={
        'labels': labels,
        'data': data,
        'time': time,
        'city': city
    }
    return render(request, 'example.html', context)

def report(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)

    if request.method == 'POST':
        city = request.POST['citycountry']
        queryset = CityInfos.objects.filter(cityname=city)
    else:
        queryset = CityInfos.objects.all()

    lines = []
    for var in queryset:
        formatted_date = var.c_date.strftime("%Y-%m-%d")
        lines.append(f"* ID is: {var.id}")
        lines.append(f"* City name is: {var.cityname}")
        lines.append(f"* Temperature is: {var.temperature}")
        lines.append(f"* Humidity is: {var.humidity}")
        lines.append(f"* Date is: {formatted_date}")
        lines.append("- - - - - - - - - - - - - - - -")

    lines_per_page = 42 
    line_count = 0
    for line in lines:
        textob.textLine(line)
        line_count += 1
        if line_count == lines_per_page:
            c.drawText(textob)
            c.showPage()
            textob = c.beginText()
            textob.setTextOrigin(inch, inch)
            textob.setFont("Helvetica", 14)
            line_count = 0

    if line_count > 0:
        c.drawText(textob)
        c.showPage()

    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='report.pdf')