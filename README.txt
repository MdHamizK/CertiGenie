# Birth & Death Certificate Generator

## Overview
This project generates digitally verifiable Birth and Death Certificates using structured user input and secure PDF generation.

## Features
- Form-based CLI data entry.
- Auto-generated certificate ID and date.
- PDF certificate generation using FPDF2.
- Optional QR code integration for verification.
- Automatic CSV logging of issued certificates for record keeping.

## Requirements
- Python 3.x
- Libraries: `fpdf2`, `qrcode[pil]`

## Installation
Run:
pip install fpdf2 qrcode[pil]

##Steps to Run

1. Run the script: python generate_certificate.py
2. Choose between:
-> 1 for Birth Certificate.
-> 2 for Death Certificate.
3. Enter required details in the terminal
4. A formatted PDF will be saved in the certificates/ folder
5. All issued certificates are automatically logged in certificates_log.csv

## Folder Structure
- /certificates → Generated PDFs.
- /static/qrcodes → QR codes for each certificate.
- /static/fonts → Optional assets.
- /static/bg_images → Background Image for PDF.
- static/certificates_log.csv → Log of all issued certificates.

##CSV Logging Details
Each time a certificate is generated, the following details are recorded in certificates_log.csv:

FIELD                         |           DESCRIPTION

Certificate ID                |     Auto-generated unique ID
Full Name                     |     Name of child/deceased 
Certificate Type              |     Birth or Death
Issue Date                    |     Date when certificate was generated
Date of Event                 |     DOB or DOD
Gender                        |     Male/Female/Other
Registration Number           |     Provided during form input
File Path                     |     Location of the generated PDF

## Optional Enhancements
- Convert CLI to GUI using Flask.
- Store issued certificates in a CSV or database.
- Add digital signatures or encryption.
- Create a web interface for municipal staff.