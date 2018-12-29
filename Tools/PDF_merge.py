import PyPDF2

def merge_PDF(pdf_file1,pdf_file2):

    file1 = open(pdf_file1,'rb')
    file2 = open(pdf_file2,'rb')

    pdf_reader1 = PyPDF2.PdfFileReader(file1)
    pdf_reader2 = PyPDF2.PdfFileReader(file2)

    pdf_merger = PyPDF2.PdfFileMerger()
    pdf_merger.append(pdf_reader1)
    pdf_merger.append(pdf_reader2)

    file_output = open('output.pdf','wb')
    pdf_merger.write(file_output)

    file1.close()
    file2.close()
    file_output.close()


#merge_PDF ('1.pdf', '2.pdf')  
