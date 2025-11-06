# Pre-Submission Checklist - Cloud Run Hackathon

## Overview

Complete this checklist before submitting to Devpost to maximize your chances of winning!

**Deadline**: November 10, 2025 at 5:00 PM PT

---

## 📋 Required Submission Materials

### ✅ Hosted Project URL (REQUIRED)
- [ ] Backend deployed to Cloud Run
- [ ] Frontend deployed to Cloud Run (or accessible URL)
- [ ] URL is public (no authentication required for demo)
- [ ] URL works from incognito/private browser
- [ ] URL added to Devpost submission

**Your URLs**:
- Frontend: `____________________`
- Backend API: `____________________`

### ✅ Demo Video (REQUIRED - Max 3 minutes)
- [ ] Video recorded (screen capture + audio)
- [ ] Shows complete workflow: upload → analysis → results
- [ ] Under 3 minutes duration
- [ ] English audio OR English subtitles
- [ ] Uploaded to YouTube or Vimeo
- [ ] Set to Public (not unlisted or private)
- [ ] URL added to Devpost submission

**Demo Video Script** (2:45 target):
- 0:00-0:30: Problem statement (injuries from poor form)
- 0:30-1:00: Solution overview (AI coaching with ADK)
- 1:00-2:15: Live demo (upload video, show analysis, highlight results)
- 2:15-2:45: Technical highlights (Cloud Run, Gemini, MediaPipe, architecture)

**Video URL**: `____________________`

### ✅ Public Code Repository (REQUIRED)
- [ ] GitHub repository is PUBLIC
- [ ] README.md exists and comprehensive
- [ ] LICENSE file included
- [ ] .gitignore configured (no secrets, no build artifacts)
- [ ] Code is clean and commented
- [ ] No placeholder TODOs in production code
- [ ] URL added to Devpost submission

**Repository URL(s)**:
- Monorepo: `____________________`
- Backend (if split): `____________________`
- Frontend (if split): `____________________`

### ✅ Architecture Diagram (REQUIRED)
- [ ] Diagram created (PNG, JPG, or PDF)
- [ ] Shows all major components
- [ ] Includes Cloud Run services
- [ ] Labels technologies used
- [ ] Uploaded to Devpost or linked in README
- [ ] Also in docs/ARCHITECTURE.md for reference

**Diagram Location**: `____________________`

### ✅ Project Description (REQUIRED)
- [ ] Written in English
- [ ] Clear problem statement
- [ ] Solution explanation
- [ ] Technologies used listed
- [ ] Data sources documented
- [ ] Key findings/learnings included
- [ ] Minimum 200 words (aim for 500-800)

---

## 🎯 Technical Requirements

### ✅ Cloud Run Deployment
- [ ] Deployed as Cloud Run Service (responds to HTTP)
- [ ] Service is publicly accessible
- [ ] Health endpoint returns 200 OK
- [ ] Handles requests without errors
- [ ] Auto-scaling configured
- [ ] Environment variables set correctly

**Test Commands**:
```bash
# Health check
curl https://your-backend-url.run.app/health

# Upload test
curl -X POST https://your-backend-url.run.app/api/analyze \
  -F "video=@test_video.mp4" \
  -F "exercise_name=Squat"
```

### ✅ Google ADK Integration
- [ ] Using Google ADK framework
- [ ] Agent properly defined in agent.py
- [ ] Tools follow ADK conventions
- [ ] ToolContext parameter included
- [ ] Structured outputs (dict with "status")
- [ ] Solves real-world problem

**Verify**:
```bash
# Check ADK agent
python -c "from biome_coaching_agent.agent import root_agent; print(root_agent)"
```

### ✅ Google AI Model
- [ ] Using Gemini model (2.0 Flash or Pro)
- [ ] API key configured
- [ ] Model integrated into analysis workflow
- [ ] Generates meaningful coaching feedback
- [ ] Documented in submission

**Bonus**: +0.4 points for using Gemini

---

## 🎁 Bonus Points (Optional but Valuable!)

### ✅ Multiple Cloud Run Services (+0.4 points)
- [ ] Backend deployed as separate Cloud Run service
- [ ] Frontend deployed as separate Cloud Run service
- [ ] Both services communicate correctly
- [ ] Documented in architecture diagram
- [ ] Mentioned in Devpost submission

**Current Setup**:
- [ ] Monorepo (0 bonus points)
- [ ] Split repos (✅ +0.4 bonus points)

