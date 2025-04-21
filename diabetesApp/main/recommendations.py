def generate_recommendations(patient_data_scaled, patient_data_imputed, prediction):
    try:
        # Extract features from the imputed data (already in original scale)
        glucose = patient_data_imputed[0][1]
        insulin = patient_data_imputed[0][2]
        bmi = patient_data_imputed[0][3]
        age = patient_data_imputed[0][5]

        recommendation_mapping = {
            0: 'You are not diabetic. 😊',
            1: 'You are diabetic. 🩺',
            2: 'You are still at risk: Your glucose levels are elevated or there is a family history of diabetes. It is important to monitor your glucose and blood pressure. Lifestyle changes like a healthier diet and regular physical activity are highly recommended.',
            3: 'You’re doing well: Keep up your healthy habits! Regular check-ups are important to ensure you maintain good health.',
            4: 'Your glucose levels are high. Medication may be necessary, along with frequent monitoring. In addition, managing your diet and staying physically active are essential to control your condition.',
            5: 'Your glucose levels are under moderate control, but ongoing monitoring and a balanced diet are still crucial. Consider incorporating more physical activity and regularly consulting with your healthcare provider.',
            6: 'Though you have diabetes, your family history and other factors (e.g., age, BMI) suggest a higher risk of complications. It is essential to maintain regular check-ups and follow a strict diet and exercise plan.',
            7: 'You are overweight but not diabetic. It is important to maintain a healthy diet and engage in regular physical activity to reduce health risks.',
            8: 'You are diabetic and overweight. Managing your weight through a balanced diet and exercise is crucial to avoid complications.',
        }

        # Initialize default recommendations
        diabetes_status = recommendation_mapping[1]  # Default to diabetic
        recommendation = recommendation_mapping[6]  # Default to high-risk

        # Conditions for non-diabetic
        if prediction == 0:
            if glucose > 100:  # Elevated glucose
                recommendation = recommendation_mapping[2]
            elif bmi > 30:  # Overweight condition for non-diabetic
                recommendation = recommendation_mapping[7]
            else:
                recommendation = recommendation_mapping[3]
            diabetes_status = recommendation_mapping[0]

        # Conditions for diabetic
        else:
            if glucose > 150:  # High glucose condition
                if bmi > 30:  # Overweight condition for diabetic
                    recommendation = recommendation_mapping[8]
                else:
                    recommendation = recommendation_mapping[4]
            elif 100 < glucose <= 150:  # Moderate glucose condition
                recommendation = recommendation_mapping[5]
            elif bmi > 30:  # Overweight condition for diabetic
                recommendation = recommendation_mapping[8]
            elif insulin > 200 or age > 50:  # Default to high risk
                recommendation = recommendation_mapping[6]

        return {
            'status': diabetes_status,
            'recommendation': recommendation,
            'health_metrics': {
                'glucose': glucose,
                'insulin': insulin,
                'bmi': bmi,
                'age': age
            }
        }

    except Exception as e:
        return {
            'error': str(e)
        }