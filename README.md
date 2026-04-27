# 🥗 Calorie Estimation from Dietary Images Using Deep Learning

A deep learning-powered web application that identifies **fruits and vegetables** from images and provides **real-time calorie and nutritional information**, along with **personalized dietary plan recommendations**.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Model Architecture](#-model-architecture)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Supported Food Items](#-supported-food-items)
- [Diet Plans](#-diet-plans)
- [Results](#-results)
- [Future Work](#-future-work)

---

## 🔍 Overview

This project addresses the growing need for intelligent dietary monitoring by combining **computer vision** and **deep learning** to identify food items from images and estimate their caloric content. Users simply upload a photo of a fruit or vegetable, and the system classifies it, fetches live nutritional data, and suggests relevant dietary plans for various health conditions.

---

## ✨ Features

- 📸 **Image-based food recognition** — Upload any JPG/PNG image of a fruit or vegetable
- 🔎 **36-class food classification** — Identifies a wide range of common produce
- 🔥 **Live calorie estimation** — Fetches real-time calorie data (per 100g) from the web
- 🥑 **Fat content information** — Also retrieves total fat content dynamically
- 🏥 **Dietary plan recommendations** — Curated HTML diet plans for multiple health conditions
- 🖥️ **Interactive Streamlit UI** — Clean, easy-to-use web interface

---

## 🛠️ Tech Stack

| Category | Tools / Libraries |
|---|---|
| Language | Python 3.x |
| Deep Learning | TensorFlow / Keras |
| Pretrained Models | VGG16, MobileNetV2 (ImageNet weights) |
| Web App | Streamlit |
| Image Processing | Pillow (PIL), OpenCV |
| Data Handling | NumPy, Pandas |
| Web Scraping | BeautifulSoup4, Requests |
| Visualization | Matplotlib |

---

## 🧠 Model Architecture

The final model is an **ensemble of two powerful pretrained CNNs** — their features are fused for superior classification accuracy.

```
Input Image (224 × 224 × 3)
        │
        ├──────────────────────────────────┐
        ▼                                  ▼
   VGG16 (frozen)                MobileNetV2 (frozen)
   Feature Extractor              Feature Extractor
        │                                  │
        └──────────── Concatenate ─────────┘
                           │
                    Dense(256, ReLU)
                           │
                     Dropout(0.5)
                           │
               Dense(36, Softmax) ──► Predicted Class
```

### Training Details

| Parameter | Value |
|---|---|
| Input Size | 224 × 224 × 3 |
| Optimizer | Adam |
| Loss Function | Categorical Cross-Entropy |
| Epochs | Up to 5 (with Early Stopping) |
| Batch Size | 32 |
| Early Stopping | Patience = 2 (monitors `val_loss`) |
| Data Augmentation | Rotation, Zoom, Flip, Shift, Shear |

> **Note:** Both VGG16 and MobileNetV2 base layers are frozen (pre-trained on ImageNet) — only the custom classification head is trained.

---

## 📦 Dataset

The dataset is organized into three splits:

```
Dataset/
├── train/          # Training images (per-class subdirectories)
├── test/           # Testing images
└── validation/     # Validation images
```

Each subdirectory is named after its class label (e.g., `apple`, `banana`, `tomato`, etc.), following the standard Keras `flow_from_dataframe` convention. Images are in `.jpg` format at 224×224 resolution.

---

## 📁 Project Structure

```
Major project/
│
├── Data_Training.py          # Model training script (ensemble VGG16 + MobileNetV2)
├── DT_2.py                   # Model comparison script (individual MobileNetV2 vs VGG16)
├── Model_Deployment.py       # Primary Streamlit deployment app (uses FV.h5)
├── MD_2.py                   # Alternate Streamlit deployment (uses combined_model.h5)
├── Data_Training.ipynb       # Jupyter notebook for training
├── Model_Deployment.ipynb    # Jupyter notebook for deployment exploration
│
├── FV.h5                     # Saved model (single MobileNetV2-based)
├── combined_model.h5         # Saved model (ensemble VGG16 + MobileNetV2)
│
├── Dataset/                  # Image dataset (train/test/validation)
├── Images/                   # UI background images
├── upload_images/            # Temp storage for user-uploaded images
├── Reports/                  # Project reports and documentation
│
├── index1.html               # Diet plan landing page
├── cardio.html               # Cardiovascular diet plan
├── dietdbt.html              # Diabetes diet plan
├── diethbp.html              # High blood pressure diet plan
├── diethc.html               # High cholesterol diet plan
├── dietlbp.html              # Low blood pressure diet plan
├── dietpcod.html             # PCOD diet plan
├── dietra.html               # Rheumatoid arthritis diet plan
├── dietthyroid.html          # Thyroid diet plan
├── dietwl.html               # Weight loss diet plan
├── mystyle.css               # Stylesheet for diet pages
├── style.css                 # General stylesheet
│
└── .gitignore
```

---

## ⚙️ Installation

### Prerequisites

- Python 3.8+ 
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/AmanRahman34/Calorie_Estimation_Deitary-Images_Using-Deep-Learning.git
cd Calorie_Estimation_Deitary-Images_Using-Deep-Learning
```

### 2. Install Dependencies

```bash
pip install tensorflow keras streamlit pillow numpy pandas matplotlib requests beautifulsoup4
```

### 3. Dataset Setup

Download or provide your own dataset and place it in the `Dataset/` directory following this structure:

```
Dataset/
├── train/
│   ├── apple/
│   ├── banana/
│   └── ...
├── test/
│   └── ...
└── validation/
    └── ...
```

---

## 🚀 Usage

### Option 1: Run the Pre-trained Streamlit App (Recommended)

Make sure `FV.h5` or `combined_model.h5` is present in the root directory, then run:

```bash
streamlit run Model_Deployment.py
```

Or for the ensemble model version:

```bash
streamlit run MD_2.py
```

Then open your browser at `http://localhost:8501`.

### Option 2: Retrain the Model

```bash
python Data_Training.py
```

This will train the ensemble model on your dataset and save it as `combined_model.h5`.

---

## 🍎 Supported Food Items

The model classifies **36 food categories** across fruits and vegetables:

| Fruits | Vegetables |
|---|---|
| Apple, Banana, Chilli Pepper | Beetroot, Cabbage, Capsicum |
| Grapes, Jalapeno, Kiwi | Carrot, Cauliflower, Corn |
| Lemon, Mango, Orange | Cucumber, Eggplant, Garlic |
| Paprika, Pear, Pineapple | Ginger, Lettuce, Onion |
| Pomegranate, Watermelon | Peas, Potato, Raddish |
| | Soy Beans, Spinach, Sweetcorn |
| | Sweetpotato, Tomato, Turnip |

---

## 🏥 Diet Plans

The application includes curated diet plan pages for the following health conditions:

| Condition | File |
|---|---|
| Weight Loss | `dietwl.html` |
| Diabetes | `dietdbt.html` |
| High Blood Pressure | `diethbp.html` |
| Low Blood Pressure | `dietlbp.html` |
| High Cholesterol | `diethc.html` |
| Cardiovascular Disease | `cardio.html` |
| PCOD | `dietpcod.html` |
| Thyroid | `dietthyroid.html` |
| Rheumatoid Arthritis | `dietra.html` |

---

## 📊 Results

The ensemble model (VGG16 + MobileNetV2) outperforms individual models:

| Model | Approach |
|---|---|
| MobileNetV2 (standalone) | Transfer learning, 2× Dense(128) head |
| VGG16 (standalone) | Transfer learning, 2× Dense(128) head |
| **Ensemble (Combined)** | **Concatenated features → Dense(256) + Dropout(0.5)** |

Training uses early stopping on validation loss to prevent overfitting and restore the best weights automatically.

---

## 🔮 Future Work

- [ ] Expand dataset to include cooked meals and mixed dishes
- [ ] Integrate a dedicated nutrition API (e.g., USDA FoodData, Edamam) for more accurate nutritional data
- [ ] Add portion size estimation using object detection (e.g., YOLO)
- [ ] Deploy as a cloud-hosted web app (Streamlit Cloud / Hugging Face Spaces)
- [ ] Build a mobile-friendly version using TensorFlow Lite
- [ ] Add user history tracking and personalized recommendations

---

## 👨‍💻 Author

**Aman Rahman**  
[GitHub](https://github.com/AmanRahman34)

---

## 📄 License

This project is intended for academic and educational purposes.
## Dataset
**Source:** [Fruits and Vegetables Image Recognition - Kaggle](https://www.kaggle.com/datasets/kritikseth/fruit-and-vegetable-image-recognition)

Contains 36 categories of fruits and vegetables with train/test/validation split.

To use:
1. Download from the Kaggle link above
2. Place it in the project root as `Dataset/`
