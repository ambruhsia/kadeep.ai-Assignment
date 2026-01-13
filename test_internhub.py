"""
Test script to demonstrate InternHub capabilities
Run: python test_internhub.py
"""
import json
from student_profile import StudentProfile
from internship_job import InternshipJob
from ai_agent import InternHubAIAgent, analyze_internship_fit, generate_resume, get_ats_score
from example_data.examples import (
    get_example_student, 
    get_example_job,
    get_example_student_2,
    get_example_job_2
)


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def test_case_1():
    """Test Case 1: Strong candidate for full-stack role"""
    print_section("TEST CASE 1: Strong Full-Stack Match")
    
    student = get_example_student()
    job = get_example_job()
    
    print(f"\n👤 Student: {student.name}")
    print(f"   Skills: {', '.join(student.skills)}")
    print(f"   CGPA: {student.cgpa}")
    
    print(f"\n💼 Job: {job.title} at {job.company}")
    print(f"   Required: {', '.join(job.required_skills)}")
    
    result = analyze_internship_fit(student, job)
    
    print(f"\n✨ MATCH SCORE: {result['confidence_score']}/1.0 ({result['match_percentage']})")
    print(f"   Recommendation: {'✅ APPLY NOW' if result['is_match'] else '⚠️  UPSKILL FIRST'}")
    print(f"\n💪 Strengths: {len(result['strengths'])} found")
    for strength in result['strengths']:
        print(f"   ✓ {strength}")
    
    print(f"\n🔧 Skill Gaps: {len(result['skill_gaps'])} gaps")
    for gap in result['skill_gaps']:
        print(f"   • {gap['skill']} ({gap['category']})")


def test_case_2():
    """Test Case 2: Beginner candidate for backend role"""
    print_section("TEST CASE 2: Beginner for Backend Role (High Challenge)")
    
    student = get_example_student_2()
    job = get_example_job_2()
    
    print(f"\n👤 Student: {student.name}")
    print(f"   Skills: {', '.join(student.skills)}")
    print(f"   CGPA: {student.cgpa}")
    
    print(f"\n💼 Job: {job.title} at {job.company}")
    print(f"   Required: {', '.join(job.required_skills)}")
    
    result = analyze_internship_fit(student, job)
    
    print(f"\n✨ MATCH SCORE: {result['confidence_score']}/1.0 ({result['match_percentage']})")
    print(f"   Recommendation: {'✅ APPLY NOW' if result['is_match'] else '⚠️  UPSKILL FIRST'}")
    print(f"\n💪 Strengths: {len(result['strengths'])} found")
    for strength in result['strengths']:
        print(f"   ✓ {strength}")
    
    print(f"\n🔧 Skill Gaps: {len(result['skill_gaps'])} gaps")
    for gap in result['skill_gaps'][:5]:
        print(f"   • {gap['skill']} ({gap['category']})")


def test_resume_generation():
    """Test Case 3: Resume generation"""
    print_section("TEST CASE 3: Resume Generation")
    
    student = get_example_student()
    job = get_example_job()
    
    print(f"\n📄 Generating resume for {student.name}")
    print(f"   Target: {job.title} at {job.company}")
    
    resume = generate_resume(student, job)
    
    print(f"\n✅ Generated Resume Preview:")
    print("-" * 70)
    print(resume[:500] + "...")
    print("-" * 70)


def test_ats_scoring():
    """Test Case 4: ATS scoring"""
    print_section("TEST CASE 4: ATS Score Calculation")
    
    student = get_example_student()
    job = get_example_job()
    
    # Generate resume first
    resume = generate_resume(student, job)
    ats_result = get_ats_score(student, job, resume)
    
    print(f"\n🤖 ATS Analysis for {job.title}")
    print(f"   Job Keywords: {ats_result['keyword_count']}")
    
    print(f"\n✨ ATS SCORE: {ats_result['ats_percentage']} ({ats_result['ats_score']}/1.0)")
    
    if ats_result['matched_keywords']:
        print(f"\n✅ Matched Keywords ({len(ats_result['matched_keywords'])}):")
        for kw in ats_result['matched_keywords']:
            print(f"   • {kw}")
    
    if ats_result['missing_keywords']:
        print(f"\n❌ Missing Keywords ({len(ats_result['missing_keywords'])}):")
        for kw in ats_result['missing_keywords']:
            print(f"   • {kw}")


