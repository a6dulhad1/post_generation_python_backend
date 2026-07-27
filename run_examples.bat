@echo off
REM Windows batch script to run examples

echo ================================================
echo AI Social Media Automation - Examples
echo ================================================
echo.

:menu
echo Select an option:
echo 1. Test API Connections
echo 2. Generate Ideas Only (No Posting)
echo 3. Manual Post with Custom Prompt
echo 4. Run Automated Posts
echo 5. Start Web Dashboard
echo 6. Run Example Scripts
echo 7. Exit
echo.

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto test_api
if "%choice%"=="2" goto generate_only
if "%choice%"=="3" goto manual_post
if "%choice%"=="4" goto auto_post
if "%choice%"=="5" goto dashboard
if "%choice%"=="6" goto examples
if "%choice%"=="7" goto end

echo Invalid choice. Please try again.
echo.
goto menu

:test_api
echo.
echo Testing API connections...
python utils\test_apis.py
echo.
pause
goto menu

:generate_only
echo.
set /p topics="Enter topics (comma-separated, or press Enter for default): "
if "%topics%"=="" (
    python main.py --mode generate-only
) else (
    python main.py --mode generate-only --topics "%topics%"
)
echo.
pause
goto menu

:manual_post
echo.
set /p prompt="Enter your prompt: "
set /p image="Enter image path (or press Enter to skip): "
if "%image%"=="" (
    python main.py --mode manual --prompt "%prompt%"
) else (
    python main.py --mode manual --prompt "%prompt%" --image "%image%"
)
echo.
pause
goto menu

:auto_post
echo.
echo Running automated posts...
python main.py --mode auto
echo.
pause
goto menu

:dashboard
echo.
echo Starting web dashboard...
echo Dashboard will be available at http://localhost:5000
echo Press Ctrl+C to stop
python dashboard.py
pause
goto menu

:examples
echo.
python examples\example_usage.py
echo.
pause
goto menu

:end
echo.
echo Goodbye!
exit
