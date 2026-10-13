"""Generate the synthetic PDF pack + answer_key.json.
Usage: pip install fpdf2 pillow && python documents/generate_docs.py
Digital PDFs carry real text; *_scanned.pdf files are image-only (need OCR).
Every page is clearly marked synthetic. No real agencies, people or ID formats.
"""
import json
import random
from pathlib import Path

from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFilter

OUT = Path(__file__).resolve().parent
rng = random.Random(7)
BANNER = "SYNTHETIC SAMPLE - AI BUILD DAY - NOT A REAL GOVERNMENT DOCUMENT"


def new_pdf():
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(160, 60, 60)
    pdf.cell(0, 5, BANNER, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(2)
    return pdf


def head(pdf, agency, office, title, docno, date):
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 6, agency, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, office, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 7, title, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(95, 6, f"Document No.: {docno}")
    pdf.cell(0, 6, f"Date: {date}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)


def fields(pdf, pairs):
    pdf.set_font("Helvetica", "", 10)
    for k, v in pairs:
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(58, 6.5, k + ":")
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6.5, str(v), new_x="LMARGIN", new_y="NEXT")


def sig(pdf, label, name, title):
    pdf.ln(9)
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, label, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(7)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 5, name.upper(), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 9)
    pdf.cell(0, 5, title, new_x="LMARGIN", new_y="NEXT")


def save(pdf, name):
    pdf.output(str(OUT / name))
    print("wrote", name)


def scanned_version(src_name, out_name, angle=0.8):
    """Rasterize page 1 of a generated PDF into an image-only 'scanned' PDF."""
    try:
        import pypdfium2 as pdfium
        page = pdfium.PdfDocument(str(OUT / src_name))[0]
        img = page.render(scale=2.2).to_pil().convert("L")
    except Exception:
        # Fallback: draw a plain-text facsimile onto a blank page (still OCR-able).
        img = Image.new("L", (1240, 1754), 252)
        d = ImageDraw.Draw(img)
        d.text((60, 60), f"(fallback render of {src_name})", fill=60)
    img = img.rotate(angle, expand=True, fillcolor=245)
    noise = Image.effect_noise(img.size, 14).point(lambda p: 235 + p * 0.08)
    img = Image.composite(img, noise.convert("L"), img.point(lambda p: 255 if p < 250 else 0))
    img = img.filter(ImageFilter.GaussianBlur(0.4)).convert("RGB")
    tmp = OUT / "_scan_tmp.jpg"
    img.save(tmp, quality=62)
    pdf = FPDF(format="A4")
    pdf.add_page()
    pdf.image(str(tmp), x=4, y=4, w=202)
    pdf.output(str(OUT / out_name))
    tmp.unlink()
    print("wrote", out_name, "(image-only)")


KEY = {}


def leave_app(n, docno, emp, etype, days, start, end, scanned=False):
    name = f"leave_application_{docno}{'_scanned' if scanned else ''}.pdf"
    pdf = new_pdf()
    head(pdf, "SANDBOX AGENCY A", "Human Resource Section", "APPLICATION FOR LEAVE", docno, "2026-10-10")
    fields(pdf, [("Employee No", emp[0]), ("Name", emp[1]), ("Position", emp[2]), ("Unit", emp[3]),
                 ("Type of leave", etype), ("Inclusive dates", f"{start} to {end}"),
                 ("Number of working days", days), ("Commutation", "Not requested")])
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 9)
    pdf.multi_cell(0, 5, "Certification of leave credits as of 2026-09-30: Vacation 12.5 days / Sick 18.25 days. (Synthetic values.)")
    sig(pdf, "Applicant's signature:", emp[1], emp[2])
    sig(pdf, "Recommending approval:", "Teresa P. Salazar", "Chief, Human Resource Section")
    save(pdf, name)
    KEY[name] = {"documentType": "leave_application", "documentNo": docno, "employeeNo": emp[0],
                 "employeeName": emp[1], "leaveType": etype, "startDate": start, "endDate": end,
                 "workingDays": days, "ocrRequired": scanned}
    return name


def travel_order(docno, emp, dest, purpose, start, end, scanned=False):
    name = f"travel_order_{docno}{'_scanned' if scanned else ''}.pdf"
    pdf = new_pdf()
    head(pdf, "SANDBOX AGENCY A", "Office of the Director", "TRAVEL ORDER", docno, "2026-10-08")
    fields(pdf, [("Employee No", emp[0]), ("Name", emp[1]), ("Position", emp[2]),
                 ("Destination", dest), ("Purpose", purpose),
                 ("Inclusive dates", f"{start} to {end}"), ("Fund source", "Regular agency fund (synthetic)"),
                 ("Per diem", "PHP 2,200.00/day (synthetic rate)")])
    sig(pdf, "Approved:", "Ramon V. Ocampo", "Director IV")
    save(pdf, name)
    KEY[name] = {"documentType": "travel_order", "documentNo": docno, "employeeNo": emp[0], "employeeName": emp[1],
                 "destination": dest, "startDate": start, "endDate": end, "ocrRequired": scanned}
    return name


