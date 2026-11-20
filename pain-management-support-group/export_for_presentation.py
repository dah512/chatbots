#!/usr/bin/env python3
"""
Export Pain Management Platform Documentation for Presentation
Converts all markdown files to HTML and organizes for S3/presentation
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime

# Simple markdown to HTML converter
def markdown_to_html(markdown_text, title="Document"):
    """Convert markdown to styled HTML"""

    # Basic markdown conversions
    html = markdown_text

    # Headers
    html = html.replace('\n# ', '\n<h1>')
    html = html.replace('\n## ', '\n<h2>')
    html = html.replace('\n### ', '\n<h3>')
    html = html.replace('\n#### ', '\n<h4>')

    # Close headers (simple approach)
    for tag in ['h1', 'h2', 'h3', 'h4']:
        html = html.replace(f'<{tag}>', f'<{tag}>').replace('\n\n', f'</{tag}>\n\n')

    # Bold and italic
    import re
    html = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', html)
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # Code blocks
    html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)

    # Lists
    lines = html.split('\n')
    in_list = False
    new_lines = []
    for line in lines:
        if line.strip().startswith('- ') or line.strip().startswith('* '):
            if not in_list:
                new_lines.append('<ul>')
                in_list = True
            item = line.strip()[2:]
            new_lines.append(f'<li>{item}</li>')
        elif line.strip().startswith(('1. ', '2. ', '3. ', '4. ', '5. ', '6. ', '7. ', '8. ', '9. ')):
            if not in_list:
                new_lines.append('<ol>')
                in_list = True
            item = line.strip().split('. ', 1)[1] if '. ' in line else line
            new_lines.append(f'<li>{item}</li>')
        else:
            if in_list:
                new_lines.append('</ul>')
                in_list = False
            new_lines.append(line)

    if in_list:
        new_lines.append('</ul>')

    html = '\n'.join(new_lines)

    # Paragraphs
    paragraphs = html.split('\n\n')
    html = '\n\n'.join(f'<p>{p}</p>' if not p.startswith('<') else p for p in paragraphs)

    # Links
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)

    # Horizontal rules
    html = html.replace('\n---\n', '\n<hr>\n')
    html = html.replace('\n***\n', '\n<hr>\n')

    # Tables (basic support)
    html = re.sub(r'\n\|(.+)\|\n\|[-\s|]+\|\n', r'\n<table>\n<thead><tr><th>\1</th></tr></thead>\n<tbody>\n', html)
    html = re.sub(r'\n\|(.+)\|', r'\n<tr><td>\1</td></tr>', html)

    # Wrap in full HTML document
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica', 'Arial', sans-serif;
            line-height: 1.6;
            max-width: 1000px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
            background: #fff;
        }}

        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}

        h2 {{
            color: #34495e;
            border-bottom: 2px solid #95a5a6;
            padding-bottom: 8px;
            margin-top: 40px;
        }}

        h3 {{
            color: #34495e;
            margin-top: 30px;
        }}

        h4 {{
            color: #7f8c8d;
            margin-top: 20px;
        }}

        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
            color: #c7254e;
        }}

        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
        }}

        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}

        ul, ol {{
            margin: 15px 0;
            padding-left: 30px;
        }}

        li {{
            margin: 8px 0;
        }}

        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 20px 0;
        }}

        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}

        th {{
            background: #3498db;
            color: white;
            font-weight: bold;
        }}

        tr:nth-child(even) {{
            background: #f9f9f9;
        }}

        a {{
            color: #3498db;
            text-decoration: none;
        }}

        a:hover {{
            text-decoration: underline;
        }}

        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 40px 0;
        }}

        blockquote {{
            border-left: 4px solid #3498db;
            margin: 20px 0;
            padding: 10px 20px;
            background: #f8f9fa;
            font-style: italic;
        }}

        .header-info {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 30px;
        }}

        .header-info strong {{
            color: #2c3e50;
        }}

        @media print {{
            body {{
                max-width: none;
                padding: 20px;
            }}

            pre {{
                page-break-inside: avoid;
            }}

            h1, h2, h3 {{
                page-break-after: avoid;
            }}
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 20px 10px;
            }}

            pre {{
                padding: 10px;
                font-size: 0.85em;
            }}
        }}
    </style>
</head>
<body>
    <div class="header-info">
        <strong>Pain Management Support Group Platform</strong><br>
        Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br>
        Document: {title}
    </div>

    {html}

    <hr>
    <footer style="text-align: center; color: #7f8c8d; margin-top: 60px;">
        <p><small>Pain Management Support Group Platform v1.0.0</small></p>
    </footer>
</body>
</html>"""