### ⚠️ Blog Post (+0.4 points)
- [ ] Published on Medium, dev.to, or personal blog
- [ ] Minimum 500 words
- [ ] Includes "Created for Cloud Run Hackathon"
- [ ] Covers development experience with ADK/Cloud Run
- [ ] Discusses challenges and solutions
- [ ] Link added to Devpost submission

**Topics to Cover**:
- Why you built Biome
- How Google ADK simplified agent development
- Cloud Run deployment experience
- MediaPipe integration challenges
- What you learned

**Blog URL**: `____________________`

### ⚠️ Social Media Post (+0.4 points)
- [ ] Posted on LinkedIn or X (Twitter)
- [ ] Includes #CloudRunHackathon hashtag
- [ ] Links to deployed project
- [ ] Includes screenshot or demo GIF
- [ ] Brief description of project
- [ ] Link added to Devpost submission

**Post Requirements**:
- Must be public
- Must use #CloudRunHackathon
- Must link to project

**Post URL**: `____________________`

---

## 📄 Documentation Quality

### ✅ README.md
- [ ] Project title and tagline
- [ ] Problem statement (2-3 paragraphs)
- [ ] Solution overview (what it does)
- [ ] Tech stack clearly listed
- [ ] Setup instructions (step-by-step)
- [ ] Usage examples
- [ ] Architecture overview
- [ ] Link to deployed app
- [ ] Link to demo video
- [ ] Screenshots (3-5 key screens)
- [ ] License information

### ✅ Code Quality
- [ ] Type hints on all functions
- [ ] Docstrings for all tools
- [ ] Error handling in every tool
- [ ] No hardcoded secrets
- [ ] Parameterized SQL queries (no f-strings)
- [ ] Consistent code style
- [ ] No console.log in production
- [ ] Meaningful variable names

**Run Checks**:
```bash
# Python linting
flake8 biome_coaching_agent/

# Type checking
mypy biome_coaching_agent/

# Frontend build
npm run build
```

---

## 🧪 Testing Checklist

### ✅ Local Testing
- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Database schema applies cleanly
- [ ] Video upload works
- [ ] Analysis completes successfully
- [ ] Results display correctly
- [ ] No errors in console

### ✅ Production Testing (Cloud Run)
- [ ] Deployed services are accessible
- [ ] Health endpoint returns 200
- [ ] Can upload video through UI
- [ ] Processing completes (check logs)
- [ ] Results appear in UI
- [ ] Database stores data correctly
- [ ] No CORS errors
- [ ] Works on mobile devices

### ✅ Edge Cases
- [ ] Large video (95MB) uploads successfully
- [ ] Invalid file type rejected gracefully
- [ ] Missing person in video handled
- [ ] Database connection failure handled
- [ ] API timeout handled (if > 60s video)
- [ ] Concurrent uploads work

---

## 🎬 Demo Video Content

### Must Show:
1. **Problem** (15-20 seconds)
   - Quick explanation of poor form injuries
   - Why existing solutions fall short

2. **Solution** (30-40 seconds)
   - Biome overview
   - Key features
   - Value proposition

3. **Live Demo** (60-90 seconds)
   - Upload test video
   - Show processing (agents working)
   - Display results:
     - Overall score
     - Specific issues with frames
     - Coaching cues
     - Recommendations

4. **Technical Architecture** (30-45 seconds)
   - Show architecture diagram
   - Mention Cloud Run deployment
   - Highlight Google ADK + Gemini
   - Explain MediaPipe integration
   - Note multiple services (if applicable)

5. **Impact & Future** (15-20 seconds)
   - Injury prevention potential
   - Scalability
   - Future features

### Tips:
- **Practice 3-5 times** before recording
- **Time yourself** - must be under 3 minutes
- **Use clear audio** - no background noise
- **Show, don't just tell** - demo is key
- **Be enthusiastic** - judges respond to energy
- **Edit tightly** - every second counts

---

## ✅ Devpost Submission Fields

### Basic Info
- [ ] Project name: "Biome - AI Fitness Form Coach"
- [ ] Tagline (< 120 chars): "AI-powered form coaching that prevents injuries"
- [ ] Category: AI Agents
- [ ] Built With: Google ADK, Gemini 2.0, MediaPipe, Cloud Run, FastAPI, React

### Details
- [ ] Problem clearly stated
- [ ] Solution explained
- [ ] How you built it (tech stack, architecture)
- [ ] Challenges faced
- [ ] What you learned
- [ ] What's next for the project

