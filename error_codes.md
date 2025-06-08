# Google Maps 爬虫错误代码说明

## 错误代码列表

| 错误代码 | 错误类型 | 描述 | 可能原因 | 建议处理方式 |
|---------|---------|------|----------|-------------|
| 0 | SUCCESS | 成功 | - | 正常处理结果 |
| 1001 | BROWSER_INIT_FAILED | 浏览器初始化失败 | Chrome驱动问题、权限问题、依赖缺失 | 检查Chrome驱动版本、系统权限 |
| 1002 | URL_LOAD_FAILED | URL加载失败 | 网络问题、URL无效、超时 | 检查网络连接、URL格式 |
| 1003 | BUSINESS_INFO_EXTRACTION_FAILED | 商户信息提取失败 | 页面结构变化、元素定位失败 | 可忽略，会使用默认值 |
| 1004 | REVIEWS_BUTTON_NOT_FOUND | 未找到Reviews按钮 | 商户无评论、页面结构变化 | 正常情况，返回商户基本信息 |
| 1005 | REVIEWS_SCROLL_FAILED | 评论滚动加载失败 | 页面加载慢、网络问题 | 重试或忽略 |
| 1006 | REVIEWS_EXTRACTION_FAILED | 评论提取失败 | 页面结构变化、权限问题 | 重试或忽略 |
| 1007 | COORDINATES_EXTRACTION_FAILED | 坐标提取失败 | URL格式变化、页面跳转 | 可忽略，坐标字段为空 |
| 1008 | CSV_SAVE_FAILED | CSV文件保存失败 | 磁盘空间不足、权限问题 | 检查磁盘空间和目录权限 |
| 1009 | NETWORK_TIMEOUT | 网络超时 | 网络连接慢、服务器响应慢 | 增加重试次数或超时时间 |
| 1010 | ELEMENT_NOT_FOUND | 元素未找到 | 文件不存在、URL列表为空 | 检查输入文件和参数 |
| 1999 | UNEXPECTED_ERROR | 意外错误 | 未知异常、代码逻辑错误 | 检查日志详情，联系技术支持 |

## 错误处理策略

### 1. 可重试的错误
以下错误代码建议进行重试：
- `1002` (URL加载失败)
- `1005` (评论滚动加载失败) 
- `1006` (评论提取失败)
- `1009` (网络超时)
- `1999` (意外错误)

### 2. 可忽略的错误
以下错误代码不影响主要功能：
- `1003` (商户信息提取失败) - 会使用默认值
- `1004` (未找到Reviews按钮) - 商户可能无评论
- `1007` (坐标提取失败) - 坐标字段为空

### 3. 严重错误
以下错误代码需要立即处理：
- `1001` (浏览器初始化失败) - 环境配置问题
- `1008` (CSV文件保存失败) - 系统资源问题  
- `1010` (元素未找到) - 输入参数问题

## 使用示例

### Python代码中处理错误
```python
from caller_example import GoogleMapsReviewsAPI

api = GoogleMapsReviewsAPI()
result = api.scrape_single_url("YOUR_URL")

if result["success"]:
    print("爬取成功")
    print(f"商家: {result['data']['business_info']['name']}")
else:
    error_code = result["error_code"]
    
    if error_code in [1002, 1005, 1006, 1009, 1999]:
        print("可重试的错误，建议重试")
    elif error_code in [1003, 1004, 1007]:
        print("可忽略的错误，继续处理")
    elif error_code in [1001, 1008, 1010]:
        print("严重错误，需要立即处理")
        print(f"错误详情: {result['error_message']}")
```

### 命令行查看详细错误
```bash
# 启用详细日志
python main.py --url "YOUR_URL" --verbose --json-output

# 增加重试次数
python main.py --url "YOUR_URL" --max-retries 5
```

## 日志级别说明

- `INFO`: 正常处理信息
- `WARNING`: 可忽略的错误和警告
- `ERROR`: 严重错误，导致处理失败

使用 `--verbose` 参数可以看到更详细的调试信息。

