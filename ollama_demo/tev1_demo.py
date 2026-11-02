import ollama

year = "2022"

response = ollama.systemone(
    model='tev1:0.8b',
    state='Hello',
    questions={
        'check_year': {
            'type': 'choice',
            'instructions': f'Are we living in year {year}?',
            'criteria': {
                'true': f'Means we are living in {year}.',
                'false': f'Means we are not living in {year}.',
            },
        },
    },
)
print(response.answers['check_year'])