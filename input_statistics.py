#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
输入文件统计工具
统计JSONL文件中每个parent_type和sub_type的地点数量

用法：
python 统计输入文件.py [输入文件路径]

作者：AI Assistant
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
import time

def load_jsonl_with_encoding(file_path):
    """
    加载JSONL文件，尝试多种编码方式
    
    Args:
        file_path: JSONL文件路径
        
    Returns:
        (数据列表, 使用的编码)
    """
    encodings_to_try = ['utf-8', 'utf-8-sig', 'gbk', 'gb2312']
    
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                file_content = f.read()
                return file_content, encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # 如果所有编码都失败，使用UTF-8并忽略错误
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        file_content = f.read()
        return file_content, 'utf-8 (with errors ignored)'

def analyze_places_data(input_file):
    """
    分析地点数据并生成统计报告
    
    Args:
        input_file: 输入的JSONL文件路径
        
    Returns:
        统计结果字典
    """
    print(f"📊 开始分析文件: {input_file}")
    
    # 读取文件
    try:
        file_content, used_encoding = load_jsonl_with_encoding(input_file)
        print(f"✅ 使用编码: {used_encoding}")
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None
    
    # 统计数据结构
    stats = {
        "total_places": 0,
        "parent_types": defaultdict(int),  # parent_type -> 总数
        "sub_types": defaultdict(int),     # sub_type -> 总数
        "type_combinations": defaultdict(int),  # parent_type/sub_type -> 数量
        "detailed_breakdown": defaultdict(lambda: defaultdict(int)),  # parent_type -> {sub_type: count}
        "missing_fields": {
            "missing_parent_type": 0,
            "missing_sub_type": 0,
            "missing_place_id": 0,
            "missing_maps_url": 0
        }
    }
    
    # 逐行解析JSONL
    line_count = 0
    valid_places = 0
    
    for line_num, line in enumerate(file_content.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
            
        line_count += 1
        
        try:
            place_data = json.loads(line)
            
            # 检查必需字段
            place_id = place_data.get('place_id', '')
            maps_url = place_data.get('Maps_url', '')
            parent_type = place_data.get('parent_type', '')
            sub_type = place_data.get('sub_type', '')
            
            # 统计缺失字段
            if not place_id:
                stats["missing_fields"]["missing_place_id"] += 1
            if not maps_url:
                stats["missing_fields"]["missing_maps_url"] += 1
            if not parent_type:
                stats["missing_fields"]["missing_parent_type"] += 1
            if not sub_type:
                stats["missing_fields"]["missing_sub_type"] += 1
            
            # 只统计有有效parent_type和sub_type的记录
            if parent_type and sub_type:
                valid_places += 1
                stats["parent_types"][parent_type] += 1
                stats["sub_types"][sub_type] += 1
                stats["type_combinations"][f"{parent_type}/{sub_type}"] += 1
                stats["detailed_breakdown"][parent_type][sub_type] += 1
            
        except json.JSONDecodeError as e:
            print(f"⚠️  第{line_num}行JSON解析失败: {e}")
            continue
    
    stats["total_places"] = valid_places
    stats["total_lines"] = line_count
    
    print(f"✅ 解析完成！")
    print(f"   总行数: {line_count}")
    print(f"   有效地点: {valid_places}")
    print(f"   Parent类型数: {len(stats['parent_types'])}")
    print(f"   Sub类型数: {len(stats['sub_types'])}")
    print(f"   类型组合数: {len(stats['type_combinations'])}")
    
    return stats

def generate_report(stats, output_file):
    """
    生成详细的统计报告
    
    Args:
        stats: 统计数据
        output_file: 输出文件路径
    """
    # 准备报告数据
    report = {
        "analysis_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "summary": {
            "total_places": stats["total_places"],
            "total_lines": stats["total_lines"],
            "unique_parent_types": len(stats["parent_types"]),
            "unique_sub_types": len(stats["sub_types"]),
            "unique_combinations": len(stats["type_combinations"])
        },
        "data_quality": {
            "missing_fields": dict(stats["missing_fields"]),
            "data_completeness_rate": (stats["total_places"] / stats["total_lines"] * 100) if stats["total_lines"] > 0 else 0
        },
        "parent_type_distribution": dict(sorted(stats["parent_types"].items(), key=lambda x: x[1], reverse=True)),
        "sub_type_distribution": dict(sorted(stats["sub_types"].items(), key=lambda x: x[1], reverse=True)),
        "detailed_breakdown": {}
    }
    
    # 整理详细分解数据
    for parent_type, sub_types in stats["detailed_breakdown"].items():
        report["detailed_breakdown"][parent_type] = {
            "total": stats["parent_types"][parent_type],
            "sub_types": dict(sorted(sub_types.items(), key=lambda x: x[1], reverse=True))
        }
    
    # 按parent_type的总数排序
    report["detailed_breakdown"] = dict(sorted(
        report["detailed_breakdown"].items(), 
        key=lambda x: x[1]["total"], 
        reverse=True
    ))
    
    # 保存报告为JSONL格式（每个parent_type一行，便于阅读）
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # 写入汇总信息
            f.write(json.dumps({
                "type": "summary",
                "data": report["summary"]
            }, ensure_ascii=False) + '\n')
            
            f.write(json.dumps({
                "type": "data_quality",
                "data": report["data_quality"]
            }, ensure_ascii=False) + '\n')
            
            # 写入每个parent_type的详细信息
            for parent_type, breakdown in report["detailed_breakdown"].items():
                f.write(json.dumps({
                    "type": "parent_type_breakdown",
                    "parent_type": parent_type,
                    "data": breakdown
                }, ensure_ascii=False) + '\n')
            
            # 写入top子类型分布
            f.write(json.dumps({
                "type": "top_sub_types",
                "data": dict(list(report["sub_type_distribution"].items())[:20])  # 前20个
            }, ensure_ascii=False) + '\n')
        
        print(f"✅ 统计报告已保存到: {output_file}")
        
    except Exception as e:
        print(f"❌ 保存报告失败: {e}")
        return False
    
    return True

