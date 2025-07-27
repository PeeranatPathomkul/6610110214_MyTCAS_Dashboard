import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import pandas as pd
import re
from urllib.parse import urljoin, urlparse
import time
import json
from datetime import datetime
import requests

class TCASScraper:
    def __init__(self):
        self.base_url = "https://www.mytcas.com"
        self.programs_data = []
        self.browser = None
        self.page = None
        self.session = requests.Session()
        
        # User agent
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # คำสำคัญสำหรับโปรแกรม
        self.target_keywords = [
            'คอมพิวเตอร์', 'computer', 'คอม',
            'ปัญญาประดิษฐ์', 'artificial intelligence', 'ai',
            'วิศวกรรม', 'engineering'
        ]

    async def init_browser(self, headless=False, slow_mo=500):
        """เริ่มต้น browser"""
        print("🚀 เริ่มต้น browser...")
        
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=headless,
            slow_mo=slow_mo,
            args=['--start-maximized', '--no-sandbox', '--disable-blink-features=AutomationControlled']
        )
        
        self.context = await self.browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        
        self.page = await self.context.new_page()
        self.page.set_default_timeout(30000)
        
        print("✅ Browser พร้อมใช้งาน")

    async def close_browser(self):
        """ปิด browser"""
        try:
            if self.browser:
                await self.browser.close()
            if hasattr(self, 'playwright'):
                await self.playwright.stop()
        except Exception as e:
            print(f"⚠️ Warning: {e}")

    async def search_via_website(self):
        """ค้นหาผ่านเว็บไซต์"""
        print("🎯 เริ่มการรวบรวมข้อมูลผ่านเว็บไซต์...")
        links = []
        
        try:
            await self.page.goto(self.base_url, wait_until='networkidle')
            await self.page.wait_for_timeout(3000)
            
            search_terms = [
                'วิศวกรรมคอมพิวเตอร์',
                'computer engineering', 
                'วิศวกรรมปัญญาประดิษฐ์',
                'artificial intelligence engineering',
                'ai engineering',
                'com engineering'
            ]
            
            for term in search_terms:
                print(f"   🔍 ค้นหา: {term}")
                term_links = await self.perform_search(term)
                links.extend(term_links)
                await self.page.wait_for_timeout(1000)
                
        except Exception as e:
            print(f"   ❌ ไม่สามารถค้นหาผ่านเว็บไซต์: {e}")
        
        # รวมและลบซ้ำ
        unique_links = list(set(links))
        print(f"📊 รวมทั้งหมด: {len(unique_links)} ลิงก์ (ไม่ซ้ำ)")
        
        # ดึงข้อมูลจากทุกลิงก์
        if unique_links:
            await self.extract_comprehensive_data(unique_links)
        else:
            print("❌ ไม่พบลิงก์")

    async def perform_search(self, search_term):
        """ดำเนินการค้นหา"""
        found_links = []
        
        try:
            # หา search input
            search_selectors = [
                '#search', 'input[type="search"]', 'input[name="q"]', 
                'input[placeholder*="ค้นหา"]', '.search-box input'
            ]
            
            search_input = None
            for selector in search_selectors:
                search_input = await self.page.query_selector(selector)
                if search_input:
                    break
            
            if search_input:
                await search_input.fill('')
                await search_input.fill(search_term)
                await search_input.press('Enter')
                await self.page.wait_for_timeout(3000)
                
                # รวบรวมลิงก์
                links = await self.page.query_selector_all('a[href]')
                for link in links:
                    try:
                        href = await link.get_attribute('href')
                        text = await link.inner_text()
                        
                        if href and self.is_relevant_link(text, href):
                            full_url = urljoin(self.base_url, href)
                            found_links.append(full_url)
                    except:
                        continue
                        
        except Exception as e:
            print(f"     ❌ เกิดข้อผิดพลาด: {e}")
        
        return found_links

    def is_relevant_link(self, text, href):
        """ตรวจสอบว่าลิงก์เกี่ยวข้องหรือไม่"""
        if not text or not href:
            return False
        
        text_lower = text.lower()
        href_lower = href.lower()
        combined = f"{text_lower} {href_lower}"
        
        # ต้องมีคำสำคัญ
        has_keyword = any(keyword.lower() in combined for keyword in self.target_keywords)
        
        # ไม่ควรเป็นลิงก์ไม่เกี่ยวข้อง
        excluded = ['login', 'register', 'contact', 'about', 'news', 'facebook', 'twitter']
        has_excluded = any(ex in combined for ex in excluded)
        
        return has_keyword and not has_excluded

    async def extract_comprehensive_data(self, links):
        """ดึงข้อมูลแบบครอบคลุม"""
        print(f"\n📊 เริ่มดึงข้อมูลจาก {len(links)} ลิงก์...")
        
        success_count = 0
        
        for i, link in enumerate(links, 1):
            print(f"\n📄 [{i}/{len(links)}] กำลังประมวลผล:")
            print(f"    🔗 {link}")
            
            try:
                # ลองด้วย Playwright ก่อน
                program_data = await self.extract_with_playwright(link)
                
                if not program_data:
                    # ลองด้วย requests + BeautifulSoup
                    program_data = await self.extract_with_requests(link)
                
                if program_data:
                    self.programs_data.append(program_data)
                    success_count += 1
                    
                    print(f"    ✅ สำเร็จ!")
                    print(f"       🏫 {program_data['มหาวิทยาลัย']}")
                    print(f"       📚 {program_data['หลักสูตร'][:50]}...")
                    print(f"       💰 {program_data['ค่าเทอม']}")
                else:
                    print(f"    ⚠️ ไม่พบข้อมูล")
                
                await asyncio.sleep(0.5)  # หน่วงเวลา
                
            except Exception as e:
                print(f"    ❌ ข้อผิดพลาด: {str(e)[:50]}...")
                continue
        
        print(f"\n🎯 สรุป: ดึงข้อมูลสำเร็จ {success_count}/{len(links)} ลิงก์")

    async def extract_with_playwright(self, url):
        """ดึงข้อมูลด้วย Playwright"""
        try:
            await self.page.goto(url, wait_until='networkidle', timeout=15000)
            await self.page.wait_for_timeout(2000)
            
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            return self.extract_program_info(soup, url)
            
        except:
            return None

    async def extract_with_requests(self, url):
        """ดึงข้อมูลด้วย requests"""
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                return self.extract_program_info(soup, url)
        except:
            pass
        return None

    def extract_program_info(self, soup, url):
        """แยกข้อมูลโปรแกรม"""
        try:
            program_data = {
                'มหาวิทยาลัย': self.extract_university(soup, url),
                'หลักสูตร': self.extract_program_name(soup),
                'ค่าเทอม': self.extract_tuition_info(soup),
                'URL': url
            }

            if (program_data['หลักสูตร'] != 'ไม่ระบุ' and 
                len(program_data['หลักสูตร']) > 10):
                return program_data

            return None

        except Exception as e:
            return None

    def extract_university(self, soup, url):
        """ดึงชื่อมหาวิทยาลัยจาก alt ของโลโก้"""
        print(f"    🔍 กำลังหาชื่อมหาวิทยาลัย...")

        # หา logo ที่อยู่ใน class h-brand แล้วดึง alt
        img = soup.select_one('span.h-brand img[alt]')
        if img:
            alt_text = img.get('alt', '').strip()
            if alt_text.startswith('มหาวิทยาลัย') and len(alt_text) < 100:
                print(f"    ✅ พบจาก <img alt>: {alt_text}")
                return alt_text

        print("    ❌ ไม่พบจาก <img alt>")
        return 'ไม่ระบุ'

    def extract_program_name(self, soup):
        """ดึงชื่อหลักสูตร"""
        # หาจากตาราง
        program_patterns = ['ชื่อหลักสูตร', 'หลักสูตร', 'program', 'course']
        for pattern in program_patterns:
            elements = soup.find_all(text=re.compile(pattern, re.IGNORECASE))
            for element in elements:
                parent = element.parent
                if parent:
                    next_cell = parent.find_next_sibling()
                    if next_cell:
                        text = next_cell.get_text(strip=True)
                        if len(text) > 10 and any(kw.lower() in text.lower() for kw in self.target_keywords):
                            return text
        
        # หาจาก heading
        headings = soup.find_all(['h1', 'h2', 'h3'])
        for heading in headings:
            text = heading.get_text(strip=True)
            if (len(text) > 10 and 
                any(kw.lower() in text.lower() for kw in self.target_keywords) and
                'TCAS' not in text):
                return text
        
        # หาจาก title
        title = soup.find('title')
        if title:
            text = title.get_text(strip=True)
            if any(kw.lower() in text.lower() for kw in self.target_keywords):
                return text
        
        return 'ไม่ระบุ'

    def extract_tuition_info(self, soup):
        """ดึงข้อมูลค่าเทอมจาก <dt>ค่าใช้จ่าย</dt> แล้วเอา <dd> ถัดไป"""
        print("    🔍 กำลังดึงข้อมูลค่าใช้จ่าย...")
        
        # หา <dt> ที่มีข้อความ "ค่าใช้จ่าย"
        dt_elements = soup.find_all('dt')
        
        for dt in dt_elements:
            dt_text = dt.get_text(strip=True)
            if 'ค่าใช้จ่าย' in dt_text:
                # หา <dd> ถัดไป
                dd = dt.find_next_sibling('dd')
                if dd:
                    tuition_text = dd.get_text(strip=True)
                    print(f"    ✅ พบข้อมูลค่าใช้จ่าย: {tuition_text}")
                    return tuition_text
        
        print("    ❌ ไม่พบข้อมูลค่าใช้จ่าย")
        return "ไม่พบข้อมูล"

    def save_to_excel(self, filename='ข้อมูล_TCAS_วิศวคอม.xlsx'):
        """บันทึกไฟล์ Excel"""
        if not self.programs_data:
            print("❌ ไม่มีข้อมูลให้บันทึก")
            return
        
        print(f"\n💾 บันทึกข้อมูล {len(self.programs_data)} รายการ...")
        
        # เตรียมข้อมูล
        df_data = []
        for program in self.programs_data:
            row = {
                'มหาวิทยาลัย': program.get('มหาวิทยาลัย', 'ไม่ระบุ'),
                'หลักสูตร': program.get('หลักสูตร', 'ไม่ระบุ'),
                'ค่าเทอม': program.get('ค่าเทอม', 'ไม่พบข้อมูล'),
                'URL': program.get('URL', '')
            }
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        df = df.sort_values(['มหาวิทยาลัย'], na_position='last')
        
        # บันทึก Excel
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='ข้อมูลหลักสูตร', index=False)
            
            # เพิ่ม hyperlink
            workbook = writer.book
            worksheet = writer.sheets['ข้อมูลหลักสูตร']
            
            # สร้าง hyperlink ใน column D (URL)
            for row_idx, url in enumerate(df['URL'], start=2):
                if url and url.startswith('http'):
                    cell = worksheet.cell(row=row_idx, column=4)  # Column D
                    cell.hyperlink = url
                    cell.value = url
                    cell.style = "Hyperlink"
            
            # ปรับความกว้างคอลัมน์
            worksheet.column_dimensions['A'].width = 40  # มหาวิทยาลัย
            worksheet.column_dimensions['B'].width = 60  # หลักสูตร
            worksheet.column_dimensions['C'].width = 20  # ค่าเทอม
            worksheet.column_dimensions['D'].width = 60  # URL
        
        print(f"✅ บันทึกข้อมูลลงไฟล์ {filename}")
        print("🔗 คอลัมน์ 'URL' สามารถคลิกได้เลย!")
        
        self.print_summary(df)

    def print_summary(self, df):
        """แสดงสรุปผล"""
        print(f"\n📈 สรุปผลการรวบรวมข้อมูล:")
        print("=" * 50)
        
        total = len(df)
        universities = df[df['มหาวิทยาลัย'] != 'ไม่ระบุ']['มหาวิทยาลัย'].nunique()
        
        print(f"📚 จำนวนหลักสูตรทั้งหมด: {total}")
        print(f"🏫 จำนวนมหาวิทยาลัย: {universities}")
        
        print(f"\n📋 ตัวอย่างข้อมูล:")
        display_df = df[['มหาวิทยาลัย', 'หลักสูตร', 'ค่าเทอม']].head(5)
        print(display_df.to_string(index=False))

async def main():
    scraper = TCASScraper()
    
    try:
        print("🚀 ระบบดึงข้อมูล TCAS")
        print("=" * 50)
        print("🎯 เป้าหมาย: หลักสูตรวิศวกรรมคอมพิวเตอร์และ AI")
        
        # เริ่มต้น browser
        await scraper.init_browser(headless=False, slow_mo=500)
        
        # ค้นหาและรวบรวมข้อมูล
        await scraper.search_via_website()
        
        print(f"\n✅ รวบรวมข้อมูลเสร็จ: {len(scraper.programs_data)} รายการ")
        
        # บันทึกข้อมูล
        if scraper.programs_data:
            scraper.save_to_excel()
        else:
            print("❌ ไม่พบข้อมูล")
        
        print("\n🎉 เสร็จสมบูรณ์!")
        print("⏳ รอ 10 วินาที...")
        await asyncio.sleep(10)
        
    except KeyboardInterrupt:
        print("\n⏹️ ยกเลิก")
    except Exception as e:
        print(f"❌ ข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await scraper.close_browser()

if __name__ == "__main__":
    asyncio.run(main())