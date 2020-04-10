import xml.etree.ElementTree as ET
from zipfile import ZipFile
import os
import argparse
from payment import Payment
from payroll_plotter import PayrollPlotter

def get_concept(node, concept_tag, amount_tag, amount_tax_tag=None):
    concept = node.get(concept_tag)
    amount = float(node.get(amount_tag))
    amount_taxed = float(node.get(amount_tax_tag)) if amount_tax_tag else 0.0 

    return (concept, amount + amount_taxed)

def get_date(node):
    # TODO: return a date object
    date = node.get("Fecha")
    return date

def generate_payment(payroll_path):
    nomina_path = payroll_path

    tree = ET.parse(nomina_path)
    root = tree.getroot()
    perceptions = {}
    deductions = {}
    tag = "{http://www.sat.gob.mx/nomina12}" # TODO code a function to get tag

    for node in tree.iter(): 
        # TODO: create a dictionary with all strings keys    
        if tag+"Percepcion" == node.tag:
            concept, amount = get_concept(node, "Concepto", "ImporteExento", "ImporteGravado")
            perceptions[concept] = amount

        elif tag+"Deduccion" == node.tag:
            concept, amount = get_concept(node, "Concepto", "Importe")
            deductions[concept] = amount

    date = get_date(root)
    payment = Payment(date, perceptions, deductions)
    return payment

def find_xml(zipfile):
    for file in zipfile.filelist:
        if file.filename.endswith("xml"):
            return file.filename
    return None

if __name__=="__main__":
    
    parser = argparse.ArgumentParser(description="Parsea y gráfica archivos de nomina")
    parser.add_argument("payroll_folder", type=str,
                        help="<nominas_folder>")
    
    args = parser.parse_args()
    payroll_folder = args.payroll_folder

    payments = []

    for file in os.listdir(payroll_folder):
        file_path = payroll_folder + file
        if file_path.endswith(".zip"):
            zipfile = ZipFile(file_path)
            xmlfile_path = zipfile.extract(find_xml(zipfile))
            payments.append(generate_payment(xmlfile_path))
            os.remove(xmlfile_path)

    
    payments.sort(key = lambda x : x.date)
    for payment in payments:
        print(payment)

    payroll_plt = PayrollPlotter(payments)
    payroll_plt.plot()