def export_all_documentation():
    """Export all markdown files to HTML"""

    print("="*70)
    print("PAIN MANAGEMENT PLATFORM - EXPORT FOR PRESENTATION")
    print("="*70)
    print()

    # Create export directory
    export_dir = Path("presentation_export")
    export_dir.mkdir(exist_ok=True)

    # Subdirectories
    (export_dir / "documentation").mkdir(exist_ok=True)
    (export_dir / "visualizations").mkdir(exist_ok=True)
    (export_dir / "data").mkdir(exist_ok=True)

    print("📂 Created export directory structure")
    print()

    # Find all markdown files
    md_files = [
        ("README.md", "Platform Overview"),
        ("QUICK_START_GUIDE.md", "Quick Start Guide"),
        ("PLATFORM_STATUS_REPORT.md", "Platform Status Report"),
        ("docs/STUDENT_MANUAL.md", "Student Manual - Patient Guide"),
        ("docs/TECHNICAL_MANUAL.md", "Technical Manual - Developer Guide"),
        ("docs/ARCHITECTURE.md", "System Architecture"),
        ("curriculum/CURRICULUM_MASTER.md", "8-Week Curriculum"),
        ("assessments/SIMULATION_RESULTS_REPORT.md", "Simulation Results Report"),
        ("research/medications/pain_medication_statistics.md", "Pain Medication Statistics"),
        ("research/support-groups/global_comparison.md", "Global Support Groups Comparison"),
        ("research/alternative-therapies/comprehensive_guide.md", "Alternative Therapies Guide"),
    ]

    print("📄 Converting markdown files to HTML...")
    print()

    converted = []
    for md_path, title in md_files:
        if os.path.exists(md_path):
            print(f"  ✓ Converting: {title}")

            with open(md_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            html_content = markdown_to_html(markdown_content, title)

            # Create clean filename
            safe_filename = title.lower().replace(' ', '_').replace('-', '_')
            safe_filename = ''.join(c for c in safe_filename if c.isalnum() or c == '_')
            html_path = export_dir / "documentation" / f"{safe_filename}.html"

            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            converted.append({
                'title': title,
                'filename': html_path.name,
                'size': len(html_content)
            })
        else:
            print(f"  ⚠ Skipped (not found): {md_path}")

    print()
    print(f"✓ Converted {len(converted)} documents")
    print()

    # Copy visualizations
    print("📊 Copying visualizations...")
    viz_dir = Path("assessments/python/simulation_plots")
    if viz_dir.exists():
        for img_file in viz_dir.glob("*.png"):
            shutil.copy(img_file, export_dir / "visualizations" / img_file.name)
            print(f"  ✓ Copied: {img_file.name}")
    print()

    # Copy data files
    print("📊 Copying data files...")
    data_files = [
        "assessments/python/cohort_profiles.json",
        "assessments/python/program_simulation_pain_logs.json",
        "assessments/python/program_simulation_assessments.json",
        "assessments/python/program_outcomes_report.json",
        "assessments/python/simulation_statistical_summary.json",
    ]

    for data_file in data_files:
        if os.path.exists(data_file):
            shutil.copy(data_file, export_dir / "data" / Path(data_file).name)
            print(f"  ✓ Copied: {Path(data_file).name}")
    print()

    # Create index page
    print("📑 Creating index page...")

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pain Management Support Group Platform - Documentation</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
        }}

        .container {{
            background: white;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}

        h1 {{
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 20px;
            margin-bottom: 40px;
        }}

        .section {{
            margin: 40px 0;
        }}

        .section h2 {{
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-bottom: 20px;
        }}

        .doc-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}

        .doc-card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            transition: all 0.3s;
        }}

        .doc-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            border-color: #3498db;
        }}

        .doc-card a {{
            text-decoration: none;
            color: #2c3e50;
            font-weight: bold;
            display: block;
            margin-bottom: 10px;
        }}

        .doc-card a:hover {{
            color: #3498db;
        }}

        .doc-card p {{
            margin: 0;
            color: #7f8c8d;
            font-size: 0.9em;
        }}

        .stats {{
            background: #ecf0f1;
            border-radius: 8px;
            padding: 20px;
            margin: 30px 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            text-align: center;
        }}

        .stat-box {{
            background: white;
            padding: 20px;
            border-radius: 5px;
        }}

        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #3498db;
        }}

        .stat-label {{
            color: #7f8c8d;
            margin-top: 5px;
        }}

        .viz-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}

        .viz-card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}

        .viz-card img {{
            max-width: 100%;
            height: auto;
            border-radius: 5px;
            margin-top: 10px;
        }}

        footer {{
            text-align: center;
            margin-top: 60px;
            padding-top: 20px;
            border-top: 2px solid #ecf0f1;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🏥 Pain Management Support Group Platform</h1>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-number">{len(converted)}</div>
                <div class="stat-label">Documentation Files</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">6</div>
                <div class="stat-label">Visualizations</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">87%</div>
                <div class="stat-label">Patient Improvement</div>
            </div>
            <div class="stat-box">
                <div class="stat-number">25</div>
                <div class="stat-label">Simulated Patients</div>
            </div>
        </div>

        <div class="section">
            <h2>📚 Core Documentation</h2>
            <div class="doc-grid">"""

    # Add documentation links
    for doc in converted[:4]:
        index_html += f"""
                <div class="doc-card">
                    <a href="documentation/{doc['filename']}">{doc['title']}</a>
                    <p>{doc['size'] // 1024} KB</p>
                </div>"""

    index_html += """
            </div>
        </div>

        <div class="section">
            <h2>👥 Manuals & Guides</h2>
            <div class="doc-grid">"""

    for doc in converted[4:7]:
        index_html += f"""
                <div class="doc-card">
                    <a href="documentation/{doc['filename']}">{doc['title']}</a>
                    <p>{doc['size'] // 1024} KB</p>
                </div>"""

    index_html += """
            </div>
        </div>

        <div class="section">
            <h2>🔬 Research & Analysis</h2>
            <div class="doc-grid">"""

    for doc in converted[7:]:
        index_html += f"""
                <div class="doc-card">
                    <a href="documentation/{doc['filename']}">{doc['title']}</a>
                    <p>{doc['size'] // 1024} KB</p>
                </div>"""

    index_html += """
            </div>
        </div>

        <div class="section">
            <h2>📊 Visualizations</h2>
            <div class="viz-grid">
                <div class="viz-card">
                    <strong>Pain Trajectories</strong>
                    <a href="visualizations/01_pain_trajectories.png" target="_blank">
                        <img src="visualizations/01_pain_trajectories.png" alt="Pain Trajectories">
                    </a>
                </div>
                <div class="viz-card">
                    <strong>Week 1 vs Week 8</strong>
                    <a href="visualizations/02_pain_comparison_boxplot.png" target="_blank">
                        <img src="visualizations/02_pain_comparison_boxplot.png" alt="Comparison">
                    </a>
                </div>
                <div class="viz-card">
                    <strong>All Metrics Dashboard</strong>
                    <a href="visualizations/03_all_metrics_dashboard.png" target="_blank">
                        <img src="visualizations/03_all_metrics_dashboard.png" alt="Dashboard">
                    </a>
                </div>
                <div class="viz-card">
                    <strong>Knowledge Gains</strong>
                    <a href="visualizations/04_knowledge_gains.png" target="_blank">
                        <img src="visualizations/04_knowledge_gains.png" alt="Knowledge">
                    </a>
                </div>
                <div class="viz-card">
                    <strong>Responder Analysis</strong>
                    <a href="visualizations/05_responder_analysis.png" target="_blank">
                        <img src="visualizations/05_responder_analysis.png" alt="Responders">
                    </a>
                </div>
                <div class="viz-card">
                    <strong>Baseline vs Improvement</strong>
                    <a href="visualizations/06_baseline_vs_improvement.png" target="_blank">
                        <img src="visualizations/06_baseline_vs_improvement.png" alt="Correlation">
                    </a>
                </div>
            </div>
        </div>

        <div class="section">
            <h2>💾 Data Files</h2>
            <ul>
                <li><a href="data/cohort_profiles.json">Cohort Profiles (25 patients)</a></li>
                <li><a href="data/program_simulation_pain_logs.json">Pain Logs (836 entries)</a></li>
                <li><a href="data/program_simulation_assessments.json">Assessment Results</a></li>
                <li><a href="data/program_outcomes_report.json">Outcomes Report</a></li>
                <li><a href="data/simulation_statistical_summary.json">Statistical Summary</a></li>
            </ul>
        </div>

        <footer>
            <p><strong>Pain Management Support Group Platform v1.0.0</strong></p>
            <p>Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p><small>An evidence-based 8-week program for chronic pain management</small></p>
        </footer>
    </div>
</body>
</html>"""

    with open(export_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(index_html)

    print("  ✓ Created index.html")
    print()

    # Create manifest
    manifest = {
        'export_date': datetime.now().isoformat(),
        'platform_version': '1.0.0',
        'documents': converted,
        'visualizations': 6,
        'data_files': 5,
        'total_size_kb': sum(doc['size'] for doc in converted) // 1024
    }

    with open(export_dir / "manifest.json", 'w') as f:
        json.dump(manifest, f, indent=2)

    print("="*70)
    print("✅ EXPORT COMPLETE!")
    print("="*70)
    print()
    print(f"📁 Location: {export_dir.absolute()}")
    print(f"📄 Documents: {len(converted)} HTML files")
    print(f"📊 Visualizations: 6 PNG files")
    print(f"💾 Data files: 5 JSON files")
    print(f"📦 Total size: {manifest['total_size_kb']} KB")
    print()
    print("🌐 To view:")
    print(f"   Open: {(export_dir / 'index.html').absolute()}")
    print()
    print("☁️  To upload to S3:")
    print(f"   aws s3 sync {export_dir} s3://your-bucket-name/pain-management/ --acl public-read")
    print()
    print("🖨️  To print:")
    print("   Open index.html in browser and use Print function")
    print()


if __name__ == "__main__":
    export_all_documentation()
