"""
LLM Evaluation Framework

This module provides evaluation tools for AI-powered features in the UE5 Semantic Asset Organizer.

Features:
- Functional tests (rule-based validation)
- AI-judge evaluation (LLM-as-judge)
- Gold standard comparison
- Metrics tracking and reporting
"""

from evaluation.evaluator import LLMEvaluator, EvaluationResult, EvaluationMetric
from evaluation.datasets import EvaluationDataset

__all__ = ['LLMEvaluator', 'EvaluationResult', 'EvaluationMetric', 'EvaluationDataset']
