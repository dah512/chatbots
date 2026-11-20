#!/bin/bash
# Deploy Pain Management Support Group to Firebase Hosting
# Custom domain: pmsg.edmhs.us

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "================================================"
echo "Firebase Hosting Deployment"
echo "Pain Management Support Group Platform"
echo "================================================"
echo ""

# Check if Firebase CLI is installed
if ! command -v firebase &> /dev/null; then
    echo -e "${YELLOW}⚠️  Firebase CLI not found. Installing...${NC}"
    echo ""
    echo "Run this command:"
    echo "  npm install -g firebase-tools"
    echo ""
    echo "Or:"
    echo "  curl -sL https://firebase.tools | bash"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Firebase CLI installed${NC}"
echo ""

# Check if logged in
echo -e "${BLUE}🔐 Checking Firebase authentication...${NC}"
if ! firebase projects:list &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Firebase${NC}"
    echo ""
    echo "Please run:"
    echo "  firebase login"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Authenticated with Firebase${NC}"
echo ""

# Check if presentation_export exists
if [ ! -d "presentation_export" ]; then
    echo -e "${YELLOW}⚠️  presentation_export directory not found${NC}"
    echo "Running export script..."
    python3 export_for_presentation.py
fi

echo -e "${GREEN}✓ Presentation export ready${NC}"
echo ""

# Check for firebase.json
if [ ! -f "firebase.json" ]; then
    echo -e "${BLUE}📝 Creating Firebase configuration...${NC}"

    cat > firebase.json << 'EOF'
{
  "hosting": {
    "public": "presentation_export",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "headers": [
      {
        "source": "**/*.@(jpg|jpeg|gif|png|svg|webp)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=7200"
          }
        ]
      },
      {
        "source": "**/*.@(js|css)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=3600"
          }
        ]
      },
      {
        "source": "**/*.@(json)",
        "headers": [
          {
            "key": "Cache-Control",
            "value": "max-age=300"
          }
        ]
      }
    ],
    "rewrites": [
      {
        "source": "/",
        "destination": "/index.html"
      }
    ],
    "cleanUrls": true,
    "trailingSlash": false
  }
}
EOF

    echo -e "${GREEN}✓ Created firebase.json${NC}"
    echo ""
fi

# Check for .firebaserc
if [ ! -f ".firebaserc" ]; then
    echo -e "${YELLOW}⚠️  Firebase project not initialized${NC}"
    echo ""
    echo "Please run:"
    echo "  firebase init hosting"
    echo ""
    echo "Then run this script again"
    exit 1
fi

PROJECT_ID=$(grep -o '"default": "[^"]*"' .firebaserc | cut -d'"' -f4)

echo -e "${BLUE}🚀 Deploying to Firebase...${NC}"
echo "  Project: $PROJECT_ID"
echo "  Source: presentation_export/"
echo ""

# Deploy
firebase deploy --only hosting

echo ""
echo "================================================"
echo -e "${GREEN}✅ DEPLOYMENT COMPLETE!${NC}"
echo "================================================"
echo ""

# Get the Firebase URL
FIREBASE_URL="https://$PROJECT_ID.web.app"

echo -e "${BLUE}🌐 Your site is live at:${NC}"
echo "  $FIREBASE_URL"
echo ""

echo -e "${BLUE}📋 To set up custom domain (pmsg.edmhs.us):${NC}"
echo ""
echo "1. Go to Firebase Console:"
echo "   https://console.firebase.google.com/project/$PROJECT_ID/hosting/sites"
echo ""
echo "2. Click 'Add custom domain'"
echo ""
echo "3. Enter: pmsg.edmhs.us"
echo ""
echo "4. Add these DNS records to your edmhs.us domain:"
echo "   (Firebase will show you the exact records)"
echo ""
echo "   Type  | Name | Value"
echo "   ------|------|------"
echo "   A     | pmsg | (Firebase IP)"
echo "   TXT   | pmsg | (Verification code)"
echo ""
echo "5. Wait for DNS propagation (5-30 minutes)"
echo ""
echo "6. Firebase will auto-provision SSL certificate"
echo ""

echo -e "${BLUE}💡 Quick Links:${NC}"
echo "  Documentation: $FIREBASE_URL/documentation/platform_overview.html"
echo "  Student Manual: $FIREBASE_URL/documentation/student_manual___patient_guide.html"
echo "  Simulation Results: $FIREBASE_URL/documentation/simulation_results_report.html"
echo "  Visualizations: $FIREBASE_URL/visualizations/"
echo ""

# Create a links file
cat > firebase_links.txt << EOF
Pain Management Support Group Platform
Firebase Deployment Links
Deployed: $(date)

Main Site: $FIREBASE_URL
Custom Domain: https://pmsg.edmhs.us (after DNS setup)

Documentation:
- Platform Overview: $FIREBASE_URL/documentation/platform_overview.html
- Quick Start: $FIREBASE_URL/documentation/quick_start_guide.html
- Student Manual: $FIREBASE_URL/documentation/student_manual___patient_guide.html
- Technical Manual: $FIREBASE_URL/documentation/technical_manual___developer_guide.html
- System Architecture: $FIREBASE_URL/documentation/system_architecture.html
- 8-Week Curriculum: $FIREBASE_URL/documentation/8_week_curriculum.html
- Simulation Results: $FIREBASE_URL/documentation/simulation_results_report.html
- Medication Stats: $FIREBASE_URL/documentation/pain_medication_statistics.html
- Global Comparison: $FIREBASE_URL/documentation/global_support_groups_comparison.html
- Alternative Therapies: $FIREBASE_URL/documentation/alternative_therapies_guide.html

Visualizations:
- Pain Trajectories: $FIREBASE_URL/visualizations/01_pain_trajectories.png
- Week 1 vs 8: $FIREBASE_URL/visualizations/02_pain_comparison_boxplot.png
- Dashboard: $FIREBASE_URL/visualizations/03_all_metrics_dashboard.png
- Knowledge Gains: $FIREBASE_URL/visualizations/04_knowledge_gains.png
- Responders: $FIREBASE_URL/visualizations/05_responder_analysis.png
- Correlation: $FIREBASE_URL/visualizations/06_baseline_vs_improvement.png

Data Files:
- Cohort Profiles: $FIREBASE_URL/data/cohort_profiles.json
- Pain Logs: $FIREBASE_URL/data/program_simulation_pain_logs.json
- Assessments: $FIREBASE_URL/data/program_simulation_assessments.json
- Outcomes: $FIREBASE_URL/data/program_outcomes_report.json
- Statistics: $FIREBASE_URL/data/simulation_statistical_summary.json

Firebase Console:
https://console.firebase.google.com/project/$PROJECT_ID/hosting/sites

To redeploy:
  firebase deploy --only hosting

To view logs:
  firebase hosting:channel:list
EOF

echo -e "${GREEN}✓ Created firebase_links.txt with all URLs${NC}"
echo ""
