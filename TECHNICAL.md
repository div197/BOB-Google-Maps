# 技术文档 - 代码详解

本文档详细介绍项目中各个Python脚本的功能、用法和实现细节。

## 📝 目录

- [核心爬虫模块](#核心爬虫模块)
  - [main.py - 单点爬虫](#mainpy---单点爬虫)
  - [batch_scraper.py - 批量处理器](#batch_scraperpy---批量处理器)
- [工具模块](#工具模块)
  - [process_urls.py - URL预处理器](#process_urlspy---url预处理器)
  - [check_progress.py - 进度检查器](#check_progresspy---进度检查器)
  - [retry_failed_scrapes.py - 失败重试器](#retry_failed_scrapespy---失败重试器)
  - [find_duplicates_simple.py - 重复数据检测](#find_duplicates_simplepy---重复数据检测)
  - [input_statistics.py - 输入数据统计](#input_statisticspy---输入数据统计)
- [配置和错误处理](#配置和错误处理)
  - [error_codes.md - 错误代码说明](#error_codesmd---错误代码说明)

---

## 核心爬虫模块

### main.py - 单点爬虫

**功能描述**：Google Maps单个地点的数据爬取核心引擎

#### 主要特性

- **完整数据提取**：商户基本信息、评论内容、评分、坐标等
- **智能重试机制**：网络超时和临时错误自动重试
- **多种输出格式**：JSON和CSV格式同时输出
- **错误分类处理**：详细的错误代码和错误信息
- **编码兼容性**：完美支持中文字符和特殊字符

#### 核心功能

1. **商户信息提取**
   ```python
   business_info = {
       "name": "商户名称",
       "address": "详细地址", 
       "phone": "联系电话",
       "website": "官方网站",
       "rating": 4.5,
       "total_reviews": 1250,
       "coordinates": {"latitude": 40.7128, "longitude": -74.0060},
       "hours": "营业时间信息"
   }
   ```

2. **评论数据提取**
   ```python
   review = {
       "author": "用户名",
       "rating": 5,
       "date": "2024-01-15", 
       "text": "评论内容",
       "helpful_count": 12
   }
   ```

#### 使用方法

```bash
# 基础用法
python main.py "https://maps.google.com/maps/place/..."

# 高级参数
python main.py "URL" \
    --output-dir custom_output \
    --max-retries 5 \
    --no-headless \
    --json-output
```

#### 参数说明

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `url` | string | 必需 | Google Maps地点URL |
| `--output-dir` | string | "output" | 输出目录路径 |
| `--max-retries` | int | 3 | 最大重试次数 |
| `--no-headless` | flag | False | 显示浏览器界面 |
| `--json-output` | flag | False | 仅输出JSON格式 |

#### 错误处理

脚本使用标准化错误代码系统：

- `1001`: 浏览器初始化失败
- `1002`: URL加载失败
- `1003`: 商户信息提取失败
- `1004`: 评论按钮未找到
- `1005`: 评论滚动失败
- `1006`: 评论提取失败
- `1007`: 坐标提取失败
- `1008`: CSV保存失败

---

### batch_scraper.py - 批量处理器

**功能描述**：大规模Google Maps数据批量爬取工具，支持数万级地点处理

#### 主要特性

- **大规模处理**：支持数万个地点的批量处理
- **断点恢复**：意外中断后自动从断点继续
- **多线程并发**：可配置的并发线程数
- **智能重试**：失败地点的选择性重试
- **进度跟踪**：实时进度显示和状态保存
- **多种运行模式**：测试、生产、无人值守等模式

#### 核心架构

```python
class BatchGoogleMapsScraper:
    def __init__(self, script_path, output_base_dir, config):
        # 初始化配置和路径
        
    def process_batch(self, places, **kwargs):
        # 批量处理主逻辑
        
    def scrape_single_place(self, place_data):
        # 单个地点处理
        
    def save_progress(self, progress):
        # 保存处理进度
```

#### 配置模式

1. **默认模式** - 平衡性能和稳定性
   ```python
   DEFAULT_CONFIG = {
       'max_workers': 3,
       'max_retries': 3,
       'timeout': 300,
       'max_places': None
   }
   ```

2. **测试模式** - 快速验证功能
   ```python
   TEST_CONFIG = {
       'max_workers': 1,
       'max_places': 5,
       'timeout': 60
   }
   ```

3. **生产模式** - 大规模处理
   ```python
   PRODUCTION_CONFIG = {
       'max_workers': 5,
       'max_places': 1000,
       'timeout': 600
   }
   ```

4. **无人值守模式** - 长期自动运行
   ```python
   UNATTENDED_CONFIG = {
       'max_workers': 6,
       'max_places': 120,
       'continuous_mode': True,
       'auto_retry_failed': True
   }
   ```

#### 使用示例

```bash
# 基础批量处理
python batch_scraper.py input/places.jsonl

# 测试模式
python batch_scraper.py input/places.jsonl --test

# 生产模式
python batch_scraper.py input/places.jsonl --production \
    --max-workers 8 --max-places 2000

# 无人值守模式
python batch_scraper.py input/places.jsonl --unattended

# 自定义配置
python batch_scraper.py input/places.jsonl \
    --max-workers 4 \
    --max-retries 5 \
    --timeout 600 \
    --max-places 500 \
    --resume \
    --retry-failed
```

#### 输出文件结构

```
batch_output/
├── parent_type/
│   └── sub_type/
│       ├── place_id_商户名称.json
│       └── place_id_商户名称.csv
├── progress.json          # 处理进度
├── errors.jsonl          # 错误日志
└── success.jsonl         # 成功日志
```

---

## 工具模块

### process_urls.py - URL预处理器

**功能描述**：批量为输入文件中的Google Maps URL添加`&hl=en`参数，以强制浏览器使用英文界面。这是确保爬虫能正确解析页面的关键预处理步骤。

#### 主要特性
- **强制英文**：确保所有URL都指向英文版Google Maps页面。
- **幂等性**：不会重复为已经包含`&hl=en`的URL添加参数。
- **容错性**：会跳过文件中格式错误的JSON行。

#### 使用方法
1.  **配置路径**：在 `process_urls.py` 脚本中，修改 `input_file` 和 `output_file` 变量以匹配你的文件路径。
2.  **执行脚本**：
    ```bash
    python process_urls.py
    ```
3.  **使用输出**：使用脚本生成的新文件（例如 `..._en.jsonl`）作为 `batch_scraper.py` 的输入。

#### 核心逻辑
```python
def process_urls():
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                data = json.loads(line)
                # In the actual script, the key is 'Maps_url'. 
                # This is a representative example.
                if 'url' in data and data['url']:
                    if '&hl=en' not in data['url']:
                        data['url'] += '&hl=en'
                outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
            except json.JSONDecodeError:
                print(f"Skipping malformed JSON line: {line.strip()}")
```

### check_progress.py - 进度检查器

**功能描述**：快速检查批量处理的进度和统计信息

#### 主要功能

- **进度统计**：成功、失败、跳过的地点数量
- **重复检测**：检查是否存在重复处理的地点
- **状态分析**：分析处理状态的分布情况

#### 使用方法

```bash
python check_progress.py
```

#### 输出示例

```
=== Progress.json 统计 ===
successful count: 1250
failed count: 45
skipped count: 0
total processed: 1295

=== 去重后统计 ===
unique successful: 1250
unique failed: 45
unique skipped: 0

=== 交集检查 ===
successful & failed: 0
successful & skipped: 0
failed & skipped: 0

=== 总计 ===
total unique processed IDs: 1295
```

#### 代码解析

```python
# 读取进度文件
with open('batch_output/progress.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 统计各状态数量
successful_count = len(data['successful'])
failed_count = len(data['failed'])
skipped_count = len(data['skipped'])

# 检查重复和交集
successful_set = set(data['successful'])
failed_set = set(data['failed'])
intersection = successful_set & failed_set
```

---

### retry_failed_scrapes.py - 失败重试器

**功能描述**：专门重试之前失败的地点，提高数据完整性

#### 主要特性

- **智能筛选**：自动识别失败的地点
- **批量重试**：支持批量重新处理失败项目
- **配置继承**：继承原有的批量处理配置
- **进度合并**：重试结果自动合并到主进度文件

#### 使用方法

```bash
# 基础重试
python retry_failed_scrapes.py

# 指定输入文件和配置
python retry_failed_scrapes.py \
    --input input/places.jsonl \
    --max-workers 3 \
    --max-retries 5
```

#### 工作流程

1. **读取进度文件**：从`progress.json`获取失败列表
2. **加载原始数据**：从输入文件中找到对应的地点信息
3. **执行重试**：使用batch_scraper重新处理
4. **更新进度**：将结果更新到进度文件

#### 核心逻辑

```python
def retry_failed_places():
    # 1. 读取失败列表
    progress = load_progress()
    failed_place_ids = progress.get('failed', [])
    
    # 2. 加载原始地点数据
    original_places = load_input_data()
    failed_places = filter_failed_places(original_places, failed_place_ids)
    
    # 3. 重新处理
    scraper = BatchGoogleMapsScraper()
    scraper.process_batch(failed_places, retry_mode=True)
    
    # 4. 更新进度
    update_progress(results)
```

---

### find_duplicates_simple.py - 重复数据检测

**功能描述**：检测和处理输出数据中的重复项目

#### 主要功能

- **重复检测**：基于place_id检测重复的数据文件
- **统计报告**：生成详细的重复情况报告
- **清理建议**：提供重复文件的清理建议

#### 使用方法

```bash
python find_duplicates_simple.py
```

#### 检测逻辑

```python
def find_duplicates():
    file_dict = {}
    duplicates = []
    
    # 遍历所有输出文件
    for file_path in glob("batch_output/**/*.json"):
        place_id = extract_place_id(file_path)
        
        if place_id in file_dict:
            duplicates.append({
                'place_id': place_id,
                'files': [file_dict[place_id], file_path]
            })
        else:
            file_dict[place_id] = file_path
    
    return duplicates
```

#### 输出报告

```
=== 重复文件检测报告 ===
总文件数: 1295
唯一place_id数: 1290
重复place_id数: 5

重复详情:
place_id: ChIJ123...
  - batch_output/food_and_drink/restaurant/ChIJ123_餐厅A.json
  - batch_output/food_and_drink/chinese_restaurant/ChIJ123_餐厅A.json
```

---

### input_statistics.py - 输入数据统计

**功能描述**：分析输入数据的分布和统计信息

#### 主要功能

- **类型分布**：统计各parent_type和sub_type的数量
- **数据质量**：检查缺失字段和格式问题
- **地理分布**：分析地点的地理分布情况（如果有坐标）

#### 使用方法

```bash
python input_statistics.py input/places.jsonl
```

#### 分析维度

1. **数据总量统计**
   ```python
   total_places = len(places)
   unique_place_ids = len(set(p['place_id'] for p in places))
   ```

2. **类型分布统计**
   ```python
   parent_type_dist = Counter(p['parent_type'] for p in places)
   sub_type_dist = Counter(p['sub_type'] for p in places)
   ```

3. **数据质量检查**
   ```python
   missing_fields = {
       'place_id': sum(1 for p in places if not p.get('place_id')),
       'url': sum(1 for p in places if not p.get('url')),
       'place_name': sum(1 for p in places if not p.get('place_name'))
   }
   ```

#### 输出示例

```
=== 输入数据统计报告 ===

基础统计:
总地点数: 15,847
唯一place_id数: 15,847
重复place_id数: 0

Parent Type分布:
food_and_drink: 8,234 (52.0%)
shopping: 3,456 (21.8%)
entertainment_and_recreation: 2,123 (13.4%)
transportation: 1,234 (7.8%)
其他: 800 (5.0%)

Sub Type分布 (Top 10):
restaurant: 3,456
store: 2,345
cafe: 1,234
park: 987
...

数据质量检查:
缺失place_id: 0
缺失URL: 12
缺失place_name: 5
无效URL格式: 3
```

---

## 配置和错误处理

### error_codes.md - 错误代码说明

**功能描述**：标准化错误代码定义和问题解决方案

#### 错误代码分类

1. **浏览器相关错误 (1000-1099)**
   - `1001`: 浏览器初始化失败
   - `1002`: URL加载失败

2. **数据提取错误 (1100-1199)**
   - `1003`: 商户信息提取失败
   - `1004`: 评论按钮未找到
   - `1005`: 评论滚动失败
   - `1006`: 评论提取失败
   - `1007`: 坐标提取失败

3. **文件操作错误 (1200-1299)**
   - `1008`: CSV保存失败

4. **网络相关错误 (1300-1399)**
   - `1009`: 网络超时

5. **通用错误 (1900-1999)**
   - `1010`: 元素未找到
   - `1999`: 未预期错误

#### 错误处理策略

```python
class ErrorCodes:
    SUCCESS = 0
    BROWSER_INIT_FAILED = 1001
    URL_LOAD_FAILED = 1002
    # ... 其他错误代码
    
def handle_error(error_code, error_message):
    """错误处理和重试策略"""
    if error_code in [1001, 1002]:
        # 浏览器相关错误，重启浏览器
        return "restart_browser"
    elif error_code in [1009, 1010]:
        # 网络或元素问题，可重试
        return "retry"
    else:
        # 其他错误，记录并跳过
        return "skip"
```

---

## 🔧 开发和扩展

### 添加新功能

1. **扩展数据提取字段**
   ```python
   # 在main.py中添加新的提取逻辑
   def extract_additional_info(driver):
       # 新的数据提取逻辑
       pass
   ```

2. **自定义输出格式**
   ```python
   # 在batch_scraper.py中添加新的输出处理器
   def save_custom_format(data, output_path):
       # 自定义格式保存逻辑
       pass
   ```

3. **集成数据库存储**
   ```python
   # 添加数据库连接和存储逻辑
   def save_to_database(data):
       # 数据库保存逻辑
       pass
   ```

### 性能优化建议

1. **内存优化**：使用生成器处理大文件
2. **并发优化**：根据机器性能调整线程数
3. **网络优化**：添加请求间隔和重试机制
4. **存储优化**：压缩输出文件或使用更高效的格式

### 监控和维护

1. **日志监控**：定期检查错误日志
2. **性能监控**：跟踪处理速度和成功率
3. **数据质量**：定期验证输出数据的完整性
4. **版本管理**：保持代码和依赖的更新

---

# Technical Documentation - Code Details

This document provides a detailed introduction to the functionality, usage, and implementation details of each Python script in the project.

## 📝 Table of Contents

- [Core Scraper Modules](#core-scraper-modules)
  - [main.py - Single-Place Scraper](#mainpy---single-place-scraper)
  - [batch_scraper.py - Batch Processor](#batch_scraperpy---batch-processor)
- [Utility Modules](#utility-modules)
  - [process_urls.py - URL Pre-processor](#process_urlspy---url-pre-processor)
  - [check_progress.py - Progress Checker](#check_progresspy---progress-checker)
  - [retry_failed_scrapes.py - Failure Retrier](#retry_failed_scrapespy---failure-retrier)
  - [find_duplicates_simple.py - Duplicate Detection](#find_duplicates_simplepy---duplicate-detection)
  - [input_statistics.py - Input Data Statistics](#input_statisticspy---input-data-statistics)
- [Configuration and Error Handling](#configuration-and-error-handling)
  - [error_codes.md - Error Code Explanations](#error_codesmd---error-code-explanations)

---

## Core Scraper Modules

### main.py - Single-Place Scraper

**Functional Description**: The core engine for scraping data for a single Google Maps place.

#### Key Features

- **Comprehensive Data Extraction**: Business info, review content, ratings, coordinates, etc.
- **Intelligent Retry Mechanism**: Automatic retries for network timeouts and temporary errors.
- **Multiple Output Formats**: Simultaneous output in JSON and CSV formats.
- **Categorized Error Handling**: Detailed error codes and messages.
- **Encoding Compatibility**: Perfect support for Chinese and special characters.

#### Core Functions

1. **Business Information Extraction**
   ```python
   business_info = {
       "name": "Business Name",
       "address": "Detailed Address",
       "phone": "Contact Phone",
       "website": "Official Website",
       "rating": 4.5,
       "total_reviews": 1250,
       "coordinates": {"latitude": 40.7128, "longitude": -74.0060},
       "hours": "Business Hours Information"
   }
   ```

2. **Review Data Extraction**
   ```python
   review = {
       "author": "Username",
       "rating": 5,
       "date": "2024-01-15",
       "text": "Review content",
       "helpful_count": 12
   }
   ```

#### Usage

```bash
# Basic usage
python main.py "https://maps.google.com/maps/place/..."

# Advanced parameters
python main.py "URL" \
    --output-dir custom_output \
    --max-retries 5 \
    --no-headless \
    --json-output
```

#### Parameter Description

| Parameter | Type | Default | Description |
|---|---|---|---|
| `url` | string | Required | Google Maps place URL |
| `--output-dir` | string | "output" | Output directory path |
| `--max-retries` | int | 3 | Maximum number of retries |
| `--no-headless` | flag | False | Show browser UI |
| `--json-output` | flag | False | Output only in JSON format |

#### Error Handling

The script uses a standardized error code system:

- `1001`: Browser initialization failed
- `1002`: URL loading failed
- `1003`: Business info extraction failed
- `1004`: Reviews button not found
- `1005`: Review scrolling failed
- `1006`: Review extraction failed
- `1007`: Coordinate extraction failed
- `1008`: CSV save failed

---

### batch_scraper.py - Batch Processor

**Functional Description**: A tool for large-scale batch scraping of Google Maps data, supporting tens of thousands of places.

#### Key Features

- **Large-Scale Processing**: Supports batch processing of tens of thousands of places.
- **Resume from Breakpoint**: Automatically resumes from the last processed point after an interruption.
- **Multi-threaded Concurrency**: Configurable number of concurrent threads.
- **Intelligent Retry**: Selective retries for failed places.
- **Progress Tracking**: Real-time progress display and state saving.
- **Multiple Run Modes**: Test, production, unattended, etc.

#### Core Architecture

```python
class BatchGoogleMapsScraper:
    def __init__(self, script_path, output_base_dir, config):
        # Initialize configuration and paths
        
    def process_batch(self, places, **kwargs):
        # Main logic for batch processing
        
    def scrape_single_place(self, place_data):
        # Process a single place
        
    def save_progress(self, progress):
        # Save processing progress
```

#### Configuration Modes

1. **Default Mode** - Balanced performance and stability
   ```python
   DEFAULT_CONFIG = {
       'max_workers': 3,
       'max_retries': 3,
       'timeout': 300,
       'max_places': None
   }
   ```

2. **Test Mode** - For quick feature validation
   ```python
   TEST_CONFIG = {
       'max_workers': 1,
       'max_places': 5,
       'timeout': 60
   }
   ```

3. **Production Mode** - For large-scale processing
   ```python
   PRODUCTION_CONFIG = {
       'max_workers': 5,
       'max_places': 1000,
       'timeout': 600
   }
   ```

4. **Unattended Mode** - For long-term automatic operation
   ```python
   UNATTENDED_CONFIG = {
       'max_workers': 6,
       'max_places': 120,
       'continuous_mode': True,
       'auto_retry_failed': True
   }
   ```

#### Usage Example

```bash
# Basic batch processing
python batch_scraper.py input/places.jsonl

# Test mode
python batch_scraper.py input/places.jsonl --test

# Production mode
python batch_scraper.py input/places.jsonl --production \
    --max-workers 8 --max-places 2000

# Unattended mode
python batch_scraper.py input/places.jsonl --unattended

# Custom configuration
python batch_scraper.py input/places.jsonl \
    --max-workers 4 \
    --max-retries 5 \
    --timeout 600 \
    --max-places 500 \
    --resume \
    --retry-failed
```

#### Output File Structure

```
batch_output/
├── parent_type/
│   └── sub_type/
│       ├── place_id_BusinessName.json
│       └── place_id_BusinessName.csv
├── progress.json          # Processing progress
├── errors.jsonl          # Error log
└── success.jsonl         # Success log
```

---

## Utility Modules

### process_urls.py - URL Pre-processor

**Functional Description**: Batch processes input files to add the `&hl=en` parameter to Google Maps URLs, forcing the browser to use the English interface. This is a critical pre-processing step to ensure the scraper can parse pages correctly.

#### Key Features
- **Force English**: Ensures all URLs point to the English version of Google Maps.
- **Idempotent**: Does not repeatedly add the parameter to URLs that already contain `&hl=en`.
- **Fault-Tolerant**: Skips malformed JSON lines in the file.

#### Usage
1.  **Configure Paths**: In the `process_urls.py` script, modify the `input_file` and `output_file` variables to match your file paths.
2.  **Execute Script**:
    ```bash
    python process_urls.py
    ```
3.  **Use Output**: Use the new file generated by the script (e.g., `..._en.jsonl`) as input for `batch_scraper.py`.

#### Core Logic
```python
def process_urls():
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                data = json.loads(line)
                # In the actual script, the key is 'Maps_url'. 
                # This is a representative example.
                if 'url' in data and data['url']:
                    if '&hl=en' not in data['url']:
                        data['url'] += '&hl=en'
                outfile.write(json.dumps(data, ensure_ascii=False) + '\n')
            except json.JSONDecodeError:
                print(f"Skipping malformed JSON line: {line.strip()}")
```

### check_progress.py - Progress Checker

**Functional Description**: Quickly check the progress and statistics of batch processing.

#### Key Functions

- **Progress Statistics**: Number of successful, failed, and skipped places.
- **Duplicate Detection**: Checks for duplicate processing of places.
- **Status Analysis**: Analyzes the distribution of processing statuses.

#### Usage

```bash
python check_progress.py
```

#### Example Output

```
=== Progress.json Statistics ===
successful count: 1250
failed count: 45
skipped count: 0
total processed: 1295

=== Statistics after Deduplication ===
unique successful: 1250
unique failed: 45
unique skipped: 0

=== Intersection Check ===
successful & failed: 0
successful & skipped: 0
failed & skipped: 0

=== Total ===
total unique processed IDs: 1295
```

#### Code Analysis

```python
# Read the progress file
with open('batch_output/progress.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Count quantities for each status
successful_count = len(data['successful'])
failed_count = len(data['failed'])
skipped_count = len(data['skipped'])

# Check for duplicates and intersections
successful_set = set(data['successful'])
failed_set = set(data['failed'])
intersection = successful_set & failed_set
```

### retry_failed_scrapes.py - Failure Retrier

**Functional Description**: Specifically retries previously failed places to improve data integrity.

#### Key Features

- **Intelligent Filtering**: Automatically identifies failed places.
- **Batch Retry**: Supports batch reprocessing of failed items.
- **Configuration Inheritance**: Inherits the original batch processing configuration.
- **Progress Merging**: Retry results are automatically merged into the main progress file.

#### Usage

```bash
# Basic retry
python retry_failed_scrapes.py

# Specify input file and configuration
python retry_failed_scrapes.py \
    --input input/places.jsonl \
    --max-workers 3 \
    --max-retries 5
```

#### Workflow

1. **Read Progress File**: Get the list of failed places from `progress.json`.
2. **Load Original Data**: Find the corresponding place information from the input file.
3. **Execute Retry**: Reprocess using `batch_scraper`.
4. **Update Progress**: Update the results in the progress file.

#### Core Logic

```python
def retry_failed_places():
    # 1. Read the list of failed places
    progress = load_progress()
    failed_place_ids = progress.get('failed', [])
    
    # 2. Load original place data
    original_places = load_input_data()
    failed_places = filter_failed_places(original_places, failed_place_ids)
    
    # 3. Reprocess
    scraper = BatchGoogleMapsScraper()
    scraper.process_batch(failed_places, retry_mode=True)
    
    # 4. Update progress
    update_progress(results)
```

### find_duplicates_simple.py - Duplicate Detection

**Functional Description**: Detects and handles duplicate items in the output data.

#### Key Functions

- **Duplicate Detection**: Detects duplicate data files based on `place_id`.
- **Statistical Report**: Generates a detailed report on duplicates.
- **Cleanup Suggestions**: Provides suggestions for cleaning up duplicate files.

#### Usage

```bash
python find_duplicates_simple.py
```

#### Detection Logic

```python
def find_duplicates():
    file_dict = {}
    duplicates = []
    
    # Iterate through all output files
    for file_path in glob("batch_output/**/*.json"):
        place_id = extract_place_id(file_path)
        
        if place_id in file_dict:
            duplicates.append({
                'place_id': place_id,
                'files': [file_dict[place_id], file_path]
            })
        else:
            file_dict[place_id] = file_path
    
    return duplicates
```

#### Output Report

```
=== Duplicate File Detection Report ===
Total files: 1295
Unique place_ids: 1290
Duplicate place_ids: 5

Duplicate Details:
place_id: ChIJ123...
  - batch_output/food_and_drink/restaurant/ChIJ123_RestaurantA.json
  - batch_output/food_and_drink/chinese_restaurant/ChIJ123_RestaurantA.json
```

### input_statistics.py - Input Data Statistics

**Functional Description**: Analyzes the distribution and statistical information of the input data.

#### Key Functions

- **Type Distribution**: Counts the number of each `parent_type` and `sub_type`.
- **Data Quality**: Checks for missing fields and format issues.
- **Geographic Distribution**: Analyzes the geographic distribution of places (if coordinates are available).

#### Usage

```bash
python input_statistics.py input/places.jsonl
```

#### Analysis Dimensions

1. **Total Data Statistics**
   ```python
   total_places = len(places)
   unique_place_ids = len(set(p['place_id'] for p in places))
   ```

2. **Type Distribution Statistics**
   ```python
   parent_type_dist = Counter(p['parent_type'] for p in places)
   sub_type_dist = Counter(p['sub_type'] for p in places)
   ```

3. **Data Quality Check**
   ```python
   missing_fields = {
       'place_id': sum(1 for p in places if not p.get('place_id')),
       'url': sum(1 for p in places if not p.get('url')),
       'place_name': sum(1 for p in places if not p.get('place_name'))
   }
   ```

#### Example Output

```
=== Input Data Statistics Report ===

Basic Statistics:
Total places: 15,847
Unique place_ids: 15,847
Duplicate place_ids: 0

Parent Type Distribution:
food_and_drink: 8,234 (52.0%)
shopping: 3,456 (21.8%)
entertainment_and_recreation: 2,123 (13.4%)
transportation: 1,234 (7.8%)
Other: 800 (5.0%)

Sub Type Distribution (Top 10):
restaurant: 3,456
store: 2,345
cafe: 1,234
park: 987
...

Data Quality Check:
Missing place_id: 0
Missing URL: 12
Missing place_name: 5
Invalid URL format: 3
```

---

## Configuration and Error Handling

### error_codes.md - Error Code Explanations

**Functional Description**: Standardized error code definitions and problem solutions.

#### Error Code Categories

1. **Browser-related Errors (1000-1099)**
   - `1001`: Browser initialization failed
   - `1002`: URL loading failed

2. **Data Extraction Errors (1100-1199)**
   - `1003`: Business info extraction failed
   - `1004`: Reviews button not found
   - `1005`: Review scrolling failed
   - `1006`: Review extraction failed
   - `1007`: Coordinate extraction failed

3. **File Operation Errors (1200-1299)**
   - `1008`: CSV save failed

4. **Network-related Errors (1300-1399)**
   - `1009`: Network timeout

5. **General Errors (1900-1999)**
   - `1010`: Element not found
   - `1999`: Unexpected error

#### Error Handling Strategy

```python
class ErrorCodes:
    SUCCESS = 0
    BROWSER_INIT_FAILED = 1001
    URL_LOAD_FAILED = 1002
    # ... other error codes
    
def handle_error(error_code, error_message):
    """Error handling and retry strategy"""
    if error_code in [1001, 1002]:
        # Browser-related error, restart browser
        return "restart_browser"
    elif error_code in [1009, 1010]:
        # Network or element issue, retryable
        return "retry"
    else:
        # Other errors, log and skip
        return "skip"
```

---

## 🔧 Development and Extension

### Adding New Features

1. **Extend Data Extraction Fields**
   ```python
   # Add new extraction logic in main.py
   def extract_additional_info(driver):
       # New data extraction logic
       pass
   ```

2. **Custom Output Formats**
   ```python
   # Add a new output handler in batch_scraper.py
   def save_custom_format(data, output_path):
       # Custom format saving logic
       pass
   ```

3. **Integrate Database Storage**
   ```python
   # Add database connection and storage logic
   def save_to_database(data):
       # Database saving logic
       pass
   ```

### Performance Optimization Suggestions

1. **Memory Optimization**: Use generators to process large files.
2. **Concurrency Optimization**: Adjust the number of threads based on machine performance.
3. **Network Optimization**: Add request intervals and retry mechanisms.
4. **Storage Optimization**: Compress output files or use more efficient formats.

### Monitoring and Maintenance

1. **Log Monitoring**: Regularly check error logs.
2. **Performance Monitoring**: Track processing speed and success rate.
3. **Data Quality**: Periodically validate the integrity of the output data.
4. **Version Management**: Keep code and dependencies updated.

</rewritten_file>