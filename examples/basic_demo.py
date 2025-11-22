#!/usr/bin/env python3
"""
Basic demo of The Socratic Protocol
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from socratic_protocol.core import SocraticEvaluator
from socratic_protocol.adapters import SimulatedAdapter
from socratic_protocol.visualization import ResultsVisualizer

def run_basic_demo():
    print("🚀 The Socratic Protocol - Basic Demo")
    print("=" * 50)
    
    # Initialize components
    evaluator = SocraticEvaluator()
    visualizer = ResultsVisualizer()
    
    # Test different model personalities
    models = [
        SimulatedAdapter("balanced_model", "balanced"),
        SimulatedAdapter("rigid_model", "rigid"), 
        SimulatedAdapter("flexible_model", "flexible")
    ]
    
    results = []
    
    for model in models:
        print(f"\n🧠 Testing {model.model_id}...")
        
        for dialogue_id in ["boundary_test", "resource_negotiation"]:
            print(f"  📝 Running {dialogue_id}...")
            result = evaluator.evaluate_model(model, dialogue_id)
            results.append(result)
            
            # Print scores
            print(f"    Scores: {result.scores}")
    
    # Generate visualizations
    print("\n📊 Generating visualizations...")
    visualizer.create_radar_chart(results, "demo_radar.png")
    visualizer.create_comparison_barplot(results, "demo_barplot.png") 
    visualizer.generate_html_report(results, "demo_report.html")
    
    print("✅ Demo complete!")
    print("📁 Generated files:")
    print("   - demo_radar.png (Radar chart)")
    print("   - demo_barplot.png (Bar plot)")
    print("   - demo_report.html (Detailed report)")

if __name__ == "__main__":
    run_basic_demo()
