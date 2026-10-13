"""Regenerate the synthetic CSVs. Deterministic: same seed -> same data.
Usage: python data/generate_data.py [seed]
Everything is invented; IDs start SBX-; emails end .example.
"""
import csv
import datetime as dt
import random
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 2026
TODAY = dt.date(2026, 10, 14)

FIRST = ["Maria", "Jose", "Ana", "Mark", "Kristine", "Angelica", "Christian", "Jasmine", "Ramon", "Liza",
         "Rafael", "Patricia", "Miguel", "Camille", "Joshua", "Bea", "Paolo", "Rowena", "Gilbert", "Teresa",
         "Noel", "Cristina", "Jerome", "Divina", "Arnel", "Lourdes", "Kevin", "Aileen", "Dennis", "Grace",
         "Emmanuel", "Joy", "Carlo", "Melissa", "Ronaldo", "Shiela", "Victor", "Hazel", "Benjie", "Marites"]
LAST = ["Santos", "Reyes", "Cruz", "Bautista", "Garcia", "Mendoza", "Torres", "Ramos", "Aquino", "Flores",
        "Villanueva", "Castillo", "Fernandez", "Dela Cruz", "Navarro", "Salazar", "Domingo", "Gonzales",
        "Lopez", "Mercado", "Pascual", "Soriano", "Valdez", "Manalo", "Agustin", "Rivera", "Tolentino",
        "Panganiban", "Lim", "Tan", "Del Rosario", "Javier", "Ocampo", "Samonte", "Esguerra"]
UNITS = ["Office of the Director", "Administrative Division", "Human Resource Section", "Finance Division",
         "Budget Section", "Accounting Section", "Cash Section", "Records Section", "Supply and Property Unit",
         "ICT Unit", "Planning Unit", "Legal Unit", "Technical Services Division", "Regional Coordination Unit"]
POSITIONS = ["Information Systems Analyst II", "Information Technology Officer I", "Computer Programmer II",
             "Administrative Officer IV", "Administrative Assistant III", "Accountant III", "Budget Officer II",
             "Records Officer II", "Supply Officer II", "Planning Officer III",
             "Human Resource Management Officer II", "Science Research Specialist II", "Attorney III",
             "Engineer II", "Statistician II", "Project Development Officer II"]
STATUSES = (["Permanent"] * 78 + ["Temporary"] * 6 + ["Casual"] * 10 + ["Coterminous"] * 6)
DOC_TYPES = ["Disbursement Voucher", "Purchase Request", "Travel Order", "Memorandum", "Letter request",
             "Contract for review", "Inspection and Acceptance Report", "Leave application"]
DOC_OFFICES = ["Records Section", "Office of the Director", "Budget Section", "Accounting Section",
               "Cash Section", "Supply and Property Unit", "Legal Unit", "Human Resource Section"]
CLASSES = [("simple", 3)] * 45 + [("complex", 7)] * 40 + [("highly_technical", 20)] * 15
ASSET_TYPES = [("Laptop", 62000, 78000), ("Desktop computer", 45000, 60000), ("Printer", 9000, 28000),
               ("UPS", 4000, 9000), ("Network switch", 18000, 65000), ("Projector", 30000, 52000),
               ("Tablet", 15000, 32000)]
REGISTRY_ROWS = [
    ("SBX-REG-0001", "Sampaguita Transport Service Cooperative", "Transport cooperative", "ACTIVE", "2027-06-30", "NCR"),
    ("SBX-REG-0002", "Bagong Umaga Urban Poor Association", "People's organization", "ACTIVE", "2027-03-31", "NCR"),
    ("SBX-REG-0003", "Mabuhay Wood Products Testing Laboratory", "Testing laboratory", "ACTIVE", "2026-12-31", "Region IV-A"),
    ("SBX-REG-0004", "Kalayaan Jeepney Operators Cooperative", "Transport cooperative", "PROVISIONAL", "2026-11-30", "Region III"),
    ("SBX-REG-0005", "Hiraya Design Studio", "Design firm", "ACTIVE", "2027-09-30", "NCR"),
    ("SBX-REG-0006", "Liwanag Metals Calibration Center", "Calibration laboratory", "SUSPENDED", "2026-10-31", "Region VII"),
    ("SBX-REG-0007", "Bayanihan Fisherfolk Association", "People's organization", "EXPIRED", "2026-06-30", "Region V"),
    ("SBX-REG-0008", "Dagat at Lupa Heritage Partners", "Museum partner", "ACTIVE", "2027-12-31", "Region VI"),
    ("SBX-REG-0009", "Tanglaw Tricycle Operators Cooperative", "Transport cooperative", "ACTIVE", "2027-01-31", "Region X"),
    ("SBX-REG-0010", "Sinag Postharvest Equipment Fabricators", "Equipment fabricator", "ACTIVE", "2027-05-31", "Region II"),
    ("SBX-REG-0011", "Pag-asa Racing Stables", "Racing stable", "ACTIVE", "2026-12-31", "Region IV-A"),
    ("SBX-REG-0012", "Habagat Coastal Development Corp.", "Reclamation proponent", "UNDER_REVIEW", "", "NCR"),
    ("SBX-REG-0013", "Kapit-Bisig Neighborhood Association", "People's organization", "ACTIVE", "2027-04-30", "NCR"),
    ("SBX-REG-0014", "Masagana Industrial Chemistry Laboratory", "Testing laboratory", "ACTIVE", "2027-02-28", "NCR"),
    ("SBX-REG-0015", "Silangan UV Express Transport Cooperative", "Transport cooperative", "EXPIRED", "2026-09-30", "Region IV-A"),
    ("SBX-REG-0016", "Ugnayan Overseas Family Circle", "Community organization", "ACTIVE", "2027-08-31", "Region I"),
    ("SBX-REG-0017", "Alon Furniture Makers Guild", "Design firm", "ACTIVE", "2027-03-31", "Region VII"),
    ("SBX-REG-0018", "Kabisig Probation Volunteers Group", "Volunteer organization", "ACTIVE", "2027-06-30", "Region XI"),
    ("SBX-REG-0019", "Banaag Bamboo Testing Center", "Testing laboratory", "PROVISIONAL", "2026-12-15", "Region IV-A"),
    ("SBX-REG-0020", "Bituin Horse Owners Association", "Racing association", "ACTIVE", "2027-01-31", "NCR"),
]


