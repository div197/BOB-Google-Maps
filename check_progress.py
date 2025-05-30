#!/usr/bin/env python3
import json

# 读取progress.json
with open('batch_output/progress.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=== Progress.json 统计 ===")
print(f"successful count: {len(data['successful'])}")
print(f"failed count: {len(data['failed'])}")
print(f"skipped count: {len(data['skipped'])}")
print(f"total processed: {len(data['successful']) + len(data['failed']) + len(data['skipped'])}")

# 检查是否有重复
successful_set = set(data['successful'])
failed_set = set(data['failed'])
skipped_set = set(data['skipped'])

print(f"\n=== 去重后统计 ===")
print(f"unique successful: {len(successful_set)}")
print(f"unique failed: {len(failed_set)}")
print(f"unique skipped: {len(skipped_set)}")

# 检查交集
print(f"\n=== 交集检查 ===")
print(f"successful & failed: {len(successful_set & failed_set)}")
print(f"successful & skipped: {len(successful_set & skipped_set)}")
print(f"failed & skipped: {len(failed_set & skipped_set)}")

# 计算总的已处理ID
all_processed = successful_set | failed_set | skipped_set
print(f"\n=== 总计 ===")
print(f"total unique processed IDs: {len(all_processed)}") 