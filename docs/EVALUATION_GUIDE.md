# 🧪 LLM Evaluation Framework - User Guide

## Overview

The LLM Evaluation Framework provides automated testing for AI-powered features in the UE5 Semantic Asset Organizer. It uses a combination of functional tests (rule-based) and AI-judge evaluation (LLM-as-judge) to ensure quality.

---

## 📁 Module Structure

```
src/evaluation/
├── __init__.py           # Module exports
├── evaluator.py          # Core evaluation logic
└── datasets.py           # Test datasets

tests/
└── test_llm_evaluation.py  # Test runner
```

---

## 🎯 Features Evaluated

### 1. **Asset Naming** (`ai/asset_naming.py`)
- **Metrics**:
  - `naming_convention`: Follows UE5 prefixes (SM_, T_, M_, etc.)
  - `format_validity`: No special characters or spaces
  - `relevance`: AI-judge score for quality and descriptiveness

### 2. **Material Generation** (`materials/material_generator.py`)
- **Metrics**:
  - `format_validity`: Valid JSON structure with required keys
  - `pbr_plausibility`: Values in valid ranges (0-1)
  - `relevance`: AI-judge score for prompt alignment

### 3. **Metadata Generation** (`ai/metadata_generator.py`)
- **Metrics**:
  - `format_validity`: Has description and tags
  - `consistency`: Description length (< 50 words)
  - `relevance`: AI-judge score for quality

---

## 🚀 Quick Start

### **Step 1: Run Evaluation Suite**

```bash
cd <project_root>
python tests/test_llm_evaluation.py
```

### **Step 2: Review Results**

The test runner will:
1. Run all test cases
2. Display pass/fail status
3. Show detailed metrics
4. Export results to `evaluation_results.json`

### **Expected Output:**

```
============================================================
LLM EVALUATION SUITE
============================================================

Initializing evaluator with Claude AI...
Provider: anthropic
Model: claude-sonnet-4-6

Total tests to run: 14
  - Asset Naming: 5
  - Material Generation: 5
  - Metadata Generation: 4

============================================================
1. ASSET NAMING EVALUATION
============================================================

Test 1/5: Basic static mesh naming - should add SM_ prefix
  Input: cube_01 (StaticMesh)
  Result: SM_Cube_01
  Status: ✓ PASS
  ✓ naming_convention: 1.00 | ✓ format_validity: 1.00 | ✓ relevance: 0.95

...

============================================================
EVALUATION SUMMARY
============================================================
Total Tests: 14
Passed: 13
Failed: 1
Pass Rate: 92.9%

Average Scores:
  naming_convention: 0.98
  format_validity: 1.00
  pbr_plausibility: 0.96
  relevance: 0.89

✓ Results exported to evaluation_results.json
```

---

## 📊 Understanding Results

### **EvaluationResult Object**

```python
@dataclass
class EvaluationResult:
    feature: str                    # "asset_naming", "material_generation", etc.
    input: Dict                     # Test input
    output: Dict                    # Generated output
    expected: Optional[Dict]        # Expected output (if available)
    metrics: Dict[str, float]       # Metric scores (0-1)
    passed: bool                    # Overall pass/fail
    feedback: str                   # Human-readable feedback
    timestamp: str                  # ISO timestamp
```

### **Pass Threshold**

- Default: **0.7** (70%)
- All metrics must score ≥ 0.7 to pass
- Configurable via `evaluator.pass_threshold`

### **Metric Scores**

- **1.0** = Perfect
- **0.7-0.9** = Good (passes)
- **0.5-0.7** = Needs improvement (fails)
- **< 0.5** = Poor (fails)

---

## 🔧 Advanced Usage

### **Custom Evaluation**

```python
from evaluation.evaluator import LLMEvaluator

# Initialize
evaluator = LLMEvaluator()

# Evaluate asset naming
result = evaluator.evaluate_asset_naming(
    original_name="cube_01",
    suggested_name="SM_Cube_01",
    asset_type="StaticMesh"
)

print(f"Passed: {result.passed}")
print(f"Metrics: {result.metrics}")
```

### **Evaluate Material Generation**

```python
result = evaluator.evaluate_material_generation(
    prompt="shiny red metal",
    parameters={
        'BaseColor': [0.65, 0.08, 0.05],
        'Metallic': 0.82,
        'Roughness': 0.38,
        'Specular': 0.5
    }
)
```

### **Evaluate Metadata Generation**

```python
result = evaluator.evaluate_metadata_generation(
    asset_info={'name': 'SM_Chair', 'type': 'StaticMesh'},
    metadata={
        'description': 'Static mesh of a chair',
        'tags': ['furniture', 'chair', 'prop']
    }
)
```

### **Export Results**

```python
# Export to JSON
evaluator.export_results('my_results.json')

# Get summary statistics
summary = evaluator.get_summary()
print(f"Pass rate: {summary['pass_rate']:.1%}")
```

---

## 📝 Adding New Test Cases

### **Edit `src/evaluation/datasets.py`**

