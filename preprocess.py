import cv2

def preprocess_image(input_path, output_path):

    # Read image
    image = cv2.imread(input_path)

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Noise removal
    denoised = cv2.fastNlMeansDenoising(
        gray,
        None,
        30,
        7,
        21
    )

    # Thresholding
    threshold = cv2.adaptiveThreshold(
        denoised,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )

    # Sharpening kernel
    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (1, 1)
    )

    sharpened = cv2.morphologyEx(
        threshold,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Save processed image
    cv2.imwrite(output_path, sharpened)

    print("Preprocessed image saved:", output_path)