[English Version](#google-maps-review-scraper)

# Google Maps 评论爬虫

一个强大的Google Maps商户信息和用户评论数据爬取工具，专为大规模数据采集设计。

## 🌟 主要特性

- **大规模批量处理**：支持数万个地点的批量数据爬取
- **智能断点恢复**：意外中断后可自动继续处理
- **多线程并发**：支持多线程并发处理，提高效率
- **错误重试机制**：智能重试失败的地点，提高成功率
- **详细进度跟踪**：实时显示处理进度和统计信息
- **灵活输出格式**：支持JSON和CSV格式输出
- **完整数据提取**：包括商户基本信息、评论内容、评分等

## 📚 文档导航

- 📖 **[技术文档](TECHNICAL.md)** - 详细的代码功能说明和实现细节
- 📋 **[错误代码](error_codes.md)** - 完整的错误代码定义和解决方案

## 📁 项目结构

```
googlemaps-scraper-reviews/
├── main.py                    # 单点爬虫核心脚本
├── batch_scraper.py          # 批量处理脚本
├── process_urls.py           # URL预处理工具，强制英文界面
├── check_progress.py         # 进度检查工具
├── retry_failed_scrapes.py   # 失败重试工具
├── find_duplicates_simple.py # 去重工具
├── input_statistics.py       # 输入数据统计
├── error_codes.md           # 错误代码说明
├── input/                   # 输入数据目录
├── batch_output/           # 批量输出数据目录
│   ├── culture/           # 文化场所数据
│   ├── education/         # 教育场所数据
│   ├── entertainment_and_recreation/ # 娱乐休闲数据
│   ├── facilities/        # 设施数据
│   ├── food_and_drink/    # 餐饮数据
│   ├── natural_features/  # 自然景观数据
│   ├── places_of_worship/ # 宗教场所数据
│   ├── shopping/          # 购物场所数据
│   ├── sports/            # 体育场所数据
│   ├── transportation/    # 交通相关数据
│   ├── progress.json      # 处理进度记录
│   ├── errors.jsonl       # 错误日志
│   └── success.jsonl      # 成功日志
└── backup/                # 备份数据目录
```

## 🚀 快速开始

### 环境要求

- Python 3.7+
- Chrome浏览器
- ChromeDriver（会自动管理）

### 安装依赖

```bash
pip install selenium pandas tqdm
```

### 准备输入数据

在 `input/` 目录下放置JSONL格式的输入文件，每行包含一个地点的信息：

```json
{
    "place_id": "ChIJ...",
    "place_name": "商户名称",
    "parent_type": "food_and_drink",
    "sub_type": "restaurant",
    "url": "https://maps.google.com/..."
}
```

### URL预处理：强制英文界面

**重要提示：** 当前版本的爬虫仅能识别和解析Google Maps的 **英文页面** 结构。为确保数据能被正确抓取，所有URL都必须经过预处理以强制页面以英文显示。未经处理的URL将导致爬取失败。

项目中的 `process_urls.py` 脚本可用于批量为URL添加 `&hl=en` 参数。

**使用步骤：**

1.  **配置脚本**：打开 `process_urls.py` 文件，根据您的文件位置修改 `input_file` 和 `output_file` 变量。
2.  **运行脚本**：
    ```bash
    python process_urls.py
    ```
3.  **使用新文件**：脚本会生成一个处理后的新文件。请务必使用这个新生成的文件（例如 `..._en.jsonl`）作为后续爬取操作的输入。

### 单点爬取

爬取单个地点的数据：

```bash
python main.py "https://maps.google.com/..."
```

支持的参数：
- `--output-dir`：输出目录（默认：output）
- `--no-headless`：显示浏览器界面
- `--json-output`：仅输出JSON格式
- `--max-retries`：最大重试次数（默认：3）

### 批量爬取

处理大量地点数据：

```bash
# 基础批量处理
python batch_scraper.py input/places.jsonl

# 指定并发数和处理数量
python batch_scraper.py input/places.jsonl --max-workers 5 --max-places 100

# 启用断点恢复
python batch_scraper.py input/places.jsonl --resume

# 重试失败的地点
python batch_scraper.py input/places.jsonl --retry-failed

# 无人值守模式（长期运行）
python batch_scraper.py input/places.jsonl --unattended

# 无限运行模式
python batch_scraper.py input/places.jsonl --infinite
```

## 📊 监控和管理

### 检查处理进度

```bash
python check_progress.py
```

输出示例：
```
=== Progress.json 统计 ===
successful count: 1250
failed count: 45
skipped count: 0
total processed: 1295
```

### 重试失败的爬取

```bash
python retry_failed_scrapes.py
```

### 查看输入数据统计

```bash
python input_statistics.py input/places.jsonl
```

## ⚙️ 配置选项

### 预设配置模式

- **默认模式**：平衡的性能和稳定性
- **测试模式**：用于快速测试（`--test`）
- **生产模式**：高性能大规模处理（`--production`）
- **无人值守模式**：长期自动运行（`--unattended`）
- **无限模式**：持续运行直到所有数据处理完成（`--infinite`）
- **快速模式**：高速处理，较少重试（`--fast`）

### 主要参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--max-workers` | 最大并发线程数 | 3 |
| `--max-retries` | 单个地点最大重试次数 | 3 |
| `--timeout` | 单个地点超时时间（秒） | 300 |
| `--max-places` | 单次最大处理地点数 | 无限制 |
| `--resume` | 启用断点恢复 | True |
| `--retry-failed` | 重试失败的地点 | False |

## 📄 输出格式

### JSON格式

每个商户的数据保存为独立的JSON文件：

```json
{
    "place_id": "ChIJ...",
    "business_info": {
        "name": "商户名称",
        "address": "详细地址",
        "phone": "联系电话",
        "website": "官方网站",
        "rating": 4.5,
        "total_reviews": 1250,
        "coordinates": {
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        "hours": "营业时间信息"
    },
    "reviews": [
        {
            "author": "用户名",
            "rating": 5,
            "date": "2024-01-15",
            "text": "评论内容",
            "helpful_count": 12
        }
    ],
    "scrape_info": {
        "scraped_at": "2024-01-15T10:30:00",
        "total_reviews_scraped": 45,
        "scrape_duration": 120.5
    }
}
```

### CSV格式

同时生成CSV格式的评论数据，便于进一步分析。

## 🛠️ 故障排除

### 常见问题

1. **Chrome浏览器启动失败**
   - 确保已安装Chrome浏览器
   - 检查ChromeDriver版本兼容性

2. **网络超时**
   - 增加 `--timeout` 参数值
   - 检查网络连接稳定性

3. **验证码或反爬虫检测**
   - 降低并发数（`--max-workers 1`）
   - 增加随机延迟
   - 使用代理IP

4. **内存不足**
   - 降低 `--max-workers` 值
   - 使用 `--max-places` 分批处理

### 错误代码

详细的错误代码说明请查看 [error_codes.md](error_codes.md)

## 📈 性能优化

### 推荐配置

- **小规模测试**（<100个地点）：`--max-workers 1 --max-places 10`
- **中等规模**（100-1000个地点）：`--max-workers 3 --max-places 100`
- **大规模处理**（>1000个地点）：`--max-workers 5 --max-places 500`

### 注意事项

- 过高的并发可能触发反爬虫机制
- 建议在非高峰时段运行大规模爬取
- 定期检查和清理输出目录

## 🔧 开发说明

### 扩展功能

项目采用模块化设计，可以轻松扩展：

- 添加新的数据提取字段
- 自定义输出格式
- 集成不同的存储后端
- 添加数据清洗和验证

### 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 创建 Pull Request

## 📞 支持

如有问题或建议，请：

1. 查看错误代码文档
2. 检查日志文件
3. 提交Issue描述问题

## ⚖️ 免责声明

本工具仅用于学习和研究目的。使用者需要：

- 遵守Google Maps的服务条款
- 遵守相关法律法规
- 合理控制爬取频率
- 尊重网站的robots.txt

请负责任地使用此工具，避免对目标网站造成过大负担。

---

[中文版](#google-maps-评论爬虫)

# Google Maps Review Scraper

A powerful tool for scraping business information and user reviews from Google Maps, designed for large-scale data collection.

## 🌟 Key Features

- **Large-Scale Batch Processing**: Supports batch scraping of tens of thousands of places.
- **Intelligent Resume**: Automatically resumes processing after an unexpected interruption.
- **Multi-threaded Concurrency**: Supports multi-threaded processing to improve efficiency.
- **Error Retry Mechanism**: Intelligently retries failed places to increase success rate.
- **Detailed Progress Tracking**: Real-time display of processing progress and statistics.
- **Flexible Output Formats**: Supports JSON and CSV output formats.
- **Comprehensive Data Extraction**: Includes basic business information, review content, ratings, etc.

## 📚 Documentation

- 📖 **[Technical Documentation](TECHNICAL.md)** - Detailed code function descriptions and implementation details.
- 📋 **[Error Codes](error_codes.md)** - Complete error code definitions and solutions.

## 📁 Project Structure

```
googlemaps-scraper-reviews/
├── main.py                    # Core script for single-place scraping
├── batch_scraper.py          # Batch processing script
├── process_urls.py           # URL pre-processing tool to force English interface
├── check_progress.py         # Progress checking tool
├── retry_failed_scrapes.py   # Failed scrapes retry tool
├── find_duplicates_simple.py # Duplicate removal tool
├── input_statistics.py       # Input data statistics tool
├── error_codes.md           # Error code descriptions
├── input/                   # Input data directory
├── batch_output/           # Batch output data directory
│   ├── culture/           # Data for cultural places
│   ├── education/         # Data for educational places
│   ├── entertainment_and_recreation/ # Data for entertainment and recreation
│   ├── facilities/        # Data for facilities
│   ├── food_and_drink/    # Data for food and drink
│   ├── natural_features/  # Data for natural features
│   ├── places_of_worship/ # Data for places of worship
│   ├── shopping/          # Data for shopping
│   ├── sports/            # Data for sports
│   ├── transportation/    # Data for transportation
│   ├── progress.json      # Processing progress log
│   ├── errors.jsonl       # Error log
│   └── success.jsonl      # Success log
└── backup/                # Backup data directory
```

## 🚀 Quick Start

### Requirements

- Python 3.7+
- Google Chrome Browser
- ChromeDriver (managed automatically)

### Installation

```bash
pip install selenium pandas tqdm
```

### Prepare Input Data

Place JSONL format input files in the `input/` directory. Each line should contain information for one place:

```json
{
    "place_id": "ChIJ...",
    "place_name": "Business Name",
    "parent_type": "food_and_drink",
    "sub_type": "restaurant",
    "url": "https://maps.google.com/..."
}
```

### URL Pre-processing: Force English Interface

**IMPORTANT:** The current version of the scraper can only recognize and parse the structure of **English Google Maps pages**. To ensure data is scraped correctly, all URLs must be pre-processed to force the page to display in English. Unprocessed URLs will lead to scraping failures.

The `process_urls.py` script in the project can be used to add the `&hl=en` parameter to URLs in bulk.

**Steps:**

1.  **Configure the script**: Open the `process_urls.py` file and modify the `input_file` and `output_file` variables according to your file locations.
2.  **Run the script**:
    ```bash
    python process_urls.py
    ```
3.  **Use the new file**: The script will generate a new processed file. Be sure to use this new file (e.g., `..._en.jsonl`) as the input for subsequent scraping operations.

### Single Place Scraping

Scrape data for a single place:

```bash
python main.py "https://maps.google.com/..."
```

Supported arguments:
- `--output-dir`: Output directory (default: output)
- `--no-headless`: Show browser UI
- `--json-output`: Output only in JSON format
- `--max-retries`: Maximum number of retries (default: 3)

### Batch Scraping

Process a large number of places:

```bash
# Basic batch processing
python batch_scraper.py input/places.jsonl

# Specify number of workers and places
python batch_scraper.py input/places.jsonl --max-workers 5 --max-places 100

# Enable resume functionality
python batch_scraper.py input/places.jsonl --resume

# Retry failed places
python batch_scraper.py input/places.jsonl --retry-failed

# Unattended mode (for long-running tasks)
python batch_scraper.py input/places.jsonl --unattended

# Infinite mode
python batch_scraper.py input/places.jsonl --infinite
```

## 📊 Monitoring and Management

### Check Progress

```bash
python check_progress.py
```

Example output:
```
=== Progress.json Statistics ===
successful count: 1250
failed count: 45
skipped count: 0
total processed: 1295
```

### Retry Failed Scrapes

```bash
python retry_failed_scrapes.py
```

### View Input Data Statistics

```bash
python input_statistics.py input/places.jsonl
```

## ⚙️ Configuration Options

### Preset Configuration Modes

- **Default Mode**: Balanced performance and stability.
- **Test Mode**: For quick testing (`--test`).
- **Production Mode**: High-performance for large-scale processing (`--production`).
- **Unattended Mode**: For long-term automatic operation (`--unattended`).
- **Infinite Mode**: Runs continuously until all data is processed (`--infinite`).
- **Fast Mode**: High-speed processing with fewer retries (`--fast`).

### Main Parameters

| Parameter | Description | Default |
|---|---|---|
| `--max-workers` | Maximum number of concurrent workers | 3 |
| `--max-retries` | Max retries for a single place | 3 |
| `--timeout` | Timeout for a single place (seconds) | 300 |
| `--max-places` | Maximum number of places to process | unlimited |
| `--resume` | Enable resume functionality | True |
| `--retry-failed` | Retry failed places | False |

## 📄 Output Format

### JSON Format

Data for each business is saved in a separate JSON file:

```json
{
    "place_id": "ChIJ...",
    "business_info": {
        "name": "Business Name",
        "address": "Detailed Address",
        "phone": "Contact Phone",
        "website": "Official Website",
        "rating": 4.5,
        "total_reviews": 1250,
        "coordinates": {
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        "hours": "Business Hours Information"
    },
    "reviews": [
        {
            "author": "Username",
            "rating": 5,
            "date": "2024-01-15",
            "text": "Review content",
            "helpful_count": 12
        }
    ],
    "scrape_info": {
        "scraped_at": "2024-01-15T10:30:00",
        "total_reviews_scraped": 45,
        "scrape_duration": 120.5
    }
}
```

### CSV Format

CSV format review data is also generated for further analysis.

## 🛠️ Troubleshooting

### Common Issues

1. **Chrome Browser Fails to Start**
   - Ensure Google Chrome is installed.
   - Check ChromeDriver version compatibility.

2. **Network Timeout**
   - Increase the `--timeout` parameter value.
   - Check network connection stability.

3. **CAPTCHA or Anti-scraping Detection**
   - Reduce concurrency (`--max-workers 1`).
   - Increase random delays.
   - Use proxy IPs.

4. **Insufficient Memory**
   - Decrease the `--max-workers` value.
   - Use `--max-places` to process in batches.

### Error Codes

For detailed error code descriptions, please see [error_codes.md](error_codes.md).

## 📈 Performance Optimization

### Recommended Configurations

- **Small-scale testing** (<100 places): `--max-workers 1 --max-places 10`
- **Medium-scale** (100-1000 places): `--max-workers 3 --max-places 100`
- **Large-scale processing** (>1000 places): `--max-workers 5 --max-places 500`

### Notes

- High concurrency may trigger anti-scraping mechanisms.
- It's recommended to run large-scale scraping during off-peak hours.
- Periodically check and clean the output directory.

## 🔧 Development

### Extending Functionality

The project uses a modular design, making it easy to extend:

- Add new data extraction fields.
- Customize output formats.
- Integrate different storage backends.
- Add data cleaning and validation.

### Contribution Guidelines

1. Fork the project.
2. Create a feature branch.
3. Commit your changes.
4. Create a Pull Request.

## 📞 Support

If you have questions or suggestions, please:

1. Check the error code documentation.
2. Check the log files.
3. Submit an Issue describing the problem.

## ⚖️ Disclaimer

This tool is for learning and research purposes only. Users must:

- Comply with Google Maps' Terms of Service.
- Adhere to relevant laws and regulations.
- Control scraping frequency responsibly.
- Respect the website's robots.txt file.

Please use this tool responsibly and avoid placing an excessive burden on the target website.