def write(name, header, rows):
    with (OUT / name).open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"{name}: {len(rows)} rows")


def main():
    rng = random.Random(SEED)
    # employees
    emps, used = [], set()
    for i in range(1, 61):
        while True:
            nm = (rng.choice(FIRST), rng.choice("ABCDEFGHJLMNOPRSTV"), rng.choice(LAST))
            if nm not in used:
                used.add(nm)
                break
        hired = dt.date(rng.randint(2008, 2025), rng.randint(1, 12), rng.randint(1, 28))
        months = max(0, (TODAY.year - hired.year) * 12 + TODAY.month - hired.month)
        vl_e = round(months * 1.25, 2)
        sl_e = round(months * 1.25, 2)
        emps.append([
            f"SBX-{i:04d}", nm[0], nm[1] + ".", nm[2], rng.choice(POSITIONS), rng.choice(UNITS),
            rng.choice(STATUSES), hired.isoformat(),
            "" if i not in (13, 27, 44) else dt.date(2026, rng.randint(1, 8), rng.randint(1, 28)).isoformat(),
            vl_e, round(vl_e * rng.uniform(.35, .8), 2), sl_e, round(sl_e * rng.uniform(.1, .6), 2),
            f"{nm[0].lower()}.{nm[2].lower().replace(' ', '')}{i}@sandbox-agency.example",
        ])
    write("employees.csv",
          ["employeeNo", "firstName", "middleInitial", "lastName", "positionTitle", "unit", "employmentStatus",
           "dateHired", "separatedOn", "vlEarned", "vlUsed", "slEarned", "slUsed", "email"], emps)
    # registry (fixed rows + generated contacts)
    reg = []
    for rid, name, etype, status, valid, region in REGISTRY_ROWS:
        person = f"{rng.choice(FIRST)} {rng.choice(LAST)}"
        reg.append([rid, name, etype, status, valid, region, person,
                    person.lower().replace(" ", ".") + "@org.example", "Synthetic record"])
    write("registry.csv",
          ["registryNo", "name", "entityType", "status", "validUntil", "region", "contactPerson", "contactEmail", "remarks"], reg)
    # document log
    docs = []
    for i in range(1, 41):
        cls, target = rng.choice(CLASSES)
        received = TODAY - dt.timedelta(days=rng.randint(0, 34))
        holder = rng.choice(DOC_OFFICES)
        status = rng.choice(["OPEN"] * 7 + ["CLOSED"] * 3)
        docs.append([f"SBX-DOC-2026-{i:04d}", rng.choice(DOC_TYPES),
                     f"Synthetic subject no. {rng.randint(100, 999)}", cls, target,
                     received.isoformat(), rng.choice(UNITS), holder if status == "OPEN" else "",
                     status, rng.choice(["", "", "yes"])])
    write("document_log.csv",
          ["controlNumber", "docType", "subject", "classification", "targetWorkingDays",
           "receivedOn", "fromOffice", "currentHolder", "status", "confidential"], docs)
    # assets
    assets = []
    for i in range(1, 51):
        kind, lo, hi = rng.choice(ASSET_TYPES)
        cost = rng.randrange(lo, hi, 500)
        acquired = dt.date(rng.randint(2018, 2026), rng.randint(1, 9), rng.randint(1, 28))
        assets.append([f"SBX-PROP-{i:04d}", kind, f"SN-SBX-{rng.randint(100000, 999999)}",
                       f"SBX-{rng.randint(1, 60):04d}",
                       rng.choice(["IN_USE"] * 75 + ["FOR_REPAIR"] * 10 + ["UNSERVICEABLE"] * 8 + ["RETURNED"] * 7),
                       acquired.isoformat(), cost, "PAR" if cost >= 50000 else "ICS"])
    write("assets.csv",
          ["propertyNo", "assetType", "serialNo", "accountableEmployeeNo", "status", "acquiredOn",
           "acquisitionCost", "custodyDocument"], assets)


if __name__ == "__main__":
    main()