def print_summary(stats):
    """
    在控制台打印汇总信息
    
    Args:
        stats: 统计数据
    """
    print(f"""
📊 统计汇总:
========================================
总地点数: {stats['total_places']:,}
Parent类型数: {len(stats['parent_types'])}
Sub类型数: {len(stats['sub_types'])}
类型组合数: {len(stats['type_combinations'])}

🔝 Top 10 Parent类型:""")
    
    # 显示Top 10 parent types
    sorted_parents = sorted(stats['parent_types'].items(), key=lambda x: x[1], reverse=True)
    for i, (parent_type, count) in enumerate(sorted_parents[:10], 1):
        print(f"{i:2d}. {parent_type}: {count:,} 个地点")
    
    print(f"""
🔝 Top 10 Sub类型:""")
    
    # 显示Top 10 sub types  
    sorted_subs = sorted(stats['sub_types'].items(), key=lambda x: x[1], reverse=True)
    for i, (sub_type, count) in enumerate(sorted_subs[:10], 1):
        print(f"{i:2d}. {sub_type}: {count:,} 个地点")
    
    # 数据质量信息
    if any(stats['missing_fields'].values()):
        print(f"""
⚠️  数据质量警告:""")
        for field, count in stats['missing_fields'].items():
            if count > 0:
                print(f"   {field}: {count} 条记录")

def main():
    """主函数"""
    # 处理命令行参数
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "input/hong_kong_place_ids_and_urls_ENG.jsonl"
    
    # 检查文件是否存在
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"❌ 文件不存在: {input_file}")
        print(f"💡 用法: python {Path(__file__).name} [输入文件路径]")
        return
    
    # 生成输出文件路径
    output_file = input_path.parent / f"{input_path.stem}_statistics.jsonl"
    
    print(f"🚀 开始统计分析...")
    print(f"📁 输入文件: {input_file}")
    print(f"📁 输出文件: {output_file}")
    
    # 分析数据
    stats = analyze_places_data(input_file)
    if not stats:
        return
    
    # 生成报告
    if generate_report(stats, output_file):
        # 打印汇总信息
        print_summary(stats)
        print(f"""
========================================
🎉 统计分析完成！
📊 详细报告已保存到: {output_file}

💡 您可以使用以下命令查看报告内容:
   cat "{output_file}"
   或者用文本编辑器打开查看
========================================""")
    else:
        print("❌ 报告生成失败")

if __name__ == "__main__":
    main() 