def purchase_request(docno):
    name = f"purchase_request_{docno}.pdf"
    pdf = new_pdf()
    head(pdf, "SANDBOX AGENCY A", "Supply and Property Unit", "PURCHASE REQUEST", docno, "2026-10-06")
    fields(pdf, [("Requesting unit", "ICT Unit"), ("Purpose", "Replacement peripherals for public assistance counters")])
    pdf.ln(2)
    pdf.set_font("Helvetica", "B", 9)
    for w, t in ((14, "Qty"), (22, "Unit"), (98, "Item description"), (28, "Unit cost"), (28, "Total")):
        pdf.cell(w, 6, t, border=1)
    pdf.ln()
    pdf.set_font("Helvetica", "", 9)
    items = [(6, "pc", "Optical mouse, USB", 350, 2100), (6, "pc", "Keyboard, USB", 550, 3300),
             (3, "pc", "Webcam, 1080p", 1850, 5550), (2, "pc", "Headset with microphone", 1200, 2400)]
    for q, u, d, c, t in items:
        for w, v in ((14, q), (22, u), (98, d), (28, f"{c:,.2f}"), (28, f"{t:,.2f}")):
            pdf.cell(w, 6, str(v), border=1)
        pdf.ln()
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(162, 6, "TOTAL", border=1)
    pdf.cell(28, 6, "13,350.00", border=1)
    pdf.ln()
    sig(pdf, "Requested by:", "Kevin L. Bautista", "Information Technology Officer I")
    save(pdf, name)
    KEY[name] = {"documentType": "purchase_request", "documentNo": docno, "requestingUnit": "ICT Unit",
                 "lineItems": 4, "totalAmount": 13350.00, "ocrRequired": False}


def disbursement_voucher(docno):
    name = f"disbursement_voucher_{docno}.pdf"
    pdf = new_pdf()
    head(pdf, "SANDBOX AGENCY A", "Accounting Section", "DISBURSEMENT VOUCHER", docno, "2026-10-09")
    fields(pdf, [("Payee", "Sinag Postharvest Equipment Fabricators (SBX-REG-0010)"),
                 ("Particulars", "Payment for fabrication services, Job Order SBX-JO-2026-0113, inspection accepted 2026-10-02"),
                 ("Amount", "PHP 148,500.00"), ("Mode of payment", "Check"),
                 ("ORS No.", "SBX-ORS-2026-0457")])
    sig(pdf, "Certified: supporting documents complete:", "Divina R. Agustin", "Accountant III")
    sig(pdf, "Approved for payment:", "Ramon V. Ocampo", "Director IV")
    save(pdf, name)
    KEY[name] = {"documentType": "disbursement_voucher", "documentNo": docno,
                 "payee": "Sinag Postharvest Equipment Fabricators", "amount": 148500.00,
                 "orsNo": "SBX-ORS-2026-0457", "ocrRequired": False}


def memo(docno):
    name = f"memo_{docno}.pdf"
    pdf = new_pdf()
    head(pdf, "SANDBOX AGENCY A", "Office of the Director", "MEMORANDUM", docno, "2026-10-05")
    fields(pdf, [("To", "All Division Chiefs"), ("From", "The Director"),
                 ("Subject", "Submission of year-end property inventory reports")])
    pdf.ln(2)
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, "All divisions shall submit their physical count of property and equipment to the Supply and "
                         "Property Unit on or before 2026-11-14. Items below PHP 50,000.00 shall be reported on the "
                         "ICS summary; items at or above PHP 50,000.00 on the PAR summary. Unlocated items must carry "
                         "an explanation signed by the accountable officer. (Synthetic content for a build exercise.)")
    sig(pdf, "", "Ramon V. Ocampo", "Director IV")
    save(pdf, name)
    KEY[name] = {"documentType": "memorandum", "documentNo": docno, "to": "All Division Chiefs",
                 "subject": "Submission of year-end property inventory reports", "deadline": "2026-11-14",
                 "ocrRequired": False}


