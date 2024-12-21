import cohere
import pdfplumber

# Set your Cohere API key
co = cohere.Client("TeOtelSUJiwoyJui9dYHWf4k0qdbGsNZDPbkXRWu")

# Function to extract all text from the PDF
def extract_text_from_pdf(pdf_path):
    try:
        with pdfplumber.open(pdf_path) as pdf:
            # Extract text from all pages
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"  # Append text from each page
        return text.strip()  # Return the full text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None

# Function to get a report from Cohere, including role suggestion
def get_report_from_cohere(text):
    # The prompt you want to send to the Cohere model for analysis
    prompt = f"""
    Please analyze the following resume text and provide a detailed report with the following sections:
    
    1. **Grammatical Errors**: Identify any grammatical or syntactical issues in the resume.
    2. **Improvements**: Suggest improvements to the content, structure, and presentation of the resume.
    3. **Suggestions**: Recommend any additional details or information that would enhance the resume.
    4. **Overall Thoughts**: Summarize the strengths and weaknesses of the resume, and provide general feedback.
    5. **Suggested Role**: Based on the skills and experience in the resume, suggest the most suitable job role for the candidate.

    Resume Text:
    {text}
    """

    # Call Cohere API to analyze the resume text
    response = co.generate(
        model="command-r-plus-04-2024",  # Use a suitable model
        prompt=prompt,
        max_tokens=1500,  # Increase tokens for more detailed output
        temperature=0.7  # Adjust temperature for creativity in suggestions
    )
    
    # The result is in response['generations'][0]['text']
    report = response.generations[0].text.strip()  # Access the generated text from the response
    return report

# Function to process the PDF and generate a report
def process_pdf_and_generate_report(pdf_path):
    print("Extracting text from PDF...")
    text = extract_text_from_pdf(pdf_path)
    if not text:
        raise Exception("No text extracted from the PDF. Ensure the file is not scanned or image-based.")
    
    print(f"\nExtracted Text:\n{text[:1000]}...")  # Print the first 1000 characters for brevity
    
    # Generate report for the full content
    print("\nGenerating report for the extracted text...\n")
    report = get_report_from_cohere(text)
    return report

# Provide the correct file path to your PDF
pdf_path = r"C:\Users\Sher Ali\Downloads\SherAli Resume.pdf"

# Generate the report
try:
    report = process_pdf_and_generate_report(pdf_path)
    if report:
        print("\n--- Generated Report ---\n")
        print(report)
except Exception as e:
    print(f"Error: {e}")
