
# RISE Inventory Scraper Project

This project automates the monitoring of MAP pricing and inventory levels for Rise Armament products listed on reseller websites (starting with ar15discounts.com).

## 📌 Features

- ✅ **Excel Integration**: Reads product SKUs and URLs from an Excel file and updates MAP price + inventory status.
- ✅ **Playwright Automation**: Uses browser automation to select product variants and extract cart-level inventory info.
- ✅ **Email Alerts**: Sends notifications when products go out of stock using Gmail SMTP.
- ✅ **.BAT + Task Scheduler**: Runs automatically on a schedule via a local `.bat` script.
- ✅ **Multi-site Ready**: Built to support scraping from more than one retail domain.

---

## 🗂 Folder Structure

```
/Extract Data - Products
├── scrape_inventory_alerts.py       # Main scraping + alert script
├── CustomerInventory_Extract_Data.xlsx  # Excel input/output file
├── .env                             # Secure credentials for email
├── inventory_scraper.bat           # Scheduled task runner
├── log_output.txt                  # Log output from .bat execution
├── chat_log.md                     # Markdown log of ChatGPT session
├── chat_log.json                   # Structured summary of features + goals
```

---

## 🔧 Setup

1. **Python Dependencies**:
   ```bash
   pip install playwright openpyxl python-dotenv
   playwright install
   ```

2. **Configure .env**:
   ```env
   EMAIL_FROM=yourgmail@gmail.com
   EMAIL_PASSWORD=your_app_password
   EMAIL_TO=adickerson@risearmament.com,yourgmail@gmail.com
   ```

3. **Run Manually**:
   Double-click the `.bat` file or run in terminal:
   ```bash
   python scrape_inventory_alerts.py
   ```

4. **Schedule**:
   Use Windows Task Scheduler to run `.bat` file automatically twice daily.

---

## 🔮 Future Enhancements

- Add support for new websites by implementing new handlers in the script
- Integrate Slack or desktop pop-up notifications
- Email out of stock items or low price notifications via email

---

Maintained by: **A Dickerson**  

