import os
import shutil

# =========================================================
# DELETE OLD GENERATED FILES
# =========================================================

def clear_old_files():

    folders = [
        "segmented_lines",
        "images",
        "pdf_pages"
    ]

    for folder in folders:

        if os.path.exists(folder):

            shutil.rmtree(folder)

        os.makedirs(folder)

    print("\n==============================")
    print("OLD FILES REMOVED")
    print("==============================")