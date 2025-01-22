
COLUMNS: dict[str, str] = {
    'Age': 'int64',
    'Gender': 'object',
    'Years at Company': 'int64',
    'Job Role': 'object',
    'Monthly Income': 'int64',
    'Work-Life Balance': 'object',
    'Job Satisfaction': 'object',
    'Performance Rating': 'object',
    'Number of Promotions': 'int64',
    'Overtime': 'object',
    'Distance from Home': 'int64',
    'Education Level': 'object',
    'Marital Status': 'object',
    'Number of Dependents': 'int64',
    'Job Level': 'object',
    'Company Size': 'object',
    'Company Tenure': 'int64',
    'Remote Work': 'object',
    'Leadership Opportunities': 'object',
    'Innovation Opportunities': 'object',
    'Company Reputation': 'object',
    'Employee Recognition': 'object'
}

SCALE_COLUMNS: list[str] = [
    'Age',
    'Years at Company',
    'Monthly Income',
    'Number of Promotions',
    'Distance from Home',
    'Company Tenure',
    'Number of Dependents'
]

OH_ENC_COLUMNS: list[str] = [
    'Job Role',
    'Work-Life Balance',
    'Job Satisfaction',
    'Performance Rating',
    'Marital Status',
    'Education Level',
    'Job Level',
    'Company Size',
    'Company Reputation',
    'Employee Recognition'
]

ORD_ENC_COLUMNS: list[str] = [
    'Remote Work',
    'Overtime',
    'Leadership Opportunities',
    'Innovation Opportunities'
]