"""
InternHub Flask API - Minimal web interface
"""
from flask import Flask, request, jsonify
from student_profile import StudentProfile
from internship_job import InternshipJob
from ai_agent import (
    InternHubAIAgent,
    analyze_internship_fit,
    generate_resume,
    get_ats_score
)
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API documentation"""
    return jsonify({
        "name": "InternHub AI",
        "version": "1.0",
        "description": "AI-powered internship matching and optimization platform",
        "endpoints": {
            "POST /analyze": "Analyze internship fit (returns match score, gaps, recommendation)",
            "POST /resume": "Generate optimized resume for a job",
            "POST /ats": "Calculate ATS score",
            "POST /full-analysis": "Run complete analysis (fit + resume + ATS)"
        },
        "example_body": {
            "student": {
                "name": "John Doe",
                "email": "john@example.com",
                "skills": ["Python", "JavaScript", "React"],
                "interests": ["Web Development", "AI"],
                "experience": "2 projects, 1 year learning",
                "cgpa": 3.5,
                "resume_text": ""
            },
            "job": {
                "title": "Backend Intern",
                "company": "TechCorp",
                "description": "Backend development role",
                "required_skills": ["Python", "REST APIs"],
                "preferred_skills": ["Docker", "AWS"],
                "responsibilities": ["Code", "Test", "Deploy"],
                "duration_months": 3,
                "location": "Remote"
            }
        }
    })


@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze internship fit"""
    try:
        data = request.get_json()
        
        student = StudentProfile.from_dict(data['student'])
        job = InternshipJob.from_dict(data['job'])
        
        result = analyze_internship_fit(student, job, use_mock=True)
        
        return jsonify({
            "status": "success",
            "data": result
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@app.route('/resume', methods=['POST'])
def resume():
    """Generate optimized resume"""
    try:
        data = request.get_json()
        
        student = StudentProfile.from_dict(data['student'])
        job = InternshipJob.from_dict(data['job'])
        
        optimized_resume = generate_resume(student, job, use_mock=True)
        
        return jsonify({
            "status": "success",
            "data": {
                "optimized_resume": optimized_resume,
                "job": job.title,
                "company": job.company
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@app.route('/ats', methods=['POST'])
def ats():
    """Calculate ATS score"""
    try:
        data = request.get_json()
        
        student = StudentProfile.from_dict(data['student'])
        job = InternshipJob.from_dict(data['job'])
        resume_text = data.get('resume_text', '')
        
        ats_result = get_ats_score(
            student, job, 
            resume_text if resume_text else None,
            use_mock=True
        )
        
        return jsonify({
            "status": "success",
            "data": ats_result
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@app.route('/full-analysis', methods=['POST'])
def full_analysis():
    """Run complete analysis"""
    try:
        data = request.get_json()
        
        student = StudentProfile.from_dict(data['student'])
        job = InternshipJob.from_dict(data['job'])
        
        # Run all analyses
        match_result = analyze_internship_fit(student, job, use_mock=True)
        optimized_resume = generate_resume(student, job, use_mock=True)
        ats_result = get_ats_score(student, job, optimized_resume, use_mock=True)
        
        return jsonify({
            "status": "success",
            "data": {
                "student_name": student.name,
                "job_title": job.title,
                "company": job.company,
                "match_analysis": match_result,
                "optimized_resume": optimized_resume,
                "ats_score": ats_result
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 400


@app.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    print("🚀 InternHub API running on http://localhost:5000")
    print("📖 API docs: http://localhost:5000/")
    app.run(debug=True, port=5000)