```python
class EvaluationDataset:
    ASSET_NAMING_TESTS = [
        # Add your test case
        {
            'input': {
                'name': 'my_asset',
                'type': 'StaticMesh'
            },
            'expected': {
                'name': 'SM_MyAsset'
            },
            'description': 'My custom test case'
        }
    ]
```

---

## 🎓 Evaluation Types Explained

### **1. Functional Tests (Rule-based)**

Fast, deterministic validation:
- Naming conventions
- Value ranges
- Required fields
- Format validation

**Pros:** Fast, reliable, no API calls  
**Cons:** Can't evaluate quality or semantics

### **2. AI-Judge Evaluation (LLM-as-judge)**

Uses Claude to evaluate Claude's outputs:
- Descriptiveness
- Relevance to prompt
- Quality assessment
- Semantic correctness

**Pros:** Evaluates quality and semantics  
**Cons:** Slower, costs API tokens, less deterministic

### **3. Gold Standard Comparison**

Compare against known good outputs:
- Similarity scoring
- Regression detection

**Note:** Currently using expected values in test datasets

---

## 🔍 Troubleshooting

### **Issue: All AI-judge scores are 0.5**

**Cause:** LLM client not initialized or API error

**Solution:**
```python
# Check API key is set
import os
print(os.getenv('ANTHROPIC_API_KEY'))

# Check config
from utils.config import Config
config = Config()
print(config.get('llm.provider'))
```

### **Issue: Tests fail with import errors**

**Cause:** Python path not set correctly

**Solution:**
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
```

### **Issue: Low pass rate**

**Cause:** Threshold too high or AI outputs need improvement

**Solution:**
```python
# Lower threshold temporarily
evaluator.pass_threshold = 0.6  # 60% instead of 70%

# Or improve prompts in AI features
```

---

## 📈 Best Practices

### **1. Run Evaluations Regularly**
- Before releases
- After prompt changes
- When updating AI models
- During development

### **2. Track Metrics Over Time**
```python
# Save results with timestamps
evaluator.export_results(f'results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
```

### **3. Use for Prompt Engineering**
- Test different prompts
- Compare scores
- Iterate based on metrics

### **4. Add Real-World Test Cases**
- Use actual project assets
- Include edge cases
- Test failure scenarios

---

## 🚀 Future: LangSmith Integration

When ready for production-grade evaluation:

### **Install LangSmith**
```bash
pip install langsmith
```

### **Set API Key**
```bash
export LANGSMITH_API_KEY="your-key"
```

### **Migrate Tests**
```python
from langsmith import Client
from langsmith.evaluation import evaluate

client = Client()

# Create dataset
dataset = client.create_dataset("ue5-asset-naming")

# Run evaluation with LangSmith
results = evaluate(
    lambda x: naming.suggest_name_for_unclear_asset(x),
    data=dataset,
    evaluators=[naming_evaluator, ai_judge_evaluator]
)
```

**Benefits:**
- Human annotation workflows
- Team collaboration
- Regression tracking
- Production monitoring
- Dataset versioning

---

## 📊 Metrics Reference

### **Asset Naming Metrics**

| Metric | Description | Pass Threshold |
|--------|-------------|----------------|
| `naming_convention` | Has correct UE5 prefix | ≥ 0.7 |
| `format_validity` | No invalid characters | ≥ 0.7 |
| `relevance` | AI-judge quality score | ≥ 0.7 |

### **Material Generation Metrics**

| Metric | Description | Pass Threshold |
|--------|-------------|----------------|
| `format_validity` | Has required keys | ≥ 0.7 |
| `pbr_plausibility` | Values in 0-1 range | ≥ 0.7 |
| `relevance` | Matches prompt | ≥ 0.7 |

### **Metadata Generation Metrics**

| Metric | Description | Pass Threshold |
|--------|-------------|----------------|
| `format_validity` | Has description & tags | ≥ 0.7 |
| `consistency` | Description < 50 words | ≥ 0.7 |
| `relevance` | AI-judge quality score | ≥ 0.7 |

---

## 💡 Tips

1. **Start with functional tests** - They're fast and catch obvious issues
2. **Use AI-judge sparingly** - It costs API tokens and is slower
3. **Build test datasets gradually** - Add cases as you find edge cases
4. **Track pass rates over time** - Monitor quality trends
5. **Combine with manual testing** - Automated tests don't catch everything

---

## 📚 Related Documentation

- `README.md` - Project overview
- `USAGE.md` - Feature usage guide
- `UE5_QUICK_COMMANDS.md` - Quick reference
- `FINAL_TESTING_SUMMARY.md` - Feature testing results

---

## 🎯 Summary

The LLM Evaluation Framework provides:
- ✅ Automated quality testing for AI features
- ✅ Functional + AI-judge evaluation
- ✅ Metrics tracking and reporting
- ✅ Easy integration with existing code
- ✅ Foundation for LangSmith migration

**Run evaluations regularly to maintain high quality AI outputs!**
