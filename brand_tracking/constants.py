"""
Default questions for Brand Tracking Tool
10 questions total, organized into 5 categories
Each question scored 1-10 for a total of 100 points
"""

BRAND_TRACKING_QUESTIONS = {
    'brand_representation': {
        'display_name': 'Brand Representation',
        'order': 1,
        'questions': [
            'How prominently is the brand featured in this coverage?',
            'How well are the key brand messages included and communicated?',
        ]
    },
    'tone_sentiment': {
        'display_name': 'Tone & Sentiment',
        'order': 2,
        'questions': [
            'How positive is the overall tone of this coverage?',
            'How much does this coverage enhance the brand\'s credibility?',
        ]
    },
    'reach_impact': {
        'display_name': 'Reach & Impact',
        'order': 3,
        'questions': [
            'How significant is the reach of this publication/outlet?',
            'How well does the audience match the brand\'s target demographic?',
        ]
    },
    'content_quality': {
        'display_name': 'Content Quality',
        'order': 4,
        'questions': [
            'How accurate and factual is the coverage?',
            'How comprehensive is the depth of coverage?',
        ]
    },
    'strategic_value': {
        'display_name': 'Strategic Value',
        'order': 5,
        'questions': [
            'How valuable is this coverage for SEO and backlink purposes?',
            'How likely is this coverage to drive business results?',
        ]
    },
}
