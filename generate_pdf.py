import asyncio
from playwright.async_api import async_playwright
import os

async def generate_pdf():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        filepath = "file:///" + os.path.abspath("brochure_checklist.html").replace("\\", "/")
        await page.goto(filepath, wait_until="networkidle")
        
        pdf_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), ".gemini", "antigravity", "brain", "79b93c68-3db9-42ab-a6a2-e2b5edc53606", "Checklist_Equipamiento_Lifextreme.pdf"))
        
        await page.pdf(path=pdf_path, print_background=True, format="A4", margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"})
        await browser.close()
        print(f"PDF generated successfully at {pdf_path}")

asyncio.run(generate_pdf())
