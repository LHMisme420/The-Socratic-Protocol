#!/usr/bin/env python3
"""
Quick start script for Socratic Protocol Demo
Run with: python quick_start.py
"""

from socratic_demo import run_demo, visualize_results

if __name__ == "__main__":
    print("🚀 Launching Socratic Protocol Demo...")
    results = run_demo()
    df = visualize_results(results)
    print("\n✅ Demo completed successfully!")
    print("📁 Check generated charts and socratic_demo_results.json")
