@echo off
color 0A
echo ========================================================
echo       ShopHub E-Commerce - Complete Setup
echo ========================================================
echo.

REM Change to the project directory
cd /d D:\1 E-Commerces

echo [1/5] Creating templates folder...
if not exist "backend\templates" (
    mkdir "backend\templates"
    echo     ✓ Created backend\templates folder
) else (
    echo     ℹ Templates folder already exists
)

echo.
echo [2/5] Checking if template files exist...
echo.
echo     You need to manually copy these files:
echo     1. admin_login.html      → backend\templates\admin_login.html
echo     2. admin_dashboard.html  → backend\templates\admin_dashboard.html  
echo     3. product_list.html     → frontend\product_list.html
echo     4. product_details.html  → frontend\product_details.html
echo.

echo [3/5] Current folder structure:
tree /F backend\templates 2>nul
if errorlevel 1 (
    echo     Templates folder is empty - files need to be copied
)

echo.
echo [4/5] Checking frontend files...
if exist "frontend\product_list.html" (
    echo     ✓ product_list.html exists
) else (
    echo     ✗ product_list.html NOT FOUND
)

if exist "frontend\product_details.html" (
    echo     ✓ product_details.html exists
) else (
    echo     ✗ product_details.html NOT FOUND
)

echo.
echo [5/5] Checking app.py configuration...
findstr /C:"TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')" backend\app.py >nul
if errorlevel 1 (
    echo     ✗ app.py needs to be updated with fixed version
) else (
    echo     ✓ app.py has correct template configuration
)

echo.
echo ========================================================
echo                 NEXT STEPS
echo ========================================================
echo.
echo 1. Copy the HTML files I provided to these locations:
echo.
echo    FROM YOUR DOWNLOADS:
echo    • admin_login.html       → D:\1 E-Commerces\backend\templates\
echo    • admin_dashboard.html   → D:\1 E-Commerces\backend\templates\
echo    • product_list.html      → D:\1 E-Commerces\frontend\
echo    • product_details.html   → D:\1 E-Commerces\frontend\
echo.
echo 2. Replace backend\app.py with the app_FIXED.py file
echo.
echo 3. Restart your Flask server:
echo    Ctrl+C (to stop current server)
echo    python backend\app.py
echo.
echo 4. Test these URLs:
echo    • http://localhost:5000/admin/login
echo    • http://localhost:5000/products
echo    • http://localhost:5000/product/1
echo.
echo ========================================================
echo.
pause

REM Open the directories in File Explorer to make copying easier
echo Opening folders for you...
start "" explorer "D:\1 E-Commerces\backend\templates"
start "" explorer "D:\1 E-Commerces\frontend"

echo.
echo ✓ Folders opened in File Explorer
echo   Now copy your downloaded HTML files to these folders
echo.
pause
