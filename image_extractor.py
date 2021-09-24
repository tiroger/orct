# Importing libraries
import os
import fitz # PyMuPDF
import io
from PIL import Image



def extract_images(source, file, destination):
    # Directory where images are saved
    if not os.path.exists(destination):
        os.mkdir(destination)

    # Opening the pdf file
    pdf_directory = source
    pdf_file = os.path.join(pdf_directory, file)

    pdf = fitz.open(pdf_file) 

    # Iterating over all pages
    for page_number in range(len(pdf)):
        # Getting the page
        current_page = pdf[page_number]
        image_list = current_page.getImageList()
        
        # Printing number of images found in the current page
        if image_list:
            print(f"[+] Found {len(image_list)} images in page {page_number}")
        else:
            print("[!] No images found on page", page_number)
        
        for image_index, img in enumerate(current_page.getImageList(), start=1):
            # Getting the XREF of the image
            xref = img[0]
            # Extracting the image bytes
            base_image = pdf.extractImage(xref)
            image_bytes = base_image["image"]
            # Getting the image extension
            image_ext = base_image["ext"]
            # Loading the image to PIL
            image = Image.open(io.BytesIO(image_bytes))
            
            
            # directory = path
            # Parent Directory path
            parent_dir = "./"
            # Path
            destination_path = os.path.join(parent_dir, destination, file)
  
            # Checking whether the specified path already exists
            if not os.path.exists(destination_path):
                mode = 0o777 # Writable directory
                os.mkdir(destination_path, mode)
                print("Directory '% s' created" % destination_path)
            
            # Saving image to local disk
            image.save(open(f"{destination_path}/{file}_image{page_number+1}_{image_index}.{image_ext}", "wb"))
    print("Image extraction completed!")


# Specifiy the path name where the PDF documents are located
source = './PDFs'
pdf_files = os.listdir(source)

# Give a name to the distination folder
desintation = 'extracted_images'

for pdf in pdf_files:
    extract_images(source, pdf, desintation)