# 🧪 LLM Evaluation - Quick Start

## Run Evaluations in 3 Steps

### **Step 1: Install Dependencies** (if needed)

The evaluation framework uses existing dependencies. No additional packages required!

### **Step 2: Run Evaluation Suite**

```bash
cd d:\Windsurf_AI\ue5_semantic_automation
python tests/test_llm_evaluation.py
```

### **Step 3: Review Results**

Check the console output and `evaluation_results.json` file.

---

## What Gets Tested

✅ **Asset Naming** (5 tests)
- Naming convention compliance
- Format validation
- AI quality scoring

✅ **Material Generation** (5 tests)
- PBR value ranges
- Parameter structure
- Prompt alignment

✅ **Metadata Generation** (4 tests)
- Description quality
- Tag relevance
- Format validation

**Total: 14 automated tests**

---

## Expected Output

```
============================================================
LLM EVALUATION SUITE
============================================================

Initializing evaluator with Claude AI...
Provider: anthropic
Model: claude-sonnet-4-6

Total tests to run: 14

============================================================
1. ASSET NAMING EVALUATION
============================================================

Test 1/5: Basic static mesh naming
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

## Custom Evaluation

### **Evaluate Single Feature**

```python
from evaluation.evaluator import LLMEvaluator

evaluator = LLMEvaluator()

# Test asset naming
result = evaluator.evaluate_asset_naming(
    original_name="cube_01",
    suggested_name="SM_Cube_01",
    asset_type="StaticMesh"
)

print(f"Passed: {result.passed}")
print(f"Metrics: {result.metrics}")
```

### **Evaluate Material**

```python
result = evaluator.evaluate_material_generation(
    prompt="shiny red metal",
    parameters={
        'BaseColor': [0.65, 0.08, 0.05],
        'Metallic': 0.82,
        'Roughness': 0.38
    }
)
```

---

## Files Created

```
src/evaluation/
├── __init__.py           # Module exports
├── evaluator.py          # Core evaluation logic (400+ lines)
├── datasets.py           # Test datasets (14 test cases)

tests/
└── test_llm_evaluation.py  # Test runner

docs/
└── EVALUATION_GUIDE.md   # Complete documentation
```

---

## Next Steps

1. ✅ Run the test suite
2. ✅ Review results
3. ✅ Add your own test cases to `datasets.py`
4. ✅ Integrate with CI/CD pipeline
5. ⏳ Consider LangSmith for production (future)

---

## Documentation

📚 **Full Guide**: `docs/EVALUATION_GUIDE.md`
📊 **Test Results**: `evaluation_results.json`
🎯 **Project Status**: `FINAL_TESTING_SUMMARY.md`

---

## Benefits

✅ **Quality Assurance** - Catch regressions before deployment  
✅ **Prompt Engineering** - Optimize prompts based on metrics  
✅ **Continuous Improvement** - Track quality over time  
✅ **Confidence** - Ship AI features with data-backed quality  

**Happy Testing! 🚀**
