import cv2
import os

def segment_lines(
    image_path,
    page_number
):

    # ============================================
    # READ IMAGE
    # ============================================

    image = cv2.imread(image_path)

    if image is None:
        print("ERROR: Unable to read image.")
        return []

    # ============================================
    # CONVERT TO GRAYSCALE
    # ============================================

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # ============================================
    # BINARY INVERSE THRESHOLD
    # ============================================

    thresh = cv2.threshold(
        gray,
        150,
        255,
        cv2.THRESH_BINARY_INV
    )[1]

    # ============================================
    # IMPROVED WORD MERGING
    # PREVENTS MULTI-LINE MERGING
    # ============================================

    kernel = cv2.getStructuringElement(
        cv2.MORPH_RECT,
        (100, 4)
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
    # PAGE-WISE OUTPUT FOLDER
    # ============================================

    output_folder = (
        f"segmented_lines/page_{page_number}"
    )

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # ============================================
    # DELETE OLD FILES INSIDE PAGE FOLDER
    # ============================================

    for file in os.listdir(output_folder):

        file_path = os.path.join(
            output_folder,
            file
        )

        if os.path.isfile(file_path):

            os.remove(file_path)

    # ============================================
    # STORE VALID BOXES
    # ============================================

    boxes = []

    for contour in contours:

        x, y, w, h = cv2.boundingRect(contour)

        # Ignore tiny noise regions

        if w > 180 and h > 25:

            boxes.append((x, y, w, h))

    # ============================================
    # SMART LINE ORDERING
    # ============================================

    # First sort top-to-bottom

    sorted_boxes = sorted(
        boxes,
        key=lambda b: b[1]
    )

    grouped_lines = []

    # Same-line threshold

    threshold = 50

    for box in sorted_boxes:

        x, y, w, h = box

        added = False

        # ----------------------------------------
        # CHECK EXISTING GROUPS
        # ----------------------------------------

        for group in grouped_lines:

            _, gy, _, gh = group[0]

            # Same line detection

            if abs(y - gy) < threshold:

                group.append(box)

                added = True

                break

        # ----------------------------------------
        # CREATE NEW GROUP
        # ----------------------------------------

        if not added:

            grouped_lines.append([box])

    # ============================================
    # SORT LEFT TO RIGHT INSIDE EACH GROUP
    # ============================================

    final_boxes = []

    for group in grouped_lines:

        group = sorted(
            group,
            key=lambda b: b[0]
        )

        final_boxes.extend(group)

    boxes = final_boxes

    line_images = []

    # ============================================
    # SAVE SEGMENTED LINES
    # ============================================

    for idx, (x, y, w, h) in enumerate(boxes):

        # Padding

        padding_x = 20
        padding_y = 15

        x1 = max(x - padding_x, 0)
        y1 = max(y - padding_y, 0)

        x2 = min(
            x + w + padding_x,
            image.shape[1]
        )

        y2 = min(
            y + h + padding_y,
            image.shape[0]
        )

        # Crop line

        line = image[
            y1:y2,
            x1:x2
        ]

        line_path = (
            f"{output_folder}/line_{idx+1}.jpg"
        )

        cv2.imwrite(line_path, line)

        line_images.append(line_path)

        print(f"Saved: {line_path}")

        print(
            f"Line {idx+1} -> "
            f"x:{x}, y:{y}, w:{w}, h:{h}"
        )

    # ============================================
    # FINAL STATUS
    # ============================================

    print(
        f"\nTotal Valid Lines Segmented: "
        f"{len(line_images)}"
    )

    return line_images