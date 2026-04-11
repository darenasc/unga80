# UNGA80

# UN General Assermbly 79 Speeches

The app analyses the speech of each country at the #UNGA80 in September 2025.

- Summary of the speech.
- Summary in one word.
- Countries mentioned in the speech with positive and negative sentiment.
- Risks mentioned in the speech.

## Usage locally

### Prerequisits

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
ollama pull artifish/llama3.2-uncensored
```

### UNGA80 repository

```bash
# Clone this repository
git clone https://github.com/darenasc/unga80.git

# Change directory to repository
cd unga80

# Install dependencies
pip install pipenv
python3 -m pipenv install Pipfile
python3 -m pipenv install -d Pipfile

# Activate Python environment
pipenv shell

# Run the streamlit app
streamlit run app/app.py
```

## Tools used

- Ollama
- sqlite3
- `artifish/llama3.2-uncensored` model
- [pydeckgl](https://deckgl.readthedocs.io/en/latest/gallery/arc_layer.html)
- [restcountries.com](https://restcountries.com)

## Data
- [UNGA80 Speech urls](https://docs.google.com/spreadsheets/d/1qtqfnRSW24j-XLN7SRKywDCuFatARCH8pUg1Rr6I2vI/export?format=csv&gid=747748046)
- [Admin 0 – Countries](https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/ne_110m_admin_0_countries.zip)