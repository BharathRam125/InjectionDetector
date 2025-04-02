# **Web Injection Detection - GCN-based Model**
**A GCN-based detection system for injection attacks, designed to operate at the Web Application Firewall (WAF) level.**
---

## 📌 **Overview**  
This project provides a **Graph Neural Network (GNN)-based approach** to detect web injection attacks. By structuring web request data into graph-based representations, the model improves pattern recognition and anomaly detection.  

⚠ **Disclaimer:**  
✔ **The model is not final** and is still under development.  
✔ The dataset used is a **test dataset** and might not fully cover all real-world attack scenarios.  
✔ The model currently focuses on **SQLi, XSS, and Command Injection** only.  
⚠ Warning: Dataset imbalance detected for XSS and command injection samples. Additional data collection or resampling may be required to improve model generalization.


## 🏗 **Model Architecture**  
The **GCN-based model** consists of:  
✔ **Three-layer Graph Convolutional Network (GCN)** for feature extraction.  
✔ **Batch Normalization & Dropout** for stable training and regularization.  
✔ **Fully Connected Layers** for final classification.  
✔ **Character-based Input Processing** to handle fine-grained text patterns effectively.  

### 🔍 **Model Insights & Observations**
The model employs a **character-based approach**, which differs from traditional token-based methods by analyzing individual characters rather than words. This allows for improved detection of **obfuscated payloads**, such as those using encoding or insertion techniques to bypass security filters. By constructing a **graph representation of input sequences**, the model learns the structural relationships between characters, making it more effective in recognizing subtle variations in attack patterns.

During evaluation, the model demonstrated **high precision and recall for SQLi detection** but exhibited challenges with **class imbalance in XSS and command injection cases**. Some benign inputs, particularly **short single-word payloads**, were incorrectly classified as malicious due to a bias in the training data. Future iterations should focus on **better balancing benign samples** and **fine-tuning decision thresholds** to reduce false positives.

### 🔍 **Pros & Cons of the Model**
#### ✅ **Pros:**
- **Robust Feature Extraction:** GCN effectively captures structural relationships in input data.
- **Fine-grained Analysis:** Character-based input ensures better handling of obfuscated attacks.
- **Regularization Techniques:** Batch normalization and dropout improve generalization.
- **Scalability:** Can be adapted to different types of payload-based security tasks.

#### ❌ **Cons:**
- **Computational Complexity:** GCN models require more memory and processing power than traditional methods.
- **Data Imbalance Sensitivity:** Performance can degrade if the dataset is not well-balanced.
- **Limited Interpretability:** While effective, graph-based models are often harder to interpret compared to rule-based approaches.

By leveraging these strengths while addressing limitations, future iterations of the model can further enhance web security through deep learning-driven payload analysis.


## 📂 **Dataset & Preprocessing**  

🔹 **Original Dataset:** [SQLi & XSS Dataset](https://www.kaggle.com/datasets/alextrinity/sqli-xss-dataset)  
🔹 **Additional Benign Data:** To improve class balance, we incorporated:  
   - **Common usernames & passwords** (e.g., from RockYou)  
   - **Non-malicious queries & inputs** (e.g., user-generated text, admin-related terms)  
   - **General text samples** (randomized short phrases, non-technical words)  

🔹 **Modifications:** The dataset has been **converted into a graph structure** for training, ensuring robust tokenization and improved feature representation.  

📌 **Modified datasets, preprocessing scripts, and notebooks** are available in the GitHub repository.


## 🔗 **Links & Resources**  
📌 Dataset Used: [SQLi & XSS Dataset](https://www.kaggle.com/datasets/alextrinity/sqli-xss-dataset)  
📌 Preprocessed Data, Training Code & Notebooks: [GitHub Repository](https://github.com/SaiyanSai/InjectionDetector)  


📢 **Note:** The model is trained on a limited dataset and is intended for research and educational purposes only.


## 🚀 **Future Work**
- **Improve Class Balance:** Further augment XSS and command injection samples to reduce imbalance.
- **Enhance Feature Representation:** Explore additional embedding techniques for better tokenization.
- **Expand Dataset Coverage:** Collect real-world benign and malicious samples from diverse sources.
- **Optimize Model Performance:** Experiment with different GCN architectures and hyperparameters.
- **Deploy and Evaluate:** Test the trained model in real-time web traffic analysis scenarios.



