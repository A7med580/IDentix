import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc

def calculate_biometric_metrics(y_true, y_scores, threshold=0.7):
    """
    Calculates standard biometric performance metrics.
    """
    y_pred = [1 if s >= threshold else 0 for s in y_scores]
    
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred),
        "recall": recall_score(y_true, y_pred),
        "f1": f1_score(y_true, y_pred)
    }
    
    # ROC Curve
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)
    
    # EER calculation
    fnr = 1 - tpr
    eer_index = np.nanargmin(np.absolute(fnr - fpr))
    eer = (fpr[eer_index] + fnr[eer_index]) / 2
    
    metrics["auc"] = roc_auc
    metrics["eer"] = eer
    metrics["fpr"] = fpr
    metrics["tpr"] = tpr
    
    return metrics

def plot_roc_curve(fpr, tpr, roc_auc, title="ROC Curve"):
    """
    Generates a matplotlib ROC curve.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:0.2f})')
    ax.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    ax.set_xlim([0.0, 1.0])
    ax.set_ylim([0.0, 1.05])
    ax.set_xlabel('False Positive Rate (FAR)')
    ax.set_ylabel('True Positive Rate (1 - FRR)')
    ax.set_title(title)
    ax.legend(loc="lower right")
    ax.grid(alpha=0.3)
    return fig
