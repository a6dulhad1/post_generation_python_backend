#!/bin/bash
# Linux/Mac shell script to run examples

echo "================================================"
echo "AI Social Media Automation - Examples"
echo "================================================"
echo ""

show_menu() {
    echo "Select an option:"
    echo "1. Test API Connections"
    echo "2. Generate Ideas Only (No Posting)"
    echo "3. Manual Post with Custom Prompt"
    echo "4. Run Automated Posts"
    echo "5. Start Web Dashboard"
    echo "6. Run Example Scripts"
    echo "7. Exit"
    echo ""
}

while true; do
    show_menu
    read -p "Enter your choice (1-7): " choice
    
    case $choice in
        1)
            echo ""
            echo "Testing API connections..."
            python utils/test_apis.py
            echo ""
            read -p "Press Enter to continue..."
            ;;
        2)
            echo ""
            read -p "Enter topics (comma-separated, or press Enter for default): " topics
            if [ -z "$topics" ]; then
                python main.py --mode generate-only
            else
                python main.py --mode generate-only --topics "$topics"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        3)
            echo ""
            read -p "Enter your prompt: " prompt
            read -p "Enter image path (or press Enter to skip): " image
            if [ -z "$image" ]; then
                python main.py --mode manual --prompt "$prompt"
            else
                python main.py --mode manual --prompt "$prompt" --image "$image"
            fi
            echo ""
            read -p "Press Enter to continue..."
            ;;
        4)
            echo ""
            echo "Running automated posts..."
            python main.py --mode auto
            echo ""
            read -p "Press Enter to continue..."
            ;;
        5)
            echo ""
            echo "Starting web dashboard..."
            echo "Dashboard will be available at http://localhost:5000"
            echo "Press Ctrl+C to stop"
            python dashboard.py
            ;;
        6)
            echo ""
            python examples/example_usage.py
            echo ""
            read -p "Press Enter to continue..."
            ;;
        7)
            echo ""
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please try again."
            echo ""
            ;;
    esac
done
