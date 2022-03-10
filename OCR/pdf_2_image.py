from pdf2image import convert_from_path
 
 
# Store Pdf with convert_from_path function
images = convert_from_path('/home/taha/Desktop/Stromberg PDF.pdf',500,last_page=15)
 
for i in range(len(images)):
   
      # Save pages as images in the pdf
    images[i].save('pdf_1_images/page'+ str(i) +'.jpg', 'JPEG')