from fpdf import FPDF, XPos, YPos
import datetime
import random
import string
import csv
import os
from datetime import datetime
from qr_utils import generate_qr

def get_current_date():
    return datetime.now().strftime("%d-%m-%Y")

def generate_cert_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def create_certificate(cert_type, data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Loading font 
    FONT_NAME = "IBMPlexSerifBold"
    TTF_FONT_PATH = os.path.join("static", "fonts", "IBMPlexSerif-Bold.ttf")
    pdf.add_font(FONT_NAME, fname=TTF_FONT_PATH)
    pdf.set_font(FONT_NAME, size=12)

    # Using Background image
    if cert_type == "birth":
        bg_path = os.path.join("static", "bg_images", "Birth_certificate.png")
    else:
        bg_path = os.path.join("static", "bg_images", "Death_certificate.png")

    if os.path.exists(bg_path):
        pdf.image(bg_path, x=0, y=0, w=210, h=297)  # A4 Size
    else:
        print(f"Warning: Background image not found at {bg_path}")

    # Headers
    pdf.set_font(FONT_NAME, size=16)
    pdf.cell(w=0, h=30, text="Government of India", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')

    # Certificate title
    title = "Birth Certificate" if cert_type == "birth" else "Death Certificate"

    # Setting font
    pdf.set_font(FONT_NAME, size=12)

    # Certificate ID and Issue Date
    cert_id = generate_cert_id()
    issue_date = get_current_date()

    # Alignment and text

    pdf.set_x(135)
    pdf.cell(w=0, h=-8, text=f"Certificate ID: {cert_id}")
    pdf.ln(4)

    pdf.set_x(140)
    pdf.cell(w=0, h=-2, text=f"Issue Date: {issue_date}")
    pdf.ln(2)
    pdf.set_y(170)

    pdf.set_x(25)
    pdf.cell(w=0, h=10, text=f"Full Name : {data['Full Name']}")
    pdf.ln(10)

    pdf.set_x(25)
    if cert_type == "birth":
        pdf.cell(w=0, h=10, text=f"Date of Birth : {data['Date of Birth']}")
    else:
        pdf.cell(w=0, h=10, text=f"Date of Death : {data['Date of Death']}")
    pdf.ln(10)

    pdf.set_x(25)
    pdf.cell(w=0, h=10, text=f"Gender : {data['Gender']}")
    pdf.ln(10)

    pdf.set_x(25)
    if cert_type == "birth":
        pdf.cell(w=0, h=10, text=f"Place of Birth : {data['Place of Birth']}")
    else:
        pdf.cell(w=0, h=10, text=f"Place of Death : {data['Place of Death']}")
    pdf.ln(10)

    pdf.set_x(25)
    if cert_type == "birth":
        pdf.cell(w=0, h=10, text=f"Parents : {data['Father/Mother Name']}")
    else:
        pdf.cell(w=0, h=10, text=f"Relative Name : {data['Relative Name']}")
    pdf.ln(10)

    pdf.set_x(25)
    pdf.cell(w=0, h=10, text=f"Address : {data['Address']}")
    pdf.ln(10)

    pdf.set_x(25)
    pdf.cell(w=0, h=10, text=f"Registration Number : {data['Registration Number']}")
    pdf.ln(10)

    pdf.set_x(25)
    pdf.cell(w=0, h=10, text="Issuing Authority : Municipal Officer")

    # Generating QR Code

    title = "Birth Certificate" if cert_type == "birth" else "Death Certificate"
    qr_data = f"{title} | ID: {cert_id} | Issued on: {issue_date}"
    qr_path = f"static/qrcodes/{cert_id}_qr.png"
    os.makedirs("static/qrcodes", exist_ok=True)
    generate_qr(qr_data, qr_path)
    pdf.image(qr_path, x=150, y=230, w=30, h=30)

    # Save as PDF
    name = data.get("Full Name", "Unknown")
    safe_name = "".join(c if c.isalnum() else "_" for c in name).strip("_")
    os.makedirs("certificates", exist_ok=True)
    filename = os.path.join("certificates", f"{safe_name}_{cert_type}.pdf")
    pdf.output(filename)
    print(f"\n✅ Certificate saved at: {filename}")

    # Logging Access in the certificate
    log_certificate(
        cert_type=cert_type,
        data=data,
        cert_id=cert_id,
        issue_date=issue_date,
        filename=filename
    )

# USER INPUT FORM (CLI Version) 

def collect_birth_data():
    print("\nEnter Birth Certificate Details:")
    name = input("Name of Child: ")
    dob = input("Date of Birth (YYYY-MM-DD): ")
    gender = input("Gender: ")
    place = input("Place of Birth: ")
    father = input("Father's Name: ")
    mother = input("Mother's Name: ")
    address = input("Address: ")
    regno = input("Registration Number: ")

    return {
        "Full Name": name,
        "Date of Birth": dob,
        "Gender": gender,
        "Place of Birth": place,
        "Father/Mother Name": f"Father: {father}, Mother: {mother}",
        "Address": address,
        "Registration Number": regno,
    }

def collect_death_data():
    print("\nEnter Death Certificate Details : ")
    name = input("Name of Deceased : ")
    dod = input("Date of Death (DD-MM-YYYY) : ")
    gender = input("Gender : ")
    place = input("Place of Death : ")
    relative = input("Relative's Name : ")
    address = input("Address : ")
    regno = input("Registration Number : ")

    return {
        "Full Name": name,
        "Date of Death": dod,
        "Gender": gender,
        "Place of Death": place,
        "Relative Name": relative,
        "Address": address,
        "Registration Number": regno,
    }

def log_certificate(cert_type, data, cert_id, issue_date, filename):
    log_file = "certificates_log.csv"

    # Creating file with headers for Once
    if not os.path.exists(log_file):
        with open(log_file, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "Certificate ID",
                "Full Name",
                "Certificate Type",
                "Issue Date",
                "Date of Event",
                "Gender",
                "Registration Number",
                "File Path"
            ])

    # Extracting event date based on certificate type
    date_of_event = data.get("Date of Birth", "") if cert_type == "birth" else data.get("Date of Death", "")

    # Automatic Updation of the certificate data to CSV
    try:
        with open(log_file, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                cert_id,
                data.get("Full Name", "Unknown"),
                cert_type.capitalize(),
                issue_date,
                date_of_event,
                data.get("Gender", "Unknown"),
                data.get("Registration Number", "Unknown"),
                filename
            ])
            f.flush()
    except PermissionError:    # For Professionally handling file permission issues
        print("Warning: Could not write to log file. File may be open or locked.")
    print(f"✅ Logged certificate to CSV: {data.get('Full Name', 'Unknown')} ({cert_type})")

# MAIN FUNCTION 

def main():
    print("The Birth & Death Certificate Generator")
    print("Select certificate type : ")
    print("1. Birth Certificate")
    print("2. Death Certificate")
    choice = input("Enter option (1 or 2) : ")

    if choice == "1":
        data = collect_birth_data()
        create_certificate("birth", data)
    elif choice == "2":
        data = collect_death_data()
        create_certificate("death", data)
    else:
        print("Invalid choice!")

if __name__ == "__main__":
    main()
