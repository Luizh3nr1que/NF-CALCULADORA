from flask import Flask, render_template, request, jsonify
import zipfile
import xml.etree.ElementTree as ET
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    total = 0.0
    arquivos = request.files.getlist("files[]")  # pega todos os arquivos enviados

    for arquivo in arquivos:
        if arquivo.filename.endswith('.zip'):
            with zipfile.ZipFile(BytesIO(arquivo.read())) as zip_ref:
                for nome_xml in zip_ref.namelist():
                    with zip_ref.open(nome_xml) as xml_file:
                        tree = ET.parse(xml_file)
                        root = tree.getroot()
                        vNF = root.find('.//{http://www.portalfiscal.inf.br/nfe}vNF')
                        if vNF is not None:
                            total += float(vNF.text)
    
    return jsonify({"total": round(total, 2)})

if __name__ == '__main__':
    app.run(debug=True)
