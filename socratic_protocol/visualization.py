import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict
from .core import EvaluationResult, Metric

class ResultsVisualizer:
    def __init__(self):
        plt.style.use('default')
        self.colors = sns.color_palette("husl", len(Metric))
    
    def create_radar_chart(self, results: List[EvaluationResult], save_path: str = None):
        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(projection='polar'))
        
        # Prepare data
        metrics = list(Metric)
        angles = np.linspace(0, 2*np.pi, len(metrics), endpoint=False).tolist()
        angles += angles[:1]  # Complete the circle
        
        for result in results:
            values = [result.scores.get(metric, 0) for metric in metrics]
            values += values[:1]  # Complete the circle
            ax.plot(angles, values, 'o-', linewidth=2, label=result.model_id)
            ax.fill(angles, values, alpha=0.1)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([m.value for m in metrics])
        ax.set_ylim(0, 1)
        ax.set_title('Socratic Protocol - Resilience Profile', size=15, y=1.1)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        
        return fig
    
    def create_comparison_barplot(self, results: List[EvaluationResult], save_path: str = None):
        df_data = []
        for result in results:
            for metric, score in result.scores.items():
                df_data.append({
                    'model': result.model_id,
                    'metric': metric.value,
                    'score': score
                })
        
        df = pd.DataFrame(df_data)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(data=df, x='metric', y='score', hue='model', ax=ax)
        ax.set_title('Socratic Protocol - Metric Comparison')
        ax.set_ylabel('Score')
        ax.set_xlabel('Metric')
        plt.xticks(rotation=45)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight', dpi=300)
        
        return fig
    
    def generate_html_report(self, results: List[EvaluationResult], output_path: str):
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Socratic Protocol Evaluation Report</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                .model-card { border: 1px solid #ddd; padding: 20px; margin: 10px 0; border-radius: 5px; }
                .score { color: #2c3e50; font-weight: bold; }
                .response { background: #f8f9fa; padding: 10px; margin: 5px 0; border-left: 3px solid #3498db; }
            </style>
        </head>
        <body>
            <h1>🧠 Socratic Protocol Evaluation Report</h1>
            <p>Generated on: {timestamp}</p>
        """.format(timestamp=pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        for result in results:
            html_content += f"""
            <div class="model-card">
                <h2>Model: {result.model_id}</h2>
                <h3>Dialogue: {result.dialogue_id}</h3>
                <h4>Scores:</h4>
                <ul>
            """
            
            for metric, score in result.scores.items():
                html_content += f'<li>{metric.value}: <span class="score">{score:.3f}</span></li>'
            
            html_content += "</ul><h4>Responses:</h4>"
            
            for i, response in enumerate(result.responses):
                html_content += f"""
                <div class="response">
                    <strong>Phase {i+1}:</strong><br>
                    {response}
                </div>
                """
            
            html_content += "</div>"
        
        html_content += "</body></html>"
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path
