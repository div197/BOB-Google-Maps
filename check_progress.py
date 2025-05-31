#!/usr/bin/env python3
import json
import os
from collections import defaultdict
from tqdm import tqdm

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

# 新增：详细统计各父类别的地点数量和评论数
print(f"\n=== 详细统计 ===")

# 统计变量
parent_categories = defaultdict(int)  # 每个父类别的地点数
parent_reviews_count = defaultdict(int)  # 每个父类别的评论数
parent_places_with_reviews = defaultdict(int)  # 每个父类别有评论的地点数
parent_places_without_reviews = defaultdict(int)  # 每个父类别无评论的地点数

total_reviews = 0
total_places_with_reviews = 0
total_places_without_reviews = 0

# 第一步：统计总文件数用于显示进度
print("正在统计文件总数...")
batch_output_dir = 'batch_output'
all_json_files = []

for parent_dir in os.listdir(batch_output_dir):
    parent_path = os.path.join(batch_output_dir, parent_dir)
    
    # 跳过文件，只处理目录
    if not os.path.isdir(parent_path):
        continue
    
    # 遍历每个父类别下的子类别
    for sub_dir in os.listdir(parent_path):
        sub_path = os.path.join(parent_path, sub_dir)
        
        # 跳过文件，只处理目录
        if not os.path.isdir(sub_path):
            continue
        
        # 收集所有JSON文件路径
        for json_file in os.listdir(sub_path):
            if json_file.endswith('.json'):
                json_path = os.path.join(sub_path, json_file)
                all_json_files.append((json_path, parent_dir))

print(f"找到 {len(all_json_files)} 个JSON文件，开始处理...")

# 第二步：带进度条遍历所有文件
for json_path, parent_dir in tqdm(all_json_files, desc="处理JSON文件", unit="文件"):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            place_data = json.load(f)
        
        # 统计父类别地点数
        parent_type = place_data.get('parent_type', parent_dir)
        parent_categories[parent_type] += 1
        
        # 统计评论数
        reviews_count = place_data.get('reviews_count', 0)
        parent_reviews_count[parent_type] += reviews_count
        total_reviews += reviews_count
        
        # 统计有无评论的地点数
        has_reviews = place_data.get('has_reviews', False)
        if has_reviews and reviews_count > 0:
            parent_places_with_reviews[parent_type] += 1
            total_places_with_reviews += 1
        else:
            parent_places_without_reviews[parent_type] += 1
            total_places_without_reviews += 1
            
    except Exception as e:
        tqdm.write(f"读取文件 {json_path} 时出错: {e}")

# 输出统计结果
print(f"\n=== 文件处理完成 ===")
print(f"总评论数: {total_reviews}")
print(f"总的有评论地点数: {total_places_with_reviews}")
print(f"总的无评论地点数: {total_places_without_reviews}")
print(f"总地点数: {total_places_with_reviews + total_places_without_reviews}")

print(f"\n=== 各父类别统计 ===")
for parent_type in sorted(parent_categories.keys()):
    places_count = parent_categories[parent_type]
    reviews_count = parent_reviews_count[parent_type]
    with_reviews = parent_places_with_reviews[parent_type]
    without_reviews = parent_places_without_reviews[parent_type]
    
    print(f"\n{parent_type}:")
    print(f"  地点总数: {places_count}")
    print(f"  评论总数: {reviews_count}")
    print(f"  有评论地点: {with_reviews}")
    print(f"  无评论地点: {without_reviews}")
    print(f"  平均每地点评论数: {reviews_count / places_count:.2f}" if places_count > 0 else "  平均每地点评论数: 0.00")

# 按评论数排序显示
print(f"\n=== 按评论数排序的父类别 ===")
sorted_by_reviews = sorted(parent_reviews_count.items(), key=lambda x: x[1], reverse=True)
for parent_type, reviews_count in sorted_by_reviews:
    places_count = parent_categories[parent_type]
    print(f"{parent_type}: {reviews_count} 条评论 ({places_count} 个地点)")

# 按地点数排序显示
print(f"\n=== 按地点数排序的父类别 ===")
sorted_by_places = sorted(parent_categories.items(), key=lambda x: x[1], reverse=True)
for parent_type, places_count in sorted_by_places:
    reviews_count = parent_reviews_count[parent_type]
    print(f"{parent_type}: {places_count} 个地点 ({reviews_count} 条评论)") 