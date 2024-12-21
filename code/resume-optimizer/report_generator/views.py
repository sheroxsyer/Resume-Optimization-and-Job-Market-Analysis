from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import os
from .forms import UploadPDFForm
from .utils import process_pdf_and_generate_report, extract_text_from_pdf
from .ml_utils import get_job_recommendations, analyze_job_market_trends

def index(request):
    return render(request, 'index.html')

def home(request):
    return HttpResponse("Hello, world. You're at the report_generator index.")

def upload_pdf(request):
    if request.method == 'POST':
        form = UploadPDFForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = request.FILES['pdf_file']
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, pdf_file.name)
            
            try:
                with open(temp_path, 'wb+') as destination:
                    for chunk in pdf_file.chunks():
                        destination.write(chunk)

                # Extract text from PDF
                resume_text = extract_text_from_pdf(temp_path)
                
                # Process PDF and generate report
                report = process_pdf_and_generate_report(temp_path)
                
                # Get job recommendations based on resume text
                recommendations = get_job_recommendations(resume_text)
                
                # Get trend analysis for top recommendation
                trend_analysis = analyze_job_market_trends(recommendations[0][0] if recommendations else "Software Engineer")
                
                context = {
                    'report': report,
                    'recommendations': recommendations,
                    'trend_analysis': trend_analysis
                }
                
                os.remove(temp_path)  # Clean up
                return render(request, 'report.html', context)
                
            except Exception as e:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                return render(request, 'error.html', {
                    'error': f"Error processing file: {str(e)}. Please try again with a different PDF."
                })
    else:
        form = UploadPDFForm()

    return render(request, 'index.html', {'form': form})

def get_job_trends(request):
    job_title = request.GET.get('job_title', 'Software Engineer')
    trend_data = analyze_job_market_trends(job_title)
    return JsonResponse(trend_data)

def get_recommendations(request):
    job_preference = request.POST.get('preference', '')
    if not job_preference:
        return JsonResponse({'error': 'Job preference is required'}, status=400)
        
    recommendations = get_job_recommendations(job_preference)
    return JsonResponse({'recommendations': recommendations})