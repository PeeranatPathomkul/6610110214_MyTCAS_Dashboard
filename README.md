# 🎓 TCAS Dashboard - Computer Engineering & AI Program Analysis System
## 6610110214 Peeranat Pathomkul
A comprehensive system for collecting, analyzing, and visualizing Computer Engineering and Artificial Intelligence program data from the Thai Central Admission System (TCAS). This project combines a powerful web scraper for data collection with an interactive dashboard for analysis and comparison.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/PeeranatPathomkul/6610110214_MyTCAS_Dashboard.git
cd 6610110214_MyTCAS_Dashboard
pip install -r requirements-all.txt
playwright install chromium

# Run the dashboard
python dashboard3.py
# Open http://127.0.0.1:8050/ in your browser
```

Run web scraping
```bash
# Clone and setup
git clone https://github.com/PeeranatPathomkul/6610110214_MyTCAS_Dashboard.git
cd 6610110214_MyTCAS_Dashboard
pip install -r requirements-all.txt
playwright install chromium

# Run the code
python read_file3.py
```
## 📁 Project Structure

```
6610110214_MyTCAS_Dashboard/
├── 📊 dashboard3.py              # Interactive Web Dashboard
├── 🔍 read_file3.py               # Data Collection Tool  
├── 📋 tcas_data.xlsx           # Clean Dataset (Ready to Use)
├── 📝 README.md                # This Documentation 
└── 📋 requirements-all.txt     # Complete Dependencies
```

## ✨ Key Features

### 🎯 Smart Data Collection System
Our web scraper uses **4-layer intelligent extraction** to ensure comprehensive data coverage:

**🔍 Layer 1: Keyword Search**
- Automatically searches for "Computer Engineering", "AI Engineering", "วิศวกรรมคอมพิวเตอร์"
- Uses natural language processing to identify relevant programs
- Filters out unrelated content automatically

**🏗️ Layer 2: Structure Analysis** 
- Analyzes website navigation and menu structures
- Maps university websites to find program directories
- Discovers hidden program pages through link analysis

**🎯 Layer 3: Pattern Recognition**
- Tests common URL patterns across Thai universities
- Predicts likely program page locations
- Validates discovered pages for content relevance

**📄 Layer 4: Deep Content Parsing**
- Extracts detailed program information (tuition, payment methods, university type)
- Handles dynamic content loading with Playwright browser automation
- Processes both static HTML and JavaScript-rendered content

**🧠 Smart Data Processing:**
- Auto-categorizes universities as Public/Private using keyword matching
- Standardizes tuition fee formats and payment methods
- Calculates 4-year program costs automatically
- Removes duplicates and validates data quality

### 📊 Interactive Dashboard Features

**🏠 Home Page - Quick Insights**
- **Live Statistics Cards**: Total programs, average costs, price ranges
- **Smart Overview Chart**: Compares public vs private university pricing
- **Quick Navigation**: Jump directly to analysis tools

**⚖️ Compare Page - Advanced Filtering**
- **Real-time Price Slider**: Instantly filter by budget range
- **Multi-criteria Filtering**: Payment method, university type, location
- **Smart Search**: Find universities by partial name matching
- **Cost Calculator**: Compare up to 3 universities with 4-year projections
- **Dynamic Statistics**: Updates automatically as you filter

**📈 Analytics Page - Data Insights**
- **Distribution Analysis**: Histogram showing tuition fee patterns
- **Market Segmentation**: Public vs Private university proportions  
- **Comparative Analysis**: Min/Max/Average pricing by category
- **Trend Visualization**: Interactive charts with hover details

**📋 Data Page - Full Dataset Access**
- **Interactive DataTable**: Sort, search, and paginate through all programs
- **Export Functionality**: Download filtered results
- **Responsive Design**: Works perfectly on mobile and desktop
- **Color-coded Rows**: Visual distinction between public/private institutions

## 🎯 Dashboard Pages Overview

### 🏠 Home Page
**What you'll see:**
- Total programs available
- Average tuition costs
- Quick comparison charts
- Navigation shortcuts

**Perfect for:** Getting a quick overview before diving deeper

### ⚖️ Compare Page
**Interactive Filters:**
- Payment method (per semester/total program)
- University type (public/private)
- Price range slider
- University name search

**Special Features:**
- Real-time statistics updates
- Cost calculator for 3 universities
- Visual comparison charts

**Perfect for:** Finding programs within your budget and preferences

### 📈 Analytics Page
**Advanced Visualizations:**
- Tuition distribution histogram
- University type proportions
- Min/Max/Average comparisons by category

**Perfect for:** Understanding market trends and pricing patterns

### 📋 Data Page
**Full Dataset Access:**
- Sortable columns
- Search functionality
- Pagination for large datasets
- Export capabilities

**Perfect for:** Detailed research and data exploration

## 💾 Dataset Information

### Main Data File: `tcas_data.xlsx`

**Sheet 1: Program Data**
| Column | Description | Example |
|--------|-------------|---------|
| มหาวิทยาลัย | University Name | จุฬาลงกรณ์มหาวิทยาลัย |
| หลักสูตร | Program Name | วศ.บ. วิศวกรรมคอมพิวเตอร์ |
| ค่าเทอม/เทอม | Per Semester Fee | 35,000 THB |
| ค่าเทอมจากเว็บ | Total Program Fee | 280,000 THB |
| รูปแบบการชำระ | Payment Method | ต่อภาคการศึกษา |
| ประเภทมหาวิทยาลัย | University Type | รัฐ/เอกชน |

**Sheet 2: Statistics Summary**
- Program counts by university
- Average, min, max tuition fees
- Top universities by program count

## 🛠 Installation Guide

### Prerequisites
- Python 3.7+
- Modern web browser

### Alternative: Install Everything
```bash
# Install both dashboard and scraper dependencies (single file)
pip install -r requirements-all.txt
playwright install chromium
```

### Run the Application
```bash
python dashboard3.py
```
Visit `http://127.0.0.1:8050/` to access the dashboard.

