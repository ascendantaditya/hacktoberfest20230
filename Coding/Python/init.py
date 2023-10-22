# Standard Library Imports
import os
import base64
import tempfile
import PyPDF2  # Import PyPDF2 for PDF compression
# Third-Party Library Imports
import streamlit as st
from fpdf import FPDF

# Set Streamlit page configuration
st.set_page_config(page_title='PDFMaker', page_icon=':memo:', layout='wide')

def generate_pdf(name, reg_num, ass_name, text_in, file):
    # PDF generation code goes here
    pdf = FPDF()
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Header
    pdf.cell(200, 10, txt=ass_name, ln=True, align="C")
    pdf.cell(200, 10, txt=f"Name: {name}", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Registration Number: {reg_num}", ln=True, align="C")

    # Content
    pdf.multi_cell(0, 10, txt=text_in)
    _, file_extension = os.path.splitext(file.name)
    # If a file is uploaded, save it to a temporary file and include it in the PDF
    if file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_image:
            temp_image.write(file.read())
            temp_image.seek(0)
            pdf.image(temp_image.name, x=10, w=190)

    pdf_filename = f"{name}_{ass_name}.pdf"
    pdf.output(pdf_filename)

    # Perform PDF compression using PyPDF2
    pdf_compression_filename = "compressed_" + pdf_filename
    with open(pdf_filename, "rb") as source_file:
        pdf_reader = PyPDF2.PdfFileReader(source_file)
        pdf_writer = PyPDF2.PdfFileWriter()

        for page_num in range(pdf_reader.numPages):
            page = pdf_reader.getPage(page_num)
            page.compressContentStreams()  # Compress the content streams
            pdf_writer.addPage(page)

        with open(pdf_compression_filename, "wb") as compressed_file:
            pdf_writer.write(compressed_file)

    return pdf_compression_filename  # Return the compressed PDF filename

# Create a sidebar
with st.sidebar:
    st.title('PDFMaker')
    st.markdown('An easy tool to help you make your assignments into a PDF in seconds.')
    st.markdown('Just four simple steps,')

    # Add some styling to each item
    list_item_spacing = "  \n"
    list_item_prefix = "👉 **"

    # Fill the details
    sidebar_content = ""
    sidebar_content += list_item_prefix + "Fill in the assignment details" + list_item_prefix + list_item_spacing

    # Enter content to print on the first page
    sidebar_content += list_item_prefix + "Enter the content for the first page" + list_item_prefix + list_item_spacing

    # Upload the images of your assignment
    sidebar_content += list_item_prefix + "Upload images of your assignment" + list_item_prefix + list_item_spacing

    # Click on "Generate PDF" button
    sidebar_content += list_item_prefix + 'Click on the "Generate PDF" button' + list_item_prefix + list_item_spacing

    # Add some celebratory emojis
    sidebar_content += "Voila! Your assignment PDF is downloaded. 🥳" + list_item_spacing

    # Apply Markdown formatting
    st.markdown(sidebar_content)

# Title
st.title('PDF Maker')

# Inputs
user_name = st.text_input('Enter your name')
reg_num = st.text_input('Enter your registration number')
ass_name = st.text_input('Enter assignment name')
user_text_input = st.text_area('Enter anything you want to be printed on the first page: ')

# Create a File Upload widget with customization options
uploaded_file = st.file_uploader(
    label="Choose a file",
    type=["jpg", "png"],  # Specify the allowed file types
    accept_multiple_files=False,  # Set to True if you want to allow multiple file uploads
    help="Upload JPG or PNG files",  # Custom help text
    key="file_uploader"  # Set a unique key to customize the widget
)

if st.button('Generate PDF'):
    if user_name and reg_num and ass_name:
        pdf_filename = generate_pdf(user_name, reg_num, ass_name, user_text_input, uploaded_file)
        st.success('PDF generated successfully.')

        # Read the PDF data from the generated file
        with open(pdf_filename, "rb") as f:
            pdf_data = f.read()

        # Create a download button to download the generated PDF
        st.download_button(label="Download",
                            data=pdf_data,
                            file_name=f'{user_name}_{ass_name}.pdf',
                            mime='text',)

    else:
        st.error('Please fill in all required fields.')
from pypdf import PdfReader,PdfWriter

reader = PdfReader ("Your Document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.compress_content_streams() #This is CPU Intensive
    writer.add_page(page)
    
with open("out.pdf","wb") as f :
    writer.write(f)
    
print('Compressed Successfully')
