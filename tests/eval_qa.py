"""
Evaluation script for the contract Q&A chain.
Runs a fixed set of questions and checks basic correctness + citation behavior.
"""

import json
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chains import create_qa_chain


def main():
    qa_pairs_path = PROJECT_ROOT / "tests" / "qa_pairs.json"

    if not qa_pairs_path.is_file():
        print(f"Error: qa_pairs.json not found at {qa_pairs_path}")
        return 1

    with qa_pairs_path.open(encoding="utf-8") as f:
        qa_pairs = json.load(f)

    print(f"Loaded {len(qa_pairs)} evaluation questions.\n")

    try:
        qa_chain = create_qa_chain()
    except Exception as e:
        print(f"Failed to create QA chain: {e}")
        return 1

    results = []
    success_count = 0
    citation_count = 0

    for i, item in enumerate(qa_pairs, 1):
        question = item["question"]
        expected_snippet = item["expected_answer_snippet"]

        print(f"[{i:2d}/{len(qa_pairs)}]  {question}")

        try:
            # The chain expects both 'question' and 'chat_history'
            output = qa_chain.invoke({
                "question": question,
                "chat_history": []                # ← this fixes the missing variable error
            })

            # Handle different possible output shapes
            if isinstance(output, dict) and "answer" in output:
                answer = output["answer"]
            else:
                answer = str(output)

            contains_expected = expected_snippet.lower() in answer.lower()
            has_citation = "[" in answer and "]" in answer

            success_count += contains_expected
            citation_count += has_citation

            mark = "✓" if contains_expected else "✗"
            cit  = "✓" if has_citation else "✗"

            print(f"      {mark}  expected snippet    {cit}  citation")

            if not contains_expected:
                excerpt = answer[:220].replace("\n", " ").replace("\r", " ")
                print(f"      Answer excerpt: {excerpt} …")

            print()

            results.append({
                "question": question,
                "answer": answer,
                "contains_expected": contains_expected,
                "has_citation": has_citation,
                "category": item.get("category", "?")
            })

        except Exception as e:
            print(f"      ERROR: {str(e)}\n")
            results.append({
                "question": question,
                "answer": f"ERROR: {str(e)}",
                "contains_expected": False,
                "has_citation": False
            })

    # Final summary
    total = len(results)
    if total > 0:
        print("─" * 70)
        print(f"Success rate (expected snippet present): "
              f"{success_count / total:.1%}   ({success_count}/{total})")
        print(f"Citation rate:                       "
              f"{citation_count / total:.1%}   ({citation_count}/{total})")
        print("─" * 70)

    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)