### Media
- [ ] Logo/cover image (1200x630 recommended)
- [ ] Screenshots (3-5 of key features)
- [ ] Demo video (YouTube/Vimeo link)
- [ ] Architecture diagram

### Links
- [ ] Try it out: https://your-frontend.run.app
- [ ] GitHub: https://github.com/your-username/biome_agent
- [ ] Blog post (if applicable)
- [ ] Social post (if applicable)

---

## 🏆 Judging Criteria Self-Assessment

### Technical Implementation (40%)
**Self-Rating**: ___/10

- [ ] Clean, well-documented code
- [ ] Proper ADK structure
- [ ] Production-ready error handling
- [ ] Efficient algorithms
- [ ] Secure (no SQL injection, XSS)

**Improvements Needed**:
- ____________________
- ____________________

### Demo & Presentation (40%)
**Self-Rating**: ___/10

- [ ] Clear problem definition
- [ ] Compelling demo video
- [ ] Professional documentation
- [ ] Architecture well-explained
- [ ] Easy to understand value

**Improvements Needed**:
- ____________________
- ____________________

### Innovation (20%)
**Self-Rating**: ___/10

- [ ] Novel application of ADK
- [ ] Unique combination of tech
- [ ] Addresses real pain point
- [ ] Creative solution design

**Strengths**:
- ____________________
- ____________________

---

## ⚠️ Common Mistakes to Avoid

### Disqualification Risks
- ❌ Video longer than 3 minutes
- ❌ Repository not public
- ❌ No demo video
- ❌ Not deployed to Cloud Run
- ❌ Missing required documentation
- ❌ Prohibited content (offensive, copyrighted)
- ❌ Code written before Oct 6, 2025

### Point Deductions
- ⚠️ Poor code quality
- ⚠️ Incomplete documentation
- ⚠️ Broken deployment
- ⚠️ Demo doesn't work
- ⚠️ Unclear value proposition
- ⚠️ Security vulnerabilities

---

## 📊 Final Score Estimate

### Base Score (5.0 points max)
- Technical: ___/2.0
- Demo: ___/2.0
- Innovation: ___/1.0
- **Base Total**: ___/5.0

### Bonus Points (1.6 max)
- [x] Gemini model: +0.4
- [ ] Multiple services: +0.4
- [ ] Blog post: +0.4
- [ ] Social media: +0.4
- **Bonus Total**: ___/1.6

### **ESTIMATED TOTAL**: ___/6.6

**Target**: 5.5+ for top 10, 6.0+ for category win, 6.5+ for Grand Prize consideration

---

## 🚀 Pre-Submission Workflow

### 3 Days Before Deadline
- [ ] Deploy to Cloud Run (both services if splitting)
- [ ] Test thoroughly in production
- [ ] Record demo video (rough cut)
- [ ] Write blog post draft (if doing bonus)

### 2 Days Before Deadline
- [ ] Finalize demo video (editing, audio)
- [ ] Upload video to YouTube (public)
- [ ] Polish README.md
- [ ] Create architecture diagram
- [ ] Update code documentation

### 1 Day Before Deadline
- [ ] Final production testing
- [ ] Fill out Devpost submission
- [ ] Post on social media (if doing bonus)
- [ ] Publish blog post (if doing bonus)
- [ ] Review all checklist items
- [ ] Get feedback from teammate/friend

### Submission Day
- [ ] Final review of all materials
- [ ] Click "Submit" on Devpost
- [ ] Screenshot confirmation
- [ ] Celebrate! 🎉

---

## 💬 Need Help?

- **Discord**: Check hackathon Discord for questions
- **Cloud Run Docs**: https://cloud.google.com/run/docs
- **ADK Issues**: Check ADK folder examples
- **Last Resort**: Twitter/X with #CloudRunHackathon

---

## ✅ Final Confirmation

Before clicking "Submit":

- [ ] I have tested the deployed app from 3 different devices
- [ ] All links work (GitHub, demo video, hosted app)
- [ ] Demo video is under 3 minutes
- [ ] Repository is public
- [ ] No API keys or secrets in code
- [ ] Architecture diagram uploaded
- [ ] Description is comprehensive
- [ ] I am proud of this submission

**Submission Date**: ____________________

**Submission Time**: ____________________

**Confirmation Number**: ____________________

---

**Good luck!** 🏆

You've built something amazing. Now show it to the judges!

