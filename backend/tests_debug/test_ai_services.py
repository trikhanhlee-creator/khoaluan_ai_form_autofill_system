"""
Test file for AI Services
Run: python backend/test_ai_services.py
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.services.ai import ThinkingService, SuggestionsService


def test_thinking_service():
    """Test thinking service"""
    print("\n" + "="*60)
    print("TESTING THINKING SERVICE")
    print("="*60)
    
    try:
        service = ThinkingService()
        
        sample_text = """
        The quick brown fox jumped over the lazy dog. This sentence is very important.
        It contains many words. The dog was sleeping under the tree.
        """
        
        print("\n1. Testing text analysis...")
        result = service.analyze_text(
            text=sample_text,
            focus_areas=["clarity", "structure"],
            context="Sample paragraph analysis"
        )
        
        if result["status"] == "success":
            print("✓ Analysis successful!")
            print(f"Response:\n{result['analysis'][:200]}...\n")
        else:
            print(f"✗ Error: {result['message']}")
        
        print("\n2. Testing insightgeneration...")
        result = service.generate_insights(
            text=sample_text,
            insight_type="clarity"
        )
        
        if result["status"] == "success":
            print("✓ Insights generated successfully!")
            print(f"Response:\n{result['insights'][:200]}...\n")
        else:
            print(f"✗ Error: {result['message']}")
    
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")


def test_suggestions_service():
    """Test suggestions service"""
    print("\n" + "="*60)
    print("TESTING SUGGESTIONS SERVICE")
    print("="*60)
    
    try:
        service = SuggestionsService()
        
        sample_text = "The big giant elephant was very very large and extremely huge in size."
        
        print("\n1. Testing suggestion generation...")
        result = service.generate_suggestions(
            text=sample_text,
            suggestion_type="clarity",
            count=3
        )
        
        if result["status"] == "success":
            print("✓ Suggestions generated successfully!")
            print(f"Response:\n{result['suggestions'][:200]}...\n")
        else:
            print(f"✗ Error: {result['message']}")
        
        print("\n2. Testing alternative suggestions...")
        result = service.suggest_alternatives(
            text="very very large",
            context="describing an elephant"
        )
        
        if result["status"] == "success":
            print("✓ Alternatives suggested successfully!")
            print(f"Response:\n{result['alternatives'][:200]}...\n")
        else:
            print(f"✗ Error: {result['message']}")
        
        print("\n3. Testing quick suggestion...")
        result = service.quick_suggestion("The dog eat food")
        
        if result["status"] == "success":
            print("✓ Quick suggestion generated successfully!")
            print(f"Response:\n{result['suggestion'][:200]}...\n")
        else:
            print(f"✗ Error: {result['message']}")
    
    except Exception as e:
        print(f"✗ Test failed: {str(e)}")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI SERVICES TEST SUITE")
    print("="*60)
    print("\nMake sure you have set OPENROUTER_API_KEY in .env")
    print("And run: pip install -r requirements.txt")
    
    try:
        test_thinking_service()
        test_suggestions_service()
        
        print("\n" + "="*60)
        print("TESTS COMPLETED")
        print("="*60)
    
    except KeyError as e:
        print(f"\n✗ Configuration error: {str(e)}")
        print("Please ensure OPENROUTER_API_KEY is set in .env file")
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")


if __name__ == "__main__":
    main()
