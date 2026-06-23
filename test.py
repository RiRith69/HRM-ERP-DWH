import pandas as pd
import matplotlib.pyplot as plt
import os

# 1. Define the file paths to your trained model results
# (Update these paths to match your actual folders after training)
results_paths = {
    "YOLOv8s": "C:/Users/User/Documents/CADT/Year3Term2/Internship I/Document-During-Internship-1/hrm_erp_dwh/results_v8.csv",
    "YOLOv10s": "C:/Users/User/Documents/CADT/Year3Term2/Internship I/Document-During-Internship-1/hrm_erp_dwh/results_v10.csv"
}

# Color palette for academic charts
colors = {"YOLOv5s": "#1f77b4", "YOLOv8s": "#ff7f0e", "YOLOv10s": "#2ca02c"}

# 2. Set up the 2x2 plotting grid structure
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
plt.rcParams['font.family'] = 'serif' # Academic style serif font

# 3. Loop through each model file and extract the trends
for model_name, file_path in results_paths.items():
    if not os.path.exists(file_path):
        print(f"Warning: {file_path} not found. Skip training first?")
        continue
        
    # Read the data sheet
    df = pd.read_csv(file_path)
    # Strip whitespace from column names to avoid parsing errors
    df.columns = df.columns.str.strip()
    
    # Calculate Total Training Loss (Box + Cls + DFL losses combined)
    # Note: Column names can vary slightly by YOLO version, double-check your CSV headers!
    train_loss = df['train/box_loss'] + df['train/cls_loss'] + df.get('train/dfl_loss', 0)
    val_loss = df['val/box_loss'] + df['val/cls_loss'] + df.get('val/dfl_loss', 0)
    
    epochs = df['epoch']

    # --- Plot A: Training Accuracy (mAP50) ---
    # YOLO doesn't have "train accuracy" logged directly, so we often show validation performance
    # If your dataset tracks training metrics specifically, swap this column name
    axs[0, 0].plot(epochs, df['metrics/mAP50(B)'], label=f"{model_name} Train", color=colors[model_name])
    
    # --- Plot B: Training Loss ---
    axs[0, 1].plot(epochs, train_loss, label=f"{model_name} Train", color=colors[model_name])
    
    # --- Plot C: Validation Accuracy (mAP50) ---
    axs[1, 0].plot(epochs, df['metrics/mAP50(B)'], label=f"{model_name} Val", color=colors[model_name])
    
    # --- Plot D: Validation Loss ---
    axs[1, 1].plot(epochs, val_loss, label=f"{model_name} Val", color=colors[model_name])

# 4. Format and clean up the charts (Labels, Titles, and Legends)
titles = [
    "(a) Training accuracy curve (mAP50)", 
    "(b) Training loss curve", 
    "(c) Validation accuracy curve (mAP50)", 
    "(d) Validation loss curve"
]
y_labels = ["Accuracy (mAP)", "Loss", "Accuracy (mAP)", "Loss"]

for i, ax in enumerate(axs.flat):
    ax.set_title(titles[i], fontsize=12, pad=10)
    ax.set_xlabel("Epochs", fontsize=10)
    ax.set_ylabel(y_labels[i], fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend(loc='best', fontsize=9)
    # Dynamically scale x-ticks based on your epoch limit
    ax.set_xlim(left=1) 

# 5. Optimize layout and save the final image
plt.tight_layout()
plt.savefig("YOLO_Comparison_Trends.png", dpi=300) # Save in high resolution
plt.show()
