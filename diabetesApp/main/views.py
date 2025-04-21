from django.http import JsonResponse
import logging
from .utils import model, scaler, imputer, validate_input, preprocess_input
from .recommendations import generate_recommendations

logger = logging.getLogger(__name__)
from django.shortcuts import render


def home(request):
    return render(request, 'index.html')


def predict_diabetes(request):
    if request.method == 'POST':
        try:
            # Get raw input data
            input_data = {
                'Pregnancies': request.POST.get('pregnancies', 0),
                'Glucose': request.POST.get('glucose'),
                'Insulin': request.POST.get('insulin'),
                'BMI': request.POST.get('bmi'),
                'DiabetesPedigreeFunction': request.POST.get('pedigree'),
                'Age': request.POST.get('age')
            }
            
            # Validate and convert types
            validated_data = validate_input(input_data)
            
            # Preprocess (impute + scale)
            patient_data_scaled, patient_data_imputed = preprocess_input(validated_data)
            
            # Make prediction
            proba = model.predict_proba(patient_data_scaled)[0]
            prediction = int(model.predict(patient_data_scaled)[0])
            
            # Generate recommendations
            recommendation = generate_recommendations(
                patient_data_scaled,
                patient_data_imputed,
                prediction
            )
            
            return JsonResponse({
                'success': True,
                'prediction': prediction,
                'probability': float(proba[1]),
                'recommendation': recommendation,
                'input_data': validated_data
            })
            
        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)