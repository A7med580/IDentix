# 📘 IDentix User Manual

Welcome to **IDentix**, your Multi-Modal Biometric Authentication System. This manual allows you to fully understand, configure, and operate the system.

---

## 🚀 1. Quick Start Guide

### Prerequisites
- **Python 3.8+** installed.
- **Google Account** (for Colab).

### Step-by-Step Setup

#### **Phase A: Data & Feature Setup (The "Cloud" Method)**
Since dataset storage is a constraint, we use Google Colab to do the heavy lifting.

1.  **Open the Notebook**: 
    - Go to [Google Colab](https://colab.research.google.com/).
    - Upload the file: `docs/IDentix_Colab_Preprocessing.ipynb`.
    
2.  **Run the Notebook**:
    - Select **Runtime > Run all**.
    - The notebook will download the datasets (Face & Voice) into the Colab environment.
    - It will extract the key features and save them as `.npy` files.

3.  **Download Files**:
    - Once the notebook finishes, download `face_embeddings.npy` and `voice_mfccs.npy`.

4.  **Place Files Locally**:
    - Move these two files into the `IDentix/data/features/` folder on your computer.
    - *Note: If the folder doesn't exist, create it.*

#### **Phase B: Local Installation**
1.  Open your terminal in the `IDentix` folder.
2.  Install the required software:
    ```bash
    pip install -r requirements.txt
    ```

#### **Phase C: Launching the App**
Run the following command:
```bash
streamlit run main.py
```
This will open the IDentix Dashboard in your web browser (usually at `http://localhost:8501`).

---

## 🖥️ 2. Interface Guide

### **Tab 1: Live Authentication (The "Main" Screen)**
This is where the actual biometric checking happens.

1.  **Upload Face**: Click "Browse files" under "Face Identification" and select a photo (JPG/PNG).
2.  **Upload Voice**: Click "Browse files" under "Voice Verification" and select an audio clip (WAV/MP3).
    - *Tip: For a successful match, these should belong to a person present in the dataset you processed.*
3.  **Verify Identity**: Click the big **VERIFY IDENTITY** button.
4.  **Results**:
    - The system compares your uploads against the precomputed features (`.npy` files).
    - It gives a **Confidence Score** for Face and Voice separately.
    - It produces a **Fused Score** (Weighted Average).
    - **Access Granted**: If the Fused Score > 70%.
    - **Access Denied**: If the Fused Score < 70%.

### **Tab 2: Evaluation Dashboard**
This tab is for academic analysis.

- **Metrics**: Shows Accuracy, EER (Equal Error Rate) for Face, Voice, and Fused systems.
- **ROC Curve**: Displays the Receiver Operating Characteristic curve.
    - *What to look for*: A curve that goes closer to the top-left corner indicates a better system.

---

## ⚙️ 3. Customization

### Changing Thresholds
You can adjust how strict the system is by editing `fusion/fusion_engine.py`:
```python
    def make_decision(self, fused_score, threshold=0.7): # Change 0.7 to 0.8 for higher security
```

### Changing Weights
If you trust Face more than Voice, edit `ui/app.py` (or `main.py`):
```python
fusion_engine = FusionEngine(face_weight=0.7, voice_weight=0.3)
```

---

## ❓ Troubleshooting

**Q: "No precomputed galaxy found" message?**
A: Ensure `face_embeddings.npy` and `voice_mfccs.npy` are exactly in `IDentix/data/features/`.

**Q: verification fails for everyone?**
A: This system matches the *uploaded file* against the *database*. If you upload a picture of yourself, but you are not in the generic Kaggle dataset, it **should** reject you. That is correct behavior!

**Q: How do I add myself to the database?**
A: You would need to add your photo to the raw dataset and re-run the Colab preprocessing step.