---

# Google Maps Scraper Error Code Explanations

## Error Code List

| Error Code | Error Type | Description | Possible Causes | Recommended Action |
|---|---|---|---|---|
| 0 | SUCCESS | Success | - | Normal processing result |
| 1001 | BROWSER_INIT_FAILED | Browser initialization failed | Chrome driver issue, permission problem, missing dependencies | Check Chrome driver version, system permissions |
| 1002 | URL_LOAD_FAILED | URL loading failed | Network issue, invalid URL, timeout | Check network connection, URL format |
| 1003 | BUSINESS_INFO_EXTRACTION_FAILED | Business info extraction failed | Page structure change, element location failed | Can be ignored, default values will be used |
| 1004 | REVIEWS_BUTTON_NOT_FOUND | "Reviews" button not found | Business has no reviews, page structure change | Normal case, returns basic business info |
| 1005 | REVIEWS_SCROLL_FAILED | Review scroll loading failed | Slow page load, network issue | Retry or ignore |
| 1006 | REVIEWS_EXTRACTION_FAILED | Review extraction failed | Page structure change, permission issue | Retry or ignore |
| 1007 | COORDINATES_EXTRACTION_FAILED | Coordinate extraction failed | URL format change, page redirect | Can be ignored, coordinate field will be empty |
| 1008 | CSV_SAVE_FAILED | CSV file save failed | Insufficient disk space, permission issue | Check disk space and directory permissions |
| 1009 | NETWORK_TIMEOUT | Network timeout | Slow network connection, slow server response | Increase retry count or timeout |
| 1010 | ELEMENT_NOT_FOUND | Element not found | File does not exist, URL list is empty | Check input file and parameters |
| 1999 | UNEXPECTED_ERROR | Unexpected error | Unknown exception, code logic error | Check log details, contact technical support |

## Error Handling Strategy

### 1. Retryable Errors
The following error codes are recommended for retry:
- `1002` (URL_LOAD_FAILED)
- `1005` (REVIEWS_SCROLL_FAILED)
- `1006` (REVIEWS_EXTRACTION_FAILED)
- `1009` (NETWORK_TIMEOUT)
- `1999` (UNEXPECTED_ERROR)

### 2. Ignorable Errors
The following errors do not affect the main functionality:
- `1003` (BUSINESS_INFO_EXTRACTION_FAILED) - Default values will be used.
- `1004` (REVIEWS_BUTTON_NOT_FOUND) - The business may have no reviews.
- `1007` (COORDINATES_EXTRACTION_FAILED) - The coordinate field will be empty.

### 3. Critical Errors
The following errors require immediate attention:
- `1001` (BROWSER_INIT_FAILED) - Environment configuration issue.
- `1008` (CSV_SAVE_FAILED) - System resource issue.
- `1010` (ELEMENT_NOT_FOUND) - Input parameter issue.

## Usage Example

### Handling Errors in Python Code
```python
from caller_example import GoogleMapsReviewsAPI

api = GoogleMapsReviewsAPI()
result = api.scrape_single_url("YOUR_URL")

if result["success"]:
    print("Scraping successful")
    print(f"Business: {result['data']['business_info']['name']}")
else:
    error_code = result["error_code"]
    
    if error_code in [1002, 1005, 1006, 1009, 1999]:
        print("Retryable error, retrying is recommended")
    elif error_code in [1003, 1004, 1007]:
        print("Ignorable error, continuing processing")
    elif error_code in [1001, 1008, 1010]:
        print("Critical error, requires immediate attention")
        print(f"Error details: {result['error_message']}")
```

### Viewing Detailed Errors via Command Line
```bash
# Enable detailed logging
python main.py --url "YOUR_URL" --verbose --json-output

# Increase retry attempts
python main.py --url "YOUR_URL" --max-retries 5
```

## Log Level Explanations

- `INFO`: Normal processing information
- `WARNING`: Ignorable errors and warnings
- `ERROR`: Critical error, causing processing failure

Use the `--verbose` flag to see more detailed debugging information. 