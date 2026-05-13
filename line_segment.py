import cv2
import os

def segment_lines(image_path):

    # Read image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Binary inverse threshold
    thresh = cv2.threshold(
        gray,
        150,
        255,
        cv2.THRESH_BINARY_INV
    )[1]

    # ============================================
    # MERGE WORDS INTO LINES
    # ============================================

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (100, 5)
    )

    dilated = cv2.dilate(
        thresh,
        kernel,
        iterations=1
    )

    # ============================================
    # FIND CONTOURS
    # ============================================

    contours, _ = cv2.findContours(
        dilated,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # ============================================
    # OUTPUT FOLDER
    # ============================================

    output_folder = "segmented_lines"

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # Delete old files
    for file in os.listdir(output_folder):

        file_path = os.path.join(
            output_folder,
            file
        )

        if os.path.isfile(file_path):
            os.remove(file_path)

    # ============================================
    # STORE BOXES
    # ============================================

    boxes = []

    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)

        # Ignore tiny regions
        if w > 200 and h > 20:
            boxes.append((x, y, w, h))

    # Sort top-to-bottom
    boxes = sorted(
        boxes,
        key=lambda b: b[1]
    )

    line_images = []

    # ============================================
    # SAVE LINES
    # ============================================

    for idx, (x, y, w, h) in enumerate(boxes):

        # Add padding
        padding = 10

        line = image[
            max(y-padding, 0):min(y+h+padding, image.shape[0]),
            max(x-padding, 0):min(x+w+padding, image.shape[1])
        ]

        line_path = (
            f"{output_folder}/line_{idx+1}.jpg"
        )

        cv2.imwrite(line_path, line)

        line_images.append(line_path)

        print(f"Saved: {line_path}")

    return line_images