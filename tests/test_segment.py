from backend.preprocess import preprocess_image
from backend.line_segment import segment_lines

# Original image
original_image = "images/student_answer.jpg"

# Processed image
processed_image = "images/processed.jpg"

# Step 1: Preprocess image
preprocess_image(
    original_image,
    processed_image
)

# Step 2: Segment lines
segment_lines(processed_image)