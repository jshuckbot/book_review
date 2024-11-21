from weasyprint import HTML, CSS


def generate_pdf(url, pdf_file):
    css = CSS(string='body{font-size: 8px; }')
    HTML(url).write_pdf(pdf_file, stylesheets=[css])
    
    
if __name__ == '__main__':
    url = 'https://text.npr.org'
    pdf_file = 'demo_page.pdf'
    generate_pdf(url, pdf_file)