def coe_request(docno, emp):
    name = f"coe_request_{docno}.pdf"
    pdf = new_pdf()
    head(pdf, "SANDBOX AGENCY A", "Human Resource Section", "REQUEST FOR CERTIFICATE OF EMPLOYMENT", docno, "2026-10-12")
    fields(pdf, [("Employee No", emp[0]), ("Name", emp[1]), ("Position", emp[2]), ("Unit", emp[3]),
                 ("Purpose of request", "Bank loan application"), ("Copies requested", "2"),
                 ("Release preference", "Pick up at HR counter")])
    sig(pdf, "Requested by:", emp[1], emp[2])
    save(pdf, name)
    KEY[name] = {"documentType": "coe_request", "documentNo": docno, "employeeNo": emp[0],
                 "employeeName": emp[1], "purpose": "Bank loan application", "copies": 2, "ocrRequired": False}


def ict_request(docno, emp):
    name = f"ict_service_request_{docno}.pdf"
    pdf = new_pdf()
    head(pdf, "SANDBOX AGENCY A", "ICT Unit", "ICT SERVICE REQUEST", docno, "2026-10-13")
    fields(pdf, [("Requester", f"{emp[1]} ({emp[0]})"), ("Unit", emp[3]),
                 ("Category", "SYSTEM_ACCESS"), ("Property No", "SBX-PROP-0012"),
                 ("Description", "Cannot sign in to the records tracking system after password expiry; requesting reset and unlock.")])
    sig(pdf, "Received by (ICT):", "Grace T. Manalo", "Information Systems Analyst II")
    save(pdf, name)
    KEY[name] = {"documentType": "ict_service_request", "documentNo": docno, "requesterNo": emp[0],
                 "category": "SYSTEM_ACCESS", "propertyNo": "SBX-PROP-0012", "ocrRequired": False}


def registry_renewal(docno):
    name = f"registry_renewal_{docno}.pdf"
    pdf = new_pdf()
    head(pdf, "SANDBOX AGENCY B", "Registration Division", "APPLICATION FOR RENEWAL OF REGISTRATION", docno, "2026-10-11")
    fields(pdf, [("Registry No", "SBX-REG-0015"), ("Entity name", "Silangan UV Express Transport Cooperative"),
                 ("Entity type", "Transport cooperative"), ("Current status", "EXPIRED (since 2026-09-30)"),
                 ("Contact person", "Hazel D. Mercado"), ("Requested validity", "2027-09-30"),
                 ("Attachments", "Audited financial statement (synthetic); roster of members (synthetic)")])
    sig(pdf, "Applicant:", "Hazel D. Mercado", "Authorized representative")
    save(pdf, name)
    KEY[name] = {"documentType": "registry_renewal", "documentNo": docno, "registryNo": "SBX-REG-0015",
                 "entityName": "Silangan UV Express Transport Cooperative",
                 "requestedValidity": "2027-09-30", "ocrRequired": False}


def main():
    e1 = ("SBX-0007", "Jasmine R. Navarro", "Administrative Officer IV", "Administrative Division")
    e2 = ("SBX-0021", "Paolo S. Mercado", "Computer Programmer II", "ICT Unit")
    e3 = ("SBX-0034", "Lourdes B. Tolentino", "Budget Officer II", "Budget Section")
    src1 = leave_app(1, "SBX-LA-2026-0001", e1, "Vacation leave", 3, "2026-11-09", "2026-11-11")
    travel_order("SBX-TO-2026-0003", e3, "Cebu City", "Attend the regional budget forum (synthetic)", "2026-11-17", "2026-11-19")
    src2 = travel_order("SBX-TO-2026-0009", e2, "Baguio City", "On-site systems support (synthetic)", "2026-11-24", "2026-11-26")
    purchase_request("SBX-PR-2026-0004")
    disbursement_voucher("SBX-DV-2026-0005")
    memo("SBX-MEMO-2026-0006")
    coe_request("SBX-COE-2026-0007", e2)
    ict_request("SBX-TKT-2026-0008", e1)
    registry_renewal("SBX-RR-2026-0010")
    # scanned (image-only) variants of two documents
    la2 = leave_app(2, "SBX-LA-2026-0002", e3, "Sick leave", 2, "2026-10-01", "2026-10-02")
    scanned_version(la2, "leave_application_SBX-LA-2026-0002_scanned.pdf")
    (OUT / la2).unlink()  # keep only the scanned variant for this one
    k = KEY.pop(la2)
    k["ocrRequired"] = True
    KEY["leave_application_SBX-LA-2026-0002_scanned.pdf"] = k
    scanned_version(src2, "travel_order_SBX-TO-2026-0009_scanned.pdf")
    (OUT / src2).unlink()
    k = KEY.pop(src2)
    k["ocrRequired"] = True
    KEY["travel_order_SBX-TO-2026-0009_scanned.pdf"] = k
    (OUT / "answer_key.json").write_text(json.dumps(KEY, indent=2), encoding="utf-8")
    print(f"answer_key.json: {len(KEY)} documents")


if __name__ == "__main__":
    main()
