import os
from flask import Flask, request, render_template
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
PLOTS_FOLDER = 'static/eda_plots'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PLOTS_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['dataset']
    filename = file.filename
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    df = pd.read_csv(path)
    summary_html = df.describe(include='all').to_html(classes='table table-bordered')
    numeric_df = df.select_dtypes(include='number')


    plots = []

    # Histogram
    plt.figure(figsize=(6, 4))
    sns.histplot(numeric_df.iloc[:, 0], kde=True)
    hist_path = os.path.join(PLOTS_FOLDER, 'hist.png')
    plt.title("Histogram")
    plt.savefig(hist_path)
    plt.close()
    plots.append('hist.png')

    # Boxplot
    plt.figure(figsize=(6, 4))
    sns.boxplot(data=numeric_df)
    box_path = os.path.join(PLOTS_FOLDER, 'box.png')
    plt.title("Boxplot")
    plt.savefig(box_path)
    plt.close()
    plots.append('box.png')

    # Heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(numeric_df.corr(), annot=True, cmap='vanimo')
    heatmap_path = os.path.join(PLOTS_FOLDER, 'heatmap.png')
    plt.title("Correlation Heatmap")
    plt.savefig(heatmap_path)
    plt.close()
    plots.append('heatmap.png')

    return render_template('report.html', summary_table=summary_html, plots=plots)

if __name__ == '__main__':
    app.run(debug=True)
