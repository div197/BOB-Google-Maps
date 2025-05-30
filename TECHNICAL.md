# 技术文档 - 代码详解

本文档详细介绍项目中各个Python脚本的功能、用法和实现细节。

## 📝 目录

- [核心爬虫模块](#核心爬虫模块)
  - [main.py - 单点爬虫](#mainpy---单点爬虫)
  - [batch_scraper.py - 批量处理器](#batch_scraperpy---批量处理器)
- [工具模块](#工具模块)
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