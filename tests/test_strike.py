from backend.utils.text_classifier import is_strike_text

samples = [

    "/////// cancelled ///////",
    
    "xxxxxxxxxxxxxxxx",
    
    "-------------------",
    
    "The earth revolves around the sun",
    
    "Cloud computing provides storage",
    
    "Machine learning uses data",
    
    "______/\\/\\/\\/_____",
    
    "AI simulates human intelligence"
]

for text in samples:

    result = is_strike_text(text)

    print(f"{text} --> {result}")