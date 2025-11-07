# 🇵🇹
# 🚚 VASP Tracker CLI

Ferramenta em **Python 3** para consultar o estado de envios da **VASP Expresso** via API pública (Track & Trace) e exportar os resultados em formato **JSON** ou **CSV**.

Desenvolvido como parte do **teste técnico para Junior Backend Developer**.

---

## 📦 Funcionalidades

- Aceita um ou mais números de tracking (ficheiro `.txt` ou `.csv`)
- Consulta a API pública da VASP (`https://www.vaspexpresso.pt/api/TrackAndTrace/?term=`)
- Extrai e normaliza o histórico de eventos de cada envio
- Gera **snapshots JSON e HTML** de cada pedido
- Exporta resultados em `.json` ou `.csv`
- Inclui **delay de 1 segundo entre pedidos**
- Inclui **testes automatizados com pytest**

---

## 🧰 Requisitos

- Python **3.9+** (testado com **Python 3.12**)
- `git`, `pip` e `venv` instalados

Instalar o suporte a ambientes virtuais (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3.12-venv
```

---

## 🧭 Como correr o programa

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/Diogo-A-Fernandes/vasp-tracker-cli.git
cd vasp-tracker-cli
```

### 2️⃣ Criar e ativar o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 No Windows usa:
> ```bash
> venv\Scripts\activate
> ```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Alterar ou criar um ficheiro com códigos (`codes.txt` ou `codes.csv`)

Exemplo (`codes.txt`):

```
0746825000240
0746825000241
0746825000242
```

### 5️⃣ Executar o programa

Modo direto (com argumentos):

```bash
python main.py -i codes.txt -o results.json
```

Modo interativo (com perguntas no terminal):

```bash
python main.py
```

---

## 🧪 Como correr os testes

Ativar o ambiente virtual:

```bash
source venv/bin/activate
```

Executar os testes com **pytest**:

```bash
python3 -m pytest -v
```

Exemplo de saída esperada:

```
collected 6 items

tests/test_vasp.py::test_normalize_vasp_response_basic PASSED
tests/test_vasp.py::test_no_events_returns_not_found PASSED
tests/test_vasp.py::test_missing_optional_fields PASSED
tests/test_vasp.py::test_events_sorted_by_timestamp PASSED
tests/test_vasp.py::test_read_codes_txt PASSED
tests/test_vasp.py::test_read_codes_csv PASSED
```

---

## ⚙️ Estrutura do projeto

```
DNL/
├── codes.txt
├── main.py
├── requirements.txt
├── results.json
├── snapshots
│   ├── 0746825000200.html
│   ├── 0746825000200.json
│   ├── 0746825000240.html
│   ├── 0746825000240.json
│   ├── 0746825000250.html
│   └── 0746825000250.json
└── tests
    └── test_vasp.py
---

## 🧱 Dependências principais

```text
requests   # chamadas HTTP à API
pandas     # leitura/escrita de CSVs
pytest     # testes automatizados
```

Instalar com:

```bash
pip install -r requirements.txt
```

---

## 🧾 Boas práticas

- Usa apenas o **endpoint público oficial da VASP**
- Inclui **delay de 1 segundo** entre pedidos
- Guarda snapshots locais (`snapshots/*.json` e `.html`)
- Não faz scraping nem renderização JavaScript

---

## 🧑‍💻 Autor

**Diogo A. Fernandes**  
Teste técnico — *Junior Backend Developer*  
© 2025 Todos os direitos reservados.

---

## 🪪 Licença

MIT License — uso livre para fins técnicos e educacionais.

# 🇬🇧
# 🚚 VASP Tracker CLI

A **Python 3** command-line tool to check shipment statuses from **VASP Expresso** using their public API (Track & Trace) and export the results to **JSON** or **CSV** formats.

Developed as part of the **technical assessment for Junior Backend Developer**.

---

## 📦 Features

- Accepts one or multiple tracking codes (from `.txt` or `.csv` files)
- Queries the official VASP public API (`https://www.vaspexpresso.pt/api/TrackAndTrace/?term=`)
- Extracts and normalizes the shipment tracking history
- Generates **JSON and HTML snapshots** for each request
- Exports results to `.json` or `.csv`
- Includes a **1-second delay between requests** (rate-limit friendly)
- Includes **automated tests** using pytest

---

## 🧰 Requirements

- Python **3.9+** (tested with **Python 3.12**)
- `git`, `pip`, and `venv` installed

Install virtual environment support (Ubuntu/Debian):

```bash
sudo apt update
sudo apt install python3.12-venv
```

---

## 🧭 How to Run the Program

### 1️⃣ Clone the repository

```bash
git clone https://github.com/Diogo-A-Fernandes/vasp-tracker-cli.git
cd vasp-tracker-cli
```

### 2️⃣ Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

> 💡 On Windows:
> ```bash
> venv\Scripts\activate
> ```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create or edit the codes file (`codes.txt` or `codes.csv`)

Example (`codes.txt`):

```
0746825000240
0746825000241
0746825000242
```

### 5️⃣ Run the program

Direct mode (with arguments):

```bash
python main.py -i codes.txt -o results.json
```

Interactive mode (prompts in the terminal):

```bash
python main.py
```

---

## 🧪 Running the Tests

Activate the virtual environment:

```bash
source venv/bin/activate
```

Run all tests with **pytest**:

```bash
python3 -m pytest -v
```

Expected output example:

```
collected 6 items

tests/test_vasp.py::test_normalize_vasp_response_basic PASSED
tests/test_vasp.py::test_no_events_returns_not_found PASSED
tests/test_vasp.py::test_missing_optional_fields PASSED
tests/test_vasp.py::test_events_sorted_by_timestamp PASSED
tests/test_vasp.py::test_read_codes_txt PASSED
tests/test_vasp.py::test_read_codes_csv PASSED
```

---

## ⚙️ Project Structure

```
DNL/
├── codes.txt
├── main.py
├── requirements.txt
├── results.json
├── snapshots
│   ├── 0746825000200.html
│   ├── 0746825000200.json
│   ├── 0746825000240.html
│   ├── 0746825000240.json
│   ├── 0746825000250.html
│   └── 0746825000250.json
└── tests
    └── test_vasp.py
```

---

## 🧱 Main Dependencies

```text
requests   # HTTP API requests
pandas     # CSV read/write operations
pytest     # automated testing
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🧾 Best Practices

- Uses only the **official public VASP API endpoint**
- Adds a **1-second delay** between each request
- Stores local snapshots (`snapshots/*.json` and `.html`)
- Does **not** perform HTML scraping or JavaScript rendering

---

## 🧑‍💻 Author

**Diogo A. Fernandes**  
Technical Test — *Junior Backend Developer*  
© 2025 All rights reserved.

---

## 🪪 License

MIT License — free to use for technical and educational purposes.
