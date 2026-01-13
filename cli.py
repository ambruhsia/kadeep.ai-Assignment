"""
InternHub CLI - Command Line Interface for AI Matching
"""
import json
import sys
from typing import Dict, Optional
from student_profile import StudentProfile
from internship_job import InternshipJob
from ai_agent import (
    InternHubAIAgent,
    analyze_internship_fit,
    generate_resume,
    get_ats_score
)


class InternHubCLI:
    """Command-line interface for InternHub"""
    
    def __init__(self):
        self.agent = InternHubAIAgent(use_mock=True)
    
    def run_interactive(self):
        """Run interactive mode"""
        print("=" * 60)
        print("   🎓 INTERNHUB - AI-Powered Internship Matching")
        print("=" * 60)
        print()
        
        while True:
            print("What would you like to do?")
            print("1. Analyze internship fit")
            print("2. Generate optimized resume")
            print("3. Get ATS score")
            print("4. Full analysis (all features)")
            print("5. Load from JSON files")
            print("6. Exit")
            print()
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                self._analyze_fit_interactive()
            elif choice == "2":
                self._generate_resume_interactive()
            elif choice == "3":
                self._ats_score_interactive()
            elif choice == "4":
                self._full_analysis_interactive()
            elif choice == "5":
                self._load_from_files()
            elif choice == "6":
                print("Thank you for using InternHub! Goodbye! 👋")
                break
            else:
                print("❌ Invalid choice. Please try again.\n")
    
    def _analyze_fit_interactive(self):
        """Analyze internship fit"""
        print("\n" + "=" * 60)
        print("STEP 1: ANALYZE INTERNSHIP FIT")
        print("=" * 60)
        
        student = self._input_student_profile()
        job = self._input_internship_job()
        
        print("\n⏳ Analyzing fit...")
        result = analyze_internship_fit(student, job, use_mock=True)
        
        self._print_match_analysis(result)
    
    def _generate_resume_interactive(self):
        """Generate optimized resume"""
        print("\n" + "=" * 60)
        print("STEP 2: GENERATE OPTIMIZED RESUME")
        print("=" * 60)
        
        student = self._input_student_profile()
        job = self._input_internship_job()
        
        print("\n⏳ Generating resume...")
        resume = generate_resume(student, job, use_mock=True)
        
        print("\n📄 OPTIMIZED RESUME FOR:", job.title)
        print("-" * 60)
        print(resume)
        print("-" * 60)
    
    def _ats_score_interactive(self):
        """Get ATS score"""
        print("\n" + "=" * 60)
        print("STEP 3: ATS SCORE ANALYSIS")
        print("=" * 60)
        
        student = self._input_student_profile()
        job = self._input_internship_job()
        
        resume = input("Enter your resume text (or press Enter for auto-generated): ").strip()
        
        print("\n⏳ Calculating ATS score...")
        ats = get_ats_score(student, job, resume if resume else None, use_mock=True)
        
        self._print_ats_score(ats)
    
    def _full_analysis_interactive(self):
        """Full analysis: fit + resume + ATS"""
        print("\n" + "=" * 60)
        print("FULL ANALYSIS: INTERNSHIP MATCHING & OPTIMIZATION")
        print("=" * 60)
        
        student = self._input_student_profile()
        job = self._input_internship_job()
        
        print("\n⏳ Running full analysis...")
        
        # 1. Match analysis
        print("\n" + "-" * 60)
        print("1️⃣  MATCH ANALYSIS")
        print("-" * 60)
        match_result = analyze_internship_fit(student, job, use_mock=True)
        self._print_match_analysis(match_result)
        
        # 2. Generate resume
        print("\n" + "-" * 60)
        print("2️⃣  OPTIMIZED RESUME")
        print("-" * 60)
        resume = generate_resume(student, job, use_mock=True)
        print(resume)
        
        # 3. ATS score
        print("\n" + "-" * 60)
        print("3️⃣  ATS SCORE")
        print("-" * 60)
        ats = get_ats_score(student, job, resume, use_mock=True)
        self._print_ats_score(ats)
        
        # 4. Summary
        print("\n" + "=" * 60)
        print("📊 FINAL RECOMMENDATION")
        print("=" * 60)
        print(f"Match Score: {match_result['confidence_score']}/1.0")
        print(f"ATS Score: {ats['ats_percentage']}")
        print(f"Recommendation: {'✅ APPLY' if match_result['is_match'] else '⚠️  CONSIDER UPSKILLING'}")
        print("=" * 60 + "\n")
    
    def _load_from_files(self):
        """Load student and job from JSON files"""
        print("\n" + "=" * 60)
        print("LOAD FROM JSON FILES")
        print("=" * 60)
        
        student_file = input("Enter student profile JSON path (default: example_data/student.json): ").strip()
        job_file = input("Enter job description JSON path (default: example_data/job.json): ").strip()
        
        student_file = student_file or "example_data/student.json"
        job_file = job_file or "example_data/job.json"
        
        try:
            with open(student_file, 'r') as f:
                student_data = json.load(f)
                student = StudentProfile.from_dict(student_data)
            
            with open(job_file, 'r') as f:
                job_data = json.load(f)
                job = InternshipJob.from_dict(job_data)
            
            print(f"✅ Loaded student: {student.name}")
            print(f"✅ Loaded job: {job.title} at {job.company}")
            
            # Run full analysis
            print("\n⏳ Running full analysis...")
            match_result = analyze_internship_fit(student, job, use_mock=True)
            resume = generate_resume(student, job, use_mock=True)
            ats = get_ats_score(student, job, resume, use_mock=True)
            
            print("\n" + "=" * 60)
            print("RESULTS")
            print("=" * 60)
            self._print_match_analysis(match_result)
            print("\n📄 OPTIMIZED RESUME:")
            print("-" * 60)
            print(resume)
            print("-" * 60)
            self._print_ats_score(ats)
            
        except FileNotFoundError as e:
            print(f"❌ Error: File not found - {e}")
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON - {e}")
    
    # ==================== INPUT HELPERS ====================
    
    def _input_student_profile(self) -> StudentProfile:
        """Get student profile from user input"""
        print("\n📝 Enter Student Profile:")
        name = input("  Full Name: ").strip()
        email = input("  Email: ").strip()
        skills_str = input("  Skills (comma-separated): ").strip()
        skills = [s.strip() for s in skills_str.split(",")]
        interests_str = input("  Interests (comma-separated): ").strip()
        interests = [i.strip() for i in interests_str.split(",")]
        experience = input("  Experience summary: ").strip()
        cgpa = float(input("  CGPA (0-4.0): ").strip())
        
        return StudentProfile(
            name=name,
            email=email,
            skills=skills,
            interests=interests,
            experience=experience,
            cgpa=cgpa
        )
    
    def _input_internship_job(self) -> InternshipJob:
        """Get internship job from user input"""
        print("\n💼 Enter Internship Job Details:")
        title = input("  Job Title: ").strip()
        company = input("  Company: ").strip()
        description = input("  Job Description: ").strip()
        required_str = input("  Required Skills (comma-separated): ").strip()
        required_skills = [s.strip() for s in required_str.split(",")]
        preferred_str = input("  Preferred Skills (comma-separated): ").strip()
        preferred_skills = [s.strip() for s in preferred_str.split(",")]
        resps_str = input("  Responsibilities (comma-separated): ").strip()
        responsibilities = [r.strip() for r in resps_str.split(",")]
        duration = int(input("  Duration (months): ").strip())
        location = input("  Location: ").strip()
        
        return InternshipJob(
            title=title,
            company=company,
            description=description,
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            responsibilities=responsibilities,
            duration_months=duration,
            location=location
        )
    
    # ==================== OUTPUT HELPERS ====================
    
    def _print_match_analysis(self, result: Dict):
        """Pretty print match analysis"""
        print(f"\n✨ MATCH SCORE: {result['confidence_score']}/1.0 ({result['match_percentage']})")
        print(f"{'✅ STRONG FIT' if result['is_match'] else '⚠️  CONSIDER IMPROVING'}")
        
        print(f"\n💪 Strengths:")
        for strength in result['strengths']:
            print(f"  ✓ {strength}")
        
        if result['skill_gaps']:
            print(f"\n🔧 Skill Gaps to Address:")
            for gap in result['skill_gaps']:
                print(f"  • {gap['skill']} ({gap['category']})")
        
        print(f"\n📋 Recommendation:")
        print(f"  {result['recommendation']}")
    
    def _print_ats_score(self, ats: Dict):
        """Pretty print ATS score"""
        print(f"\n🤖 ATS SCORE: {ats['ats_percentage']} ({ats['ats_score']}/1.0)")
        print(f"  Matched keywords: {ats['matched_count']}/{ats['keyword_count']}")
        
        if ats['matched_keywords']:
            print(f"\n✅ Matched Keywords:")
            for kw in ats['matched_keywords']:
                print(f"  • {kw}")
        
        if ats['missing_keywords']:
            print(f"\n❌ Missing Keywords:")
            for kw in ats['missing_keywords']:
                print(f"  • {kw}")


def main():
    """Main entry point"""
    cli = InternHubCLI()
    
    if len(sys.argv) > 1:
        # Command-line argument mode
        if sys.argv[1] == "--quick-test":
            print("Running quick test with example data...")
            from example_data.examples import get_example_student, get_example_job
            student = get_example_student()
            job = get_example_job()
            
            print(student.get_profile_summary())
            print(job.get_jd_summary())
            
            result = analyze_internship_fit(student, job)
            cli._print_match_analysis(result)
    else:
        # Interactive mode
        cli.run_interactive()


if __name__ == "__main__":
    main()
