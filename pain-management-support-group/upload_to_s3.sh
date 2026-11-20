#!/bin/bash
# Upload Pain Management Platform to AWS S3
# Usage: ./upload_to_s3.sh your-bucket-name [optional-prefix]

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "================================================"
echo "AWS S3 Upload for Pain Management Platform"
echo "================================================"
echo ""

# Check arguments
if [ -z "$1" ]; then
    echo "Usage: $0 <s3-bucket-name> [optional-prefix]"
    echo ""
    echo "Example:"
    echo "  $0 my-knowledge-base pain-management"
    echo "  $0 my-bucket"
    echo ""
    exit 1
fi

BUCKET_NAME=$1
PREFIX=${2:-"pain-management"}
EXPORT_DIR="presentation_export"

echo -e "${BLUE}📦 Configuration:${NC}"
echo "  Bucket: s3://$BUCKET_NAME"
echo "  Prefix: $PREFIX"
echo "  Source: $EXPORT_DIR"
echo ""

# Check if export directory exists
if [ ! -d "$EXPORT_DIR" ]; then
    echo -e "${YELLOW}⚠️  Export directory not found. Running export script...${NC}"
    python3 export_for_presentation.py
    echo ""
fi

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   https://aws.amazon.com/cli/"
    exit 1
fi

# Check AWS credentials
echo -e "${BLUE}🔐 Checking AWS credentials...${NC}"
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials not configured. Run:"
    echo "   aws configure"
    exit 1
fi

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo -e "${GREEN}✓ Authenticated as AWS Account: $ACCOUNT_ID${NC}"
echo ""

# Check if bucket exists
echo -e "${BLUE}🪣 Checking bucket...${NC}"
if aws s3 ls "s3://$BUCKET_NAME" &> /dev/null; then
    echo -e "${GREEN}✓ Bucket exists: $BUCKET_NAME${NC}"
else
    echo -e "${YELLOW}⚠️  Bucket not found: $BUCKET_NAME${NC}"
    read -p "Create bucket? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        aws s3 mb "s3://$BUCKET_NAME"
        echo -e "${GREEN}✓ Created bucket: $BUCKET_NAME${NC}"
    else
        echo "❌ Aborted"
        exit 1
    fi
fi
echo ""

# Upload files
echo -e "${BLUE}☁️  Uploading files to S3...${NC}"
echo ""

aws s3 sync "$EXPORT_DIR" "s3://$BUCKET_NAME/$PREFIX" \
    --acl public-read \
    --delete \
    --no-progress \
    --exclude ".DS_Store" \
    --exclude "*.pyc"

echo ""
echo "================================================"
echo -e "${GREEN}✅ UPLOAD COMPLETE!${NC}"
echo "================================================"
echo ""
echo -e "${BLUE}📊 Upload Summary:${NC}"

# Count files
HTML_COUNT=$(find "$EXPORT_DIR" -name "*.html" | wc -l)
PNG_COUNT=$(find "$EXPORT_DIR" -name "*.png" | wc -l)
JSON_COUNT=$(find "$EXPORT_DIR" -name "*.json" | wc -l)

echo "  HTML files: $HTML_COUNT"
echo "  PNG files: $PNG_COUNT"
echo "  JSON files: $JSON_COUNT"
echo ""

# Generate URLs
BASE_URL="https://$BUCKET_NAME.s3.amazonaws.com/$PREFIX"

echo -e "${BLUE}🌐 Access URLs:${NC}"
echo ""
echo "  Main Index:"
echo "  $BASE_URL/index.html"
echo ""
echo "  Student Manual:"
echo "  $BASE_URL/documentation/student_manual_patient_guide.html"
echo ""
echo "  Simulation Results:"
echo "  $BASE_URL/documentation/simulation_results_report.html"
echo ""
echo "  Visualizations:"
echo "  $BASE_URL/visualizations/01_pain_trajectories.png"
echo "  $BASE_URL/visualizations/02_pain_comparison_boxplot.png"
echo "  ... (and 4 more)"
echo ""

# Create shareable link file
cat > s3_links.txt << EOF
Pain Management Support Group Platform - S3 Links
Generated: $(date)

Main Index: $BASE_URL/index.html

Documentation:
- Platform Overview: $BASE_URL/documentation/platform_overview.html
- Quick Start: $BASE_URL/documentation/quick_start_guide.html
- Student Manual: $BASE_URL/documentation/student_manual_patient_guide.html
- Technical Manual: $BASE_URL/documentation/technical_manual_developer_guide.html
- System Architecture: $BASE_URL/documentation/system_architecture.html
- Curriculum: $BASE_URL/documentation/8_week_curriculum.html
- Simulation Results: $BASE_URL/documentation/simulation_results_report.html
- Medication Stats: $BASE_URL/documentation/pain_medication_statistics.html
- Global Comparison: $BASE_URL/documentation/global_support_groups_comparison.html
- Alternative Therapies: $BASE_URL/documentation/alternative_therapies_guide.html

Visualizations:
- Pain Trajectories: $BASE_URL/visualizations/01_pain_trajectories.png
- Week 1 vs 8: $BASE_URL/visualizations/02_pain_comparison_boxplot.png
- Dashboard: $BASE_URL/visualizations/03_all_metrics_dashboard.png
- Knowledge Gains: $BASE_URL/visualizations/04_knowledge_gains.png
- Responders: $BASE_URL/visualizations/05_responder_analysis.png
- Correlation: $BASE_URL/visualizations/06_baseline_vs_improvement.png

Data Files:
- Cohort Profiles: $BASE_URL/data/cohort_profiles.json
- Pain Logs: $BASE_URL/data/program_simulation_pain_logs.json
- Assessments: $BASE_URL/data/program_simulation_assessments.json
- Outcomes: $BASE_URL/data/program_outcomes_report.json
- Statistics: $BASE_URL/data/simulation_statistical_summary.json
EOF

echo -e "${GREEN}✓ Created s3_links.txt with all URLs${NC}"
echo ""

echo -e "${BLUE}💡 Next Steps:${NC}"
echo ""
echo "1. Test the main page:"
echo "   open $BASE_URL/index.html"
echo ""
echo "2. Configure bucket for website hosting (optional):"
echo "   aws s3 website s3://$BUCKET_NAME --index-document $PREFIX/index.html"
echo ""
echo "3. Share the links in s3_links.txt with your team"
echo ""
echo "4. For S3 Knowledge Base integration, use the base URL:"
echo "   $BASE_URL/"
echo ""
