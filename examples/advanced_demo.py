#!/usr/bin/env python3
"""
Advanced demo with real model integration (when API keys available)
"""

import os
from socratic_protocol.core import SocraticEvaluator
from socratic_protocol.adapters import OpenAIModelAdapter, HuggingFaceAdapter
from socratic_protocol.visualization import ResultsVisualizer

def run_advanced_demo():
    print("🚀 The Socratic Protocol - Advanced Demo")
    print("=" * 50)
    
    evaluator = SocraticEvaluator()
    visualizer = ResultsVisualizer()
    results = []
    
    # Example with OpenAI (commented out - needs API key)
    if os.getenv('OPENAI_API_KEY'):
        openai_model = OpenAIModelAdapter("gpt-3.5-turbo", os.getenv('OPENAI_API_KEY'))
        result = evaluator.evaluate_model(openai_model, "boundary_test")
        results.append(result)
    
    # Example with Hugging Face (commented out - needs API key)  
    if os.getenv('HF_API_KEY'):
        hf_model = HuggingFaceAdapter("microsoft/DialoGPT-large", os.getenv('HF_API_KEY'))
        result = evaluator.evaluate_model(hf_model, "boundary_test")
        results.append(result)
    
    if results:
        visualizer.create_radar_chart(results, "advanced_radar.png")
        visualizer.generate_html_report(results, "advanced_report.html")
        print("✅ Advanced demo complete!")
    else:
        print("ℹ️  Set OPENAI_API_KEY or HF_API_KEY environment variables to run with real models")

if __name__ == "__main__":
    run_advanced_demo()