def test_full_analysis():
    """Test Case 5: Complete end-to-end analysis"""
    print_section("TEST CASE 5: Complete End-to-End Analysis")
    
    student = get_example_student()
    job = get_example_job()
    
    print(f"\n📊 Running full analysis pipeline...")
    print(f"   Student: {student.name}")
    print(f"   Job: {job.title} at {job.company}")
    
    # 1. Match analysis
    print("\n1️⃣  MATCH ANALYSIS")
    match = analyze_internship_fit(student, job)
    print(f"    Match Score: {match['confidence_score']}/1.0")
    print(f"    Fit Assessment: {'✅ APPLY' if match['is_match'] else '⚠️  PREPARE'}")
    
    # 2. Resume generation
    print("\n2️⃣  RESUME GENERATION")
    resume = generate_resume(student, job)
    print(f"    ✓ Resume generated ({len(resume)} chars)")
    
    # 3. ATS scoring
    print("\n3️⃣  ATS SCORING")
    ats = get_ats_score(student, job, resume)
    print(f"    ATS Score: {ats['ats_percentage']}")
    print(f"    Keywords Matched: {ats['matched_count']}/{ats['keyword_count']}")
    
    # 4. Summary
    print("\n📊 PIPELINE SUMMARY")
    print(f"    ├─ Match Confidence: {match['confidence_score']}")
    print(f"    ├─ ATS Compatibility: {ats['ats_score']}")
    print(f"    └─ Ready to Apply: {'✅ YES' if match['is_match'] and ats['ats_score'] >= 0.7 else '⚠️  REVIEW'}")


def test_json_serialization():
    """Test Case 6: JSON serialization"""
    print_section("TEST CASE 6: JSON Serialization")
    
    student = get_example_student()
    job = get_example_job()
    
    print("\n📝 Testing JSON serialization...")
    
    # Serialize to JSON
    student_json = student.to_json()
    job_json = job.to_json()
    
    print(f"\n✅ Student serialized ({len(student_json)} chars)")
    print(f"✅ Job serialized ({len(job_json)} chars)")
    
    # Deserialize from JSON
    student_restored = StudentProfile.from_json(student_json)
    job_restored = InternshipJob.from_json(job_json)
    
    print(f"\n✅ Student deserialized: {student_restored.name}")
    print(f"✅ Job deserialized: {job_restored.title}")
    
    # Verify they match
    match_before = analyze_internship_fit(student, job)
    match_after = analyze_internship_fit(student_restored, job_restored)
    
    print(f"\n🔍 Verification:")
    print(f"    Score before: {match_before['confidence_score']}")
    print(f"    Score after:  {match_after['confidence_score']}")
    print(f"    Match: {'✅ IDENTICAL' if match_before['confidence_score'] == match_after['confidence_score'] else '❌ DIFFERENT'}")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "🎓 INTERNHUB - COMPREHENSIVE TEST SUITE" + " " * 13 + "║")
    print("╚" + "=" * 68 + "╝")
    
    try:
        test_case_1()
        test_case_2()
        test_resume_generation()
        test_ats_scoring()
        test_full_analysis()
        test_json_serialization()
        
        print_section("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("\n📊 Summary:")
        print("   ✓ Match scoring algorithm")
        print("   ✓ Skill gap analysis")
        print("   ✓ Resume generation")
        print("   ✓ ATS scoring")
        print("   ✓ Full pipeline")
        print("   ✓ Data serialization")
        print("\n" + "=" * 70 + "\n")
        
    except Exception as e:
        print_section("❌ TEST FAILED!")
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