## 🔍 Data Collection Deep Dive

### How Our Scraper Works

**🤖 Intelligent University Detection**
```python
# Example: Auto-categorizing universities
university_type = 'เอกชน' if any(keyword in university_name) else 'รัฐ'
```

**💰 Smart Fee Extraction**
- Detects different payment formats (per semester vs. total program)
- Handles Thai language fee descriptions automatically
- Calculates equivalent 4-year costs for comparison
- Validates fee ranges to filter out errors

**🎯 Program Relevance Scoring**
The system scores each discovered program based on:
- Keyword presence in program name (Computer, Engineering, AI)
- University credibility (official .ac.th domains preferred)
- Content completeness (programs with full details ranked higher)
- Page authority (linked from main university pages)

**⚡ Performance Optimizations**
- **Asynchronous Processing**: Handles multiple pages simultaneously
- **Smart Caching**: Avoids re-downloading unchanged content
- **Graceful Degradation**: Falls back to simpler methods if advanced techniques fail
- **Rate Limiting**: Respects website resources with built-in delays

### Data Quality Assurance

**🔍 Multi-layer Validation**
1. **Format Validation**: Ensures tuition fees are numeric and reasonable
2. **Completeness Check**: Flags programs missing critical information
3. **Duplicate Detection**: Removes identical programs from different sources
4. **Relevance Filtering**: Excludes non-engineering programs automatically

**📊 Data Enrichment**
- Generates short program names for better display
- Adds calculated fields (4-year costs, cost per credit)
- Creates categorical variables for analysis
- Standardizes university naming conventions

## 💡 Usage Examples & Scenarios

### 🎯 Scenario 1: Budget-Conscious Student
**Goal**: Find quality programs under 30,000 THB/semester

**Steps in Dashboard**:
1. **Compare Page** → Set price slider to 15,000-30,000 THB
2. **Filter** → Select "Public Universities" only  
3. **Review Results** → 15+ programs available
4. **Use Calculator** → Compare top 3 choices for 4-year costs

**Expected Results**: Programs from universities like Kasetsart, KMUTT, regional public universities

