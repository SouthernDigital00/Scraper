import asyncio
import openpyxl
import os
from urllib.parse import urlparse
from playwright.async_api import async_playwright
from openpyxl.styles import Font

EXCEL_FILE = r"C:\Users\ADickerson.RISEMFG\OneDrive - Rise Manufacturing\Desktop\Work Creations\CustomerInventory_Extract_Data.xlsx"
SHEET_NAME = "Inventory Scrape"

def extract_shape_color(sku):
    sku = sku.upper()
    color = "Black" if "BLK" in sku else "Red" if "RED" in sku else "Silver" if "SLVR" in sku else "Green" if "GRN" in sku else "Grey" if "GRY" in sku else "FDE" if "FDE" in sku else None
    shape = "Flat" if "F" in sku.split("-")[0] else "Curved" if "T017" in sku else None
    return shape, color

async def select_variants(page, shape, color):
    try:
        if shape:
            await page.locator(f'span.variable-item-span:has-text("{shape}")').click(timeout=5000)
            print(f"✅ Selected shape: {shape}")
    except:
        print(f"❌ Shape not found: {shape}")
    try:
        if color:
            await page.locator(f'li.color-variable-item-{color.lower()}').click(timeout=5000)
            print(f"✅ Selected color: {color}")
    except:
        print(f"❌ Color not found: {color}")

async def dismiss_popups(page):
    try:
        await page.evaluate("""
            () => {
                ['#ltkpopup-overlay', '#ltkpopup-container', '.chat-button', '.popup', '.close'].forEach(sel => {
                    const el = document.querySelector(sel);
                    if (el) el.remove();
                });
                window.scrollTo(0, document.body.scrollHeight);
            }
        """)
    except:
        pass

async def extract_price_and_stock_ar15(page, shape, color):
    await select_variants(page, shape, color)
    await page.wait_for_timeout(1000)

    max_inventory = "Out of Stock"
    try:
        qty_input = await page.query_selector("input[name='quantity']")
        if qty_input:
            max_attr = await qty_input.get_attribute("max")
            if max_attr and max_attr.isdigit():
                max_inventory = int(max_attr)
            await qty_input.fill("1")
    except:
        print("⚠️ Could not extract max quantity")

    try:
        await page.locator("button:has-text('Add to cart')").click(timeout=5000)
        await page.wait_for_timeout(3000)

        await page.wait_for_selector("div.woocommerce-mini-cart__total", timeout=5000)
        el = await page.query_selector("div.woocommerce-mini-cart__total strong.woocommerce-Price-amount")
        price = await el.inner_text() if el else "N/A"
        return price, max_inventory
    except Exception as e:
        print(f"❌ AR15 flow failed: {e}")
        return "Error", max_inventory

async def run():
    wb = openpyxl.load_workbook(EXCEL_FILE)
    ws = wb[SHEET_NAME]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        for i, row in enumerate(ws.iter_rows(min_row=2, values_only=False)):
            if i >= 4:
                break

            sku = row[1].value
            url = row[2].value
            print(f"🔍 {sku}")
            if not url or not url.startswith("http"):
                row[3].value = "Invalid URL"
                row[4].value = "N/A"
                continue

            domain = urlparse(url).netloc
            shape, color = extract_shape_color(sku)

            try:
                await page.goto(url, timeout=30000)
                await page.wait_for_timeout(2000)
                await dismiss_popups(page)

                if "ar15discounts.com" in domain:
                    price, inventory = await extract_price_and_stock_ar15(page, shape, color)
                else:
                    price, inventory = "TODO", "TODO"  # placeholder for future sites

                row[3].value = price
                row[4].value = inventory
                print(f"✅ {sku} → Price: {price} | Inventory: {inventory}")

            except Exception as e:
                print(f"❌ Failed {sku}: {e}")
                row[3].value = "Error"
                row[4].value = "Out of Stock"

        await browser.close()
    wb.save(EXCEL_FILE)
    print("✅ Excel updated.")

if __name__ == "__main__":
    asyncio.run(run())