import argparse
import os

from analyzer import analyze_content
from truth_fetcher_v2 import get_truths_incremental

def main():
    parser = argparse.ArgumentParser(description="分析特朗普 Truth Social 发言并生成投资建议")
    parser.add_argument("--count", type=int, default=5, help="抓取的发文数量")

    args = parser.parse_args()

    print(f"📡 正在抓取特朗普 Truth Social 上最新 {args.count} 条内容...\n")

    truths = get_truths_incremental(max_items=args.count)

    print(truths)

    print(f"\n📊 分析并生成投资建议 \n")
    analyze_content(truths,"deepseek-r1")

if __name__ == "__main__":
    main()
