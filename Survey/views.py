from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from .models import Client, Surveyor, Payment, TitleProcess, TitleDocument, send_mobile_sasa_message
from .forms import TitleDocumentForm
from .forms import ClientForm
def dashboard(request):
    return render(request, 'admin-dash.html')

def surveyors(request):
    surveyors = Surveyor.objects.all()
    return render(request, 'surveyors.html', {'surveyors': surveyors})

def clients(request):
    clients = Client.objects.all()
    return render(request, 'clients.html', {'clients': clients})

# ✅ Updated client details view with process update fix
def client_view_details(request, object_id):
    client = get_object_or_404(Client, id=object_id)
    processes = TitleProcess.objects.filter(type=client.service)
    documents = TitleDocument.objects.filter(client=client)  # Get related documents

    if request.method == 'POST':
        new_process_id = request.POST.get("process")  # Fixed `Post` to `POST`
        if new_process_id:
            new_process = get_object_or_404(TitleProcess, id=new_process_id)
            client.process = new_process
            client.save()

            # Get custom message
            custom_message = new_process.message
            send_mobile_sasa_message(client.phone, custom_message)

            return JsonResponse({"success": True, "message": f"Process update: {custom_message}"})

    return render(request, 'client_view_details.html', {'client': client, "processes": processes, "documents": documents})

# ✅ New: View for uploading title deed documents
@login_required
def upload_title_document(request):
    if request.method == "POST":
        form = TitleDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('clients')  # Redirect after successful upload
    else:
        form = TitleDocumentForm()
    return render(request, 'upload_title_document.html', {'form': form})

def payments(request):
    payments = Payment.objects.all()
    return render(request, 'payments.html', {'payments': payments})

def registered_surveyor(request):
    return render(request, 'registered_surveyor.html')

def messages(request):
    return render(request, 'messages.html')

def new_payment(request):
    return render(request, 'new_payment.html')

def surveyor_view_details(request, object_id):
    surveyor = get_object_or_404(Surveyor, id=object_id)
    return render(request, 'surveyor_view_details.html', {'surveyor': surveyor})

def payment_details(request, object_id):
    payment = get_object_or_404(Payment, id=object_id)
    return render(request, 'payment_details.html', {'payment': payment})
@login_required
def client_dashboard(request):
    client = get_object_or_404(Client, username=request.user.username)
    form = ClientForm(instance=client)

    if request.method == 'POST':
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect('client_dashboard')

    documents = []  # Add your logic to fetch uploaded documents

    return render(request, 'client_dashboard.html', {
        'client': client,
        'form': form,
        'documents': documents
    })
