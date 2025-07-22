# AI Event Classifier

An end-to-end system that classifies event center pages by capturing screenshots and using a fine-tuned image recognition model.

### 🔍 Categories
- **Login Pages**
- **Web Pages**
- **Error Pages**
- **Executable Files (e.g., HTML/XML)**

### 🧠 How It Works

1. **Download Training Images** using keyword-based web scraping.
2. **Train a Classifier** with [ImageAI](https://github.com/OlafenwaMoses/ImageAI) and a ResNet model.
3. **Extract & Filter URLs** network scan and filter results.
4. **Take Screenshots** of target URLs with Pyppeteer.
5. **Classify Images** with the trained model.
6. **Retrain** with improved data iteratively.

### 🧰 Tech Stack

- Python 3.11+
- ImageAI (with TensorFlow backend)
- PyTorch
- Pyppeteer
- ffuf (for fuzzing/filtering)