### 🎯 Scenario 2: AI Specialization Seeker  
**Goal**: Compare AI-focused programs across university types

**Steps in Dashboard**:
1. **Data Page** → Search for "AI" or "ปัญญาประดิษฐ์"
2. **Compare Page** → Use cost calculator for AI programs
3. **Analytics Page** → View distribution of AI program costs
4. **Analysis** → Compare public vs private AI program pricing

**Expected Results**: Higher average costs but cutting-edge curriculum options

### 🎯 Scenario 3: International Program Research
**Goal**: Find English-taught computer engineering programs

**Steps in Dashboard**:
1. **Compare Page** → Search for "International" or "English"
2. **Filter** → Set higher price range (40,000+ THB)
3. **Calculator** → Compare international vs. Thai programs
4. **Decision** → Weigh cost vs. language benefits

**Expected Results**: Premium pricing but international exposure and English instruction

### 🎯 Scenario 4: University Ranking Analysis
**Goal**: Compare all programs from top-tier universities

**Steps in Dashboard**:
1. **Compare Page** → Search "จุฬา" (Chula), "เกษตร" (Kasetsart), "มหิดล" (Mahidol)
2. **Analytics** → View price distribution for elite universities
3. **Cost Calculator** → Compare flagship programs
4. **Data Table** → Export results for detailed analysis

**Expected Results**: Higher costs but prestigious institutions with strong alumni networks

## 📊 Dashboard Technical Highlights

### Advanced Interactive Features

**🎨 Modern UI/UX Design**
- **Glassmorphism Effects**: Modern backdrop-blur styling
- **Gradient Aesthetics**: Dynamic color schemes throughout
- **Responsive Grid System**: Adapts perfectly to any screen size
- **Micro-animations**: Smooth transitions and hover effects
- **Dark Mode Ready**: Designed for future dark theme implementation

**⚡ Real-time Data Processing**
```python
# Example: Dynamic filtering callback
@app.callback(
    [Output('stats', 'children'), Output('chart', 'children')],
    [Input('price-slider', 'value'), Input('university-type', 'value')]
)
def update_dashboard(price_range, uni_types):
    filtered_data = df[df['tuition'].between(*price_range)]
    return create_stats(filtered_data), create_chart(filtered_data)
```

**📈 Smart Visualization Engine**
- **Plotly Integration**: Interactive charts with zoom, pan, and hover
- **Dynamic Color Coding**: Consistent color themes across all charts
- **Responsive Charts**: Automatically adjust to container size
- **Export Capabilities**: Download charts as PNG/PDF

**🧮 Advanced Cost Calculator**
- **Multi-university Comparison**: Side-by-side cost analysis
- **4-year Projections**: Automatic calculation of total program costs
- **Payment Method Handling**: Different calculations for semester vs. total fees
- **Visual Cost Breakdown**: Bar charts showing cost differences

### Data Processing Pipeline

**📊 Real-time Analytics**
1. **Data Loading**: Efficient pandas DataFrame operations
2. **Filter Processing**: Instant filtering without page reloads  
3. **Statistical Calculation**: Live computation of averages, ranges, counts
4. **Chart Generation**: Dynamic Plotly figure creation
5. **UI Updates**: Seamless callback-driven interface updates

**🔄 State Management**
- **Multi-page Navigation**: Preserves user selections across pages
- **Session Persistence**: Maintains filter states during navigation
- **Error Handling**: Graceful fallbacks for missing data
- **Performance Optimization**: Cached calculations for faster responses

### Interactive Features Breakdown

**🎯 Smart Filtering System**
- **Range Sliders**: Intuitive price range selection with live previews
- **Multi-select Dropdowns**: University type and payment method filtering
- **Search Functionality**: Fuzzy matching for university names
- **Combined Filters**: All filters work together seamlessly

**📱 Cross-platform Compatibility**
- **Mobile Responsive**: Touch-friendly interface for smartphones
- **Tablet Optimized**: Adjusted layouts for medium screens
- **Desktop Enhanced**: Full feature set for large screens
- **Browser Tested**: Works across Chrome, Firefox, Safari, Edge