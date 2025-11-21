"""
Complete System Integration Test
Tests the full pipeline: Intake → Unified Analyzer → Report Generation
"""
import sys
sys.path.append('../backend')
sys.path.append('../backend/services')

from report_generator import ReportGenerator
import json

# Complete sample intake
SAMPLE_INTAKE = {
    "intake_id": "test-integration-001",
    "user_id": "user-test-001",
    "email": "test@example.com",
    "first_name": "Alex",
    "intake_version": "forum-ready-15-v1",
    "responses": [
        {
            "q_id": "Q1",
            "question_text": "Tell us about a recent challenge",
            "answer_text": "I faced a complex technical problem that required systematic analysis and careful planning. I broke it down into steps and solved it methodically.",
            "word_count": 25
        },
        {
            "q_id": "Q2",
            "question_text": "When overwhelmed, what happens?",
            "answer_text": "My chest tightens and I feel the need to control everything. I breathe shallowly and try to manage all the details myself.",
            "word_count": 24
        },
        {
            "q_id": "Q3",
            "question_text": "How has your understanding changed?",
            "answer_text": "I've learned to integrate multiple perspectives and see systems holistically. I value both logic and intuition now.",
            "word_count": 19
        },
        {
            "q_id": "Q4",
            "question_text": "Tell us about a time you felt misunderstood",
            "answer_text": "When I tried explaining my vision, others couldn't see it. I learned to communicate more clearly and meet people where they are.",
            "word_count": 24
        },
        {
            "q_id": "Q5",
            "question_text": "Values tested",
            "answer_text": "I had to choose between honesty and comfort. I chose truth even though it was difficult, and I felt aligned with my principles.",
            "word_count": 24
        },
        {
            "q_id": "Q6",
            "question_text": "Opposing values",
            "answer_text": "I felt pulled between ambition and rest. I realized both are necessary and now I honor cycles of effort and recovery.",
            "word_count": 22
        },
        {
            "q_id": "Q7",
            "question_text": "Inner voice",
            "answer_text": "I notice my self-talk can be harsh and critical. I'm learning to be more compassionate with myself and question negative thoughts.",
            "word_count": 22
        },
        {
            "q_id": "Q8",
            "question_text": "Role in groups",
            "answer_text": "I tend to facilitate and help the group see different perspectives. Others say I help them think more deeply.",
            "word_count": 20
        },
        {
            "q_id": "Q9",
            "question_text": "Staying open to different views",
            "answer_text": "I remind myself that everyone has valid reasons for their perspectives. Curiosity helps me stay connected even when I disagree.",
            "word_count": 21
        },
        {
            "q_id": "Q10",
            "question_text": "What gets under your skin",
            "answer_text": "Rigidity and close-mindedness frustrate me. I admire people who can hold paradoxes and remain curious.",
            "word_count": 15
        },
        {
            "q_id": "Q11",
            "question_text": "Body and energy",
            "answer_text": "I'm more aware of tension in my body now. I notice when I'm holding stress and try to release it through movement and breath.",
            "word_count": 26
        },
        {
            "q_id": "Q12",
            "question_text": "What is money?",
            "answer_text": "Money represents freedom and security to me. I'm disciplined about saving and investing for long-term goals.",
            "word_count": 17
        },
        {
            "q_id": "Q13",
            "question_text": "Creativity and imagination",
            "answer_text": "I express creativity through problem-solving and writing. Imagination helps me envision possibilities beyond current constraints.",
            "word_count": 16
        },
        {
            "q_id": "Q14",
            "question_text": "Connection to something larger",
            "answer_text": "I find meaning through meditation and contemplating my place in the universe. I feel connected to a larger purpose through serving others.",
            "word_count": 24
        },
        {
            "q_id": "Q15",
            "question_text": "Self-talk during setbacks",
            "answer_text": "I used to be very self-critical. Now I try to speak to myself like a good friend would. Perspective and patience help me move forward.",
            "word_count": 26
        },
    ]
}

def run_complete_test():
    print("="*80)
    print("COMPLETE SYSTEM INTEGRATION TEST")
    print("="*80)
    
    print("\n📝 Generating report for sample intake...")
    
    try:
        generator = ReportGenerator(SAMPLE_INTAKE)
        report = generator.generate_report()
        
        print("\n✅ Report generated successfully!\n")
        
        # Save to file first
        output_file = 'complete_test_report.json'
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"💾 Full report saved to: {output_file}")
        
        print("\n📊 REPORT CONTENTS:")
        print("-"*80)
        
        # Display report sections
        for key in report.keys():
            print(f"\n📌 {key.upper().replace('_', ' ')}:")
            value = report[key]
            
            if isinstance(value, dict):
                # Show dictionary contents
                for k, v in list(value.items())[:5]:  # Show first 5 items
                    if isinstance(v, (str, int, float)):
                        v_str = str(v)[:80] if isinstance(v, str) else str(v)
                        print(f"   {k}: {v_str}")
                    elif isinstance(v, dict):
                        print(f"   {k}: {list(v.keys())}")
                    elif isinstance(v, list):
                        print(f"   {k}: [{len(v)} items]")
                    else:
                        print(f"   {k}: {type(v).__name__}")
                
                if len(value) > 5:
                    print(f"   ... ({len(value) - 5} more items)")
            
            elif isinstance(value, list):
                print(f"   [{len(value)} items]")
                if value and len(value) > 0:
                    print(f"   First item: {value[0]}")
            
            else:
                v_str = str(value)[:100]
                print(f"   {v_str}{'...' if len(str(value)) > 100 else ''}")
        
        print("\n" + "="*80)
        print("✅ INTEGRATION TEST COMPLETE")
        print(f"📄 Review full report in: {output_file}")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_complete_test()