"""
LLM Evaluator - Core evaluation logic for AI features
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import json
from datetime import datetime
import sys
import os

if __name__ != '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai.llm_client import LLMClient, LLMProvider
from utils.logger import setup_logger
from utils.config import Config

logger = setup_logger(__name__)


class EvaluationMetric(Enum):
    """Available evaluation metrics"""
    ACCURACY = "accuracy"
    RELEVANCE = "relevance"
    CONSISTENCY = "consistency"
    FORMAT_VALIDITY = "format_validity"
    PBR_PLAUSIBILITY = "pbr_plausibility"
    NAMING_CONVENTION = "naming_convention"
    DESCRIPTION_QUALITY = "description_quality"


@dataclass
class EvaluationResult:
    """Result of a single evaluation"""
    feature: str
    input: Dict
    output: Dict
    expected: Optional[Dict]
    metrics: Dict[str, float]  # metric_name -> score (0-1)
    passed: bool
    feedback: str
    timestamp: str
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class LLMEvaluator:
    """Evaluation framework for LLM-powered features"""
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize evaluator
        
        Args:
            llm_client: Optional LLM client for AI-judge evaluation. 
                       If None, will create one with Anthropic provider from config.
        """
        if llm_client:
            self.llm_client = llm_client
        else:
            # Initialize with Anthropic provider from config
            config = Config()
            provider_str = config.get('llm.provider', 'anthropic')
            provider = LLMProvider.ANTHROPIC if provider_str == 'anthropic' else LLMProvider.OPENAI
            model = config.get('llm.model', 'claude-sonnet-4-6')
            self.llm_client = LLMClient(provider=provider, model=model)
        
        self.results: List[EvaluationResult] = []
        self.pass_threshold = 0.7  # Minimum score to pass
    
    # ==================== Main Evaluation Methods ====================
    
    def evaluate_asset_naming(self, original_name: str, suggested_name: str, 
                            asset_type: str = "Unknown") -> EvaluationResult:
        """
        Evaluate AI asset naming quality
        
        Args:
            original_name: Original asset name
            suggested_name: AI-suggested name
            asset_type: Asset type (StaticMesh, Texture2D, etc.)
        
        Returns:
            EvaluationResult with metrics and pass/fail status
        """
        metrics = {}
        
        # Functional test: Check naming convention
        metrics['naming_convention'] = self._check_naming_convention(suggested_name, asset_type)
        
        # Functional test: No special characters
        metrics['format_validity'] = self._check_valid_format(suggested_name)
        
        # AI-judge: Evaluate descriptiveness and quality
        metrics['relevance'] = self._ai_judge_naming(original_name, suggested_name, asset_type)
        
        passed = all(score >= self.pass_threshold for score in metrics.values())
        
        result = EvaluationResult(
            feature="asset_naming",
            input={"original_name": original_name, "asset_type": asset_type},
            output={"suggested_name": suggested_name},
            expected=None,
            metrics=metrics,
            passed=passed,
            feedback=self._generate_feedback(metrics),
            timestamp=datetime.now().isoformat()
        )
        
        self.results.append(result)
        logger.info(f"Asset naming evaluation: {original_name} -> {suggested_name} | {'PASS' if passed else 'FAIL'}")
        return result
    
    def evaluate_material_generation(self, prompt: str, parameters: Dict) -> EvaluationResult:
        """
        Evaluate AI material generation quality
        
        Args:
            prompt: Natural language material description
            parameters: Generated material parameters
        
        Returns:
            EvaluationResult with metrics and pass/fail status
        """
        metrics = {}
        
        # Functional test: Valid JSON structure
        metrics['format_validity'] = self._check_material_format(parameters)
        
        # Functional test: PBR value ranges
        metrics['pbr_plausibility'] = self._check_pbr_values(parameters)
        
        # AI-judge: Prompt alignment
        metrics['relevance'] = self._ai_judge_material(prompt, parameters)
        
        passed = all(score >= self.pass_threshold for score in metrics.values())
        
        result = EvaluationResult(
            feature="material_generation",
            input={"prompt": prompt},
            output={"parameters": parameters},
            expected=None,
            metrics=metrics,
            passed=passed,
            feedback=self._generate_feedback(metrics),
            timestamp=datetime.now().isoformat()
        )
        
        self.results.append(result)
        logger.info(f"Material generation evaluation: '{prompt}' | {'PASS' if passed else 'FAIL'}")
        return result
    
    def evaluate_metadata_generation(self, asset_info: Dict, metadata: Dict) -> EvaluationResult:
        """
        Evaluate AI metadata generation quality
        
        Args:
            asset_info: Asset information (name, type, etc.)
            metadata: Generated metadata (description, tags)
        
        Returns:
            EvaluationResult with metrics and pass/fail status
        """
        metrics = {}
        
        # Functional test: Required fields
        metrics['format_validity'] = self._check_metadata_format(metadata)
        
        # Functional test: Description length
        metrics['consistency'] = self._check_description_length(metadata.get('description', ''))
        
        # AI-judge: Quality and relevance
        metrics['relevance'] = self._ai_judge_metadata(asset_info, metadata)
        
        passed = all(score >= self.pass_threshold for score in metrics.values())
        
        result = EvaluationResult(
            feature="metadata_generation",
            input=asset_info,
            output=metadata,
            expected=None,
            metrics=metrics,
            passed=passed,
            feedback=self._generate_feedback(metrics),
            timestamp=datetime.now().isoformat()
        )
        
        self.results.append(result)
        logger.info(f"Metadata generation evaluation: {asset_info.get('name')} | {'PASS' if passed else 'FAIL'}")
        return result
    
    # ==================== Functional Tests (Rule-based) ====================
    
    def _check_naming_convention(self, name: str, asset_type: str) -> float:
        """Check if name follows UE5 conventions"""
        prefix_mapping = {
            'StaticMesh': 'SM_',
            'SkeletalMesh': 'SK_',
            'Texture2D': 'T_',
            'Material': 'M_',
            'MaterialInstanceConstant': 'MI_',
            'Blueprint': 'BP_',
        }
        
        expected_prefix = prefix_mapping.get(asset_type)
        
        if expected_prefix:
            return 1.0 if name.startswith(expected_prefix) else 0.0
        else:
            # Unknown type, check for any common prefix
            common_prefixes = list(prefix_mapping.values())
            has_prefix = any(name.startswith(p) for p in common_prefixes)
            return 1.0 if has_prefix else 0.5
    
    def _check_valid_format(self, name: str) -> float:
        """Check for invalid characters"""
        invalid_chars = [' ', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')']
        has_invalid = any(char in name for char in invalid_chars)
        return 0.0 if has_invalid else 1.0
    
    def _check_material_format(self, params: Dict) -> float:
        """Validate material parameter structure"""
        required_keys = ['BaseColor', 'Metallic', 'Roughness']
        has_all_keys = all(key in params for key in required_keys)
        return 1.0 if has_all_keys else 0.0
    
    def _check_pbr_values(self, params: Dict) -> float:
        """Check if PBR values are in valid ranges"""
        try:
            # Check BaseColor (RGB 0-1)
            base_color = params.get('BaseColor', [])
            if not isinstance(base_color, list) or len(base_color) != 3:
                return 0.0
            if not all(isinstance(v, (int, float)) and 0 <= v <= 1 for v in base_color):
                return 0.0
            
            # Check Metallic (0-1)
            metallic = params.get('Metallic', -1)
            if not isinstance(metallic, (int, float)) or not (0 <= metallic <= 1):
                return 0.0
            
            # Check Roughness (0-1)
            roughness = params.get('Roughness', -1)
            if not isinstance(roughness, (int, float)) or not (0 <= roughness <= 1):
                return 0.0
            
            return 1.0
        except Exception as e:
            logger.error(f"Error checking PBR values: {e}")
            return 0.0
    
    def _check_metadata_format(self, metadata: Dict) -> float:
        """Check metadata has required fields"""
        has_description = 'description' in metadata and len(str(metadata['description'])) > 0
        has_tags = 'tags' in metadata and len(metadata['tags']) > 0
        
        if has_description and has_tags:
            return 1.0
        elif has_description or has_tags:
            return 0.5
        else:
            return 0.0
    
    def _check_description_length(self, description: str) -> float:
        """Check description is concise (< 50 words)"""
        if not description:
            return 0.0
        
        word_count = len(str(description).split())
        
        if word_count == 0:
            return 0.0
        elif word_count <= 50:
            return 1.0
        else:
            # Penalize longer descriptions
            return max(0.0, 1.0 - (word_count - 50) / 50)
    
    # ==================== AI-Judge Evaluations (LLM-as-judge) ====================
    
    def _ai_judge_naming(self, original: str, suggested: str, asset_type: str) -> float:
        """Use LLM to judge naming quality"""
        prompt = f"""Evaluate the quality of this asset naming suggestion on a scale of 0-1:

Original name: {original}
Suggested name: {suggested}
Asset type: {asset_type}

Criteria:
- Is it descriptive and clear?
- Does it follow UE5 conventions?
- Is it better than the original?

Respond with ONLY a number between 0 and 1 (e.g., 0.85). No explanation."""
        
        try:
            response = self.llm_client.generate_completion(prompt, max_tokens=10, temperature=0.3)
            if response:
                # Extract number from response
                score_str = response.strip().replace(',', '.')
                score = float(score_str)
                return max(0.0, min(1.0, score))  # Clamp to 0-1
            return 0.5
        except Exception as e:
            logger.warning(f"AI judge naming failed: {e}")
            return 0.5  # Default if AI judge fails
    
    def _ai_judge_material(self, prompt: str, parameters: Dict) -> float:
        """Use LLM to judge material generation quality"""
        eval_prompt = f"""Evaluate how well these material parameters match the description:

Description: "{prompt}"

Generated Parameters:
- Base Color: {parameters.get('BaseColor')}
- Metallic: {parameters.get('Metallic')}
- Roughness: {parameters.get('Roughness')}
- Specular: {parameters.get('Specular', 0.5)}

Does this create a realistic material matching the description?

Respond with ONLY a number between 0 and 1 (e.g., 0.92). No explanation."""
        
        try:
            response = self.llm_client.generate_completion(eval_prompt, max_tokens=10, temperature=0.3)
            if response:
                score_str = response.strip().replace(',', '.')
                score = float(score_str)
                return max(0.0, min(1.0, score))
            return 0.5
        except Exception as e:
            logger.warning(f"AI judge material failed: {e}")
            return 0.5
    
    def _ai_judge_metadata(self, asset_info: Dict, metadata: Dict) -> float:
        """Use LLM to judge metadata quality"""
        eval_prompt = f"""Evaluate the quality of this asset metadata on a scale of 0-1:

Asset: {asset_info.get('name')} ({asset_info.get('type', 'Unknown')})

Generated Metadata:
Description: {metadata.get('description')}
Tags: {metadata.get('tags')}

Is the description accurate and useful? Are the tags relevant?

Respond with ONLY a number between 0 and 1 (e.g., 0.88). No explanation."""
        
        try:
            response = self.llm_client.generate_completion(eval_prompt, max_tokens=10, temperature=0.3)
            if response:
                score_str = response.strip().replace(',', '.')
                score = float(score_str)
                return max(0.0, min(1.0, score))
            return 0.5
        except Exception as e:
            logger.warning(f"AI judge metadata failed: {e}")
            return 0.5
    
    # ==================== Reporting ====================
    
    def _generate_feedback(self, metrics: Dict[str, float]) -> str:
        """Generate human-readable feedback"""
        feedback = []
        for metric, score in metrics.items():
            if score < self.pass_threshold:
                feedback.append(f"⚠ {metric}: {score:.2f} (below threshold)")
            else:
                feedback.append(f"✓ {metric}: {score:.2f}")
        return " | ".join(feedback)
    
    def export_results(self, filepath: str):
        """Export evaluation results to JSON"""
        results_dict = [result.to_dict() for result in self.results]
        
        with open(filepath, 'w') as f:
            json.dump(results_dict, f, indent=2)
        
        logger.info(f"Exported {len(self.results)} evaluation results to {filepath}")
    
    def get_summary(self) -> Dict:
        """Get evaluation summary statistics"""
        if not self.results:
            return {
                'total_evaluations': 0,
                'passed': 0,
                'failed': 0,
                'pass_rate': 0.0,
                'average_scores': {}
            }
        
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        
        # Calculate average scores per metric
        avg_scores = {}
        for result in self.results:
            for metric, score in result.metrics.items():
                if metric not in avg_scores:
                    avg_scores[metric] = []
                avg_scores[metric].append(score)
        
        avg_scores = {k: sum(v)/len(v) for k, v in avg_scores.items()}
        
        return {
            'total_evaluations': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': passed / total if total > 0 else 0,
            'average_scores': avg_scores
        }
    
    def print_summary(self):
        """Print evaluation summary to console"""
        summary = self.get_summary()
        
        print("\n" + "=" * 60)
        print("EVALUATION SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {summary['total_evaluations']}")
        print(f"Passed: {summary['passed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pass Rate: {summary['pass_rate']:.1%}")
        
        if summary['average_scores']:
            print("\nAverage Scores:")
            for metric, score in summary['average_scores'].items():
                print(f"  {metric}: {score:.2f}")
        
        print("=" * 60)
