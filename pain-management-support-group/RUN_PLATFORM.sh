#!/bin/bash
# Pain Management Support Group Platform - Quick Run Script
# Use this to quickly run all platform demonstrations

echo "================================================================"
echo "PAIN MANAGEMENT SUPPORT GROUP PLATFORM"
echo "Interactive Platform Runner"
echo "================================================================"
echo ""

# Navigate to project root
cd "$(dirname "$0")"
PROJECT_ROOT=$(pwd)

echo "📂 Project Location: $PROJECT_ROOT"
echo ""

# Main menu
while true; do
    echo "================================================================"
    echo "MAIN MENU - What would you like to run?"
    echo "================================================================"
    echo ""
    echo "  1) Assessment Generator Demo"
    echo "     → Create weekly tests, see questions, demo scoring"
    echo ""
    echo "  2) Outcome Analytics Demo"
    echo "     → Analyze patient progress, view statistics"
    echo ""
    echo "  3) Visualization Generator"
    echo "     → Create 6 charts, run statistical analysis"
    echo ""
    echo "  4) Run ALL Demos (1, 2, 3)"
    echo "     → Complete platform demonstration"
    echo ""
    echo "  5) View Simulation Results Report"
    echo "     → Read comprehensive outcomes report"
    echo ""
    echo "  6) View Quick Start Guide"
    echo "     → Complete platform documentation"
    echo ""
    echo "  7) View Platform Status Report"
    echo "     → See what's running and what's available"
    echo ""
    echo "  8) List Generated Files"
    echo "     → Show all charts, data files, exports"
    echo ""
    echo "  9) Generate NEW Simulation Data"
    echo "     → Create fresh patient cohort and run simulation"
    echo ""
    echo "  0) Exit"
    echo ""
    echo "================================================================"
    read -p "Enter your choice (0-9): " choice
    echo ""

    case $choice in
        1)
            echo "🎯 Running Assessment Generator Demo..."
            echo ""
            cd "$PROJECT_ROOT/assessments/python"
            python test_assessment_demo.py
            echo ""
            read -p "Press ENTER to continue..."
            ;;
        2)
            echo "📊 Running Outcome Analytics Demo..."
            echo ""
            cd "$PROJECT_ROOT/assessments/python"
            python test_outcome_analytics_demo.py
            echo ""
            read -p "Press ENTER to continue..."
            ;;
        3)
            echo "📈 Running Visualization Generator..."
            echo ""
            cd "$PROJECT_ROOT/assessments/python"
            python visualize_simulation.py
            echo ""
            echo "✓ Visualizations saved to: simulation_plots/"
            ls -lh simulation_plots/
            echo ""
            read -p "Press ENTER to continue..."
            ;;
        4)
            echo "🚀 Running ALL Demos..."
            echo ""
            cd "$PROJECT_ROOT/assessments/python"

            echo "▶ Demo 1/3: Assessment Generator"
            python test_assessment_demo.py
            echo ""

            echo "▶ Demo 2/3: Outcome Analytics"
            python test_outcome_analytics_demo.py
            echo ""

            echo "▶ Demo 3/3: Visualizations"
            python visualize_simulation.py
            echo ""

            echo "✅ All demos complete!"
            echo ""
            read -p "Press ENTER to continue..."
            ;;
        5)
            echo "📖 Viewing Simulation Results Report..."
            echo ""
            cat "$PROJECT_ROOT/assessments/SIMULATION_RESULTS_REPORT.md" | less
            ;;
        6)
            echo "📚 Viewing Quick Start Guide..."
            echo ""
            cat "$PROJECT_ROOT/QUICK_START_GUIDE.md" | less
            ;;
        7)
            echo "📋 Viewing Platform Status Report..."
            echo ""
            cat "$PROJECT_ROOT/PLATFORM_STATUS_REPORT.md" | less
            ;;
        8)
            echo "📂 Generated Files:"
            echo ""
            echo "=== Visualizations ==="
            ls -lh "$PROJECT_ROOT/assessments/python/simulation_plots/" 2>/dev/null || echo "No visualizations yet - run Demo 3 to generate"
            echo ""
            echo "=== Simulation Data ==="
            ls -lh "$PROJECT_ROOT/assessments/python"/*.json 2>/dev/null | grep -E "(cohort|simulation|outcomes)" || echo "No simulation data"
            echo ""
            echo "=== Sample Assessments ==="
            ls -lh "$PROJECT_ROOT/assessments/python"/sample*.json 2>/dev/null || echo "No sample assessments yet - run Demo 1 to generate"
            echo ""
            read -p "Press ENTER to continue..."
            ;;
        9)
            echo "🔄 Generating NEW Simulation Data..."
            echo ""
            cd "$PROJECT_ROOT/assessments/python"

            echo "Step 1/3: Generating patient cohort..."
            python cohort_generator.py
            echo ""

            echo "Step 2/3: Running 8-week simulation..."
            python program_simulator.py
            echo ""

            echo "Step 3/3: Creating visualizations..."
            python visualize_simulation.py
            echo ""

            echo "✅ New simulation complete!"
            echo ""
            read -p "Press ENTER to continue..."
            ;;
        0)
            echo "👋 Exiting platform runner. Goodbye!"
            exit 0
            ;;
        *)
            echo "❌ Invalid choice. Please enter 0-9."
            sleep 2
            ;;
    esac

    clear
done
